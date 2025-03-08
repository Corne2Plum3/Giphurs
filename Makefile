.PHONY: export_fonts proof tests clean clean_fonts 

# Name of the font
FONT_NAME := Giphurs

# Paths (without '/' for directories!)
UFO_DIR := ./sources

UFO_ACCENTED_GLYPHS_SCRIPT := "scripts/ufo_accented_glyphs.py"
UFO_COMPOSITE_GLYPHS_SCRIPT := "scripts/ufo_composite_glyphs.py"
UFO_DIGITS_GLYPHS_SCRIPT := "scripts/ufo_digits_glyphs.py"
UFO_USE_TYPO_METRICS_SCRIPT := "scripts/ufo_use_typo_metrics.py"

# documentaton
help:
	@echo "Available make commands:"
	@echo "  * make clean        : Remove temporary and useless generated files, including UFO sources."
	@echo "  * make clean_fonts  : Empties the current fonts/ folder."
	@echo "  * make export_fonts : Export fonts/ directory into a zip file."
	@echo "  * make fonts        : Generate font binaries from UFO sources."
	@echo "  * make proof        : Creates HTML specimens of the font (in output/ directory) and opens the HTML report in your web browser."
	@echo "  * make tests        : Runs automated tests (in output/ directory) and opens the HTML report in your web browser."
	@echo "UFO sources scripts"
	@echo "  * make ufo_accented_glyphs  : Build accented glyphs (the UFO files must be opened and exported throught Fontforge after)."
	@echo "  * make ufo_composite_glyphs : Build composite glyphs (the UFO files must be opened and exported throught Fontforge after, and accented glyphs has to be already built)."
	@echo "  * make ufo_digits_glyphs    : Build digits based glyphs (the UFO files must be opened and exported throught Fontforge after)."
	@echo "  * make ufo_use_typo_metrics : Enable bit 7 ("use typo metrics") of openTypeOS2Selection in fontinfo.plist"

# make a zip archive of the font folder
export_fonts:
	font_version=$$(./sources/get_font_version.sh $$(find fonts/ -type f | head -n 1)); zip -r $(FONT_NAME)_fonts_v$$font_version.zip fonts/ OFL.txt

# build the fonts (otf, ttf, woof2, static + variables)
fonts: sources/
	./scripts/build_fonts.sh

# create HTML specimens of the (variable) fonts
proof: fonts/
	./sources/proof.sh

# run fontbakery tests
tests: fonts/
	./sources/tests.sh

# build accented glyphs
ufo_accented_glyphs: sources/
	UFO_FILES=$$(find $(UFO_DIR) -name "*.ufo" 2>/dev/null); \
	for ufo in $$UFO_FILES; do python3 $(UFO_ACCENTED_GLYPHS_SCRIPT) $${ufo}; done
	@echo "OPEN EACH UFO FILE WITH FONTFORGE AND EXPORT THEM AS UFO WITHOUT CHANGING ANYTHING TO FINISH THE PROCESS!!!"

# build composite glyphs (should be run AFTER ufo_accented_glyphs)
ufo_composite_glyphs: sources/
	UFO_FILES=$$(find $(UFO_DIR) -name "*.ufo" 2>/dev/null); \
	for ufo in $$UFO_FILES; do python3 $(UFO_COMPOSITE_GLYPHS_SCRIPT) $${ufo}; done
	@echo "OPEN EACH UFO FILE WITH FONTFORGE AND EXPORT THEM AS UFO WITHOUT CHANGING ANYTHING TO FINISH THE PROCESS!!!"

# build number based glyphs
ufo_digits_glyphs: sources/
	python3 $(UFO_DIGITS_GLYPHS_SCRIPT) 100 $(UFO_DIR)/$(FONT_NAME)-Thin.ufo
	python3 $(UFO_DIGITS_GLYPHS_SCRIPT) 400 $(UFO_DIR)/$(FONT_NAME)-Regular.ufo
	python3 $(UFO_DIGITS_GLYPHS_SCRIPT) 1000 $(UFO_DIR)/$(FONT_NAME)-ExtraBlack.ufo
	python3 $(UFO_DIGITS_GLYPHS_SCRIPT) 100i $(UFO_DIR)/$(FONT_NAME)-ThinItalic.ufo
	python3 $(UFO_DIGITS_GLYPHS_SCRIPT) 400i $(UFO_DIR)/$(FONT_NAME)-Italic.ufo
	python3 $(UFO_DIGITS_GLYPHS_SCRIPT) 1000i $(UFO_DIR)/$(FONT_NAME)-ExtraBlackItalic.ufo
	@echo "OPEN EACH UFO FILE WITH FONTFORGE AND EXPORT THEM AS UFO WITHOUT CHANGING ANYTHING TO FINISH THE PROCESS!!!"

# edit fontinfo.plist to set the bit 7 of openTypeOS2Selection ("use typo metrics")
# Note: This is currently automatically run when building fonts
ufo_use_typo_metrics: sources/
	UFO_FILES=$$(find $(UFO_DIR) -name "*.ufo" 2>/dev/null); \
	for ufo in $$UFO_FILES; do python3 $(UFO_USE_TYPO_METRICS_SCRIPT) $${ufo}; done

# Cleaning process
clean:
	rm -rf output/
	rm -rf scripts/__pycache__
	rm -rf $(UFO_DIR)/instance_ufos
	rm -f $(UFO_DIR)/*.ninja
	rm -f $(UFO_DIR)/.fuse_hidden*
	rm -f $(UFO_DIR)/.ninja_log
	rm -f *.zip

clean_fonts:
	rm -rf fonts/
	rm -rf fonts-backup/
	mkdir fonts
	cd fonts/ && mkdir otf ttf variable webfonts
