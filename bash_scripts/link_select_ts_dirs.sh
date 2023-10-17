#!/bin/bash

TEXT_FILE=$1

for TS_DIR in $(cat $TEXT_FILE); do
    echo "Creating a symbolic link to $TS_DIR"
    TS_DIR_NAME=$(basename $TS_DIR)
    ln -s $TS_DIR $TS_DIR_NAME
done