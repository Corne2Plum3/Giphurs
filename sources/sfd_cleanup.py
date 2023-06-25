"""
This script create a copy of a .sfd file where some issues that may affects the conversion to
UFO file and also visuals issues on the finished font.
"""

import fontforge
import shutil
import sys

def clean_sfd(sfd_source, sfd_dest):
    # copy file
    shutil.copy(sfd_source, sfd_dest)
    
    # Open the font
    font = fontforge.open(sfd_dest) 

    # corrections
    font.selection.all()  # select all glyphs

    font.simplify()
    font.round()
    font.removeOverlap()
    font.correctDirection()
    font.simplify()

    # save
    font.save(sfd_dest)

def main():
    assert (len(sys.argv) >= 3), f"{sys.argv[0]}: Too few arguments.\nUsage: python3 {sys.argv[0]} <sfd_source> <sfd_dest>"

    print(f"{sys.argv[0]}: Starting cleaning of {sys.argv[1]} into {sys.argv[2]}")
    clean_sfd(sys.argv[1], sys.argv[2])
    print(f"{sys.argv[0]}: Done.")

if __name__ == "__main__":
    main()
