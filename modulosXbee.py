#Este archivo contiene las clases para el módulo coordinador, módulo sensor y 
#la base de datos
import sqlite3

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
		self.cnxDB=db("/media/CasaL/st/Documentos/sqliteDB/xbee_db02.db")
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
		nodoXbee.lista_nodos[self.xbeeAddrStr]=xbeeSensor()
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
		self.respuesta=self.cnxDB.consultaDat('''SELECT nodo_id FROM nodoSensor WHERE direcc=?''',(self.xbeeAddrStr,))
		nodoXbee.lista_nodos[self.xbeeAddrStr]=xbeeSensor()
		nodoXbee.lista_nodos[self.xbeeAddrStr].id=self.respuesta[0][0]
		
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
			
	#def getDatosRf(self):
		#'Retorna los datos contenidos en rf_data en formato str'
		#self.rf_dataByte=self.trama_dic['rf_data']
		#try:
			#self.rf_dataStr=self.rf_dataByte.decode('UTF-8')
			#return self.rf_dataStr
		#except UnicodeDecodeError:
			#print("UnicodeDecodeError en: {}".format(self.rf_dataByte))
			#return None
	
	#def getAddress(self):
		#'Retorna la dirección del nodo sensor remoto'
		#self.xbeeAddrStr=""
		#for e in self.trama_dic['source_addr_long']:
			#self.aux=hex(e)
			#self.xbeeAddrStr+=self.aux[1:]
		#return self.xbeeAddrStr
	
	#def nuevoNodo(self,nodoAddr):
		#'''Verifica si la dirección contenida en la trama recibida es de
		#un nodo conocido o no. Retorna True si la dirección es nueva, False
		#en caso contrario.
		#'''
		#if nodoAddr not in coordinadorXbee.listaNodos:
			#return True
		#else:
			#return False
		
	#def setListaNodos(self,nodoAddr):
		#'''Actualiza el contenido del diccionario listaNodos con la dirección 
		#como llave e inicializa un objeto xbeeNodo.
		#'''
		#coordinadorXbee.listaNodos[nodoAddr]=xbeeNodo()
			
		
	#def __str__(self):
		#'Para depuración'
		#return str(self.listaNodos)

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
		
		#try:
		if len(self.listaDatos)==3:
			self.humedad=int(self.listaDatos[0])
			self.temperatura=int(self.listaDatos[1])
			self.lux=int(self.listaDatos[2])
		else:
			print ("Datos insuficientes en listaDatos:{}".format(self.listaDatos))
		#except IndexError:
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

class db():
	'''
	Maneja las conexiones con la base de datos.
	'''

	def __init__(self,db_path):
		'''
		Crea la conexión con la base de datos.
		'''
		self.cnx=sqlite3.connect(db_path)
		self.cur=self.cnx.cursor()

	def consultaSimp(self,sql):
		'''
		Consulta de datos simple
		'''
		self.cur.execute(sql)
		return self.cur.fetchall()

	def consultaDat(self,sql,datos):
		'''
		Consulta con varios parámetros.
		'''
		self.cur.execute(sql,datos)
		return self.cur.fetchall()        

	def insertarDatos(self,sql,datos):
		'''
		Inserta datos en la base de datos.
		'''
		self.cur.executemany(sql,datos)
		self.cnx.commit()

	def cnxClose(self):
		'''
		Cierra la conexión con la base de datos.
		'''
		self.cnx.close()
		
	 
