#Menú que se ejecuta en el arranque del sistema. Permite ejecutar
#el programa principal

import visualizacion_lcd.py
from teclado_4x4 import keyb
from pantallaLCD import LCDpantalla
import time

def main():
    #Pantalla LCD
    panLCD=LCDpantalla() 
    #Teclado matricial 4x4
    tec=keyb()
    try:
        #tec.keypad.registerKeyPressHandler(boton_pulsado)
        pantallaInicio(panLCD)
        time.sleep(15)
        panLCD.clear()
        tec.keypad.cleanup()            
    except KeyboardInterrupt:
        panLCD.clear()
        tec.keypad.cleanup()
        

def pantallaInicio(panLCD):
    panLCD.clear()
    panLCD.set_cursor(3,1)
    panLCD.message("ZIGBEE NETWORK")
    panLCD.set_cursor(7,2)
    panLCD.message("Ver.1")

if __name__=="__name__":
    main()
