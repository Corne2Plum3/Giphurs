#!/bin/bash
set -e

COMPILATION_START_TIME=$(date +%s)  # when the compilation started

# move to sources folder
cd sources/

# don't forget the '/' at the end!
UFO_DIR="ufo/"  # where the ufo source files are (don't forget the '/' at the end!)
UFO_LIST=$(ls $UFO_DIR)  # list of all files inside UFO_DIR

# Applying some change to ufo file
for dst in $UFO_LIST
do
    echo "Applying some changes on $UFO_DIR$dst"
    echo "Copying lib.plist into $UFO_DIR$dst"
    cp -f lib.plist $UFO_DIR$dst
    python3 ufo_use_typo_metrics.py $UFO_DIR$dst
done
python3 numbers_glyphs.py 100 ufo/Giphurs-Thin.ufo
python3 numbers_glyphs.py 400 ufo/Giphurs-Regular.ufo
python3 numbers_glyphs.py 900 ufo/Giphurs-Black.ufo

echo "Done editing UFO files."

# Build the font (the touch command is needed otherwhise I dunno why some glyphs above the )
touch Giphurs.designspace && gftools builder config.yaml

# Go back to where we come from
cd ..

# sucess message
COMPILATION_END_TIME=$(date +%s)  # when the compilation finished
COMPILATION_DURATION=$(($COMPILATION_END_TIME-$COMPILATION_START_TIME))
echo -e "\x1b[1;32mFonts built succesfully in "$COMPILATION_DURATION" second(s) UwU\x1b[0;0m"
