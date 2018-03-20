#Definición de clase para interactuar con un teclado matricial 4x4.
from pad4pi import rpi_gpio

class keyb():
    '''
    Clase para crear objetos que interactuen con un teclado
    4x4.
    '''
    def __init__(self):
        '''
        Inicializaciones de atributos
        '''
        self.KEYPAD=[
            ["1","2","3","A"],
            ["4","5","6","B"],
            ["7","8","9","C"],
            ["*","0","#","D"]
        ]
        self.COL_PINS=[27,22,10,9]
        self.ROW_PINS=[2,3,4,17]
        self.factory=rpi_gpio.KeypadFactory()
        self.keypad=self.factory.create_keypad(keypad=self.KEYPAD,row_pins=self.ROW_PINS,col_pins=self.COL_PINS)
        #self.keypad.registerKeyPressHandler(funcionExt)
#
#    def botonPulsado(self,boton):
#        '''
#        Registra y retorna el botón pulsado en el teclado.
#        '''
#        self.btnPress=boton
#        print(self.btnPress)
#        return self.btnPress

