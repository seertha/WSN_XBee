#Prueba de conexión y consulta con la base de datos
import sqlite3

conn=sqlite3.connect('/media/CasaL/st/Documentos/sqliteDB/wsnDB.db')
cur=conn.cursor()

def consulta(dato):
    sql_consulta=('''SELECT {} 
                FROM datos
                ORDER BY fecha_hora DESC
                LIMIT 1'''.format(dato))
    cur.execute(sql_consulta,)
    respuesta=cur.fetchall()
    return respuesta[0][0]


temperatura=consulta("temperatura")
humedad=consulta("humedadR")
lux=consulta("lux")
print ("TEMP:{} HUM:{} LUX:{}".format(temperatura,humedad,lux))
conn.close()