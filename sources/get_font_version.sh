#!/bin/bash

# This script put the version of a font file given in parameter in STDIN.
# IMPORTANT: Do NOT use variable font otherwise it won't work!

set -e

if [ -z $1 ]
then
    echo -e "\x1b[0;31m"$0": No file provided\x1b[0;0m"
    echo "Usage: "$0" font-file"
fi;
RAW_VERSION=$(fc-query -f '%{fontversion}\n' $1)
VERSION_NUM=$(echo "scale=3;"$(echo $RAW_VERSION"+16" | bc)"/65536" | bc)

if (( $(echo "$VERSION_NUM < 1.0" | bc -l) ))
then
    echo "0"$VERSION_NUM
else
    echo $VERSION_NUM
fi;
