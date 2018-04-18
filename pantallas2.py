#Clases para el manejo y muestra de pantallas.
#LCD 20x4
#import Adafruit_CharLCD as LCD
import os.path
import subprocess
from teclado_4x4 import keyb
from time import strftime,sleep
from threading import Thread
from base_datos import db
from datetime import timedelta,datetime

class pantalla_lcd(object):
    def __init__(self,db_dir,panlcd):
       
        #Pantalla LCD
        self.lcd=panlcd

        #Teclado matricial 4x4
        self.kpad=keyb()
        self.kpad.keypad.registerKeyPressHandler(self.botonPulsado)

        #Pantallas
        self.modoSelec=seleccion_modo()
        self.db_path=db_dir
        self.general=infoGen(self.lcd,self.db_path)
        self.nodos=nodosDetalle(self.lcd,self.db_path)
        self.res=resumen(self.lcd,self.db_path)
        self.opt=opciones(self.lcd)

        #Puntero de selección
        self.puntero=1
        self.puntero2=0
        self.puntero3=0
        self.controlAux=True
        
        
        #Threads
        self.th_ini_infoGen=Thread(target=self.general.mostrarDatos)
        self.th_end_infoGen=Thread(target=self.general.salir_modo)
        #self.th_ini_nodosDet=Thread(target=self.nodos.mostrar,args=(self.puntero2,))
        self.th_ini_nodosDet=Thread(target=self.nodos.mostrar)
        self.th_end_nodosDet=Thread(target=self.nodos.salir_loop)
        self.th_ini_resumen=Thread(target=self.res.resMostrar)
        self.th_end_resumen=Thread(target=self.res.resSalir)

    def saludoInicial(self):
        self.lcd.set_cursor(2,1)
        self.lcd.message("ZIGBEE NETWORK")
        self.lcd.set_cursor(7,2)
        self.lcd.message("Ver 1")

    def posicionPuntero(self,puntero):
        if puntero<4:
            self.lcd.set_cursor(15,puntero)
            self.lcd.message("*")
        else:
            self.lcd.set_cursor(15,1)
            self.lcd.message("*")

    def menuInicio(self,puntero=1):
        self.modoSelec.mostrar(self.lcd,puntero)
        self.posicionPuntero(puntero)
    
    def botonPulsado(self,boton):        
        #print("boton {} pulsado".format(boton))
        if boton=="A":
            self.controlAux=False 
            self.modo_enter(self.puntero)
             
                 
        elif boton=="B":
            self.puntero2=0
            self.puntero3=0
            self.nodos.nIndex=0
            self.res.mostrarCntrl=0
            self.general.infoGenCtrl=0
            self.threadCheck(self.th_end_infoGen,self.general.salir_modo)
            self.threadCheck(self.th_end_nodosDet,self.nodos.salir_loop)
            self.threadCheck(self.th_end_resumen,self.res.resSalir)            
            self.controlAux=True
            self.menuInicio(self.puntero)
            print("Pantalla principal")
            

        elif self.controlAux==True: 
            if boton=="C" or boton=="D":
                self.puntero+=self.valorBoton(boton)
                if self.puntero>3: self.puntero=4
                if self.puntero<1: self.puntero=1
                print("boton {} presionado. Valor puntero {}".format(boton,self.puntero))
                self.menuInicio(self.puntero)
                
        elif self.controlAux==False and self.puntero==1:
            if boton=="#": 
                self.general.infoGenCtrl=1
                self.general.infoAux=False
                print("Boton: {}  infoGenCtrl: {}  general.infoAux: {}".format(boton,self.general.infoGenCtrl,self.general.infoAux))
                   
            if boton=="*": 
                self.general.infoGenCtrl=0
                self.general.infoAux=True
                print("Boton: {}  infoGenCtrl: {} general.infoAux: {}".format(boton,self.general.infoGenCtrl,self.general.infoAux))   
                self.modo_enter(self.puntero)   
                
        elif self.controlAux==False and self.puntero==2:
            self.listaAuxNodos=self.nodos.obtenerNodos()
            self.listaAuxNodos.sort()
            self.indexAux=len(self.listaAuxNodos)
            if boton=="*" or boton=="#":
                self.puntero2+=self.valorBoton(boton)
                if self.puntero2>self.indexAux-1: self.puntero2=self.indexAux-1
                if self.puntero2<0: self.puntero2=0 
                self.nodos.nIndex=self.puntero2
                print("boton {} presionado. Valor puntero2 {}".format(boton,self.puntero2))

        elif self.controlAux==False and self.puntero==3:
            if boton=="*" or boton=="#":                
                self.puntero3+=self.valorBoton(boton)
                if self.puntero3>3: self.puntero3=3
                if self.puntero3<0: self.puntero3=0 
                print("puntero3= {}".format(self.puntero3))
                self.res.mostrarCntrl=self.puntero3 

        elif self.controlAux==False and self.puntero==4:
            if boton=="1": 
                self.opt.reiniciar()
            elif boton=="0":
                self.opt.apagar()         
                
                
    
    def valorBoton(self,boton):
        if self.controlAux==True:
            if boton=='C':self.valor=-1
            if boton=='D':self.valor=1
        elif self.controlAux==False:
            if boton=='*':self.valor=-1
            if boton=='#':self.valor=1
        return self.valor
    
    def modo_enter(self,punteroPos):
        if punteroPos==1:
            self.general.mostrar()
            self.threadCheck(self.th_ini_infoGen,self.general.mostrarDatos) 
          
        elif punteroPos==2:
            #self.threadCheckArg(self.th_ini_nodosDet,self.nodos.mostrar,self.puntero2)
            self.threadCheck(self.th_ini_nodosDet,self.nodos.mostrar)

        elif punteroPos==3:
            self.threadCheck(self.th_ini_resumen,self.res.resMostrar) 

        elif punteroPos==4:
            self.opt.mostrar()           
    
    def threadCheckArg(self,th,funcion,arg):
        '''
        Verifica si el thread se encuentra activo, en caso contrario
        lo inicia.
        '''
        if th.is_alive()==False:
            try:
                th.start()
            except:
                th=Thread(target=funcion,args=(arg,))
                th.start()

    def threadCheck(self,th,funcion):
        if th.is_alive()==False:
            try:
                th.start()
            except:
                th=Thread(target=funcion)
                th.start()    
      
    def finalizar(self):
        self.lcd.clear()
        self.kpad.keypad.cleanup()
        


