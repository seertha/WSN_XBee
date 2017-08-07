#Prueba de navegación de un menú de opciones utiizando un pulsador.
#El pulsador está conectado al pin 4 (Modo BCM) 
#Salida a través de un LCD 16x2
import Adafruit_CharLCD as LCD
import RPi.GPIO as GPIO
import time

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

def pulsador(canal):
    print("Pulsador presionado")
    numeroMenu+=1
    lcd.clear()
    if numeroMenu>3:
        numeroMenu=0

def mostrarPantalla(numeroMenu):
    if numeroMenu==0:
        lcd.set_cursor(5,0)
        lcd.message("MENU 1")
    elif numeroMenu==1:
        lcd.set_cursor(5,0)
        lcd.message("MENU 2")
    elif numeroMenu==2:
        lcd.set_cursor(5,0)
        lcd.message("MENU 3")
    elif numeroMenu==3:
        lcd.set_cursor(5,0)
        lcd.message("MENU 4")


GPIO.add_event_detect(4,GPIO.FALLING,callback=pulsador,bouncetime=200)
lcd.show_cursor(False)
lcd.clear()
print("Programa inicado")

while True:
    try:
        mostrarPantalla(numeroMenu)
        #time.sleep(0.5)
    except KeyboardInterrupt:
        lcd.clear()
        GPIO.cleanup()
        break
print("Programa finalizado")