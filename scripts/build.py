import subprocess

from dotenv import load_dotenv
from logger import configure_logging
from math import trunc
from multiprocessing import Pool
import os
from pathlib import Path
import shutil
import time
from ufo_copy_fea_blocks import copy_fea_blocks
from ufo_use_typo_metrics import use_typo_metrics
from verboselogs import VerboseLogger   # pyright: ignore[reportMissingTypeStubs]


# ===== Build settings =====

load_dotenv()

# Name of the font
FONT_NAME: str = os.environ.get('FONT_NAME', 'Giphurs')

# Font binary directory
FONTS_DIR_PATH: Path = Path(os.environ.get('FONTS_DIR_PATH', './fonts'))

# Font version (example: "2", "2.0.1", "2.010"). If None -> keep the version values from the UFOs
FONT_VERSION: str | None = os.environ.get('FONT_VERSION', None)

# Backup font binaries
FONTS_DIR_BACKUP_PATH: Path = Path(os.environ.get('FONTS_DIR_BACKUP_PATH', f'{FONTS_DIR_PATH}-backup'))

# Where the sources files (.ufo) are located
SOURCES_DIR_PATH: Path = Path(os.environ.get('SOURCES_DIR_PATH', './sources'))

# Temporary sources files for pre-processing
SOURCES_INST_DIR_PATH: Path = Path(os.environ.get('SOURCES_INST_DIR_PATH', f'{SOURCES_DIR_PATH}-inst'))

# Do not remove UFOs copy that are used for pre-processing and used for actually building the font
KEEP_UFO_INST: bool = os.environ.get('KEEP_UFO_INST', 'False').lower() in ['true', '1']

# How many process to run at most for parallelizable tasks (excluding gftools)
PROCESSES_COUNT: int = int(os.environ.get('PROCESSES_COUNT', '1'))

# List of features that should be the same in all tables in features.fea
COMMON_FEATURES_LIST: Path = Path(os.environ.get('COMMON_FEATURES_LIST', './scripts/common_features_list.txt'))

# List of lookups that should be the same in all tables in features.fea
COMMON_LOOKUPS_LIST: Path = Path(os.environ.get('COMMON_LOOKUPS_LIST', './scripts/common_lookups_list.txt'))

# The feature.fea to use as source for copying features and lookups
FEATURES_LOOKUPS_REF: Path = Path(os.environ.get('COMMON_LOOKUPS_LIST', SOURCES_INST_DIR_PATH / f'{FONT_NAME}-Regular.ufo' / 'features.fea'))

# Where to store gftools logs (main build + hinting)
GFTOOLS_LOGS: Path = Path(os.environ.get('GFTOOLS_LOGS', 'logs/gftools.log'))

# Where to store pyftfeatfreeze logs (small caps build)
PYFTFEATFREEZE_LOGS: Path = Path(os.environ.get('PYFTFEATFREEZE_LOGS', 'logs/pyftfeatfreeze.log'))

# ===== Constants =====

# List of directories FONTS_DIR and the type of binaries inside each of these directories (no period at the beginning)
FONTS_SUBDIRS_TYPES: dict[str, str] = {'otf': 'otf', 'ttf': 'ttf', 'variable': 'ttf', 'webfonts': 'woff2'}

# Logger (don't use print(), use this instead, there are colors :3)
logger: VerboseLogger = configure_logging()

# ===== Utils functions =====

def empty_dir(d: Path) -> int:
    """
    Creates an empty directory with the given path. If it already exists, its content is cleared.
    This function handles the logging process.
    Args:
        d: path to the directory to create or empty
    Returns:
        int: `0` if success, non-zero otherwise.
    """
    if d.exists(): 
        try:
            logger.verbose(f'Clearing directory "{d}"...')    # pyright: ignore[reportUnknownMemberType]
            shutil.rmtree(d)
        except Exception as err:
            logger.error(f'Failed to remove ""{d}"": {err}')
            return 1
    else:
        logger.info(f'"{d}" did not exist.')

    logger.verbose(f'Creating directory "{d}"...')    # pyright: ignore[reportUnknownMemberType]
    try:
        os.mkdir(d)
    except Exception as err:
        logger.error(f'Failed to create ""{d}"": {err}')
        return 1
    return 0

