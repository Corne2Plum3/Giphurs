"""
This script put all sylistic names (e.g. ss01) from sfd file into features.fea from UFO folder.
Fixes FontBakery com.google.fonts/check/stylisticset_description WARN [code: missing-description] 
"""

import pathlib
import sys

def get_stylistic_description(sfd_path):
    """ Read the sfd file at sfd_path and return a dict with the form {"ss00": "description"}. """

    assert (pathlib.Path(sfd_path).suffix).lower() == ".sfd"  # verify that we're using a .sfd file

    stylistic_dict = {}

    with open(sfd_path) as sfd_file:

        for line in sfd_file:
            
            line_content = line.strip()
            if line_content[0:11] == "OtfFeatName":  # line with the stylistic style description
                stylistic_style_name = line_content.split("'")[1]
                stylistic_style_description = line_content.split('"')[1]
                stylistic_dict[stylistic_style_name] = stylistic_style_description

    return stylistic_dict

def inject_stylistic_description(ufo_dst, sfd_src):
    """ Returns the amount of stylistic descriptions added (int). """

    stylistic_dict = get_stylistic_description(sfd_src)  # get the list of all stylisctic styles with description

    # inject text
    features_fea_file = f"{ufo_dst}/features.fea"
    for ss in stylistic_dict.keys():
        text_to_inject = f'featureNames \u007b\n\tname 3 1 0x409 "{stylistic_dict[ss]}";\n\tname 3 1 0x411 "{stylistic_dict[ss]}";\n\tname 1 "{stylistic_dict[ss]}";\n\tname 1 1 12 "{stylistic_dict[ss]}";\n\u007d;\n'
        
        # find the line where to inject the text
        with open(features_fea_file, "r") as fea:
            contents = fea.readlines()
            line_target = contents.index(f"feature {ss} \u007b\n") + 1

        # inject the text
        contents.insert(line_target, text_to_inject)

        with open(features_fea_file, "w") as fea:
            contents = "".join(contents)
            fea.write(contents)

    return len(stylistic_dict.keys())


def main():
    # stop the program if too few arguments
    assert (len(sys.argv) >= 3), f"{sys.argv[0]}: Too few arguments.\nUsage: python3 {sys.argv[0]} <ufo_dst> <sfd_src>"
    
    print(f"{sys.argv[0]}: Adding stylistic sets description to {sys.argv[1]} from {sys.argv[2]}")
    stylistic_sets_added = inject_stylistic_description(sys.argv[1], sys.argv[2])
    print(f"{sys.argv[0]}: Done, {stylistic_sets_added} stylistic sets descriptions added.")


if __name__ == "__main__":
    main()
