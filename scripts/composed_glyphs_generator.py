import argparse
from logger import configure_logging
from pathlib import Path
import sys

# === CONSTANTS (common to all) ===

CSV_HEADER: str = 'Glyphname,Styles,Category,Left overflow | Anchors,Right overflow | -,Glyph 1,Glyph 2,Glyph 3,Glyph 4'

DIGITS_NAMES: list[str] = ['zero', 'one', 'two', 'three', 'four', 'five', 'six', 'seven', 'eight', 'nine']
logger = configure_logging()

# === INTERNAL TOOLS ===

def _get_all_digits_alternates_suffixes(digit_1: int, digit_2: int | None = None) -> list[str] | dict[str, tuple[str, str]]:
    '''
        Returns all alternates suffixes for the given digit(s).
        
        If there's only 1 digit, a list of string is returned.

        If there are 2 digits, a dict is returned: each key is a suffix, mapped to a tuple with the suffixes of digit_1 and digit_2.
        
        Example: digits 1 and 2 have a variant `cv01` and `cv02`. Output is:`{'': ('', ''), '.cv01': ('.cv01', ''), '.cv02': ('', '.cv02'), '.cv01.cv02': ('.cv01', '.cv02')}`
    '''

    DIGITS_CV_LIST: dict[int, list[str]] = {
        0: ['cv10', 'cv20'],
        1: ['cv01', 'cv11'],
        2: ['cv02', 'cv12'],
        3: ['cv03', 'cv13'],
        4: ['cv04', 'cv14'],
        5: ['cv05', 'cv15'],
        6: ['cv06', 'cv16'],
        7: ['cv07', 'cv17'],
        8: ['cv08', 'cv18'],
        9: ['cv09', 'cv19'],
    }

    DIGITS_SS_LIST: dict[int, list[str]] = {
        1: ['ss06'],
        7: ['ss07'],
        0: ['zero'],
    }

    assert digit_1 >= 0 and digit_1 <= 9
    assert digit_2 is None or (digit_2 >= 0 and digit_2 <= 9)

    
    # 1 digit
    if digit_2 is None:
        alternate_list_1d: list[str] = []
        for ss in [''] + (DIGITS_SS_LIST[digit_1] if digit_1 in DIGITS_SS_LIST else []):
            for cv in [''] + DIGITS_CV_LIST[digit_1]:
                glyph_suffix: str = ('.' + cv) if cv != '' else ''
                glyph_suffix += ('.' + ss) if ss != '' else ''
                alternate_list_1d.append(glyph_suffix)
        return alternate_list_1d

    # 2 digits
    alternate_list_2d: dict[str, tuple[str, str]] = {}
    for ss2 in [''] + (DIGITS_SS_LIST[digit_2] if digit_2 in DIGITS_SS_LIST else []):
        for ss1 in [''] + (DIGITS_SS_LIST[digit_1] if digit_1 in DIGITS_SS_LIST else []):
            for cv2 in [''] + DIGITS_CV_LIST[digit_2]:
                for cv1 in [''] + DIGITS_CV_LIST[digit_1]:
                    cv1_ordered: str
                    cv2_ordered: str 
                    if cv1 != '' and cv2 != '' and int(cv1[2:]) > int(cv2[2:]):
                        cv1_ordered, cv2_ordered = cv2, cv1
                    else:
                        cv1_ordered, cv2_ordered = cv1, cv2
                    ss1_ordered: str
                    ss2_ordered: str
                    if ss1 != '' and ss2 != '' and list(DIGITS_SS_LIST.keys()).index(digit_1) > list(DIGITS_SS_LIST.keys()).index(digit_2):
                        ss1_ordered, ss2_ordered = ss2, ss1
                    else:
                        ss1_ordered, ss2_ordered = ss1, ss2
                    glyph_suffix_all: str = ('.' + cv1_ordered) if cv1_ordered != '' else ''
                    glyph_suffix_all += ('.' + cv2_ordered) if cv2_ordered != '' else ''
                    glyph_suffix_all += ('.' + ss1_ordered) if ss1_ordered != '' else ''
                    glyph_suffix_all += ('.' + ss2_ordered) if ss2_ordered != '' else ''
                    glyph_suffix_1: str = ('.' + cv1) if cv1 != '' else ''
                    glyph_suffix_1 += ('.' + ss1) if ss1 != '' else ''
                    glyph_suffix_2: str = ('.' + cv2) if cv2 != '' else ''
                    glyph_suffix_2 += ('.' + ss2) if ss2 != '' else ''
                    alternate_list_2d[glyph_suffix_all] = (glyph_suffix_1, glyph_suffix_2)
    return alternate_list_2d

