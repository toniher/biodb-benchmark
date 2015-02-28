import sys
import os
import MySQLdb
from Bio import SeqIO
from os import listdir
from os.path import isfile, join

def main(argv):

		# Put stuff in JSON config file
		myDB = 'test'
		myUser = 'toniher'

		conn = MySQLdb.connect(host="localhost", # your host, usually localhost
				user=myUser, # your username
				db=myDB) # name of the data base

		c = conn.cursor()
		# Create table
		c.execute('''CREATE TABLE SEQS ( id varchar(32) PRIMARY KEY, seq text )''')

		batch = 1000
		if len( argv ) > 1:
				batch = int(argv[1])
		
		onlyfiles = [ argv[0]+"/"+f for f in listdir(argv[0]) if isfile(join(argv[0],f)) ]
		
		for fastafile in onlyfiles:
		
			itera = 0

			handle = open( fastafile, "r")
			for record in SeqIO.parse(handle, "fasta") :
					c.execute("INSERT INTO SEQS VALUES ('" + str(record.id) + "', '" + str(record.seq) + "' )")
					itera = itera + 1
					if itera > batch :
							conn.commit()
							itera = 0
		
			if itera > 0:
					conn.commit()

			handle.close()
			
			
		conn.close()


if __name__ == "__main__":
		main(sys.argv[1:])
