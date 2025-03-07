#!/bin/bash
set -e

COMPILATION_START_TIME=$(date +%s)  # when the compilation started

# move to sources folder
cd sources/

FONTS_DIR="../fonts"
FONTS_DIR_LIST=(otf ttf variable webfonts)  # all directories in FONTS_DIR
FONTS_TYPE_LIST=(otf ttf ttf woff2)  # type of the file of each folder defined above
UFO_DIR="ufo/"  # where the ufo source files are (don't forget the '/' at the end!)
UFO_LIST=$(ls $UFO_DIR)  # list of all files inside UFO_DIR
FONTNAME="Giphurs"

# Empty the fonts folder (for real making a copy of it)
echo -e "\x1b[0;36mCleaning the fonts folder\x1b[0;0m"
rm -rf "${FONTS_DIR}-backup"
mv $FONTS_DIR "${FONTS_DIR}-backup"
mkdir $FONTS_DIR
echo "Done."

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

# Build the font (the touch command is needed otherwhise I dunno why some non-encoded glyphs don't get updated)...
echo -e "\x1b[0;36mBuilding the fonts\x1b[0;0m"
touch Giphurs.designspace && touch Giphurs-Italic.designspace && gftools builder config.yaml

# Fix incorrect name of the weight 1000
WEIGHT_1000_OLD_NAME="Giphurs-ExtraBlack"
WEIGHT_1000_NEW_NAME="GiphursExtraBlack-Regular"
WEIGHT_1000_ITALIC_OLD_NAME="Giphurs-ExtraBlackItalic"
WEIGHT_1000_ITALIC_NEW_NAME="GiphursExtraBlack-Italic"
mv $FONTS_DIR/otf/$WEIGHT_1000_OLD_NAME.otf $FONTS_DIR/otf/$WEIGHT_1000_NEW_NAME.otf 
mv $FONTS_DIR/ttf/$WEIGHT_1000_OLD_NAME.ttf $FONTS_DIR/ttf/$WEIGHT_1000_NEW_NAME.ttf 
mv $FONTS_DIR/webfonts/$WEIGHT_1000_OLD_NAME.woff2 $FONTS_DIR/webfonts/$WEIGHT_1000_NEW_NAME.woff2
mv $FONTS_DIR/otf/$WEIGHT_1000_ITALIC_OLD_NAME.otf $FONTS_DIR/otf/$WEIGHT_1000_ITALIC_NEW_NAME.otf 
mv $FONTS_DIR/ttf/$WEIGHT_1000_ITALIC_OLD_NAME.ttf $FONTS_DIR/ttf/$WEIGHT_1000_ITALIC_NEW_NAME.ttf 
mv $FONTS_DIR/webfonts/$WEIGHT_1000_ITALIC_OLD_NAME.woff2 $FONTS_DIR/webfonts/$WEIGHT_1000_ITALIC_NEW_NAME.woff2

# Build SC variants of the fonts
for (( i=0; i<4; i++));
do
    font_sub_dir=${FONTS_DIR_LIST[$i]}
    font_type=${FONTS_TYPE_LIST[$i]}
    font_dir_full="${FONTS_DIR}/${font_sub_dir}"
    font_list=$(ls $font_dir_full)
    for font in $font_list
    do
        font_extension=$(echo $font | cut -d"." -f2)
        sc_font_file_name=""
        if [[ $font =~ "[" ]]
        then
            font_name=$(echo $font | cut -d"[" -f1)
            font_axis=$(echo $font | cut -d"[" -f2 | cut -d"]" -f1)
            sc_font_file_name="${font_name}SC[${font_axis}].${font_extension}"
        else
            font_name=$(echo $font | cut -d"-" -f1)
            font_weight=$(echo $font | cut -d"-" -f2)
            sc_font_file_name="${font_name}SC-${font_weight}"
        fi
        pyftfeatfreeze -f "smcp" -S -U "SC" $font_dir_full/$font $font_dir_full/$sc_font_file_name
        echo "Done building $sc_font_file_name"
    done
    wait
done

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
rm -rf "${FONTS_DIR}-backup"
cd $FONTS_DIR/otf
ls | grep backup | xargs rm
cd ../ttf
ls | grep backup | xargs rm
cd ../webfonts
ls | grep backup | xargs rm
echo "Done."

# Go back to where we come from
cd ../..

# Sucess message
COMPILATION_END_TIME=$(date +%s)  # when the compilation finished
COMPILATION_DURATION=$(($COMPILATION_END_TIME-$COMPILATION_START_TIME))
echo -e "\x1b[1;32mFonts built succesfully in "$COMPILATION_DURATION" second(s) UwU\x1b[0;0m"
