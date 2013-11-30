# """
# Reads from the legacy Access '97 MDB file.
# """

# #http://code.google.com/p/pyodbc/wiki/Features
# #http://stackoverflow.com/questions/827502/pyodbc-and-microsoft-access-inconsistent-results-from-simple-query


# import csv
# import pyodbc


# class MdbFile(object):

# 	def __init__(self, file_path):		
# 		MDB = file_path #"C:\\Blanco\\MAR2013.mdb"
# 		DRV = '{Microsoft Access Driver (*.mdb)}'
# 		PWD = 'pw'
# 		self.con_string = 'DRIVER=%s;DBQ=%s;PWD=%s' % (DRV, MDB, PWD)			

# 	def __enter__(self):
# 		self.con = pyodbc.connect(self.con_string)
# 		self.cur = self.con.cursor()
# 		return self

# 	def execute(self, query):
# 		return self.cur.execute(query).fetchall()

# 	def __exit__(self, type, value, tb):
# 		self.cur.close()
# 		self.con.close()

# 	def list_columns(self, table_name):
# 		for row in self.cur.columns(table_name):
# 			yield row

# 	def list_row_id_columns(self, table_name):
# 		for row in self.cur.rowIdColumns(table_name):
# 			yield row

# 	def list_tables(self):
# 		for row in self.cur.tables():
# 			yield row
