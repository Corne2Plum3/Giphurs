#!/bin/bash
set -e

# without '/' !!!
FONT_FILES=$(find fonts/variable -type f)
OUTPUT_DIR="output/proof"

PROOF_START_TIME=$(date +%s)

mkdir -p $OUTPUT_DIR

if [ -z FONT_FILES ]
then
    echo -e "\x1b[0;33mWARNING: No font files found to make proof.\x1b[0;0m"
else
    diffenator2 proof $FONT_FILES -o $OUTPUT_DIR
fi

PROOF_END_TIME=$(date +%s)
PROOF_DURATION=$(($PROOF_END_TIME-$PROOF_START_TIME))
echo -e "\x1b[1;32mProofs done succesfully in "$PROOF_DURATION" second(s) UwU\x1b[0;0m"
