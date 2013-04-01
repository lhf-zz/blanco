# #http://code.google.com/p/pyodbc/wiki/Features
# #http://stackoverflow.com/questions/827502/pyodbc-and-microsoft-access-inconsistent-results-from-simple-query

# import csv, pyodbc

# # set up some constants
# MDB = "C:\\Blanco\\MAR2013.mdb"
# DRV = '{Microsoft Access Driver (*.mdb)}'
# PWD = 'pw'

# # connect to db
# con = pyodbc.connect('DRIVER=%s;DBQ=%s;PWD=%s' % (DRV, MDB, PWD))
# #con = pyodbc.connect("DRIVER={Microsoft Access Driver (*.mdb)};"#
# #	                 "DBQ=c:\\sbc\\apr2013.mdb;PWD=pw")
# cur = con.cursor()

# # run a query and get the results 

# # you could change the mode from 'w' to 'a' (append) for any subsequent queries
# # with open('mytable.csv', 'wb') as fou:
# #     csv_writer = csv.writer(fou) # default field-delimiter is ","
# #     csv_writer.writerows(rows)

# for row in cur.tables():
# 	print(row)

# print("HORSE")
# for row in cur.columns("Horses"):
# 	print(row)

# # SQL = 'SELECT * FROM Horses;' # your query goes here
# # rows = cur.execute(SQL).fetchall()
# # print("\n\nHORSES!\n\n")
# # for row in rows:
# # 	print(row)

# cur.close()
# con.close()

from blanco.legacy import *

def print_table_info(t_name):
	db_name = t_name
	print(" * *  %s  * *" % db_name)
	for c in mdb.list_columns(db_name):
		print(c[3] + "\t" + c[5])

 	print("^_^")
	for c in mdb.list_row_id_columns(db_name):
		print(c[3] + " " + c[5])
	print("o _ o ")
	for r in mdb.execute("SELECT * FROM '%s'" % db_name):
		print(r)
		break


with MdbFile("C:\\Blanco\\MAR2013.mdb") as mdb:
	for table in mdb.list_tables():
		print(table)
	print("\n \n")
	# 	for column in mdb.list_columns(table[2]):
	# 		print("\t%s" % column)

	print_table_info("Next Number")	
	
	
