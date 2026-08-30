import argparse
from composed_glyphs.accented_glyph import Accented_Glyph
from composed_glyphs.composed_glyph import Composed_Glyph
from composed_glyphs.circled_number_glyph import Circled_Number_Glyph
from composed_glyphs.composed_glyph_tree import get_children_from_name, is_composed, set_glyph_priorities_from_list
from composed_glyphs.composite_glyph import Composite_Glyph
from composed_glyphs.full_stop_number_glyph import Full_Stop_Number_Glyph
from composed_glyphs.parenthesis_number_glyph import Parenthesis_Number_Glyph
from composed_glyphs.proportional_digit_glyph import Proportional_Digit_Glyph
from composed_glyphs.tabular_digit_glyph import Tabular_Digit_Glyph
from concurrent.futures import ProcessPoolExecutor
from logger import configure_logging
import os
from pathlib import Path
from tqdm import tqdm

# How many process to run at most for parallelizable tasks (excluding gftools)
PROCESSES_COUNT: int = int(os.environ.get('PROCESSES_COUNT', '1'))

logger = configure_logging()

# === INTERNAL FUNCTIONS ===

def _build_composed_glyph_from_csv_worker(cg: Composed_Glyph, weight: str, style: int, ufo_dir: Path) -> int:
    '''Subfunction of `build_composed_glyph_from_csv()`'''
    return cg.generate_glif(weight, style, ufo_dir)

def _is_str_an_integer(s: str) -> bool:
    '''Check if a given string can be converted to number'''
    if len(s) == 0:
        return False
    return (s[0] == '-' and s[1:].isnumeric()) or s.isnumeric()

# === PUBLIC FUNCTIONS ===

def get_required_composed_glyphs(target_names: list[str], cg_list: list[Composed_Glyph]) -> list[Composed_Glyph]:
    '''
        Filters a list of `Composed_Glyph` down to only the given target glyphs and everything
        they (recursively) depend on.

        This does NOT detect circular references (this is done later by `set_glyph_priorities_from_list()`
        via `build_tree_from_list()`), it only walks the dependency graph to know what has to be kept.

        Args:
            target_names: names of the glyphs to build. Glyph names that aren't defined in `cg_list`
            cg_list: full list of composed glyphs to filter (typically parsed from the CSV(s)).

        Returns:
            A NEW list, subset of `cg_list`, containing only the needed `Composed_Glyph`.
    '''
    required: set[str] = set()

    def _visit(name: str) -> None:
        if name in required:
            return
        required.add(name)
        if is_composed(name, cg_list):
            for child in get_children_from_name(name, cg_list):
                _visit(child)

    for target in target_names:
        if not is_composed(target, cg_list):
            logger.warning(f'"{target}" is not a composed glyph (or not found) in the given CSV(s): nothing to build for it.')
            continue
        _visit(target)

    filtered: list[Composed_Glyph] = [cg for cg in cg_list if cg.name in required]
    logger.info(f'Filtered down to {len(filtered)} composed glyph(s) needed to build {len(target_names)} requested glyph(s).')
    return filtered

