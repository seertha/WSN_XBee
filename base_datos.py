#Módulo para comunicación con la base de datos
import sqlite3

class db():
	'''
	Maneja las conexiones con la base de datos.
	'''

	def __init__(self,db_path):
		'''
		Crea la conexión con la base de datos.
		'''
		self.cnx=sqlite3.connect(db_path)
		self.cur=self.cnx.cursor()

	def consultaSimp(self,sql):
		'''
		Consulta de datos simple
		'''
		self.cur.execute(sql)
		return self.cur.fetchall()

	def consultaDat(self,sql,datos):
		'''
		Consulta con varios parámetros.
		'''
		self.cur.execute(sql,datos)
		return self.cur.fetchall()        

	def insertarDatos(self,sql,datos):
		'''
		Inserta datos en la base de datos.
		'''
		self.cur.executemany(sql,datos)
		self.cnx.commit()

	def cnxClose(self):
		'''
		Cierra la conexión con la base de datos.
		'''
		self.cnx.close()