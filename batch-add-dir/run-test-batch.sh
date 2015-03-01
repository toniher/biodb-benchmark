#/bin/sh

PASSWORD=$2
FASTA=$1
DIREND=../dir
TMPDIR=/data/temp

BATCHES="100;1000;10000;100000"

BATCH=$(echo $BATCHES | tr ";" "\n")

for B in $BATCH
do
        >&2 echo "BATCH: $B"
	>&2 echo "SPLIT"
	time ./splitindir.sh $FASTA $DIREND

	>&2 echo "COUCHDB - DROP"
	time curl -silent -X DELETE http://admin:$PASSWORD@localhost:5984/testseq
	>&2 echo "COUCHDB - ADD"
	time python batch-couchdb-add.py $DIREND $PASSWORD $B

	>&2 echo "REDIS - DROP"
	time redis-cli 'flushdb';
	>&2 echo "REDIS - ADD"
	time python batch-redis-add.py $DIREND $B
done
