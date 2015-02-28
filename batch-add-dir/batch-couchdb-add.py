import sys
import os
import couchdb
from Bio import SeqIO
from os import listdir
from os.path import isfile, join

def main(argv):

		# Put stuff in JSON config file
		couchServer = 'http://localhost:5984/'
		couchDB = 'testseq'
		couch = couchdb.Server(couchServer)
		couch.resource.credentials = ( 'admin', argv[1] )
	
		# In case admin permissions
		try:
			db = couch.create(couchDB)
		except Exception:
			couch.delete(couchDB)
			db = couch.create(couchDB)

		batch = 1000
		if len( argv > 2 ):
				batch = int(argv[2])

		onlyfiles = [ argv[0]+"/"+f for f in listdir(argv[0]) if isfile(join(argv[0],f)) ]
		
		for fastafile in onlyfiles:

			listDocs = []
			itera = 0

			handle = open( fastafile, "r")
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