#################################################################
class seleccion_modo(object):
    def mostrar(self,lcd,puntero):
        lcd.clear()
        lcd.message(" SELECCION DE MODO:")
        if puntero<4:
            lcd.set_cursor(1,1)
            lcd.message("Info. General")
            lcd.set_cursor(1,2)
            lcd.message("Nodos Detalle")
            lcd.set_cursor(1,3)
            lcd.message("Resumen")
        elif puntero==4:
            lcd.set_cursor(1,1)
            lcd.message("Opciones")

################################################################
class infoGen(object):
    def __init__(self,lcd,path):
        self.db_path=path
        #self.base=db(self.db_path)
        self.lcdInfo=lcd
        self.tiempo=""
        self.fecha=""
        self.size_bd=0
        self.infoAux=True
        self.file_size=""
        self.unidad="B"
        self.size_aux=0
        self.nodosConn=""
        self.infoGenCtrl=0
        self.SSID=""
        self.ipAddr=""
        
        
    def obtenerDatos(self):
        if self.infoGenCtrl==0:
            self.tiempo=strftime("%H:%M:%S")
            self.fecha=strftime("%d/%m/%Y")
            self.file_size=str(self.tam_archivo(self.db_path))
            self.nodosConn=str(len(self.nodosEnRed()))
        elif self.infoGenCtrl==1:
            self.SSID=self.getSSID()
            self.ipAddr=self.getIpAddr()

    
    def mostrarDatos(self):
        #self.base=db(self.db_path)
        self.infoAux=True
        self.obtenerDatos()

        if self.infoGenCtrl==0:
            #Muestra tamaño de la base de datos
            self.lcdInfo.set_cursor(0,2)
            self.lcdInfo.message("DB:")
            self.lcdInfo.set_cursor(3,2)
            self.lcdInfo.message(self.file_size)
            self.lcdInfo.set_cursor(9,2)
            self.lcdInfo.message(self.unidad)
            #Muestra la cantidad de nodos conectados a la red
            self.lcdInfo.set_cursor(0,3)
            self.lcdInfo.message("Nodos en red:")
            self.lcdInfo.set_cursor(13,3)
            self.lcdInfo.message(self.nodosConn)

            while self.infoAux==True:
                self.obtenerDatos()
                self.lcdInfo.set_cursor(0,1)
                self.lcdInfo.message(self.tiempo)
                self.lcdInfo.set_cursor(9,1)
                self.lcdInfo.message(self.fecha)
                sleep(1)
                #self.base.cnxClose()
            print("InfoGen loop-salida")
        
            if self.infoGenCtrl==1:
                #Muestra información sobre la conexión de red: SSID y dirección IP
                self.mostrar()
                self.obtenerDatos()
                self.lcdInfo.set_cursor(0,1)
                self.lcdInfo.message("RED")
                self.lcdInfo.set_cursor(0,2)
                self.lcdInfo.message("SSID:")
                self.lcdInfo.set_cursor(5,2)
                self.lcdInfo.message(self.SSID)
                self.lcdInfo.set_cursor(0,3)
                self.lcdInfo.message("IP:")
                self.lcdInfo.set_cursor(3,3)
                self.lcdInfo.message(self.ipAddr)
                print("Pantalla info 2")



    def mostrar(self):
        self.lcdInfo.clear()
        self.lcdInfo.message("INFORMACION GENERAL")

    def tam_archivo(self,db_path):
        self.size_aux=os.path.getsize(db_path)
        #print("Tamaño base: {}".format(len(str(self.size_aux))))
        if len(str(self.size_aux))>3 and len(str(self.size_aux))<=6: 
            self.size_aux/=1000
            self.unidad="KB"
        elif len(str(self.size_aux))>6:
            self.size_aux/=1000000
            self.unidad="MB"   
        return round(self.size_aux,1)  

    def nodosEnRed(self):
        self.base=db(self.db_path)
        self.nodosLista=[]
        self.rangoHora=timedelta(minutes=-10)
        self.fechaHoraActual=datetime.now()
        self.aux_ini=self.fechaHoraActual.strftime("%Y-%m-%dT%H:%M:%S.%f")
        self.aux_final=self.fechaHoraActual+self.rangoHora
        self.horaFinal=self.aux_final.strftime("%Y-%m-%dT%H:%M:%S.%f")
        self.resConn=self.base.consultaDat('''SELECT nodo_id FROM datos WHERE fecha_hora
                            BETWEEN ? and ? ORDER BY datetime(fecha_hora) DESC
                            ''',(self.horaFinal,self.aux_ini))
        #print("resConn:{}  len:{}".format(self.resConn,len(self.resConn)))
        for e in self.resConn:
            if e[0] not in self.nodosLista:
                self.nodosLista.append(e[0])
        self.base.cnxClose()        
        return self.nodosLista

    def getSSID(self):
        self.proc1=subprocess.Popen(['iwgetid'],stdout=subprocess.PIPE)
        self.resAux=self.proc1.communicate()[0].decode('utf-8')
        self.res=self.resAux[17:len(self.resAux)-2]
        self.proc1.stdout.close()
        return self.res
    
    def getIpAddr(self):
        self.commAux1=subprocess.check_output(['hostname','-I'])
        print("commAux1:{}".format(self.commAux1))
        self.commAux=self.commAux1.split()[0]
        self.ipAux=self.commAux.decode('utf-8')
        return self.ipAux
        
    def salir_modo(self):
        self.infoAux=False
