"""
This script put all sylistic names (e.g. ss01) from sfd file into features.fea from UFO folder.
Fixes FontBakery com.google.fonts/check/stylisticset_description WARN [code: missing-description] 
"""

import pathlib
import sys

def get_stylistic_description(sfd_path):
    """ Read the sfd file at sfd_path and return a dict with the form {"ss00": "description"}. """

    assert (pathlib.Path(sfd_path).suffix).lower() == ".sfd"  # verify that we're using a .sfd file

    sylistic_dict = {}

    with open(sfd_path) as sfd_file:

        for line in sfd_file:
            
            line_content = line.strip()
            if line_content[0:11] == "OtfFeatName":  # line with the stylistic style description
                stylistic_style_name = line_content.split("'")[1]
                stylistic_style_description = line_content.split('"')[1]
                sylistic_dict[stylistic_style_name] = stylistic_style_description

                print(f"Found style {stylistic_style_name} in sfd file.")


    return sylistic_dict


if len(sys.argv) < 3:  # too few arguments
    print(f"{sys.argv[0]}: Too few arguments.\nUsage: python3 {sys.argv[0]} <ufo_dst> <sfd_src>")

sylistic_dict = get_stylistic_description(sys.argv[2])  # get the list of all stylisctic styles with description

# inject text

features_fea_file = f"{sys.argv[1]}/features.fea"
print(f"Writing {features_fea_file}")
for ss in sylistic_dict.keys():
    text_to_inject = f'featureNames \u007b\n\tname 3 1 0x409 "{sylistic_dict[ss]}";\n\tname 3 1 0x411 "{sylistic_dict[ss]}";\n\tname 1 "{sylistic_dict[ss]}";\n\tname 1 1 12 "{sylistic_dict[ss]}";\n\u007d;\n'
    
    # find the line where to inject the text
    with open(features_fea_file, "r") as fea:
        contents = fea.readlines()
        line_target = contents.index(f"feature {ss} \u007b\n") + 1

    # inject the text
    contents.insert(line_target, text_to_inject)

    with open(features_fea_file, "w") as fea:
        contents = "".join(contents)
        fea.write(contents)

print(f"{len(sylistic_dict.keys())} stylistic styles descriptions added!")