def _update_csv(csv_file: Path, csv_lines: list[str]) -> int:
    '''
        Change the content of the composed glyphs CSV with the given glyphs data:
        * if the glyph already exists in the file, it is replaced with the new data
        * if not, the glyph is added in the end
        File is created if not found.

        Args:
            csv_file: File to write
            csv_lines: Glyph data to write, given as list of CSV line content
        
        Returns:
            `0` if success, `1` if fail and the CSV has been left untouched, `2` if fail and the CSV has been modified
    '''
    logger.info(f'Updating "{csv_file}"...')
    glyphs_to_write: dict[tuple[str, str, str], str] = {(l.split(',')[0], l.split(',')[1], l.split(',')[2]) : l for l in csv_lines}  # maps glyph name with the associated line
    replaced_lines: int = 0
    added_lines: int = 0
    new_csv_content: str = ''

    # Read file and replace existing lines
    try:
        logger.debug(f'Reading "{csv_file}"...')
        with open(csv_file, 'r') as f:
            for line_number, line in enumerate(f.readlines(), start=1):
                if line_number == 1:  # header
                    new_csv_content += line
                    continue
                if line.strip() == '':  # empty line
                    continue
                if ',' not in line.strip():
                    logger.warning(f'"{csv_file}": line {line_number} is invalid.')
                    continue
                line_glyph_name_weight_style = (line.strip().split(',')[0], line.strip().split(',')[1], line.strip().split(',')[2])
                if line_glyph_name_weight_style in glyphs_to_write.keys():  # replace
                    new_csv_content += glyphs_to_write[line_glyph_name_weight_style] + '\n'
                    glyphs_to_write.pop(line_glyph_name_weight_style)
                    replaced_lines += 1
                else:
                    new_csv_content += line
    except FileNotFoundError:
        logger.info(f'"{csv_file}" not found, it will be created.')
        new_csv_content += CSV_HEADER
    except Exception as err:
        logger.error(f'Error when reading "{csv_file}": {err}')
        return 1

    # Add remaining entries
    for line in glyphs_to_write.values():  # write remaining lines
        new_csv_content += line + '\n'
        added_lines += 1

    # Actually write in the file
    try:
        logger.debug(f'Writing "{csv_file}"...')
        with open(csv_file, 'w') as f:
            f.write(new_csv_content)
    except Exception as err:
        logger.error(f'Error when writing "{csv_file}": {err}')
        return 2

    # Success message and leave
    logger.success(f'Successfully updated "{csv_file}" ({added_lines} new lines ; {replaced_lines} replaced lines)')  # pyright: ignore[reportUnknownMemberType]
    return 0


# === GENERATORS (print csv lines in stdin) ===

