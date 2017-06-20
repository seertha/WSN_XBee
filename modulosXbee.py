#Este archivo contiene las clases para el módulo coordinador y el módulo sensor

class coordinadorXbee:
	'Representa un nodo coordinador en una red XBEE'
	listaNodos={}
	
	def __init__(self):
		'''
		Inicializa las variables de temperatura, humedad,lux y
		la variable trama_dic que contiene los datos.
		'''
				
		self.trama_dic={}
		self.rf_dataStr=""
		
		
	def setTramaDic(self,trama_dic):
		'Actualiza la trama de datos recibidos por el módulo.'
		self.trama_dic=trama_dic
		
	def getTramaDic(self):
		'Retorna el diccionario conteniendo los datos'
		return self.trama_dic
		
	def getDatosRf(self):
		'Retorna los datos contenidos en rf_data en formato str'
		rf_dataByte=self.trama_dic['rf_data']
		try:
			self.rf_dataStr=rf_dataByte.decode('UTF-8')
			return self.rf_dataStr
		except UnicodeDecodeError:
			print("UnicodeDecodeError en: {}".format(rf_dataByte))
			return None
	
	def getAddress(self):
		'Retorna la dirección del nodo sensor remoto'
		self.xbeeAddrStr=""
		for e in self.trama_dic['source_addr_long']:
			self.aux=hex(e)
			self.xbeeAddrStr+=self.aux[1:]
		return self.xbeeAddrStr
	
	def nuevoNodo(self,nodoAddr):
		'''Verifica si la dirección contenida en la trama recibida es de
		un nodo conocido o no. Retorna True si la dirección es nueva, False
		en caso contrario.
		'''
		if nodoAddr not in coordinadorXbee.listaNodos:
			return True
		else:
			return False
		
	def setListaNodos(self,nodoAddr):
		'''Actualiza el contenido del diccionario listaNodos con la dirección 
		como llave e inicializa un objeto xbeeNodo.
		'''
		coordinadorXbee.listaNodos[nodoAddr]=xbeeNodo()
			
		
	#def __str__(self):
		#'Para depuración'
		#return str(self.listaNodos)

class xbeeNodo():
	'''Crea objetos Nodo y calcula el valor de los parametros temperatura,
	humedad e intesidad luminosa'''
	id=0
	
	def __init__(self):
		'Inicia los objetos con un valor de identificación único'
		xbeeNodo.id+=1
		self.id=xbeeNodo.id
		self.temperatura=0
		self.humedad=0
		self.lux=0
		
	def setDatos(self,datosRf):
		'''Crea una lista con las datos recibidosy luego separa los parámetros
		de humedad, temperatura e intensidad luminosa'''
		self.listaDatos=datosRf.split(">")
		
		try:
			self.humedad=int(self.listaDatos[0])
			self.temperatura=int(self.listaDatos[1])
			self.lux=int(self.listaDatos[2])
		except IndexError:
			print("IndexError-listaDatos:{}".format(self.listaDatos))
		
	def getHumedad(self):
		'Retorna el valor de humedad relativa'
		return self.humedad/10
		
	def getTemperatura(self):
		'Retorna el valor de temperatura'
		return self.temperatura/10
		
	def getLux(self):
		'Retorna el valor de lux'
		return self.lux
		
	 
