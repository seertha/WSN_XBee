#Muestra la información en un display 20x4
from pantallas import pantalla_lcd
import time

db_dir='/home/pi/xbeeProyecto/basesTest/xbee_db02.db'
pantalla=pantalla_lcd(db_dir)
pantalla.menuInicio()

while True:
    try:
        time.sleep(0.2)
    except KeyboardInterrupt:
        break
pantalla.finalizar()