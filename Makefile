# remove the "0" in the first echo when version is 1.000 or above
font_version := $(shell echo "0"$(shell echo "scale=3;"$(shell fc-query -f '%{fontversion}\n' fonts/otf/Giphurs-Regular.otf)"/65536" | bc))

# make a zip archive of the font folder, used to export fonts
export_fonts:
	zip -r Giphurs_fonts_v$(font_version).zip fonts/

# build the fonts (otf, ttf, woof2, static + variables)
fonts: ufo
	cd sources && gftools builder config.yaml

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
	rm -f ufo_built.stamp
