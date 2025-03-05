#!/bin/bash
set -e

# without '/' !!!
FONT_FILES=$(find fonts/variable -type f | grep -E -v "(SC|.woff2)")  # font files to check
BADGES_DIR="output/badges"
REPORTS_DIR="output/fontbakery"
REPORTS_FILES=$REPORTS_DIR/fontbakery-report  # without extension!

# Generating the test reports
TESTING_START_TIME=$(date +%s)

mkdir -p $BADGES_DIR $REPORTS_DIR
echo -e "\x1b[0;36mFiles to check: "$FONT_FILES"\x1b[0;0m"

if [ -z FONT_FILES ]
then
    echo -e "\x1b[0;33mWARNING: No file to test found.\x1b[0;0m"
else
    FAIL_MSG="\x1b[0;33mWARNING: The fontbakery QA check reported errors in your font. Please check the generated report.\x1b[0;0m"
    fontbakery check-googlefonts -l WARN --full-lists --succinct --badges $BADGES_DIR --html $REPORTS_FILES.html --ghmarkdown $REPORTS_FILES.md $FONT_FILES || echo -e $FAIL_MSG
fi

TESTING_END_TIME=$(date +%s)  # when the compilation finished
TESTING_DURATION=$(($TESTING_END_TIME-$TESTING_START_TIME))
echo -e "\x1b[1;32mTests done succesfully in "$TESTING_DURATION" second(s) UwU\x1b[0;0m"

