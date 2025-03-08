#!/bin/bash
set -e

# without '/' for directories and without extension for files!!!
FONT_DIR="fonts"
FONT_FILES=$(find $FONT_DIR/variable -type f | grep -E -v "(SC|.woff2)")  # font files to check
BADGES_DIR="output/badges"
BADGE_LOCAL_VERSION_SVG="output/badges/localFontVersion"
BADGE_OVERALL_SVG="output/badges/overall"
REPORTS_DIR="output/fontbakery"
REPORTS_FILES=$REPORTS_DIR/fontbakery-report

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

# Creating the badges from the README and testing page.
echo -e "\x1b[0;36mCreating the Fontbakery badge...\x1b[0;0m"
# ... fontbakery QA
BADGE_VALUE=$(cat $BADGES_DIR/overall.json | jq .message | tr -d '"%')
curl "https://img.shields.io/badge/FontBakery_QA-"$BADGE_VALUE"%25-hsl("$BADGE_VALUE",100%25,35%25)?style=flat-square" > $BADGE_OVERALL_SVG".svg"
# ... local font version
FONT_FILE_TO_CHECK=$(find $FONT_DIR/ -type f | grep -E -v "(SC|.woff2|\[)" | head -n 1)
FONT_VERSION=$(./scripts/get_font_version.sh $FONT_FILE_TO_CHECK)
curl "https://img.shields.io/badge/Local_fonts_version-"$FONT_VERSION"-black?style=flat-square" > $BADGE_LOCAL_VERSION_SVG".svg"

# Open the report in the web browser
echo -e "\x1b[0;36mOpening generated HTML report in your web browser...\x1b[0;0m"
HTML_REPORT_PATH="file://"$(pwd)"/"$REPORTS_FILES".html"
xdg-open "$HTML_REPORT_PATH"
