#Muestra la información en un display 20x4
from pantallaLCD import LCDpantalla
from pantallas2 import pantalla_lcd
import time

def main():

    #db_dir='/home/pi/xbeeProyecto/basesTest/xbee_db02.db'
    panLCD=LCDpantalla()
    db_dir='/home/pi/dataBases/dbTest03.db'
    pantalla=pantalla_lcd(db_dir,panLCD)
    pantalla.menuInicio()

    while True:
        try:
            time.sleep(0.2)
        except KeyboardInterrupt:
            break
            pantalla.finalizar()

if __name__=="__main__":
    main()