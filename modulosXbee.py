#Este archivo contiene las clases para el módulo coordinador, módulo sensor y 
#la base de datos
from base_datos import db
import sqlite3
import logging

class nodoXbee:
	'Representa un nodo coordinador en una red XBEE'
	lista_nodos={}
	
	def __init__(self):
		'''
		Inicializa las variables de temperatura, humedad,lux y
		la variable trama_dic que contiene los datos.
		'''
		self.tramaDic={}
		self.respuesta=[]
		self.nodoSensor=None
		self.rf_data=""
		self.aux1=False
		self.tiempo_datos=""		
				
		
	def actualizarDatos(self,trama_dic):
		'''
		Verifica si el origen de los datos recibidos son válidos y si el 
		origen de los mismos proviene de un nuevo nodo sensor.
		Retorna: True si los datos recibidos son correctos
		'''
		self.setTramaDic(trama_dic)
		self.setAddress()
		self.cnxDB=db("/home/pi/dataBases/dbTest03.db")
		self.respuesta=self.cnxDB.consultaSimp('''SELECT direcc FROM nodoSensor''')
		#print(self.respuesta)        
		if (self.xbeeAddrStr,) not in self.respuesta:
			self.nuevoNodo()
		elif self.xbeeAddrStr not in nodoXbee.lista_nodos:
			self.agregarNodoLista()        
		self.checkRFdata()
		if self.aux1==True:
			#print("AuxTrue")
			nodoXbee.lista_nodos[self.xbeeAddrStr].setDatos(self.rf_data)
			return True
		return False
	
	def guardarDatos(self,fecha_hora):
		'''
		Guarda los datos recibidos en la base de datos
		'''
		self.tiempo_datos=fecha_hora
		#print (type(self.tiempo_datos))
		self.cnxDB.insertarDatos('''INSERT INTO datos(nodo_id,temperatura,humedadR,lux,fecha_hora) VALUES(?,?,?,?,?)''',[(nodoXbee.lista_nodos[self.xbeeAddrStr].id,
									nodoXbee.lista_nodos[self.xbeeAddrStr].getTemperatura(),
									nodoXbee.lista_nodos[self.xbeeAddrStr].getHumedad(),
									nodoXbee.lista_nodos[self.xbeeAddrStr].getLux(),
									self.tiempo_datos)])
		print("Datos guardados")
		self.cnxDB.cnxClose()
	
	def setTramaDic(self,trama_dic):
		'Actualiza la trama de datos recibidos por el módulo.'
		self.tramaDic=trama_dic
		
		
	def getTramaDic(self):
		'Retorna el diccionario conteniendo los datos'
		return self.tramaDic
		
	def setAddress(self):
		'''
		Guarda la dirección de origen de los datos recibidos
		'''
		self.xbeeAddrStr=""
		for e in self.tramaDic['source_addr_long']:
			self.aux=hex(e)
			self.xbeeAddrStr+=self.aux[1:]
	
	def nuevoNodo(self):
		'''
		Guarda la dirección y el nodo_id de un nuevo nodo sensor
		'''
		print("LLamado a método nuevoNodo")
		#logging.info("Nuevo nodo agregado: %s",self.xbeeAddrStr)
		nodoXbee.lista_nodos[self.xbeeAddrStr]=xbeeSensor()
		logging.info("Nuevo nodo agregado: %s NODO: %s",self.xbeeAddrStr,str(nodoXbee.lista_nodos[self.xbeeAddrStr].id))
		self.respuesta=self.cnxDB.consultaSimp('''SELECT nodo_id FROM nodoSensor ORDER BY nodo_id DESC LIMIT 1''')
		if(len(self.respuesta)==0):
			self.cnxDB.insertarDatos('''INSERT INTO nodoSensor(nodo_id,direcc) VALUES(?,?)''',[(nodoXbee.lista_nodos[self.xbeeAddrStr].id,self.xbeeAddrStr)])
		else:
			nodoXbee.lista_nodos[self.xbeeAddrStr].id=self.respuesta[0][0]+1
			self.cnxDB.insertarDatos('''INSERT INTO nodoSensor(nodo_id,direcc) VALUES(?,?)''',[(nodoXbee.lista_nodos[self.xbeeAddrStr].id,self.xbeeAddrStr)])

	def agregarNodoLista(self):
		'''
		Actualiza el diccionario lista_nodos.
		'''
		print("Llamado a método agregarNodoLista")
		#logging.info("Nodo %s:%s agregado",str(nodoXbee.lista_nodos[self.xbeeAddrStr].self.id),self.xbeeAddrStr)
		self.respuesta=self.cnxDB.consultaDat('''SELECT nodo_id FROM nodoSensor WHERE direcc=?''',(self.xbeeAddrStr,))
		nodoXbee.lista_nodos[self.xbeeAddrStr]=xbeeSensor()
		nodoXbee.lista_nodos[self.xbeeAddrStr].id=self.respuesta[0][0]
		logging.info("Nodo %s:%s agregado",str(nodoXbee.lista_nodos[self.xbeeAddrStr].id),self.xbeeAddrStr)
		
	def checkRFdata(self):
		'''
		Verifica si los datos enviados de los sensores contienen errores.
		'''
		try:
			self.rf_data=self.tramaDic['rf_data'].decode('UTF-8')
			self.aux1=True
		except UnicodeDecodeError:
			self.aux1=False
			print("UnicodeError")
			logging.info("Unicode error en nodo: %s",self.xbeeAddrStr)
			

class xbeeSensor():
	'''Crea objetos Nodo y calcula el valor de los parametros temperatura,
	humedad e intesidad luminosa'''
	id=0
	
	def __init__(self):
		'Inicia los objetos con un valor de identificación único'
		xbeeSensor.id+=1
		self.id=xbeeSensor.id
		self.temperatura=0
		self.humedad=0
		self.lux=0
		
	def setDatos(self,datosRf):
		'''Crea una lista con las datos recibidosy luego separa los parámetros
		de humedad, temperatura e intensidad luminosa'''
		self.listaDatos=datosRf.split(">")
		
		try:
			if len(self.listaDatos)==3:
				self.humedad=int(self.listaDatos[0])
				self.temperatura=int(self.listaDatos[1])
				self.lux=int(self.listaDatos[2])
			else:
				print ("Datos insuficientes en listaDatos:{}".format(self.listaDatos))
				logging.debug("Error de datos insuficientes en Nodo: %s",str(self.id))
		except ValueError as e:
			logging.debug("ValueError en nodo %s: %s",str(self.id),e)
			print("ValueError en nodo {}:{}".format(self.id,e))
			#print("IndexError-listaDatos:{}".format(self.listaDatos))
		
	def getHumedad(self):
		'Retorna el valor de humedad relativa'
		return self.humedad/10
		
	def getTemperatura(self):
		'Retorna el valor de temperatura'
		return self.temperatura/10
		
	def getLux(self):
		'Retorna el valor de lux'
		return self.lux


