TOMO_DIR="./tomograms"                                                                                                  
SEGMENT_DIR="./segmentations"

for TOMO in $TOMO_DIR/*.hdf; do
        if [[ ! -f "${TOMO%.hdf}.mrc" ]]; then
            echo "Converting $TOMO to MRC format"
            e2proc3d.py "$TOMO" "${TOMO%.hdf}.mrc"
        fi 
done

for SEGMENT in $SEGMENT_DIR/*.hdf; do
        if [[ ! -f "${SEGMENT%.hdf}.mrc" ]]; then
            echo "Converting $SEGMENT to MRC format"
            e2proc3d.py "$SEGMENT" "${SEGMENT%.hdf}.mrc"
        fi
done