################################################################
class nodosDetalle(object):
    def __init__(self,lcd,path):
        self.db_path=path
        self.lcdNodos=lcd
        self.lista_nodos=[]
        self.nIndex=0
        #self.base=db(self.db_path)
        self.temp=""
        self.humR=""
        self.lux=""
        self.nodosAux=True

    def obtenerDatos(self):
        self.base=db(self.db_path)
        self.lista_nodos=self.obtenerNodos() 
        self.lista_nodos.sort() 
        self.nodoSensor=self.lista_nodos[self.nIndex]
        self.sql_con=('''SELECT temperatura,humedadR,lux
            FROM datos WHERE nodo_id={}
            ORDER BY datetime(fecha_hora) DESC
            LIMIT 1'''.format(self.nodoSensor))
        self.respAux=self.base.consultaSimp(self.sql_con)
        self.temp=str(self.respAux[0][0])
        self.humR=str(self.respAux[0][1])
        self.lux=str(self.respAux[0][2])
                

    def obtenerNodos(self):
        '''
        Retorna una lista con los nodos conectados a la red.
        '''
        self.nodos=infoGen(self.lcdNodos,self.db_path)
        return self.nodos.nodosEnRed()

    def mostrar(self):
        self.nodosAux=True
        #self.obtenerDatos()
        self.lcdNodos.clear()
        
        while self.nodosAux==True:
            self.obtenerDatos()
            self.lcdNodos.set_cursor(7,0)
            self.lcdNodos.message("NODO #")
            self.lcdNodos.set_cursor(13,0)
            self.lcdNodos.message(str(self.lista_nodos[self.nIndex]))
            self.lcdNodos.set_cursor(0,1)
            self.lcdNodos.message("TEMP:")
            self.lcdNodos.set_cursor(6,1)
            self.lcdNodos.message(self.temp)
            self.lcdNodos.set_cursor(0,2)
            self.lcdNodos.message("HUMR:")
            self.lcdNodos.set_cursor(6,2)
            self.lcdNodos.message(self.humR)
            self.lcdNodos.set_cursor(0,3)
            self.lcdNodos.message("LUX :")
            self.lcdNodos.set_cursor(6,3)
            self.lcdNodos.message(self.lux)
            sleep(1)

    def salir_loop(self):
        self.nodosAux=False
