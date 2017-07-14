#Módulo principal
from xbee import XBee,ZigBee
from modulosXbee import nodoXbee
from time import localtime, strftime
import serial

def main():
	'''
	Se crea un objeto Coordinador que recibe la información a través
	del puerto serial.
	'''
	puerto_serie=serial.Serial('/dev/ttyUSB0',9600)
	xbee=ZigBee(puerto_serie)
	xbeeCoor=nodoXbee()						#objeto coordinador
	
	while True:
		try:
			tramaDatos=xbee.wait_read_frame()		#Espera la recepción de una trama de datos
			datos=xbeeCoor.actualizarDatos(tramaDatos)	#Actualiza la trama en xbeeCoor
			if datos==True:
				tiempoDatos=strftime("%H:%M:%S %d/%m/%Y")
				xbeeCoor.guardarDatos(tiempoDatos)
		except KeyboardInterrupt:
			puerto_serie.close()	


if __name__=="__main__":
	main()
