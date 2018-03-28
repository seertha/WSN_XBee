#Muestra la información en un display 20x4
from pantallas import pantalla_lcd
import time

def main():

    #db_dir='/home/pi/xbeeProyecto/basesTest/xbee_db02.db'
    db_dir='/home/pi/dataBases/dbTest03.db'
    pantalla=pantalla_lcd(db_dir)
    pantalla.menuInicio()

    while True:
        try:
            time.sleep(0.2)
        except KeyboardInterrupt:
            break
            pantalla.finalizar()

if __name__=="__main__":
    main()