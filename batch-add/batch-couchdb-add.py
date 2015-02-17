import sys
import os
import couchdb
from Bio import SeqIO


def main(argv):

		# Put stuff in JSON config file
		couchServer = 'http://localhost:5984/'
		couchDB = 'testseq'
		
		couch = couchdb.Server(couchServer)

		# In case admin permissions
		# couch.delete(couchDB)
		# couch.create(couchDB)

		db = couch[couchDB]

		batch = 1000;
		listDocs = [];
		itera = 0

		handle = open( argv[0], "r")
		for record in SeqIO.parse(handle, "fasta") :
				docSeq = dict( _id = record.id, seq = str( record.seq ) )
				listDocs.append( docSeq )
				itera = itera + 1
				if itera > batch :
					db.update( listDocs )
					del listDocs[:]
					itera = 0
		
		if len( listDocs ) > 0 :
				db.update( listDocs )

		handle.close()


if __name__ == "__main__":
		main(sys.argv[1:])