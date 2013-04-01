from blanco import Class
from blanco import Horse
from blanco.legacy import MdbFile


def load_old(src_file):
	with MdbFile(src_file) as mdb:
		horses = Horse.legacy_load_all(mdb)
		classes = Class.legacy_load_all(mdb)
		for c in classes:
			print(c)

def migrate(src_file, dst_file):
	load_old(src_file)	


if __name__=="__main__":
	migrate("C:\\Blanco\\MAR2013.mdb", "C:\\Blanco\\new_db.sql")
		
