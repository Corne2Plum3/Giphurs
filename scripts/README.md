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

### Composed glyph generator

A composed glyph is a glyph that is created using one or several other glyphs. To give some examples, the glyph `IJ` is made of `I` and `J`, the glyph `â` is made of the small letter `a` with a circumflex accent `^` (`uni0302`). More than 60% of the glyphs in the font are composed.

> [!NOTE]
> FontForge does include a built-in feature to build accented and composite (sequence of 1 or several glyphs). We do not use them, this isn't enough for our use, for several reasons:
> * Double-accented glyphs are built from a single accented glyph. This might be an issue as anchors aren't copied, giving less flexibility on how to place accents.
> * It is not possible to use custom glyphs when building an accented or composed glyphs: those settings are lost when exporting to UFO.
> * We're using custom scripts to generate some digits based glyphs, such as proportional figures, subscript variants of the font, or numbers in a circle (`uni2468` for example)

A script to generate all of those fonts called `ufo_composed_glyphs.py` exists to create all of those glyphs inside the UFOs from `sources/`. This file requires one or several CSV file to tell what to build. The script read the given CSV files and updates the UFOs file, automatically resolving dependencies and detecting circular references.

> [!IMPORTANT]
> In this project, 2 CSV files are used:
> * `composed_glyphs.csv` for glyphs that should be defined manually, mostly accented and composite glyphs.
> * `composed_glyphs_generated.csv` for glyphs defined by the `composed_glyphs_generator.py`, commonly digit-based glyphs. **Do NOT manually modify this file!!**.

### CSV config file

The CSV files are using a comma `,` separator and have the following fields (from left to right):
* `Glyphname`: name of the glyph to generate
* `Weight`: in which weight this line applies. Can be `100`, `400`, `1000`, or empty to support all weights.
* `Styles`: in which styles this line applies. `1` = normal ; `2` = italic ; `3` = both
* `Category`: type of the glyph to generate (see table below)
* `Param. 1` and `Param. 2`: depends of the category
* `Glyph 1`, `Glyph 2`, ...: the glyphs to use to build the glyph `Glyphname`.

The possible values for `Category` are given in the table below:

| Category | Python class | Description | Param. 1 | Param. 2 | Supports anchors |
|----|----|----|----|----|----|
| `A` | `Accented_Glyph` | Glyph with one or several accents | Left overflow | Right overflow | Yes |
| `C` | `Composite_Glyph` | Sequence of one or several glyph | Copy anchors | y-offset | Yes |
| `P` | `Proportional_Digit_Glyph` | Digit with a kerning matching the shape of the glyph (`pnum`) | Size | Digit value | No |
| `T` | `Accented_Glyph_Glyph` | Digit with a fixed width (`tnum`) | Size | - | No
| `O` | `Circled_Number_Glyph` | Number in a circle *(letters are not supported)* | Unlink references | - | No |
| `.` | `Full_Stop_Number_Glyph` | Number followed by a period. | - | - | No |
| `(` | `Parenthesis_Number_Glyph` | Number between parenthesis | - | - | No |

For the parameters:
* **Left overflow** (`0` or `1`): if set to `0`, forces the left kern value to be at minimum 0.
* **Right overflow** (`0` or `1`): if set to `0`, forces the right kern value to be at minimum 0.
* **Copy anchors** (`0` or `1`): if set to `1`, copy all anchors of the copied glyphs. Note that copying several times the same anchor might give unexcepted results.
* **y-offset** (`int`): how many units to move the generated glyph vertically (positive value = to the top)
* **Size** (`0` or `1`): `0` = exponent (`.superior` digit) ; `1` = normal sized digit
* **Digit value** (`0`-`9`): value of the digit
* **Unlink references** (`0` or `1`): if set to `1`, replace all references to the glyphs by their points.

> [!WARNING]
> The glyph to generate must already exists inside the UFO (as `.glif` file) to the script to work.

> [!TIP]
> To clone a single glyph, it's recommended to use the `C` (composite) category. You can then just put one glyph, the glyph you want to copy. Set the **y-offset** parameter to 0, and for the **Copy anchors**, it depends of your needs.

### Usage

It is best used with the `make ufo_composed_glyph` command from the `Makefile` in the project's root folder. It will:
1. Update `composed_glyphs_generated.csv`.
2. Edit all of the UFOs files inside `sources/`.

> [!CAUTION]
> After using one of these scripts, open ALL of the UFO files using Fontforge to regenerate the UFO with the export feature.

> [!TIP]
> It's possible to only build specific glyphs with their dependencies with the option `GLYPHS` and a list of glyphs separated by spaces. For example, the following command will build the glyphs `i`, `uni043A.sc`, and `kappa.sc` as it's needed for the previous glyph.
  ```sh
  make ufo_composed_glyphs GLYPHS="i uni043A.sc"
  ```

### Other tools

* `ufo_copy_fea_blocks.py`: copy `feature` or `lookup` block from a `.fea` file to another defined by `common_features_list.txt` and `common_lookups_list.txt`.
* `ufo_set_version.py`: change the version string inside a UFO file.
* `ufo_use_typo_metrics.py`: set the bit 7 ("use typo metrics") of fsSelection inside an UFO file.
* `ufo_utils.py`: collection of functions used to interact with UFO files.
