# Giphurs font

Your average Arial/Helvetica/Circular on budget, made with [Fontforge](https://fontforge.org/en-US/).

![It was supposed to be a preview here](documentation/quick_preview_v2.png)


## Status of the project

This project **isn't complete and is under developpement**. Things may change at any time.

# IMPORTANT

The end goal is to upload this font on [Google Fonts](https://fonts.google.com/).

I'm aware that there's already some issues, for example the font version being invalid for Google Fonts, but while I don't have a finished version, the version will be still under 1.0, it's intended.

## TODO list
* Fix other small problems that [Font Bakery](https://github.com/googlefonts/fontbakery) complains about.
* Improve font documentation (if it even exists).
* Bring back '`calt`' features which couldn't be added to the build (example change `:` height between 2 numbers)
* Add the other weights (100, 200, ..., 900?)
* Add italic.
* Add better pictures of the font and better description.


# Download

Go in [releases](https://github.com/Corne2Plum3/Giphurs/releases) page and pick the latest version. The font is available in the following formats: `otf`, `ttf` and `woff2`.

Note that these are currenly pre-releases, so the font may contains issues and everything can be changed in the future.

# Build the fonts

## Requirements

* [Fontforge](https://fontforge.org/en-US/), with its python modules. **(1)**
* [Fontmake](https://github.com/googlefonts/fontmake) to compile the UFO files.
* [Google Fonts Tools](https://github.com/googlefonts/gftools) to do some improvments to the font files.
* [Python 3.10](https://www.python.org/downloads/) or newer version
* [sfdLib](https://github.com/MFEK/sfdLib.py) to convert `sfd` files to `ufo`. **(2)**
* [woff2](https://github.com/google/woff2) to convert `ttf` files to `woff2`

To check the font quality, we use [Font Bakery](https://github.com/googlefonts/fontbakery) (the latest version).

**(1)** Should be installed when installing Fontforge.

**(2)** The magic script `build_sources.sh` install that for you ;)


## Scripts

This repo provides differents scripts to make the font files, inside the `sources` folder.
**Ensure that the source folder is your current working directory else they won't work!!!**

* `build_sources.sh`: before being converted into font files, the sources files (the `.sfd` files) are first converted into [UFO files](https://en.wikipedia.org/wiki/Unified_Font_Object) before being compiled by [Fontmake](https://github.com/googlefonts/fontmake). This is what this script does, where the `.sfd` are first cleaned (for example, correcting directions and overlaps) and put into the `sfd_cleaned` folder, then converted into UFO inside `ufo` folder.

* `build_fonts.sh`: this program will takes the UFO files (or generate them if needed) and compile them into the chosen file format. This program takes at least 1 argument which is the desired font file extension:
	* `otf`
	* `ttf`
	* `woff2` (or `webfonts`) (needs the **ttf** files first!)
	* Or `all` to generate all formats above.

	You can add `-b` as a second argument like below to force the script to force rebuilding the UFO files, for example:
	```sh
	./build_fonts.sh otf -b
	```
	...which generate the OTF files but also rebuild the sources for the compilation.

* `clean.sh`: remove the files that has been generated by the script to build the fonts, including UFO files but **not** the final font files (e.g. don't delete `fonts` folder).

# License
This font is under the [SIL Open Font License, Version 1.1](https://scripts.sil.org/OFL).
 

