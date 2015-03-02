import sys
import os
import MySQLdb
from Bio import SeqIO


def main(argv):

		# Put stuff in JSON config file
		myDB = 'test'
		myUser = 'root'
		myPass = argv[1]

		conn = MySQLdb.connect(host="localhost", # your host, usually localhost
				user=myUser, # your username
				db=myDB, # name of the data base
				passwd=myPass) 

		c = conn.cursor()
		# Avoid problems http://www.percona.com/blog/2008/07/03/how-to-load-large-files-safely-into-innodb-with-load-data-infile/
		c.execute('''set foreign_key_checks=0;''')
		c.execute('''set sql_log_bin=0;''')
		c.execute('''set unique_checks=0;''')

		# Create table
		c.execute('''CREATE TABLE SEQS ( id varchar(32) PRIMARY KEY, seq text )''')

		c.execute( "LOAD DATA INFILE '"+os.path.abspath( argv[0] )+"' INTO TABLE SEQS" )
		conn.commit()
		conn.close()


if __name__ == "__main__":
		main(sys.argv[1:])
