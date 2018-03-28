#Módulo para el manejo del display LCD 20x4
import Adafruit_CharLCD as LCD

class LCDpantalla(object):
    '''
    Clase para el manejo de display LCD 20X4
    '''
    def __init__(self):
        #Conexión de pines
        self.lcd_rs =26           #7       
        self.lcd_en =19           #5       
        self.lcd_d4 =13           #6
        self.lcd_d5 =6           #13
        self.lcd_d6 =5           #19
        self.lcd_d7 =11           #26

        #columnas y filas
        self.lcd_columns =20
        self.lcd_rows =4

        #Inicio LCD
        self.lcd=LCD.Adafruit_CharLCD(self.lcd_rs,self.lcd_en,self.lcd_d4,self.lcd_d5,self.lcd_d6,self.lcd_d7,self.lcd_columns,self.lcd_rows)
        self.lcd.show_cursor(False)
        self.lcd.clear()