def parse_composed_glyph_csv_line(line: str, index: int | None = None) -> Composed_Glyph | None:
    '''
        Converts a string with value separated by commas into a `Composed_Glyph` object (`Accented_Glyph` or `Composite_Glyph`).

        A line should look like this: `Name,Weight,Styles,Category,Param_1,Param_2,Glyph_1,Glyph_2,Glyph_3,Glyph_4,...`
        * `Name`: name of the composed glyph (`str`)
        * `Weight`: weight where this line applies (`100`, `400` and `1000`). Keep empty for all.
        * `Styles`: styles where this line applies. `1` = normal ; `2` = italic ; `3` = both
        * `Category`: how the glyph `Name` should be build. `A`: accented ; `C`: composite
        * `Param_x`: depends of the `Category`:
                * `A`: `Param_1` = allow left overflow ; `Param_2` = allow right overflow (if an accent would go out of `Glyph_1` limits horizontaly)
                * `C`: `Param_1` = copy anchors
        * `Glyph_x`: glyphs that compose the glyph `Name`, in order.

        Note:
            For `Category`, only the first char is read (case insensitive).
        Args:
            line: the line to read
            index: (optional) line number to show on error messages.
        Returns:
            `Accented_Glyph` or `Composite_Glyph` depending of the `Category` field.
    '''

    def _log_fail(msg: str, index: int | None):
        '''Logging when returning None because of invalid value.'''
        if index is None:
            logger.error(f'Failed to parse line "{line}": {msg}')
        else:
            logger.error(f'Failed to parse line {index}: {msg}')

    data: list[str] = line.split(',')

    if len(data) < 7:  # Check column count
        _log_fail('Not enough columns.', index)
        return None

    # Value check (params check columns 3 and 4 are done in their respective class)
    if data[1].strip() != "" and data[1].strip() not in ['100', '400', '1000']:
        _log_fail(f'Unsupported weight: "{data[1].strip()}"', index)
        return None

    if not data[2].isnumeric():
        _log_fail(f'Invalid style value: "{data[2]}" is not a number.', index)
        return None

    name: str = data[0]
    weight: str | None = None if data[1].strip() == "" else data[1].strip()
    styles: int = int(data[2])
    category: str = data[3].upper()[0:]
    glyphs: list[str] = [g for g in data[6:] if len(g) >= 1]

    if category == 'A':  # Accented glyphs
        if not _is_str_an_integer(data[4]):
            _log_fail(f'Invalid param value at column [4]: "{data[4]}" is not a number', index)
            return None
        if not _is_str_an_integer(data[5]):
            _log_fail(f'Invalid param value at column [5]: "{data[5]}" is not a number', index)
            return None
        left_overflow: bool = bool(int(data[4]))
        right_overflow: bool = bool(int(data[5]))
        return Accented_Glyph(name, weight, styles, left_overflow, right_overflow, glyphs)

    if category == 'C':  # Composite glyph
        if not _is_str_an_integer(data[4]):
            _log_fail(f'Invalid param value at column [4]: "{data[4]}" is not a number', index)
            return None
        copy_anchors: bool = bool(int(data[4]))
        y_offset: int = int(data[5]) if _is_str_an_integer(data[5]) else 0
        return Composite_Glyph(name, weight, styles, copy_anchors, y_offset, glyphs)

    if category == 'P':  # Proportional digit
        if not _is_str_an_integer(data[4]):
            _log_fail(f'Invalid param value at column [4]: "{data[4]}" is not a number', index)
            return None
        if not _is_str_an_integer(data[5]):
            _log_fail(f'Invalid param value at column [5]: "{data[5]}" is not a number', index)
            return None
        size = int(data[4])
        digit_value = int(data[5])
        base = data[6]
        return Proportional_Digit_Glyph(name, weight, styles, size, digit_value, [base])

    if category == 'T':  # Tabular digit
        if not _is_str_an_integer(data[4]):
            _log_fail(f'Invalid param value at column [4]: "{data[4]}" is not a number', index)
        size = int(data[4])
        base = data[6]
        return Tabular_Digit_Glyph(name, weight, styles, size, [base])

    if category == '(':  # number between ()
        return Parenthesis_Number_Glyph(name, weight, styles, glyphs)

    if category == 'O':  # Circled number
        if not _is_str_an_integer(data[4]):
            _log_fail(f'Invalid param value at column [4]: "{data[4]}" is not a number', index)
        unlink_references: bool = bool(int(data[4]))
        return Circled_Number_Glyph(name, weight, styles, unlink_references, glyphs)

    if category == 'S':  # Full stop number (w/ period)
        return Full_Stop_Number_Glyph(name, weight, styles, glyphs)

    # Unknown category
    _log_fail(f'Invalid category at column [3]: "{category}"', index)
    return None