def get_csv_fractions() -> list[str]:
    '''Write CSV lines to generate the fractions.'''

    # {'glyph name': (numr, dnom)}
    FRACTIONS_DIGITS: dict[str, tuple[int | None, int | None]] = {
        'onequarter': (1, 4),
        'onehalf': (1, 2),
        'threequarters': (3, 4),
        'uni2150': (1, 7),
        'uni2151': (1, 9),
        'uni2152': (1, 10),
        'onethird': (1, 3),
        'twothirds': (2, 3),
        'uni2155': (1, 5),
        'uni2156': (2, 5),
        'uni2157': (3, 5),
        'uni2158': (4, 5),
        'uni2159': (1, 6),
        'uni215A': (5, 6),
        'oneeighth': (1, 8),
        'threeeighths': (3, 8),
        'fiveeighths': (5, 8),
        'seveneighths': (7, 8),
        'uni215F': (1, None),
        'uni2189': (0, 3)
    }

    csv_lines: list[str] = []

    for frac_name, frac_value in FRACTIONS_DIGITS.items():
        frac_numr: int | None = frac_value[0]
        frac_dnom: int | None = frac_value[1]

        # get variants
        unique_digits_list: list[int] = []
        if frac_numr is not None and frac_dnom is not None:
            unique_digits_list = list(set([int(d) for d in str(frac_numr)] + [int(d) for d in str(frac_dnom)]))
        elif frac_numr is not None:
            unique_digits_list = list(set([int(d) for d in str(frac_numr)]))
        elif frac_dnom is not None:
            unique_digits_list = list(set([int(d) for d in str(frac_dnom)]))
        
        all_digits_alternates_suffixes: list[str] | dict[str, tuple[str, str]] = _get_all_digits_alternates_suffixes(
            unique_digits_list[0],
            unique_digits_list[1] if len(unique_digits_list) >= 2 else None
        )

        csv_line: str
        numr_glyphs: list[str] = []
        dnom_glyphs: list[str] = []
        if type(all_digits_alternates_suffixes) == list:  # 1 digit
            for suffix in all_digits_alternates_suffixes:
                numr_glyphs.clear()
                dnom_glyphs.clear()
                numr_glyphs = [f'{DIGITS_NAMES[int(d)]}{suffix}.numr' for d in str(frac_numr)] if frac_numr is not None else []
                dnom_glyphs = [f'{DIGITS_NAMES[int(d)]}{suffix}.dnom' for d in str(frac_dnom)] if frac_dnom is not None else []
                csv_line = f'{frac_name}{suffix},,3,C,0,'
                for g in numr_glyphs + ['fraction'] + dnom_glyphs:
                    csv_line += ',' + g
                csv_lines.append(csv_line)
        if type(all_digits_alternates_suffixes) == dict:  # 2 digits
            for suffix in all_digits_alternates_suffixes:
                numr_glyphs.clear()
                dnom_glyphs.clear()
                d1_str: int = unique_digits_list[0]
                d2_str: int = unique_digits_list[1]
                d1_glyph: str = DIGITS_NAMES[d1_str] + all_digits_alternates_suffixes[suffix][0]
                d2_glyph: str = DIGITS_NAMES[d2_str] + all_digits_alternates_suffixes[suffix][1]
                for d in str(frac_numr):
                    if d == str(d1_str):
                        numr_glyphs.append(d1_glyph + '.numr' + ('.pnum' if len(str(frac_numr)) >= 2 else ''))
                    elif d == str(d2_str): 
                        numr_glyphs.append(d2_glyph + '.numr' + ('.pnum' if len(str(frac_numr)) >= 2 else ''))
                    else:
                        raise ValueError
                for d in str(frac_dnom):
                    if d == str(d1_str):
                        dnom_glyphs.append(d1_glyph + '.dnom' + ('.pnum' if len(str(frac_dnom)) >= 2 else ''))
                    elif d == str(d2_str):
                        dnom_glyphs.append(d2_glyph + '.dnom' + ('.pnum' if len(str(frac_dnom)) >= 2 else ''))
                    else:
                        raise ValueError
                csv_line = f'{frac_name}{suffix},,3,C,0,0'
                for g in numr_glyphs + ['fraction'] + dnom_glyphs:
                    csv_line += ',' + g
                csv_lines.append(csv_line)

    logger.info(f'Generated {len(csv_lines)} entries.')
    return csv_lines

