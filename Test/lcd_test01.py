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

#conectar con base de datos
conn=sqlite3.connect('/home/pi/dataBases/dbTest01.db')
cur=conn.cursor()

def consulta(dato):
    '''dato:(str) 
        -temperatura
        -humedadR
        -lux '''
    sql_consulta=('''SELECT {} 
                FROM datos
                ORDER BY fecha_hora DESC
                LIMIT 1'''.format(dato))
    cur.execute(sql_consulta,)
    respuesta=cur.fetchall()
    return str(respuesta[0][0])

while True:
    try:
        temperatura=consulta("temperatura")
        humedad=consulta("humedadR")
        lux=consulta("lux")
        #mostrar datos en lcd
        lcd.set_cursor(0,0)
        lcd.message('TEMP:')
        lcd.set_cursor(5,0)
        lcd.message(temperatura)
        lcd.set_cursor(0,1)
        lcd.message('HUMR:')
        lcd.set_cursor(5,1)
        lcd.message(humedad)
        lcd.set_cursor(10,0)
        lcd.message('|')
        lcd.set_cursor(10,1)
        lcd.message('|')
        lcd.set_cursor(11,0)
        lcd.message('LUX:')
        lcd.set_cursor(11,1)
        lcd.message(lux)
        time.sleep(5)
    except KeyboardInterrupt:
        lcd.clear()
        conn.close()
        break
    