#######################################################################
class resumen(object):
    def __init__(self,lcd,path):
        self.resLcd=lcd
        self.resPath=path
        self.tempPromedio=0
        self.humPromedio=0
        self.luxPromedio=0
        self.resLoopAux=True
        self.mostrarCntrl=0
    
    def resMostrar(self):
        self.resLoopAux=True
        
        while self.resLoopAux==True:
                                  
            if self.mostrarCntrl==0:
                self.resLcd.clear()
                while self.mostrarCntrl==0 and self.resLoopAux==True:
                    self.resObtenerDatos()
                    self.resLcd.set_cursor(0,0)
                    self.resLcd.message("  RESUMEN-PROMEDIO")
                    self.resLcd.set_cursor(0,1)
                    self.resLcd.message("TEMP:")
                    self.resLcd.set_cursor(6,1)
                    self.resLcd.message(str(self.tempPromedio))
                    self.resLcd.set_cursor(0,2)
                    self.resLcd.message("HUMR:")
                    self.resLcd.set_cursor(6,2)
                    self.resLcd.message(str(self.humPromedio))
                    self.resLcd.set_cursor(0,3)
                    self.resLcd.message("LUX :")
                    self.resLcd.set_cursor(6,3)
                    self.resLcd.message(str(self.luxPromedio))
                    sleep(1)
            elif self.mostrarCntrl==1:
                #self.resLoopAux=True  
                self.resLcd.clear()
                while self.mostrarCntrl==1 and self.resLoopAux==True:
                    self.maxMinMostrar("temperatura")
                    sleep(1)                  

            elif self.mostrarCntrl==2:
                self.resLcd.clear()
                while self.mostrarCntrl==2 and self.resLoopAux==True:
                    self.maxMinMostrar("humedadR")
                    sleep(1)
                
            elif self.mostrarCntrl==3:
                self.resLcd.clear()
                while self.mostrarCntrl==3 and self.resLoopAux==True:
                    self.maxMinMostrar("lux")
                    sleep(1)               
            
        print("while out")

    def maxMinMostrar(self,parametro):
        self.listaDatosMax=self.maxMin(parametro,"max")
        self.listaDatosMin=self.maxMin(parametro,"min")
        self.nodoIdMax=self.listaDatosMax[0][0]
        self.parValMax=self.listaDatosMax[0][1]
        self.nodoIdMin=self.listaDatosMin[0][0]
        self.parValMin=self.listaDatosMin[0][1]
        
        if parametro=="temperatura": 
            self.resLcd.set_cursor(4,0)
            self.resLcd.message("TEMPERATURA")
            
        elif parametro=="humedadR": 
            self.resLcd.set_cursor(1,0)
            self.resLcd.message("HUMEDAD RELATIVA")
        elif parametro=="lux":
            self.resLcd.set_cursor(8,0)
            self.resLcd.message("LUX")

        self.resLcd.set_cursor(8,1)
        self.resLcd.message("DIA")
        self.resLcd.set_cursor(0,2)
        self.resLcd.message("MAX:")
        self.resLcd.message(str(self.parValMax))
        self.resLcd.set_cursor(10,2)
        self.resLcd.message("NODO:")
        self.resLcd.message(str(self.nodoIdMax))
        self.resLcd.set_cursor(0,3)
        self.resLcd.message("MIN:")
        self.resLcd.message(str(self.parValMin))
        self.resLcd.set_cursor(10,3)
        self.resLcd.message("NODO:")
        self.resLcd.message(str(self.nodoIdMin))           

    def maxMin(self,parametro,medida):
        self.parametro=parametro
        self.cnxBase=db(self.resPath)        
        self.tmpAux=datetime.now()
        self.inicioDia=self.tmpAux.date().strftime("%Y-%m-%d")+"T00:00:00.000000"
        self.tmpActual=self.tmpAux.strftime("%Y-%m-%dT%H:%M:%S.%f")
        self.sqlDia='''SELECT nodo_id,{}({}) AS maxMin FROM datos
                       WHERE datetime(fecha_hora)
                       BETWEEN datetime(?) AND datetime(?)'''.format(medida,self.parametro)
        self.resConsulta=self.cnxBase.consultaDat(self.sqlDia,(self.inicioDia,self.tmpActual))
        return self.resConsulta

    def resObtenerDatos(self):
        self.res_db=db(self.resPath)
        self.t1Aux=datetime.now()
        self.t2=self.t1Aux.date().strftime("%Y-%m-%d")+"T00:00:00.000000"
        self.t1=self.t1Aux.strftime("%Y-%m-%dT%H:%M:%S.%f")
        self.sqlRes='''SELECT round(avg(temperatura),1) AS temAvg, round(avg(humedadR),1) AS humAvg, round(avg(lux),1) AS luxAvg
                    FROM datos WHERE datetime(fecha_hora)
                    BETWEEN datetime(?) AND datetime(?) '''
        #self.reslsAux=self.res_db.consultaSimp(self.sqlRes)
        self.reslsAux=self.res_db.consultaDat(self.sqlRes,(self.t2,self.t1))
        self.tempPromedio=self.reslsAux[0][0]
        self.humPromedio=self.reslsAux[0][1]
        self.luxPromedio=self.reslsAux[0][2]                
        
    def resSalir(self):        
        self.resLoopAux=False

###################################################################################################################################################
class opciones(object):
    def __init__(self,lcd):
        self.optLcd=lcd
    def mostrar(self):
        self.optLcd.clear()
        self.optLcd.set_cursor(5,0)
        self.optLcd.message("OPCIONES")
        self.optLcd.set_cursor(0,2)
        self.optLcd.message("1: Reiniciar")
        self.optLcd.set_cursor(0,3)
        self.optLcd.message("0: Apagar")

    def reiniciar(self):
        print("Reiniciando...")
        self.optLcd.clear()
        self.optLcd.set_cursor(3,1)
        self.optLcd.message("Reiniciando...")
        sleep(3)
        self.optLcd.clear()
        subprocess.call("sudo reboot",shell=True)

    def apagar(self):
        print("Apagando...")
        self.optLcd.clear()
        self.optLcd.set_cursor(4,1)
        self.optLcd.message("Apagando...")
        sleep(3)
        self.optLcd.clear()
        subprocess.call("sudo halt",shell=True)



