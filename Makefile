.PHONY: export_fonts tests clean clean_fonts 

# Name of the font
font_name := Giphurs

# If the version is below 1, a 0 is added
#font_version := $(shell echo "0"$(shell echo "scale=3;("$(shell echo $(shell fc-query -f '%{fontversion}\n' fonts/otf/Giphurs-Regular.otf)"+16" | bc)"/65536)" | bc))
# If the version is 1.000 or above
font_version := $(shell echo $(shell echo "scale=3;("$(shell echo $(shell fc-query -f '%{fontversion}\n' fonts/otf/Giphurs-Regular.otf)"+16" | bc)"/65536)" | bc))

# Output directory of make tests (Don't put the '/' at the end!)
tests_output_dir := tests_results


# documentaton
help:
	@echo "Available make commands:"
	@echo "  * make clean        : Remove temporary and useless generated files, including UFO sources."
	@echo "  * make clean_fonts  : Empties the current fonts/ folder."
	@echo "  * make export_fonts : Export fonts/ directory into a zip file."
	@echo "  * make fonts        : Generate font binaries from UFO sources."
	@echo "  * make tests -i     : Runs automated tests (output at the $(tests_output_dir)/ folder ). -i option is mandatory."
	@echo "UFO sources scripts"
	@echo "  * make ufo_anchors_on_accented_glyphs : Place anchors points on accented glyphs (the UFO files must be opened and exported throught Fontforge after)."
	@echo "  * make ufo_digits_glyphs              : Build digits based glyphs."
	@echo "  * make ufo_use_typo_metrics           : Enable bit 7 ("use typo metrics") of openTypeOS2Selection in fontinfo.plist"

# make a zip archive of the font folder
export_fonts:
	zip -r $(font_name)_fonts_v$(font_version).zip fonts/ OFL.txt

# build the fonts (otf, ttf, woof2, static + variables)
fonts: sources/ufo
	./sources/build_fonts.sh

# run fontbakery tests
tests:
	rm -rf $(tests_output_dir)
	mkdir $(tests_output_dir)
	fontbakery check-googlefonts -F fonts/otf/$(font_name)-Thin.otf > $(tests_output_dir)/fontbakery_otf_100.log & \
	fontbakery check-googlefonts -F fonts/otf/$(font_name)-Regular.otf > $(tests_output_dir)/fontbakery_otf_400.log & \
	fontbakery check-googlefonts -F fonts/otf/$(font_name)ExtraBlack-Regular.otf > $(tests_output_dir)/fontbakery_otf_1000.log & \
	fontbakery check-googlefonts -F fonts/ttf/$(font_name)-Thin.ttf > $(tests_output_dir)/fontbakery_ttf_100.log & \
	fontbakery check-googlefonts -F fonts/ttf/$(font_name)-Regular.ttf > $(tests_output_dir)/fontbakery_ttf_400.log & \
	fontbakery check-googlefonts -F fonts/ttf/$(font_name)ExtraBlack-Regular.ttf > $(tests_output_dir)/fontbakery_ttf_1000.log & \
	fontbakery check-googlefonts -F fonts/variable/$(font_name)\[wght\].ttf > $(tests_output_dir)/fontbakery_ttf_var.log & \
	wait
	@echo "Done"

# place anchors points on accented glyphs
ufo_anchors_on_accented_glyphs: sources/ufo
	python3 sources/ufo_anchors_on_accented_glyphs.py sources/ufo/Giphurs-Thin.ufo
	python3 sources/ufo_anchors_on_accented_glyphs.py sources/ufo/Giphurs-Regular.ufo
	python3 sources/ufo_anchors_on_accented_glyphs.py sources/ufo/Giphurs-ExtraBlack.ufo
	@echo "OPEN EACH UFO FILE WITH FONTFORGE AND EXPORT THEM AS UFO WITHOUT CHANGING ANYTHING TO FINISH THE PROCESS!!!"

# build number based glyphs
ufo_digits_glyphs: sources/ufo
	python3 sources/ufo_digits_glyphs.py 100 sources/ufo/Giphurs-Thin.ufo
	python3 sources/ufo_digits_glyphs.py 400 sources/ufo/Giphurs-Regular.ufo
	python3 sources/ufo_digits_glyphs.py 1000 sources/ufo/Giphurs-ExtraBlack.ufo

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