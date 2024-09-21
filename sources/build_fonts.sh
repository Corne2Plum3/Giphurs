#!/bin/bash
set -e

COMPILATION_START_TIME=$(date +%s)  # when the compilation started

# move to sources folder
cd sources/

FONTS_DIR="../fonts"
UFO_DIR="ufo/"  # where the ufo source files are (don't forget the '/' at the end!)
UFO_LIST=$(ls $UFO_DIR)  # list of all files inside UFO_DIR
FONTNAME="Giphurs"

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

# Build the font (the touch command is needed otherwhise I dunno why some non-encoded glyphs don't get updated...
echo -e "\x1b[0;36mBuilding the fonts\x1b[0;0m"
touch Giphurs.designspace && gftools builder config.yaml

# Fix incorrect name of the weight 1000
WEIGHT_1000_OLD_NAME="Giphurs-ExtraBlack"
WEIGHT_1000_NEW_NAME="GiphursExtraBlack-Regular"
WEIGHT_1000_SC_OLD_NAME="GiphursSC-ExtraBlack"
WEIGHT_1000_SC_NEW_NAME="GiphursSCExtraBlack-Regular"
mv $FONTS_DIR/otf/$WEIGHT_1000_OLD_NAME.otf $FONTS_DIR/otf/$WEIGHT_1000_NEW_NAME.otf 
mv $FONTS_DIR/ttf/$WEIGHT_1000_OLD_NAME.ttf $FONTS_DIR/ttf/$WEIGHT_1000_NEW_NAME.ttf 
mv $FONTS_DIR/webfonts/$WEIGHT_1000_OLD_NAME.woff2 $FONTS_DIR/webfonts/$WEIGHT_1000_NEW_NAME.woff2 
mv $FONTS_DIR/otf/$WEIGHT_1000_SC_OLD_NAME.otf $FONTS_DIR/otf/$WEIGHT_1000_SC_NEW_NAME.otf 
mv $FONTS_DIR/ttf/$WEIGHT_1000_SC_OLD_NAME.ttf $FONTS_DIR/ttf/$WEIGHT_1000_SC_NEW_NAME.ttf 

# Add hinting
echo -e "\x1b[0;36mAdd hinting on font binaries\x1b[0;0m"
OTF_LIST=$(ls $FONTS_DIR/otf)
for font in $OTF_LIST
do
    gftools fix-nonhinting $FONTS_DIR/otf/$font $FONTS_DIR/otf/$font &
done
TTF_LIST=$(ls $FONTS_DIR/ttf)
for font in $TTF_LIST
do
    gftools fix-nonhinting $FONTS_DIR/ttf/$font $FONTS_DIR/ttf/$font &
done
WOFF2_LIST=$(ls $FONTS_DIR/webfonts)
for font in $WOFF2_LIST
do
    gftools fix-nonhinting $FONTS_DIR/webfonts/$font $FONTS_DIR/webfonts/$font &
done

wait

# Clean backup files
echo -e "\x1b[0;36mRemoving backup files\x1b[0;0m"
cd $FONTS_DIR/otf
ls | grep backup | xargs rm
cd ../ttf
ls | grep backup | xargs rm
cd ../webfonts
ls | grep backup | xargs rm

# Go back to where we come from
cd ../..

# Sucess message
COMPILATION_END_TIME=$(date +%s)  # when the compilation finished
COMPILATION_DURATION=$(($COMPILATION_END_TIME-$COMPILATION_START_TIME))
echo -e "\x1b[1;32mFonts built succesfully in "$COMPILATION_DURATION" second(s) UwU\x1b[0;0m"
