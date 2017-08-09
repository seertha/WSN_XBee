#Menu que muestra los nodos registrados en la base de datos y los
#muestra en un display LCD 16x2
import Adafruit_CharLCD as LCD
import RPi.GPIO as GPIO
import sqlite3

GPIO.setmode(GPIO.BCM)
GPIO.setup(4,GPIO.IN)
#Variable de control
numeroMenu=0
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

def conectarBase(base_path):
    try:
        cnx=sqlite3.connect(base_path)
        return cnx
    except Error as e:
        print(e)
    return None

def consulta(cnx,sql):
    cur=cnx.cursor()
    cur.execute(sql)
    return cur.fetchall()

def base_nodos():
    lista_aux=[]
    base_datos="basePath"
    sql_con="SELECT nodo_id FROM nodoSensor"
    conn=conectarBase(base_datos)
    res=consulta(cnx,sql_con)
    for e in range(len(res)):
        lista_aux.append(res[e][0])
    return lista_aux

def pulsador(numeroMenu,cantidad_nodos):
    control=numeroMenu
    print("Pulsador presionado")
    control+=1
    lcd.clear()
    #lcd.set_cursor(0,0)
    if control>cantidad_nodos:
     return 0
    else:
     return control

def mostrarPantalla(numeroMenu):
    lcd.set_cursor(5,0)
    lcd.message("NODO ")
    lcd.set_cursor(10,0)
    lcd.message(str(numeroMenu))

GPIO.add_event_detect(4,GPIO.FALLING,bouncetime=200)

lista_nodos=base_nodos()
lcd.show_cursor(False)
lcd.clear()
print("Programa inicado")
mostrarPantalla(lista_nodos[numeroMenu])

while True:
    try:
        if GPIO.event_detected(4):
         numeroMenu=pulsador(numeroMenu,len(lista_nodos))
         mostrarPantalla(lista_nodos[numeroMenu])
        
    except KeyboardInterrupt:
        lcd.clear()
        GPIO.cleanup()
        break
print("Programa finalizado")