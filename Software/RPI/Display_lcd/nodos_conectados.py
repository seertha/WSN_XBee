#Prueba para mostrar los nodos conectados a la red
from base_datos import db
import time
from datetime import timedelta, datetime,date
dir_base="/media/CasaL/st/Documentos/proyectoXbee/WSN_XBee/basesTest/xbee_db02.db"
d=timedelta(minutes=-10)
#now=datetime.now()
#calculo=now+d
#print(calculo.strftime("%H:%M:%S"))

#hoy=datetime.now()
#miFecha=date(hoy.year,7,13)
#miHoraFecha=datetime(2017,7,13,20,13)
#print(miFecha.strftime("%Y/%m/%d"))
#print(miHoraFecha)
conFechaHora='''SELECT fecha_hora FROM datos ORDER BY fecha_hora DESC LIMIT 1'''
base=db(dir_base)
ultimoRegistro=base.consultaSimp(conFechaHora)[0][0]
aux1=ultimoRegistro.split(" ")
horaReg=aux1[0].split(":")
fechaReg=aux1[1].split("/")
aux_ini=datetime(int(fechaReg[2]),int(fechaReg[1]),int(fechaReg[0]),int(horaReg[0]),int(horaReg[1]),int(horaReg[2]))
aux_final=aux_ini+d
hora_inicio=aux_ini.strftime("%H:%M:%S %d/%m/%Y")
hora_final=aux_final.strftime("%H:%M:%S %d/%m/%Y")
print (hora_final)
#print("Hora inicio: {} Hora final: {}".format(ref_ini,ref_ini+d))
respuesta=base.consultaDat('''SELECT nodo_id FROM datos WHERE fecha_hora
                            BETWEEN ? and ?''',(hora_final,hora_inicio))
lista_nodos=[]
for e in respuesta:
    if e[0] not in lista_nodos:
        lista_nodos.append(e[0])
nodos_conn=len(lista_nodos)
print("Existen {} nodos conectados a la red".format(nodos_conn))