def get_csv_digits() -> list[str]:
    '''Write CSV lines to generate .pnum and .tnum alternates of digits.'''

    csv_lines: list[str] = []
    
    for digit_value, digit_name in enumerate(DIGITS_NAMES):
        for alt_suffix in _get_all_digits_alternates_suffixes(digit_value):
            # pnum
            pnum_glyph_name: str = digit_name + alt_suffix + '.pnum'
            csv_lines.append(f'{pnum_glyph_name},,3,P,1,{digit_value},{digit_name + alt_suffix}')
            # tnum (only works because the digits are .tnum by default !!)
            tnum_glyph_name: str = digit_name + alt_suffix + '.tnum'
            csv_lines.append(f'{tnum_glyph_name},,3,T,1,,{digit_name + alt_suffix}')
    return csv_lines

def get_csv_small_digits() -> list[str]:
    '''Write CSV lines to generate .superior, .subscript, .numr and .dnom (+ .pnum, .tnum) alternates of digits.'''
    Y_OFFSET = {'.subscript': -988, '.numr': -188, '.dnom': -810}  # compared to .superior
    
    csv_lines: list[str] = []
    
    for digit_value, digit_name in enumerate(DIGITS_NAMES):
        for alt_suffix in _get_all_digits_alternates_suffixes(digit_value):
            # .superior.pnum
            csv_lines.append(f'{digit_name + alt_suffix + '.superior.pnum'},,3,P,0,{digit_value},{digit_name + alt_suffix + '.superior'}')
            # .superior.tnum
            csv_lines.append(f'{digit_name + alt_suffix + '.superior.tnum'},,3,T,0,,{digit_name + alt_suffix + '.superior'}')
            for y_suffix, y_offset in Y_OFFSET.items():  # .subscript, .numr and .dnom
                # (.subscript/.numr/.dnom)
                csv_lines.append(f'{digit_name + alt_suffix + y_suffix},,3,C,0,{y_offset},{digit_name + alt_suffix + '.superior'}')
                # (.subscript/.numr/.dnom).pnum
                csv_lines.append(f'{digit_name + alt_suffix + y_suffix + '.pnum'},,3,C,0,{y_offset},{digit_name + alt_suffix + '.superior.pnum'}')
                # (.subscript/.numr/.dnom).tnum
                csv_lines.append(f'{digit_name + alt_suffix + y_suffix + '.tnum'},,3,C,0,{y_offset},{digit_name + alt_suffix + '.superior.tnum'}')
    return csv_lines

# === ENTRY POINT ===

if __name__ == '__main__':
    # Read args
    parser = argparse.ArgumentParser(description="Generate lines for composed glyphs CSV file for fractions glyphs into stdin.")
    parser.add_argument('csv_file', type=str, help="Composed glyph CSV to update.")
    parser.add_argument('--fractions', action='store_true', help="Generate CSV lines for fractions.")
    parser.add_argument('--digits', action='store_true', help="Generate CSV lines for .pnum and .tnum digits.")
    parser.add_argument('--small_digits', action='store_true', help="Generate CSV lines for .superior, .subscript, .numr and .dnom digits.")
    args = parser.parse_args()
    if args.csv_file is None:
        logger.error(f'{sys.argv[0]}: CSV file not given.')
        parser.print_help()
        exit(1)

    # Get lines to write
    new_lines: list[str] = []
    if args.fractions:
        new_lines += get_csv_fractions()
    if args.digits:
        new_lines += get_csv_digits()
    if args.small_digits:
        new_lines += get_csv_small_digits()

    # Update file
    if len(new_lines) != 0:
        _update_csv(args.csv_file, new_lines)
    else:
        logger.warning(f'{sys.argv[0]}: No line to generate...')

    exit(0)