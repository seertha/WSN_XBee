#Menú que se ejecuta en el arranque del sistema. Permite ejecutar
#el programa principal

#import visualizacion_lcd
from teclado_4x4 import keyb
from pantallaLCD import LCDpantalla
import time

def main():
    #Pantalla LCD
    panLCD=LCDpantalla() 
    #Teclado matricial 4x4
    tec=keyb()
    try:
        print("Programa iniciado")
        #tec.keypad.registerKeyPressHandler(boton_pulsado)
        pantallaInicio(panLCD)
        time.sleep(15)
        panLCD.lcd.clear()
        tec.keypad.cleanup()            
    except KeyboardInterrupt:
        panLCD.lcd.clear()
        tec.keypad.cleanup()
        

def pantallaInicio(panLCD):
    panLCD.lcd.clear()
    panLCD.lcd.set_cursor(3,1)
    panLCD.lcd.message("ZIGBEE NETWORK")
    panLCD.lcd.set_cursor(7,2)
    panLCD.lcd.message("Ver.1")

if __name__=="__main__":
    main()