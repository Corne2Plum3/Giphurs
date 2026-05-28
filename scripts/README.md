# `scripts`

This directory contains all scripts to build the font and other tools.

> [!IMPORTANT]
> All of the Bash and Python scripts are intended to be called from the Makefile or from another script, where the current working directory is the project's root folder. You shouldn't use them directly.

## Environment variables

It is possible to configure some of the scripts using a `.env` file at the project's root folder.

> [!NOTE]
> For now only `build.py` and `logger.py`  supports variables from `.env`. Support from other scripts when needed is TODO.

### Build

| Name | Type | Default Value | Description |
| --- | --- | --- | --- |
| `COMMON_FEATURES_LIST` | `Path` | `'./scripts/common_features_list.txt'` | Path to a text file listing the standard OpenType feature blocks that must be systematically copied across all UFOs. |
| `COMMON_LOOKUPS_LIST` | `Path` | `'./scripts/common_lookups_list.txt'` | Path to a text file listing the standard OpenType lookup blocks that must be systematically copied across all UFOs. |
| `FEATURES_LOOKUPS_REF` | `Path` | `./{SOURCES_INST_DIR_PATH} / '{FONT_NAME}-Regular.ufo / features.fea'` | The master OpenType feature file utilized as the golden reference source when injecting lookups and features into other styles. |
| `FONT_NAME` | `str` | `'Giphurs'` | The primary family name of the font. Used for identifying specific source files and naming output files. |
| `FONT_VERSION` | `str` | `None` | The version string to apply to all fonts (e.g., `"2.0.1"`). If left blank/unset, the script preserves whatever version values already exist inside the UFO sources. |
| `FONTS_DIR_BACKUP_PATH` | `Path` | `'./fonts-backup'` | The directory where existing font binaries are archived before a new build process is initiated. |
| `FONTS_DIR_PATH` | `Path` | `'./fonts'` | The target output directory where all generated font binaries (`otf`, `ttf`, `woff2`) will be saved. |
| `KEEP_UFO_INST` | `bool` | `False` | Determines whether the temporary working folder (`SOURCES_INST_DIR_PATH`) should be kept or deleted after the build finishes. Evaluates to `True` if set to `true` or `1`. |
| `SOURCES_DIR_PATH` | `Path` | `'./sources'` | The folder containing your master design `.ufo` files and primary files like `lib.plist`. |
| `SOURCES_INST_DIR_PATH` | `Path` | `'./sources-inst'` | The path for the temporary working directory where a copy of your sources will be pre-processed before actual compilation. |

### Logging

| Name | Type | Default Value | Description |
| --- | --- | --- | --- |
| `FONT_LOGS` | `Path` | `'./logs/fonts'` | Where to store the log of the font. |
| `GFTOOLS_LOGS` | `Path` | `'logs/gftools.log'` | The path to the file where standard output and errors from `gftools builder` and `gftools fix-nonhinting` will be recorded when building the font. |
| `PYFTFEATFREEZE_LOGS` | `Path` | `'logs/pyftfeatfreeze.log'` | The path to the log file where data regarding the standalone Small Caps (`smcp`) build process is tracked when buildinf the font. |

### Performance setting

| Name | Type | Default Value | Description |
| --- | --- | --- | --- |
| `PROCESSES_COUNT` | `int` | `1` | Controls how many CPU cores to allocate for parallelizable tasks (excluding _gftools_). Using `1` will use single process implementations. |

## Build

All of the font building process is described inside the `build.py` script.

**Build pipeline:**
```
[ 1. SETUP STAGE ]
       │
       ├──► Create backup copy of original production fonts directory
       ├──► Duplicate raw './sources' into a temporary working directory
       └──► Purge and re-initialize the target output directory
       │
[ 2. PRE-PROCESSING STAGE (Iterated over every .ufo file) ]
       │
       ├──► Inject master 'lib.plist' metadata into the UFO bundle
       ├──► Enable OpenType OS/2 Table Bit 7 (force "use_typo_metrics")
       ├──► Inject/Synchronize shared 'feature' blocks into 'features.fea'
       ├──► Inject/Synchronize shared 'lookup' blocks into 'features.fea'
       └──► Set customized Font Version strings if explicitly declared
       │
[ 3. BUILD STAGE ]
       │
       ├──► [gftools builder] ──► Processes 'config.yaml' to compile UFOs into raw binaries
       │                                │
       │                                ├──► /otf        (.otf)
       │                                ├──► /ttf        (.ttf)
       │                                ├──► /variable   (.ttf)
       │                                └──► /webfonts   (.woff2)
       │
       ├──► [rename_loop]    ──► Rename weight 1000 fonts files
       │
       └──► [pyftfeatfreeze] ──► Spawns multiprocessing/sequential tasks to freeze 'smcp' 
                                 features into standalone Small Caps (SC) font variations
       │
[ 4. POST-PROCESSING STAGE ]
       │
       └──► [gftools fix-nonhinting] ──► Inject / apply screen-rasterization optimization hinting 
                                         to all compiled binaries, then discards intermediate backups
       │
[ 5. CLEAN-UP STAGE ]
       │
       └──► (Optional) Purges the temporary working directory
```

## Font binaries tools

* `get_font_version.sh`: bash script returning the version of a font binary.
* `index.html` : HTML page you can open manually linking to both proof and tests reports.
* `proof.sh` : generates specimens of the font into `./output/proof` in HTML format using `differnator2` and open them in your web browser.
* `tests.sh` : generates a QA report using `fontbakery` into `./output/fontbakery` and open the report in your web browser. Also update the badges at the beginning of the project's main README file.

## UFO tools

### Glyph generators

> [!CAUTION]
> After using one of these scripts, open ALL of the UFO files using Fontforge to regenerate the UFO with the export feature.

* `ufo_accented_glyphs.py` : generates accented glyph(s) inside a UFO file (for example `À` or `é`), if the glyphs components are given inside `accented_glyphs.csv`, which contains the following fields:
    * *Name*: name of the glyph.
    * *Styles*: which style the line applies. `1` = non-italic, `2` = italic, `3` = both.
    * *Allow left overflow*: if set to `0`, the left padding of the glyph will be `0` if an accent would go out of the left limit of the font.
    * *Allow right overflow*: same than above but with the right side of the glyph.
    * *Base*: glyph to use as base. By default, the generated glyph will have the same width than the base.
    * *Comp. 2*, *Comp. 3*, *Comp. 4*: accents to use, in order.
* `ufo_composite_glyphs.py`: generates a glyph based on the sequence of one or several glyphs (for example, `IJ` or `Alpha`), if it appears on the `composite_glyphs.csv`:
    * *Name*  name of the glyph
    * *Styles*: in which style this applies. `1` = non-italic, `2` = italic, `3` = both
    * *Copy anchors*: copy the anchors points of the glyphs if possible if the value is not `0`.
    * *Glyph. 1*, *Glyph. 2*, *Glyph. 3*, *Glyph. 4*: components of the glyph to build, in order.
* `ufo_digits_glyphs.py`: generates the glyphs based on numbers. The list of the glyphs to generate is given inside the script.

### Other tools

* `ufo_copy_fea_blocks.py`: copy `feature` or `lookup` block from a `.fea` file to another.
* `ufo_set_version.py`: change the version string inside a UFO file.
* `ufo_use_typo_metrics.py`: set the bit 7 ("use typo metrics") of fsSelection in an ufo file.
* `ufo_utils.py`: collection of functions used to interact with UFO files.