#Este archivo contiene las clases para el módulo coordinador y el módulo sensor

class coordinadorXbee:
	'Representa un nodo coordinador en una red XBEE'
	def __init__(self):
		'''
		Inicializa las variables de temperatura, humedad,lux y
		la variable trama_dic que contiene los datos.
		'''
		self.temperatura=0
		self.humedad=0
		self.lux=0		
		self.trama_dic={}
		self.rf_dataStr=""
		self.listaNodos=[]
		
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
	
	def getAddress(self):
		'Retorna la dirección del nodo sensor remoto'
		self.xbeeAddrStr=""
		for e in self.trama_dic['source_addr_long']:
			self.aux=hex(e)
			self.xbeeAddrStr+=self.aux[1:]
		return self.xbeeAddrStr
		
	def getListaNodos(self):
		'''Guarda una lista con las direcciones de los nodos conectados 
		a la red.
		'''
		self.auxAddr=self.getAddress()
		if self.auxAddr not in self.listaNodos:
			self.listaNodos.append(self.auxAddr)
		return self.listaNodos			
		
		
	def __str__(self):
		'Para depuración'
		return str(self.listaNodos)
	 
