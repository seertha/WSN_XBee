#Pruebas de teclado matricial 4x4
from teclado_4x4 import keyb

def btnPress(boton):
    print("Se presionó el boton: {}".format(boton))

kpad=keyb()
kpad.keypad.registerKeyPressHandler(btnPress)
print("programa Inicio")
while True:
    try:
        pass
    except KeyboardInterrupt:
        break
    
kpad.keypad.cleanup()
print("Fin programa")    