def parse_composed_glyph_csv(csv_file: Path, weight: str | None, styles: int, first_line_number: int = 1) -> list[Composed_Glyph]:
    '''
        Read an entire CSV file describing composed glyphs (see `parse_composed_glyph_csv_line()`).
        This function handles logging.

        Args:
            csv_file: path to the csv file to read
            weight: `100` (Thin), `400` (Regular), `1000` (ExtraBlack)
            styles: `1` = normal, `2` = italic, `3` = both
            first_line_number: first line number to read in the CSV. First line in the file is 1!
        Return:
            list[Composed_Glyph]. Invalid or duplicates lines are ignored.
        Note:
            This function does not check circular references or duplicates.
    '''
    cg_list: list[Composed_Glyph] = []
    cg_list_names: dict[str, int] = {}  # maps glyphs with their line number in CSV
    with open(csv_file, 'r') as f:
        for line_number, line in enumerate(f.readlines(), start=1):
            if line_number >= first_line_number:
                cg: Composed_Glyph | None = parse_composed_glyph_csv_line(line.strip(), line_number + 1)
                if cg is None:  # invalid line -> parse_composed_glyph_csv_line prints warning message
                    #logger.debug(f'Line {line_number} is invalid: skipped')
                    pass
                elif (cg.supported_weight is not None) and (cg.supported_weight != weight):  # weight check
                    #logger.debug(f'Line {line_number} failed weight check: {cg.weight} != {weight}: skipped')
                    pass
                elif not cg.supported_styles & styles:  # style check
                    #logger.debug(f'Line {line_number} failed style check: {cg.styles}&{styles} = {cg.styles & styles}: skipped')
                    pass  # nothing to do, skip the line
                elif cg.name in cg_list_names.keys():  # duplicate glyph check
                    logger.warning(f'"{csv_file}": line {line_number} will be ignored, "{cg.name}" is already defined at line {cg_list_names[cg.name]}')
                else:  # all good :)
                    cg_list.append(cg)
                    cg_list_names[cg.name] = line_number
    logger.debug(f'Parsed {len(cg_list)} composed glyphs from "{csv_file}".')
    return cg_list

