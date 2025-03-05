.PHONY: export_fonts tests clean clean_fonts 

# Name of the font
font_name := Giphurs

# If the version is below 1, a 0 is added
#font_version := $(shell echo "0"$(shell echo "scale=3;("$(shell echo $(shell fc-query -f '%{fontversion}\n' fonts/otf/Giphurs-Regular.otf)"+16" | bc)"/65536)" | bc))
# If the version is 1.000 or above
font_version := $(shell echo $(shell echo "scale=3;("$(shell echo $(shell fc-query -f '%{fontversion}\n' fonts/otf/Giphurs-Regular.otf)"+16" | bc)"/65536)" | bc))

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
	zip -r $(font_name)_fonts_v$(font_version).zip fonts/ OFL.txt

# build the fonts (otf, ttf, woof2, static + variables)
fonts: sources/ufo
	./sources/build_fonts.sh

# create HTML specimens of the (variable) fonts
proof: fonts/
	./sources/proof.sh

# run fontbakery tests
tests: fonts/
	./sources/tests.sh

# build accented glyphs
ufo_accented_glyphs: sources/ufo
	python3 sources/ufo_accented_glyphs.py sources/ufo/Giphurs-Thin.ufo
	python3 sources/ufo_accented_glyphs.py sources/ufo/Giphurs-Regular.ufo
	python3 sources/ufo_accented_glyphs.py sources/ufo/Giphurs-ExtraBlack.ufo
	@echo "OPEN EACH UFO FILE WITH FONTFORGE AND EXPORT THEM AS UFO WITHOUT CHANGING ANYTHING TO FINISH THE PROCESS!!!"

# build composite glyphs (should be run AFTER ufo_accented_glyphs)
ufo_composite_glyphs: sources/ufo
	python3 sources/ufo_composite_glyphs.py sources/ufo/Giphurs-Thin.ufo
	python3 sources/ufo_composite_glyphs.py sources/ufo/Giphurs-Regular.ufo
	python3 sources/ufo_composite_glyphs.py sources/ufo/Giphurs-ExtraBlack.ufo
	@echo "OPEN EACH UFO FILE WITH FONTFORGE AND EXPORT THEM AS UFO WITHOUT CHANGING ANYTHING TO FINISH THE PROCESS!!!"

# build number based glyphs
ufo_digits_glyphs: sources/ufo
	python3 sources/ufo_digits_glyphs.py 100 sources/ufo/Giphurs-Thin.ufo
	python3 sources/ufo_digits_glyphs.py 400 sources/ufo/Giphurs-Regular.ufo
	python3 sources/ufo_digits_glyphs.py 1000 sources/ufo/Giphurs-ExtraBlack.ufo
	@echo "OPEN EACH UFO FILE WITH FONTFORGE AND EXPORT THEM AS UFO WITHOUT CHANGING ANYTHING TO FINISH THE PROCESS!!!"

# edit fontinfo.plist to set the bit 7 of openTypeOS2Selection ("use typo metrics")
# Note: This is currently automatically run when building fonts
ufo_use_typo_metrics: sources/ufo
	python3 ufo_use_typo_metrics.py sources/ufo/Giphurs-Thin.ufo
	python3 ufo_use_typo_metrics.py sources/ufo/Giphurs-Regular.ufo
	python3 ufo_use_typo_metrics.py sources/ufo/Giphurs-ExtraBlack.ufo

# clean all generated files from the scripts

# Cleaning process
clean:
	rm -rf sources/instance_ufos
	rm -rf sources/__pycache__
	rm -f sources/*.ninja
	rm -f sources/.fuse_hidden*
	rm -f sources/.ninja_log
	rm -rf test_results
	rm -f *.zip

clean_fonts:
	rm -rf fonts/
	mkdir fonts
	cd fonts/ && mkdir otf ttf variable webfonts