def rename_loop(files: dict[Path, Path]) -> int:
    """
    Rename multiple files.
    This function handles the logging process.
    Args:
        files: dict mapping files to rename to their new name
    Return:
        Amount of files where renamming failed.
    """
    global logger
    error_count: int = 0
    for old_name, new_name in files.items():
        logger.verbose(f'Renaming "{old_name}" -> "{new_name}"')  # pyright: ignore[reportUnknownMemberType]
        try:
            os.rename(old_name, new_name)
        except FileNotFoundError:
            if new_name.exists():
                logger.info(f'"{new_name}" already exists.')
            else:
                logger.warning(f'File not found: "{old_name}"')
                error_count += 1
        except Exception as err:
            logger.warning(f'Unexpected error:{err}')
            error_count += 1

    if error_count == 0:
        logger.success('Weight 1000 fonts successfully renamed.')  # pyright: ignore[reportUnknownMemberType]
    else:
        logger.warning(f'{error_count} error(s) occured when renaming weight 1000 files.')
    return error_count

def run_shell_command(command: str, show_output_message: bool = True, output_message_fail_level: str = 'error', log_file: Path | None = None, clear_log_file: bool = True) -> int:
    '''
    Run a shell command and show it on the logs.
    Args:
        command: command to execute
        show_output_message: (optional) show a message after the execution of the command. Defaults to `True`
        output_message_fail_level: (optional) log level for message when non-zero exit code is obtained from the command. Possible values: `info`, `notice`, `warning`, `error`, `critical`.
        log_file: (optional) store the command output to a file as well
        clear_log_file: (optional) clear log_file before writing on it
    Returns:
        int: exit code from the command
    '''
    if output_message_fail_level.lower() not in ['info', 'notice', 'warning', 'error', 'critical']:
        raise ValueError(f'Invalid value for output_message_fail_level: {output_message_fail_level}')
    logger.verbose(f'{command}{f' -> ({log_file})' if log_file is not None else ''}')  # pyright: ignore[reportUnknownMemberType]
    exit_code: int
    if log_file is not None:
        with open(log_file, 'w' if clear_log_file else 'a') as f:  # print executed command in logs
            f.write(f'{command}\n')
        exit_code = subprocess.run(f'{command} 2>&1 | tee {'-a' if not clear_log_file else ''} {log_file}', shell=True).returncode
    else:
        exit_code = subprocess.run(command, shell=True).returncode
    if show_output_message:
        if exit_code != 0:
            output_msg: str = f'Something went wrong with "{command}": exit code {exit_code}'
            if output_message_fail_level.lower() == 'info':
                logger.info(output_msg)
            elif output_message_fail_level.lower() == 'notice':
                logger.notice(output_msg)   # pyright: ignore[reportUnknownMemberType]
            elif output_message_fail_level.lower() == 'warning':
                logger.warning(output_msg)
            elif output_message_fail_level.lower() == 'error':
                logger.error(output_msg)
            elif output_message_fail_level.lower() == 'critical':
                logger.critical(output_msg)
        else:
            logger.success(f'"{command}": Success.')  # pyright: ignore[reportUnknownMemberType]
    return exit_code

# ===== Build functions =====

# Setup (all fonts)

def create_fonts_backup(src_dir: Path, dst_dir: Path) -> int:
    '''
    Creates backup dir with the font binaries.
    Args:
        src_dir: Path to the directory to copy
        dst_dir: Path to the desination directory
    Returns:
        `0` if success, non-zero otherwise
    '''
    logger.verbose(f'Creating font binaries backup directory "{src_dir}" at "{dst_dir}"...')  # pyright: ignore[reportUnknownMemberType]
    try:
        if dst_dir.exists():
            logger.warning(f'"{dst_dir}" already exists. It will be replaced.')
        shutil.copytree(src_dir, dst_dir, dirs_exist_ok=True)
    except Exception as err:
        logger.error(f'Failed to create backup: {err}')
        return 1
    logger.success(f'Font binaries backup directory "{dst_dir}" created.')  # pyright: ignore[reportUnknownMemberType]
    return 0

def create_sources_inst(src_dir: Path, dst_dir: Path) -> int:
    '''
    Creates a copy of the
    Args:
        src_dir: Path to the directory to copy
        dst_dir: Path to the desination directory
    Returns:
        `0` if success, non-zero otherwise.
    '''
    logger.info(f'Copying sources files "{src_dir}" for pre-processing at "{dst_dir}"...')
    try:
        if dst_dir.exists():
            logger.warning(f'"{dst_dir}" already exists. It will be replaced.')
        shutil.copytree(src_dir, dst_dir, dirs_exist_ok=True)
    except Exception as err:
        logger.critical(f'Failed to copy sources files into "{dst_dir}": {err}.')
        return 1
    logger.success(f'Working directory "{dst_dir}" created.')  # pyright: ignore[reportUnknownMemberType]
    return 0

