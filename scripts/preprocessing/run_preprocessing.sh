
BATCHDIR="/media/michalakdj/scratch/data/wws1/"
ST_DIR="ts002"
ALIGNBINNING=5
SUMBINNING=1

NUMCPUS=36
STARTINGSTEP=0
ENDINGSTEP=7
#run_alignframes --batchdir $BATCHDIR #--alignbinning $ALIGNBINNING --sumbinning $SUMBINNING

run_batchruntomo --batchdir $BATCHDIR --numcpus 24 --startingstep $STARTINGSTEP --endingstep $ENDINGSTEP --alignbinning $ALIGNBINNING 
#--stackdir $ST_DIR
