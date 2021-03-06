#Módulo principal
from xbee import XBee,ZigBee
from modulosXbee import nodoXbee
import datetime
import serial
import logging

def main():
	'''
	Se crea un objeto Coordinador que recibe la información a través
	del puerto serial.
	'''
	puerto_serie=serial.Serial('/dev/ttyUSB0',9600)
	xbee=ZigBee(puerto_serie)
	xbeeCoor=nodoXbee()						#objeto coordinador
	logging.basicConfig(filename='/home/pi/xbeeProyecto/logs/principal.log',format=('%(asctime)s %(message)s'),level=logging.DEBUG)
	logging.info("Programa principal.py iniciado.")
	while True:
		try:
			tramaDatos=xbee.wait_read_frame()		#Espera la recepción de una trama de datos
			datos=xbeeCoor.actualizarDatos(tramaDatos)	#Actualiza la trama en xbeeCoor
			if datos==True:
				#tiempoDatos=strftime("%d-%m-%Y %H:%M:%S")
				tiempoDatos=datetime.datetime.now().isoformat()
				xbeeCoor.guardarDatos(tiempoDatos)
		except KeyboardInterrupt:
			puerto_serie.close()
			break	


if __name__=="__main__":
	main()