def remove_sources_inst(sources_inst_path: Path) -> int:
    '''
    Remove directory generated by create_sources_inst()
    Args:
        sources_inst_path: directory to remove.
    Returns:
        `0` if success, non-zero otherwise.
    '''
    logger.info(f'Deleting "{sources_inst_path}"...')
    try:
        shutil.rmtree(sources_inst_path)
    except Exception as err:
        logger.critical(f'Failed to delete "{sources_inst_path}": {err}.')
        return 1
    logger.success(f'Working directory "{sources_inst_path}" deleted.')  # pyright: ignore[reportUnknownMemberType]
    return 0

# Pre-processing (per .ufo file)

def copy_plist(src_plist: Path, dst_ufo: Path) -> int:
    """
    Copy a .plist file into an ufo file.
    Args:
        src_plist: path to the .plist file to copy
        dst_ufo: destination directory or file
    Returns:
        `0` if success, non-zero otherwise
    """
    logger.info(f'Copying "{src_plist}" into "{dst_ufo}"...')
    try:
        shutil.copy(src_plist, dst_ufo)
    except Exception as err:
        logger.critical(f'"{src_plist}" copy failed: {err}')
        return 1
    logger.success("Success.")  # pyright: ignore[reportUnknownMemberType]
    return 0

# Build

def build_all_fonts(ufo_dir: Path) -> int:
    """
    Build fonts binaries using gftools builder. This function handles the logging process
    Args:
        ufo_dir: directory with .ufo files
    Returns:
        int: exit code of gftools builder (`0` if success, non-zero otherwise)
    """
    global logger
    logger.info('Building the font with gftools builder...')
    gftools_command: str = f'gftools builder {ufo_dir}/config.yaml'
    return run_shell_command(gftools_command, True, 'critical', GFTOOLS_LOGS, True)


def build_sc_font(src_path: Path, dst_path: Path) -> int:
    '''
    Generates small caps version of the given font binary, using pyftfeatfreeze.
    Args:
        src_path: input font file
        dst_file: output font file
    Return:
        int: exit code of pyftfeatfreeze
    '''
    pyftfeatfreeze_command: str = f'pyftfeatfreeze -f "smcp" -S -U "SC" {src_path} {dst_path}'
    return run_shell_command(pyftfeatfreeze_command, True, 'critical', PYFTFEATFREEZE_LOGS, False)

def build_all_sc_fonts(font_dir: Path, font_subdir_types: dict[str, str], processes_count: int = 1) -> int:
    '''
    Generates small caps version of the font binaries, which should have been geenrate before calling this function.
    This function handles the logging process.
    Args:
        font_name: name of the font
        font_dir: Path to all font files
        font_subdir_types: dictionary mapping all sub directories inside font_dir with the files extentions (no '.')
    Returns:
        int: Return the amount of errors occured.
    '''
    global logger
    logger.verbose('Building small caps (SC) fonts...')  # pyright: ignore[reportUnknownMemberType]

    # Create a dict with all input path to output path
    font_file_list: dict[Path, Path] = {}
    for font_subdir in font_subdir_types:
        ext: str = font_subdir_types[font_subdir]
        font_list: list[Path] = [font for font in (font_dir / font_subdir).glob('*.' + ext)]
        for src_font in font_list:
            src_name: str = src_font.name
            dst_name: str
            font_name: str
            if '[' in src_name:
                font_name = src_name.split('[')[0]
                axis: str = src_name.split('[')[1].split(']')[0]
                dst_name = f'{font_name}SC[{axis}].{ext}'  # variable
            else:
                font_name = src_name.split('-')[0]
                src_weight: str = src_name.split('-')[1].split('.')[0]
                dst_name = f'{font_name}SC-{src_weight}.{ext}'  # non-variable
            src_path: Path = font_dir / font_subdir / src_name
            dst_path: Path = font_dir / font_subdir / dst_name
            font_file_list[src_path] = dst_path

    # Generate the fonts
    error_count = 0
    if processes_count > 1:  # parallel
        logger.verbose(f'Using multiprocessing ({processes_count} processes)')  # pyright: ignore[reportUnknownMemberType]
        tasks = [
            (src_font_file, font_file_list[src_font_file])
            for src_font_file in font_file_list
        ]
        with Pool(processes=processes_count) as pool:
            results = pool.starmap(build_sc_font, tasks)
        error_count += sum(1 for r in results if r != 0)
    else:  # sequential
        logger.verbose('Using a single process.')  # pyright: ignore[reportUnknownMemberType]
        for src_font_file in font_file_list:
            if build_sc_font(src_font_file, font_file_list[src_font_file]) != 0:
                error_count += 1

    if error_count == 0:
        logger.success('The small caps (SC) has been built with success')  # pyright: ignore[reportUnknownMemberType]
    else:
        logger.warning(f'{error_count} error(s) occured when building small caps (SC) fonts.')
    return error_count

