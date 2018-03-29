#Muestra la información en un display 20x4
import pantallaLCD
from pantallas2 import pantalla_lcd
import time

def main():

    #db_dir='/home/pi/xbeeProyecto/basesTest/xbee_db02.db'
    panLCD=pantallaLCD.LCDpantalla()
    db_dir='/home/pi/dataBases/dbTest03.db'
    pantalla=pantalla_lcd(db_dir,panLCD.lcd)
    pantalla.saludoInicial()
    time.sleep(10)
    pantalla.menuInicio()

    while True:
        try:
            time.sleep(0.2)
        except KeyboardInterrupt:
            pantalla.finalizar()
            break
if __name__=="__main__":
    main()