def build_composed_glyph_from_csv(csv_file: Path | list[Path], ufo_dir: Path, weight: str, style: int, processes_count: int = 1, target_glyphs: list[str] | None = None) -> int:
    '''
        Builds composed glyphs (.glif) from a CSV definition inside an UFO directory. Overwrites existing .glif files.

        This function parses a CSV file containing composed glyph definitions, assigns priority
        levels to the glyphs based on their tree structure, and iterates through each priority
        level to generate individual `.glif` files within the specified output directory (`ufo_dir`).

        It supports multiprocessing (using `ProcessPoolExecutor`) when requested via `processes_count`.

        Args:
            csv_file: Path to the CSV file(s) containing composed glyph definitions.
            ufo_dir: The base directory where the resulting `.glif` files (UFO components) will be written.
            weight: `100` (Thin), `400` (Regular), `1000` (ExtraBlack)
            style: `1` = non-italic, `2` = italic
            processes_count: (optional) Number of worker processes to use for generation. If `1` or not given, sequential execution is used.
            target_glyphs: (optional) If given, only build these glyphs and their dependencies, recursively.
        Returns:
            int: `0` if no error, `-1` if invalid input has been detected.
            An error count representing the number of glyphs that failed to generate successfully.
    '''
    logger.info(f'Working on "{ufo_dir}"...')

    # Styles value check
    if style <= 0:
        logger.error(f'Invalid value for "styles": {style}')
        return -1

    # Read CSV
    cg_list: list[Composed_Glyph] = []
    if isinstance(csv_file, list):  # several files
        for c in csv_file:
            logger.info(f'Reading "{c}"...')
            cg_list += parse_composed_glyph_csv(c, weight, style, 2)
    else:  # 1 file
        logger.info(f'Reading "{csv_file}"...')
        cg_list = parse_composed_glyph_csv(csv_file, weight, style, 2)  # priority is 0 by default
    if len(cg_list) == 0:
        logger.warning('No glyph has been generated, nothing to build.')
        return 0

    # Restrict to the requested glyphs (+ dependencies) if asked
    if target_glyphs is not None:
        logger.info(f'Restricting build to {len(target_glyphs)} requested glyph(s) and their dependencies: {" ".join([f'"{c}"' for c in target_glyphs])}')
        cg_list = get_required_composed_glyphs(target_glyphs, cg_list)
        if len(cg_list) == 0:
            logger.warning('None of the requested glyphs are composed glyphs found in the given CSV(s), nothing to build.')
            return 0
        logger.info(f'{len(cg_list)} glyphs will be built: {" ".join([f'"{c.name}"' for c in cg_list])}')

    # Set priorities by building tree
    cg_list = set_glyph_priorities_from_list(cg_list)
    total_glyphs: int = len(cg_list)
    if len(cg_list) == 0:
        logger.error('No glyph has been generated.')
        return -1

    max_priority: int = cg_list[0].priority
    logger.info(f'Found {total_glyphs} glyphs inside {" ".join([f'"{str(f)}"' for f in csv_file]) if isinstance(csv_file, list) else csv_file}.')
    logger.info(f'{processes_count} processes will be used.')
    error_count: int = 0
    with tqdm(total=total_glyphs) as progress_bar:
        for priority in reversed(range(max_priority + 1)):
            cg_with_priority: list[Composed_Glyph] = [cg for cg in cg_list if cg.priority == priority]
            logger.verbose(f'Building {len(cg_with_priority)} glyphs with priority {priority}')  # pyright: ignore[reportUnknownMemberType]
            if processes_count > 1:
                logger.verbose(f'Using multiprocessing ({processes_count} processes)')  # pyright: ignore[reportUnknownMemberType]
                with ProcessPoolExecutor(max_workers=processes_count) as executor:
                    futures = [executor.submit(_build_composed_glyph_from_csv_worker, cg, weight, style, ufo_dir) for cg in cg_with_priority]
                    for future in futures:
                        error_count += future.result()
                        progress_bar.update(1)
            else:
                logger.verbose('Using a single process.')  # pyright: ignore[reportUnknownMemberType]
                for cg in cg_with_priority:
                    if cg.generate_glif(weight, style, ufo_dir) != 0:
                        error_count += 1
                    progress_bar.update(1)

    if error_count >= total_glyphs:
        logger.error(f'Failed to generate every of the {total_glyphs} glyphs.')
    else:
        logger.success(f'Sucessfully generated {total_glyphs - error_count} / {total_glyphs} glyphs into "{ufo_dir}"')  # pyright: ignore[reportUnknownMemberType]
        if error_count > 0:
            logger.error(f'Failed to generate {error_count} glyphs.')

    logger.warning(f'PLEASE OPEN AND SAVE "{ufo_dir}" WITH FONTFORGE TO COMPLETE THE PROCESS!!!' )

    return error_count


if __name__ == '__main__':

    # Read input args
    parser = argparse.ArgumentParser(description='Generate .glif files from a CSV config.')
    parser.add_argument('ufo_dir', type=str, help='UFO dir to write.')
    parser.add_argument('weight', type=str, help='100 = Thin ; 400 = Regular ; 1000 = ExtraBlack', choices=['100', '400', '1000'])
    parser.add_argument('style', type=int, help='1 = non-italic ; 2 = italic', choices=[1, 2])
    parser.add_argument('csv_config', type=str, nargs='+', help='List(s) of glyphs as CSV file.')
    parser.add_argument('--glyphs', type=str, nargs='+', default=None, metavar='GLYPH_NAME', help='(optional) Only build these glyph name(s) and the composed glyphs they depend on instead of building every glyph listed in csv_config.')

    # Check args values
    try:
        args = parser.parse_args()
    except Exception as err:
        logger.critical(err)
        print(parser.print_help())
        exit(1)
    for csv_file in args.csv_config:
        if not Path(csv_file).exists():
            logger.critical(f'CSV config not found: "{args.csv_config}"')
            exit(1)
    if not Path(args.ufo_dir).exists():
        logger.critical(f'UFO not found: "{args.ufo_dir}"')
        exit(1)

    # Run
    csv_files: list[Path] = [Path(f) for f in args.csv_config]
    exit_code: int = build_composed_glyph_from_csv(csv_files, Path(args.ufo_dir), args.weight, args.style, PROCESSES_COUNT, args.glyphs)
    exit(1 if exit_code == -1 else 0)
