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
			tramaDatos=xbee.wait_read_frame()
			xbeeCoor.setTramaDic(tramaDatos)
			nodoAddr=xbeeCoor.getAddress()
			if xbeeCoor.nuevoNodo(nodoAddr):
				xbeeCoor.setListaNodos(nodoAddr)
			if xbeeCoor.getDatosRf()!=None:
				xbeeCoor.listaNodos[nodoAddr].setDatos(xbeeCoor.getDatosRf())
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
			break
		
			
if __name__=="__main__":
	main()
