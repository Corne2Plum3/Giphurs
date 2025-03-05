#!/bin/bash
set -e

# without '/' !!!
FONT_DIR="fonts/variable"
FONT_FILES=$(find $FONT_DIR -type f | grep -E -v "(SC|.woff2)")
OUTPUT_DIR="output"


TESTING_START_TIME=$(date +%s)
mkdir -p $OUTPUT_DIR/ $OUTPUT_DIR/fontbakery
echo -e "\x1b[0;36mFiles to check: "$FONT_FILES"\x1b[0;0m"

if [ -z FONT_FILES ]
then
    echo -e "\x1b[0;33mWARNING: No file to test found.\x1b[0;0m"
else
    FAIL_MSG="\x1b[0;33mWARNING: The fontbakery QA check reported errors in your font. Please check the generated report.\x1b[0;0m"
    fontbakery check-googlefonts -l WARN --full-lists --succinct --badges $OUTPUT_DIR/badges --html $OUTPUT_DIR/fontbakery/fontbakery-report.html --ghmarkdown $OUTPUT_DIR/fontbakery/fontbakery-report.md $FONT_FILES || echo -e $FAIL_MSG
fi

TESTING_END_TIME=$(date +%s)  # when the compilation finished
TESTING_DURATION=$(($TESTING_END_TIME-$TESTING_START_TIME))
echo -e "\x1b[1;32mTests done succesfully in "$TESTING_DURATION" second(s) UwU\x1b[0;0m"