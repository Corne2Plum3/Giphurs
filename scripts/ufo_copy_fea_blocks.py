from fontTools.feaLib.parser import Parser  # pyright: ignore[reportMissingTypeStubs]
from fontTools.feaLib.ast import FeatureBlock, FeatureFile, LookupBlock  # pyright: ignore[reportMissingTypeStubs]
from logger import configure_logging
from pathlib import Path
import sys

FEATURES_LIST = './scripts/common_features_list.txt'
LOOKUPS_LIST = './scripts/common_lookups_list.txt'

logger = configure_logging(__name__)

def copy_fea_blocks(fea_src: Path, fea_dst: Path, mode: str, names: list[str]) -> int:
    '''
    Copy a list of blocks from a features.fea to another features.fea file.
    Writes the destination file.
    Args:
        fea_src: sources of tables to copy
        fea_dst: where to copy the tables
        mode: type of what being copied. `feature` or `lookup`
        names: names of the tables to copy
    Returns:
        `0` if success, non-zero otherwise.
    '''

    # Check mode value
    statement_type: type
    if mode.lower() == 'feature':
        statement_type = FeatureBlock
    elif mode.lower() == 'lookup':
        statement_type = LookupBlock
    elif mode.lower() in ['nested', 'table']:
        raise NotImplementedError(f'Unsupported mode: {mode}')  # too lazy lol and not needed at the moment
    else:
        raise ValueError(f'Unsupported mode: "{mode}"')

    # Read .fea files
    try:
        logger.info(f'Copying {len(names)} {mode}(s) from "{fea_src}" into "{fea_dst}"...')
        src_parser: Parser = Parser(fea_src)
        src_ast: FeatureFile = src_parser.parse()
        dst_parser: Parser = Parser(fea_dst)
        dst_ast: FeatureFile = dst_parser.parse()
        
        # Copy
        for statement_target in names:
            # Find statement in source
            src_index: int | None = None  # ... of the statement with the name we want
            for i, statement in enumerate(src_ast.statements):  # pyright: ignore[reportUnknownArgumentType, reportUnknownMemberType, reportUnknownVariableType]
                if isinstance(statement, statement_type) and statement.name == statement_target:  # pyright: ignore[reportUnknownMemberType]
                    src_index = i
                    break
            if src_index is None:
                logger.warning(f'{mode} "{statement_target}" not found in source "{fea_src}".')
                continue
            # Find statement in destination
            dst_index: int | None = None
            for i, statement in enumerate(dst_ast.statements):  # pyright: ignore[reportUnknownArgumentType, reportUnknownMemberType, reportUnknownVariableType]
                if isinstance(statement, statement_type) and statement.name == statement_target:  # pyright: ignore[reportUnknownMemberType]
                    dst_index = i
                    break
            if dst_index is None:
                logger.info(f'{mode} "{statement_target}" not found in destination "{fea_dst}".')
            # Copy
            if dst_index is not None:  # statement both in src and dst
                dst_ast.statements[dst_index] = src_ast.statements[src_index]  # pyright: ignore[reportUnknownMemberType]
            else:
                logger.debug(f'Inserting {mode} "{statement_target}" at index {src_index} into "{fea_dst}".')
                dst_ast.statements.insert(src_index, src_ast.statements[src_index])  # pyright: ignore[reportUnknownMemberType, reportUnknownArgumentType]
        
        # Save
        with open(fea_dst, 'w', encoding='utf-8') as f:
            logger.debug(f'Writing into "{fea_dst}"...')
            f.write(dst_ast.asFea())

    except Exception as err:
        logger.critical(f'{err}')
        return 1
    
    logger.success(f'Done copying {mode} into "{fea_dst}".')  # pyright: ignore[reportUnknownMemberType]
    return 0

if __name__ == '__main__':

    # Read parameters
    if len(sys.argv) < 3:
        print(f"ERROR: {sys.argv[0]}: Not enough parameters.")
        print(f"Usage: {sys.argv[0]} <SRC> <DST>")
        print("* SRC: source of the features and lookups to copy (.fea file).")
        print("* DST: destination of the features and lookups. They get overwritten if already present (.fea file)")
        print("* Features and lookups to copy are defined by FEATURES_LIST and LOOKUPS_LIST in this script.")
        exit(1)
    fea_src: Path = Path(sys.argv[1])
    fea_dst: Path = Path(sys.argv[2])

    # List of what to copy
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

    # Apply modifications
    if copy_fea_blocks(fea_src, fea_dst, 'feature', feature_list) != 0:
        exit(1)
    if copy_fea_blocks(fea_src, fea_dst, 'lookup', lookup_list) != 0:
        exit(1)
    
    exit(0)