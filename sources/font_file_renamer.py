"""
Standardize the font file name (suc     cv,nvvbvbvxx"FontName-Weight 
"""

import os
import sys
import pathlib

weight_names = {
    "100": "Thin",
    "200": "ExtraLight",
    "300": "Light",
    "400": "Regular",
    "500": "Medium",
    "600": "SemiBold",
    "700": "Bold",
    "800": "ExtraBold",
    "900": "Black"
}

if len(sys.argv) < 4:  # too few arguments
    print(f"{sys.argv[0]}: Too few arguments.\nUsage: python3 {sys.argv[0]} <file> <font_family_name> <weight>")

else:
    if sys.argv[3] in weight_names.keys():
        file_ext = pathlib.Path(sys.argv[1]).suffix
        new_name = f"{sys.argv[2]}-{weight_names[sys.argv[3]]}{file_ext}"
        os.rename(sys.argv[1], new_name)
    else:
        print(f"{sys.argv[0]}: Invalid weight '{sys.argv[3]}'")