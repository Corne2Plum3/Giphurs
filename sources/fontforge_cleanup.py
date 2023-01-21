"""
This script create a copy of a .sfd file where some issues that may affects the conversion to
UFO file and also visuals issues on the finished font.
"""

import fontforge
import shutil
import sys


if len(sys.argv) < 3:  # too few arguments
    print(f"{sys.argv[0]}: Too few arguments.\nUsage: python3 {sys.argv[0]} <sfd_source> <sfd_dest>")

else:

    sfd_source = sys.argv[1]
    sfd_dest = sys.argv[2]

    # copy file
    shutil.copy(sfd_source, sfd_dest)
    print(f"Starting cleanup of .sfd file '{sfd_dest}'...")

    font = fontforge.open(sfd_dest)  # Open the font

    # corrections
    font.selection.all()  # select all glyphs

    font.simplify()
    font.round()
    font.removeOverlap()
    font.correctDirection()

    # save
    font.save(sfd_dest)

    print(f"Finished cleaning {sfd_source} on {sfd_dest}.")
