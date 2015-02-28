#/bin/sh

source $1
PASSWORD=$2
TMPDIR=/data/temp

BATCHES="100;1000;10000;100000"

BATCH=$(echo $BATCHES | tr ";" "\n")

for B in $BATCH
do
	>&2 echo "BATCH: $B"
	
	>&2 echo "COUCHDB - DROP" 
	time curl -silent -X DELETE http://admin:$PASSWORD@localhost:5984/testseq
	>&2 echo "COUCHDB - ADD"
	time python batch-couchdb-add.py $FASTA $PASSWORD $B
	>&2 echo "COUCHDB - QUERY"
	time python batch-couchdb-query.py $SEQ


	>&2 echo "REDIS - DROP"
	time redis-cli 'flushdb';
	>&2 echo "REDIS - ADD"
	time python batch-redis-add.py $FASTA $B
	>&2 echo "REDIS - QUERY"
	time python batch-redis-query.py $SEQ

done
