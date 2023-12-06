SEGMENT_DIR="/mnt/scratch/ribosomes/kas_k44a/eman2/segmentations"

for SEGMENT in $SEGMENT_DIR/*.hdf; do
        if [[ ! -f "${SEGMENT%.hdf}.mrc" ]]; then
            echo "Converting $SEGMENT to MRC format"
            e2proc3d.py "$SEGMENT" "${SEGMENT%.hdf}.mrc"
        fi
done
