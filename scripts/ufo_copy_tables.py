from fontTools.feaLib.parser import Parser
from fontTools.feaLib.ast import FeatureBlock, FeatureFile, LookupBlock
import sys

FEATURES_LIST = 'scripts/common_features_list.txt'
LOOKUPS_LIST = 'common_lookups_list'

def copy_tables(fea_src: FeatureFile, fea_dst: FeatureFile, mode: str, names: list[str]) -> FeatureFile:

    statement_type = None
    if mode.lower() == 'feature':
        statement_type = FeatureBlock
    elif mode.lower() == 'lookup':
        statement_type = LookupBlock
    else:
        raise ValueError(f'Unsupported mode: "{mode}"')

    for statement_target in names:
        # Find statement in source
        src_index = None  # ... of the statement with the name we want
        for i, statement in enumerate(src_ast.statements):
            if isinstance(statement, statement_type) and statement.name == statement_target:
                src_index = i
                break
        if src_index is None:
            print(f'[WARNING] {mode} "{statement_target}" not found in source "{fea_src}".')
            continue
        # Find statement in destination
        dst_index = None
        for i, statement in enumerate(dst_ast.statements):
            if isinstance(statement, statement_type) and statement.name == statement_target:
                dst_index = i
                break
        if dst_index is None:
            print(f'[WARNING] {mode} "{statement_target}" not found in destination "{fea_dst}".')
        # Copy
        if dst_index is not None:  # statement both in src and dst
            dst_ast.statements[dst_index] = src_ast.statements[src_index]
        else:
            print(f'[INFO] Inserting {mode} "{statement_target}" at index {src_index} into "{fea_dst}".')
            dst_ast.statements.insert(src_index, src_ast.statements[src_index])

    print(f'[INFO] Done.')
    return dst_ast

if __name__ == '__main__':

    # Read parameters
    if len(sys.argv) < 3:
        print(f"ERROR: {sys.argv[0]}: Not enough parameters.")
        print(f"Usage: {sys.argv[0]} <SRC> <DST>")
        print("* SRC: source of the features and lookups to copy (.fea file).")
        print("* DST: destination of the features and lookups. They get overwritten if already present (.fea file)")
        print("* Features and lookups to copy are defined by FEATURES_LIST and LOOKUPS_LIST in this script.")
        exit(1)

    fea_src = sys.argv[1]
    fea_dst = sys.argv[2]

    # List of what to copy
    feature_list = []
    with open('scripts/common_features_list.txt', 'r') as f:
        for line in f.readlines():
            if len(line.strip()) >= 1:
                feature_list.append(line.strip())
    
    lookup_list = []
    with open('scripts/common_lookups_list.txt', 'r') as f:
        for line in f.readlines():
            if len(line.strip()) >= 1:
                lookup_list.append(line.strip())

    # Read .fea files
    src_parser = Parser(fea_src)
    src_ast = src_parser.parse()
    dst_parser = Parser(fea_dst)
    dst_ast = dst_parser.parse()
    
    # Apply modifications
    dst_ast = copy_tables(src_ast, dst_ast, 'feature', feature_list)
    dst_ast = copy_tables(src_ast, dst_ast, 'lookup', lookup_list)

    # Save
    with open(fea_dst, 'w', encoding='utf-8') as f:
        print(f'[INFO] Writing into "{fea_dst}...')
        f.write(dst_ast.asFea())

    exit(0)