# Post-processing

def add_hinting(src_path: Path, dst_path: Path):
    """
    Add hinting to a font file using gftools fix-nonhinting.
    Args:
        src_path: input font file
        dst_file: output font file
    Return:
        int: exit code of gftools command
    """
    gftools_command: str = f'gftools fix-nonhinting {src_path} {dst_path} 2>&1 | tee -a {GFTOOLS_LOGS}'
    exit_code: int = run_shell_command(gftools_command, True, 'error', GFTOOLS_LOGS, False)
    return exit_code

def add_hinting_all(font_dir: Path, font_subdir_types: dict[str, str], keep_backup_files: bool = False, processes_count: int = 1) -> int:
    """
    Add hinting on all font binaries if missing using gftools.
    This function handles the logging process.
    Args:
        font_dir: Path to all font files
        font_subdir_types: dictionary mapping all sub directories inside font_dir with the files extentions (no '.')
        keep_backup_files: (optional) keep the backup files generated by gftools. Default value: `False`
    Returns:
        int: Return the amount of errors occured.
    """
    logger.info('Adding hinting on the fonts...')  # pyright: ignore[reportUnknownMemberType]

    # Get font list
    font_file_list: list[Path] = []
    for font_subdir in font_subdir_types:
        ext: str = font_subdir_types[font_subdir]
        font_file_list += [font for font in (font_dir / font_subdir).glob('*.' + ext)]

    # Run commands
    error_count = 0
    if processes_count > 1:  # parallel
        logger.verbose(f'Using multiprocessing ({processes_count} processes)')  # pyright: ignore[reportUnknownMemberType]
        tasks = [
            (font, font)
            for font in font_file_list
        ]
        with Pool(processes=processes_count) as pool:
            results = pool.starmap(add_hinting, tasks)
        error_count += sum(1 for r in results if r != 0)
    else:
        logger.verbose('Using a single process.')  # pyright: ignore[reportUnknownMemberType]
        for font in font_file_list:
            if add_hinting(font, font) != 0:
                error_count += 1

    if error_count == 0:
        logger.success('Hinting has been added on all fonts.')  # pyright: ignore[reportUnknownMemberType]
    else:
        logger.warning(f'{error_count} error(s) occured when adding hinting on all fonts.')

    if not keep_backup_files:
        logger.info('Removing generated backup files...')
        for subdir in font_subdir_types:        
            backup_files: list[Path] = [f for f in (font_dir / subdir).glob(f'*backup*.*')] + [f for f in (font_dir / subdir).glob(f'*.*backup*')]
            for target in backup_files:
                try:
                    logger.info(f'Removing backup file "{target}" generated by gftools...')
                    os.remove(target)
                except Exception as err:
                    logger.warning(f'Failed to remove "{target}": {err}')

    return error_count

start_time: float = time.time()  # seconds

# ===== 1. Setup =====
logger.info('Setting up the directories...')  # pyright: ignore[reportUnknownMemberType]
create_fonts_backup(FONTS_DIR_PATH, FONTS_DIR_BACKUP_PATH)
if create_sources_inst(SOURCES_DIR_PATH, SOURCES_INST_DIR_PATH) != 0:
    exit(1)
if empty_dir(FONTS_DIR_PATH) != 0:
    exit(0)
logger.success('Ready to generate the fonts.')  # pyright: ignore[reportUnknownMemberType]

# ===== 2. Pre-processing =====
logger.info(f'Pre-processing UFO files at "{SOURCES_INST_DIR_PATH}"...')

# Detect all files inside sources-inst
UFO_FILES_LIST: list[Path] = [ufo for ufo in SOURCES_INST_DIR_PATH.glob("*.ufo")]
logger.info(f'{len(UFO_FILES_LIST)} UFOs detected inside "{SOURCES_INST_DIR_PATH}"')
if len(UFO_FILES_LIST) == 0:
    logger.error('No UFO file detected. Exiting...')
    logger.error('If this is the first time it happens, try again. Also, ensure the SOURCES_DIR_PATH and/or SOURCES_INST_DIR_PATH environement variable is correct if set in .env file.')
    exit(1)

