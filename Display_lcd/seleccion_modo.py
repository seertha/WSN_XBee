#Pantalla de selección de modo de operación.
#La interacción es a través de un teclado matricial 4x4.
import Adafruit_CharLCD as LCD
from pad4pi import rpi_gpio
import time 

#Conexión de pines
lcd_rs =7       #25
lcd_en =5       #24
lcd_d4 =6       #23
lcd_d5 =13      #17
lcd_d6 =19      #21
lcd_d7 =26      #22

#columnas y filas
lcd_columns =20
lcd_rows =4

#Configuraciones keypad
KEYPAD=[
    ["1","2","3","A"],
    ["4","5","6","B"],
    ["7","8","9","C"],
    ["*","0","#","D"]
]

COL_PINS=[10,9,11,8]
ROW_PINS=[12,16,20,21]

factory=rpi_gpio.KeypadFactory()
keypad=factory.create_keypad(keypad=KEYPAD,row_pins=ROW_PINS,col_pins=COL_PINS)

#Iniciar LCD
lcd=LCD.Adafruit_CharLCD(lcd_rs, lcd_en, lcd_d4, lcd_d5, lcd_d6, lcd_d7, lcd_columns,lcd_rows)
lcd.show_cursor(False)
lcd.clear()
print("Programa iniciado")

#Funciones

def botonPulsado(boton):
    '''
    Registra el botón pulsado, si es válido ejecuta la acción
    Valores aceptados para opciones: A,B,C,D,*,#
    '''
    global punteroPos
    global controlAux
    
    if boton=="A":
        selecciónModo(punteroPos)
        controlAux=False        
    elif boton=="B":
        controlAux=True
        pantallaInicial()
        posicionPuntero(punteroPos)
        print("Pantalla principal")
    elif controlAux==True: 
        if boton=="C" or boton=="D":
            punteroPos+=valorBoton(boton)
            if punteroPos>3: punteroPos=3
            if punteroPos<1: punteroPos=1
            print("boton {} presionado. Valor puntero {}".format(boton,punteroPos))
            posicionPuntero(punteroPos)
    


def pantallaInicial():
    '''
    Pantalla principal del selector de modo.
    Valor del puntero (1-3)
    '''
    lcd.clear()
    lcd.message(" SELECCION DE MODO:")
    lcd.set_cursor(1,1)
    lcd.message("Info. General")
    lcd.set_cursor(1,2)
    lcd.message("Nodos Detalle")
    lcd.set_cursor(1,3)
    lcd.message("Resumen")
    

def posicionPuntero(puntero=1):
    
    pantallaInicial()
    lcd.set_cursor(15,puntero)
    lcd.message("*")



def valorBoton(boton):
    '''Devuelve el valor del botón pulsado'''
    if boton=='C':valor=-1
    if boton=='D':valor=1
    return valor

def selecciónModo(punteroPos):
    '''Ingresa en el modo seleccionado'''
    if punteroPos==1: infoGeneral()
    if punteroPos==2: nodosDetalle()
    if punteroPos==3: resumen()
    

def infoGeneral():
    '''Muestra la información general'''
    lcd.clear()
    lcd.message("INFORMACION GENERAL")
    print("Pantalla info general")

def nodosDetalle():
    '''Muestra la información detallada de cada nodo'''
    lcd.clear()
    lcd.message("DETALLE NODOS")
    print("Pantalla detalle nodos")

def resumen():
    '''Muestra un resumen general del sistema'''
    lcd.clear()
    lcd.message("RESUMEN")
    print("Pantalla resumen")

pantallaInicial()
punteroPos=1
controlAux=True
posicionPuntero(punteroPos)
keypad.registerKeyPressHandler(botonPulsado)

while True:
    try:
        time.sleep(0.5)
    except KeyboardInterrupt:
        break
    except:
        break
lcd.clear()
keypad.cleanup()
print("Programa finalizado")