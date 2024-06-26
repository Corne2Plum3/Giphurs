# remove the "0" in the first echo when version is 1.000 or above
font_version := $(shell echo "0"$(shell echo "scale=3;("$(shell echo $(shell fc-query -f '%{fontversion}\n' fonts/otf/Giphurs-Regular.otf)"+16" | bc)"/65536)" | bc))

# documentaton
help:
	@echo "Available make commands:"
	@echo "  * make clean        : Remove temporary and useless generated files, including UFO sources."
	@echo "  * make export_fonts : Export fonts/ directory into a zip file."
	@echo "  * make fonts        : Generate font binaries, and UFO sources if needed."
	@echo "  * make ufo          : Generate UFO sources files only."

# make a zip archive of the font folder, used to export fonts
export_fonts:
	zip -r Giphurs_fonts_v$(font_version).zip fonts/ OFL.txt

# build the fonts (otf, ttf, woof2, static + variables)
fonts: ufo
	d=$$(date +%s) \
	; cd sources && touch Giphurs.designspace && gftools builder config.yaml \
	&& echo "\033[1;32mFonts build in $$(($$(date +%s)-d)) second(s) UwU\033[0;0m"

# build the ufo files from sfd
ufo:
	cd sources && ./build_sources.sh

# clean all generated files from the scripts
clean:
	rm -rf sources/py/
	rm -rf sources/sfd_cleaned/
	rm -rf sources/ufo/
	rm -f sources/-backup*
	rm -f sources/.fuse_hidden*
	rm -f *.zip