# For copy_tables()
feature_list: list[str] = []
with open('scripts/common_features_list.txt', 'r') as f:
    for line in f.readlines():
        if len(line.strip()) >= 1:
            feature_list.append(line.strip())
lookup_list: list[str] = []
with open('scripts/common_lookups_list.txt', 'r') as f:
    for line in f.readlines():
        if len(line.strip()) >= 1:
            lookup_list.append(line.strip())
# Loop for every .ufo
for ufo in UFO_FILES_LIST:
    logger.info(f'Pre-processing {ufo}...')  # pyright: ignore[reportUnknownMemberType]
    # lib.plist
    if copy_plist(SOURCES_INST_DIR_PATH / 'lib.plist', ufo / 'lib.plist') != 0:
        exit(1)
    # use typo metrics
    logger.verbose(f'Enabling openTypeOS2Selection bit 7 "use_typo_metrics" in "{ufo}"...')  # pyright: ignore[reportUnknownMemberType]
    if use_typo_metrics(ufo) != 0:
        exit(1)
    # feature blocks
    if FEATURES_LOOKUPS_REF != ufo / 'features.fea':
        if copy_fea_blocks(FEATURES_LOOKUPS_REF, ufo / 'features.fea', 'feature', feature_list) != 0:
            exit(1)
    # lookup blocks
    if FEATURES_LOOKUPS_REF != ufo / 'features.fea':
        if copy_fea_blocks(FEATURES_LOOKUPS_REF, ufo / 'features.fea', 'lookup', lookup_list) != 0:
            exit(1)
logger.success('Pre-processing done with success.')  # pyright: ignore[reportUnknownMemberType]

# ===== 3. Building the fonts =====
logger.info(f'Building font binaries at "{FONTS_DIR_PATH}"...')
# Build the fonts
# --- Main
if build_all_fonts(SOURCES_INST_DIR_PATH) != 0:  # gftools
    exit(1)
rename_loop(
    {
        FONTS_DIR_PATH / 'otf' / f'{FONT_NAME}-ExtraBlack.otf'           : FONTS_DIR_PATH / 'otf' / f'{FONT_NAME}ExtraBlack-Regular.otf',
        FONTS_DIR_PATH / 'otf' / f'{FONT_NAME}-ExtraBlackItalic.otf'     : FONTS_DIR_PATH / 'otf' / f'{FONT_NAME}ExtraBlack-Italic.otf',
        FONTS_DIR_PATH / 'ttf' / f'{FONT_NAME}-ExtraBlack.ttf'           : FONTS_DIR_PATH / 'ttf' / f'{FONT_NAME}ExtraBlack-Regular.ttf',
        FONTS_DIR_PATH / 'ttf' / f'{FONT_NAME}-ExtraBlackItalic.ttf'     : FONTS_DIR_PATH / 'ttf' / f'{FONT_NAME}ExtraBlack-Italic.ttf',
        FONTS_DIR_PATH / 'webfonts' / f'{FONT_NAME}-ExtraBlack.woff2'      : FONTS_DIR_PATH / 'webfonts' / f'{FONT_NAME}ExtraBlack-Regular.woff2',
        FONTS_DIR_PATH / 'webfonts' / f'{FONT_NAME}-ExtraBlackItalic.woff2': FONTS_DIR_PATH / 'webfonts' / f'{FONT_NAME}ExtraBlack-Italic.woff2'
    }
)
# --- Small Caps
if build_all_sc_fonts(font_dir=FONTS_DIR_PATH, font_subdir_types=FONTS_SUBDIRS_TYPES, processes_count=PROCESSES_COUNT):
    exit(1)
logger.success('Building process done with success.')  # pyright: ignore[reportUnknownMemberType]

# ===== 4. Post-processing =====
logger.info('Post-processing all fonts...')
add_hinting_all(FONTS_DIR_PATH, FONTS_SUBDIRS_TYPES, False, PROCESSES_COUNT)
logger.success('Post-processing done with success.')  # pyright: ignore[reportUnknownMemberType]

# ===== 5. Clean-up =====
logger.info('Cleaning up useless files...')
if KEEP_UFO_INST:  # Clean temporary source files
    remove_sources_inst(SOURCES_INST_DIR_PATH)

end_time: float = time.time()
logger.success(f'Finished in {int((end_time - start_time) // 60)} minute(s) and {trunc((end_time - start_time) % 60)} second(s) UwU')  # pyright: ignore[reportUnknownMemberType]
