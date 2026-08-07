.PHONY: archive proof tests clean clean_fonts setup_venv

# Name of the font
FONT_NAME := Giphurs
FONT_VERSION := 3.000

# Paths (without '/' for directories!)
FONT_DIR := ./fonts
ONE_FONT_FILE := ./fonts/ttf/Giphurs-Regular.ttf  # Used to grab the font version when generating images
IMAGES_DIR := ./documentation
IMAGES_PREPROCESSING_SCRIPT := ./documentation/svg_version_and_commit.py
UFO_DIR := ./sources
UFO_COMPOSED_GENERATOR_SCRIPT := "scripts/composed_glyphs_generator.py"
UFO_COMPOSED_SCRIPT := "scripts/ufo_composed_glyphs.py"
UFO_COMPOSED_CSV_1 := "scripts/composed_glyphs.csv"  # filled by hand
UFO_COMPOSED_CSV_2 := "scripts/composed_glyphs_generated.csv"  # filled by UFO_COMPOSED_SCRIPT
UFO_SET_VERSION := "scripts/ufo_set_version.py"
UFO_USE_TYPO_METRICS_SCRIPT := "scripts/ufo_use_typo_metrics.py"

SVGS := $(wildcard $(IMAGES_DIR)/*.svg)
PNGS := $(SVGS:.svg=.png)

# documentaton
help:
	@echo "Available make commands:"
	@echo "  * make archive      : Export fonts/ directory into a zip file (created at the project's root directory)"
	@echo "  * make build        : Generate font binaries from UFO sources."
	@echo "  * make clean        : Remove temporary and useless generated files, including UFO sources."
	@echo "  * make clean_fonts  : Empties the current fonts/ folder."
	@echo "  * make proof        : Creates HTML specimens of the font (in output/ directory) and opens the HTML report in your web browser."
	@echo "  * make images       : Prints font version and commit number on SVG previews and converts them to PNG if inkscape is installed."
	@echo "  * make tests        : Runs automated tests (in output/ directory) and opens the HTML report in your web browser."
	@echo "UFO sources scripts"
	@echo "  * make ufo_composed_glyphs  : Build all glyphs based on other glyphs across all UFOs (the UFO files must be opened and exported with Fontforge after, and accented glyphs has to be already built)."
	@echo "  * ufo_set_version           : Change version string inside sources/ UFOs (value defined in the Makefile as FONT_VERSION variable.)"
	@echo "  * make ufo_use_typo_metrics : Enable bit 7 ("use typo metrics") of openTypeOS2Selection in fontinfo.plist"

# make a zip archive of the font folder
archive:
	font_version=$$(./scripts/get_font_version.sh $$(find fonts/ -type f | head -n 1)); zip -r $(FONT_NAME)_fonts_v$$font_version.zip fonts/ OFL.txt

# build the fonts (otf, ttf, woof2, static + variables)
build: sources/
	python3 ./scripts/build.py

# generate the images of the font
images: $(PNGS)

$(IMAGES_DIR)/%.png: $(IMAGES_DIR)/%.svg
	python3 $(IMAGES_PREPROCESSING_SCRIPT) $< $(ONE_FONT_FILE) "version"
	which inkscape || (echo "inkscape not found. You have to convert all SVG files inside documentation/ to PNG manually." && exit 1)
	inkscape "$<" --export-type="png" -o "$@"

# create HTML specimens of the (variable) fonts
proof: fonts/
	./scripts/proof.sh

# run fontbakery tests
tests: fonts/
	./scripts/tests.sh

# build composed glyphs (accented + composite + digits)
# Updates UFO_COMPOSED_CSV_2 and then edit UFOs
ufo_composed_glyphs: scripts/ sources/
	python3 $(UFO_COMPOSED_GENERATOR_SCRIPT) $(UFO_COMPOSED_CSV_2) --all
	python3 $(UFO_COMPOSED_SCRIPT) $(UFO_DIR)/$(FONT_NAME)-Thin.ufo 100 1 $(UFO_COMPOSED_CSV_1) $(UFO_COMPOSED_CSV_2)
	python3 $(UFO_COMPOSED_SCRIPT) $(UFO_DIR)/$(FONT_NAME)-ThinItalic.ufo 100 2 $(UFO_COMPOSED_CSV_1) $(UFO_COMPOSED_CSV_2)
	python3 $(UFO_COMPOSED_SCRIPT) $(UFO_DIR)/$(FONT_NAME)-Regular.ufo 400 1 $(UFO_COMPOSED_CSV_1) $(UFO_COMPOSED_CSV_2)
	python3 $(UFO_COMPOSED_SCRIPT) $(UFO_DIR)/$(FONT_NAME)-Italic.ufo 400 2 $(UFO_COMPOSED_CSV_1) $(UFO_COMPOSED_CSV_2)
	python3 $(UFO_COMPOSED_SCRIPT) $(UFO_DIR)/$(FONT_NAME)-ExtraBlack.ufo 1000 1 $(UFO_COMPOSED_CSV_1) $(UFO_COMPOSED_CSV_2)
	python3 $(UFO_COMPOSED_SCRIPT) $(UFO_DIR)/$(FONT_NAME)-ExtraBlackItalic.ufo 1000 2 $(UFO_COMPOSED_CSV_1) $(UFO_COMPOSED_CSV_2)

ufo_set_version:
	UFO_FILES=$$(find $(UFO_DIR) -name "*.ufo" 2>/dev/null); \
	for ufo in $$UFO_FILES; do python3 $(UFO_SET_VERSION) $(FONT_VERSION) $${ufo}; done

# edit fontinfo.plist to set the bit 7 of openTypeOS2Selection ("use typo metrics")
# Note: This is currently automatically run when building fonts
ufo_use_typo_metrics: sources/
	UFO_FILES=$$(find $(UFO_DIR) -name "*.ufo" 2>/dev/null); \
	for ufo in $$UFO_FILES; do python3 $(UFO_USE_TYPO_METRICS_SCRIPT) $${ufo}; done

# Cleaning process
clean:
	rm -rf logs/
	rm -rf output/
	rm -rf scripts/__pycache__
	rm -rf scripts/composed_glyphs/__pycache__
	rm -rf sources-inst
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
	cd ..
