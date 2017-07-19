#El programa consulta la última información registrada en la
#base de datos y la muestra en un diplay LCD 16x2.
#Ver:1.0
import time
import sqlite3
import Adafruit_CharLCD as LCD

#Conexión de pines
lcd_rs =7       #25
lcd_en =5       #24
lcd_d4 =6       #23
lcd_d5 =13      #17
lcd_d6 =19      #21
lcd_d7 =26      #22

#columnas y filas
lcd_columns =16
lcd_rows =2

#Inicializar LCD
lcd=LCD.Adafruit_CharLCD(lcd_rs, lcd_en, lcd_d4, lcd_d5, lcd_d6, lcd_d7, lcd_columns,lcd_rows)

lcd.show_cursor(False)
lcd.clear()
lcd.set_cursor(4,0)
lcd.message('WSN-XBEE')
lcd.set_cursor(4,1)
lcd.message('ver1.0')
time.sleep(5)
lcd.clear()

