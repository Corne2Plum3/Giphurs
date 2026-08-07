import argparse
from fontTools.ttLib import TTFont
from git import Repo
from pathlib import Path
import sys
import xml.etree.ElementTree as ET

def get_commit_hash(git_repo_path: str | Path = '.') -> str:
    return str(Repo(git_repo_path).head.commit)[:7]

def get_font_version(font_path: str | Path) -> str:
    font = TTFont(font_path)
    name_table = font['name']  # Access the name table
    for record in name_table.names:  # Name ID 5 represents the Version string
        if record.nameID == 5:
            return record.toUnicode()  # Decode the version string using the record's encoding
    return 'Version unknown'

def print_commit_hash_on_svg(svg_filename: str | Path, font_filename: str | Path, xml_text_node: str) -> int:
    '''
        Writes the font version and the latest commit hash in a text node. The target node must exist.

        Args:
            svg_filename: SVG file to edit.
            font_filename: font file where to get the version
            xml_text_node: `id` of the `<text>` node to write
        Returns:
            `0` if success, non-zero of fail.
    '''
    print('Updating the commit hash inside some images.')

    xml_tree = ET.parse(svg_filename)
    xml_root = xml_tree.getroot()
    commit_written: bool = False
    for elem in xml_root.iter():
        if any(attr.endswith("id") and val == xml_text_node for attr, val in elem.attrib.items()):
            new_text = f'{get_font_version(font_filename)} ({get_commit_hash(".")})'
            
            # If the element has child nodes (like <tspan>), update the first child's text
            if len(elem) > 0:
                elem[0].text = new_text
                elem.text = None  # Ensure parent has no direct text
            else:
                elem.text = new_text
                
            commit_written = True
            break

    if not commit_written:
        print(f'Failed to write commit version into "{svg_filename}"')
        return 1

    print(f'Writing into "{svg_filename}"...')
    xml_tree.write(svg_filename, encoding='utf-8', xml_declaration=True)
    print(f'Successfully wrote "{get_font_version(font_filename)} ({get_commit_hash('.')})" into "{svg_filename}"')
    return 0

if __name__ == '__main__':
    # Read args
    parser = argparse.ArgumentParser(description='Writes the font version and the latest commit hash in a text node. The target node must exist.')
    parser.add_argument('svg_filename', type=str, help='SVG file to edit.')
    parser.add_argument('font_filename', type=str, help='font file where to get the version')
    parser.add_argument('xml_text_node', type=str, help='id of the <text> node to write inside the SVG')
    args = parser.parse_args()
    if args.svg_filename is None or args.font_filename is None or args.xml_text_node is None:
        print(f'{sys.argv[0]}: Not enough arguments.')
        parser.print_help()
        exit(1)

    # Run
    print_commit_hash_on_svg(args.svg_filename, args.font_filename, args.xml_text_node)
    exit(0)
