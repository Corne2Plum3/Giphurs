#!/bin/bash
set -e

COMPILATION_START_TIME=$(date +%s)  # when the compilation started

# move to sources folder
cd sources/

UFO_DIR="ufo/"  # where the ufo source files are (don't forget the '/' at the end!)
UFO_LIST=$(ls $UFO_DIR)  # list of all files inside UFO_DIR
FONTNAME="Giphurs"
WEIGHT_1000_SRC="Giphurs-ExtraBlack.ufo"

# Applying some change to ufo file
echo -e "\x1b[0;36mApplying some changes to the ufo sources.\x1b[0;0m"
for dst in $UFO_LIST
do
    echo "Applying some changes on $UFO_DIR$dst"
    echo "Copying lib.plist into $UFO_DIR$dst"
    cp -f lib.plist $UFO_DIR$dst
    echo "Setting bit 7 of openTypeOS2Selection in fontinfo.plist"
    python3 ufo_use_typo_metrics.py $UFO_DIR$dst
done

echo "Done editing UFO files."

# Build the font (the touch command is needed otherwhise I dunno why some glyphs above th
echo -e "\x1b[0;36mBuilding the fonts (weight 100-900)\x1b[0;0m"
touch Giphurs.designspace && gftools builder config.yaml

# Rebuild weight 1000
echo -e "\x1b[0;36mRebuilding font binaries for weight 1000\x1b[0;0m"
WEIGHT_1000_BINARY_NAME=$(echo $WEIGHT_1000_SRC | cut -d '.' -f 1)
TEMP_OTF_PATH="/tmp/"$WEIGHT_1000_BINARY_NAME"_temp.otf"
TEMP_TTF_PATH="/tmp/"$WEIGHT_1000_BINARY_NAME"_temp.ttf"
TEMP_WOFF2_PATH="/tmp/"$WEIGHT_1000_BINARY_NAME"_temp.woff2"
fontmake -u $UFO_DIR/$WEIGHT_1000_SRC -o otf --output-path $TEMP_OTF_PATH
gftools fix-font $TEMP_OTF_PATH -o ../fonts/otf/$WEIGHT_1000_BINARY_NAME.otf
fontmake -u $UFO_DIR/$WEIGHT_1000_SRC -o ttf --output-path $TEMP_TTF_PATH
gftools fix-font $TEMP_TTF_PATH -o ../fonts/ttf/$WEIGHT_1000_BINARY_NAME.ttf
fonttools ttLib.woff2 compress ../fonts/ttf/$WEIGHT_1000_BINARY_NAME.ttf -o $TEMP_WOFF2_PATH
gftools fix-font $TEMP_WOFF2_PATH -o ../fonts/webfonts/$WEIGHT_1000_BINARY_NAME.woff2

# Add hinting
echo -e "\x1b[0;36mRebuilding font binaries for weight 1000\x1b[0;0m"
OTF_LIST=$(ls ../fonts/otf)
for font in $OTF_LIST
do
    gftools fix-nonhinting ../fonts/otf/$font ../fonts/otf/$font
done
TTF_LIST=$(ls ../fonts/ttf)
for font in $TTF_LIST
do
    gftools fix-nonhinting ../fonts/ttf/$font ../fonts/ttf/$font
done
WOFF2_LIST=$(ls ../fonts/webfonts)
for font in $WOFF2_LIST
do
    gftools fix-nonhinting ../fonts/webfonts/$font ../fonts/webfonts/$font
done

# clean backup files
cd ../fonts/otf
ls | grep backup | xargs rm
cd ../ttf
ls | grep backup | xargs rm
cd ../webfonts
ls | grep backup | xargs rm

# Go back to where we come from
cd ../..

# sucess message
COMPILATION_END_TIME=$(date +%s)  # when the compilation finished
COMPILATION_DURATION=$(($COMPILATION_END_TIME-$COMPILATION_START_TIME))
echo -e "\x1b[1;32mFonts built succesfully in "$COMPILATION_DURATION" second(s) UwU\x1b[0;0m"
