#Módulo principal
from xbee import XBee,ZigBee
from modulosXbee import coordinadorXbee
import serial

def main():
	'''
	Se crea un objeto Coordinador que recibe la información a través
	del puerto serial.
	'''
	puerto_serie=serial.Serial('/dev/ttyUSB0',9600)
	xbee=ZigBee(puerto_serie)
	xbeeCoor=coordinadorXbee()						#objeto coordinador
	
	while True:
		try:
			tramaDatos=xbee.wait_read_frame()		#Espera la recepción de una trama de datos
			xbeeCoor.setTramaDic(tramaDatos)		#Actualiza la trama en xbeeCoor
			nodoAddr=xbeeCoor.getAddress()			#Obtiene la dirreción de origen de la trama
			if xbeeCoor.nuevoNodo(nodoAddr):		#Si la dirección es de un nodo recién conectado a la red lo agrega a la lista de nodos
				xbeeCoor.setListaNodos(nodoAddr)
			datosRf=xbeeCoor.getDatosRf()			#Obtiene los datos de los sensores contenidos en la trama 
			if datosRf!=None:						#Si los datos contienen errores se descartan
				xbeeCoor.listaNodos[nodoAddr].setDatos(datosRf)
				humedad=xbeeCoor.listaNodos[nodoAddr].getHumedad()
				temperatura=xbeeCoor.listaNodos[nodoAddr].getTemperatura()
				lux=xbeeCoor.listaNodos[nodoAddr].getLux()
				nodoId=xbeeCoor.listaNodos[nodoAddr].id
				print("NODOID: {}  HUMEDAD_R: {}  TEMPERATURA: {}  LUX: {}".format(nodoId,humedad,temperatura,lux))
			#datosRf=xbeeCoor.getDatosRf()
			#xbeeAddr=xbeeCoor.getAddress()
			#if datosRf!=None:
				#print("Datos: {} Direccion:{} ListaDatos:{}".format(datosRf,xbeeAddr,xbeeCoor.getListaNodos()))
			#trama_dic=xbeeCoor.getTramaDic()
			#print (trama_dic)
		except KeyboardInterrupt:
			puerto_serie.close()
			break
		
			
if __name__=="__main__":
	main()
