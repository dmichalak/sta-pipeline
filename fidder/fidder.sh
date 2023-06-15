INPUT_MRC="wws1_ts002_ali.mrc"
PIX=4.33
PROB_THRESHOLD=0.5
OUTPUT_MASK="maskfid.mrc"
OUTPUT_IMAGE="wws1_ts002_ali_nofid_prob${PROB_THRESHOLD}.mrc"

fidder predict --input-image $INPUT_MRC --pixel-spacing $PIX --output-mask $OUTPUT_MASK --probability-threshold $PROB_THRESHOLD &&
	fidder erase --input-image $INPUT_MRC --input-mask $OUTPUT_MASK --output-image $OUTPUT_IMAGE
