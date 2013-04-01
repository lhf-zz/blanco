import sqlite3

class Database(object):

	def __init__(self, file_path):
		self.file = file_path

	def __enter__(self):
		self.con = sqlite3.connect(self.file)
		self.cur = self.con.cursor()
		return self

	def __exit__(self, type, value, tb):
		self.cur.close()
		self.con.close()

	

