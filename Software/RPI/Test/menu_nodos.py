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

def base_nodos(base_path):
    '''Retorna una lista con los nodos registrados en la base 
    de datos
    '''
    lista_aux=[]
    sql_con="SELECT nodo_id FROM nodoSensor"
    conn=conectarBase(base_path)
    res=consulta(conn,sql_con)
    for e in range(len(res)):
        lista_aux.append(res[e][0])
    conn.close()
    return lista_aux

def pulsador(numeroMenu,cantidad_nodos):
    control=numeroMenu
    print("Pulsador presionado")
    control+=1
    lcd.clear()
    #print(cantidad_nodos)
    #print (control)
    if control>cantidad_nodos:
     return 0
    else:
     return control

def mostrarPantalla(numeroMenu,base_path):
    '''    Muestra en el display LCD el nodo y sus datos correspondientes.
    '''
    datos_nodo=obtenerDatos(numeroMenu,base_path)
    #print(datos_nodo)
    if len(datos_nodo)<3:
     lcd.set_cursor(5,0)
     lcd.message("NODO ")
     lcd.set_cursor(10,0)
     lcd.message(str(numeroMenu))
     lcd.set_cursor(2,1)
     lcd.message("ERROR DATOS")
    else:
     temp=datos_nodo[0]
     hum=datos_nodo[1]
     lux=datos_nodo[2]
     lcd.set_cursor(0,0)
     lcd.message("NODO:")
     lcd.set_cursor(5,0)
     lcd.message(str(numeroMenu))
     lcd.set_cursor(9,0)
     lcd.message("T:")
     lcd.set_cursor(11,0)
     lcd.message(str(temp))
     lcd.set_cursor(0,1)
     lcd.message("HR:")
     lcd.set_cursor(3,1)
     lcd.message(str(hum))
     lcd.set_cursor(9,1)
     lcd.message("L:")
     lcd.set_cursor(11,1)
     lcd.message(str(lux))

def obtenerDatos(nodo,base_path):
    '''Retorna una lista conteniendo los últimos datos registrados en
    la base de datos por el sensor especificado en nodo
    '''
    lista_aux=[]
    sql_con=('''SELECT temperatura,humedadR,lux
            FROM datos WHERE nodo_id={}
            ORDER BY fecha_hora DESC
            LIMIT 1'''.format(nodo))
    conn=conectarBase(base_path)
    resp=consulta(conn,sql_con)
    #print("Res_con:{}".format(resp))
    for e in resp:
        for x in e:
         lista_aux.append(x)
    conn.close()
    return lista_aux


GPIO.add_event_detect(4,GPIO.FALLING,bouncetime=200)
base_datos="/home/pi/xbeeProyecto/basesTest/xbee_db02.db"
lista_nodos=base_nodos(base_datos)
lcd.show_cursor(False)
lcd.clear()
print("Programa inicado")
mostrarPantalla(lista_nodos[numeroMenu],base_datos)

while True:
    try:
        if GPIO.event_detected(4):
         numeroMenu=pulsador(numeroMenu,len(lista_nodos)-1)
         mostrarPantalla(lista_nodos[numeroMenu],base_datos)
        
    except KeyboardInterrupt:
        lcd.clear()
        GPIO.cleanup()
        break
print("Programa finalizado")
