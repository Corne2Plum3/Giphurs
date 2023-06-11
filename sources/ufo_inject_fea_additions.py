"""
This script inject the content of src_file at the end of dst_file, both being path to text files.
"""

import sys

def copy_src_content_into_dst(src_path, src_dst):
    """ Copy content of src_path at the end of src_dst. """

    # open the files
    f_src = open(sys.argv[1], "r")
    f_dst = open(sys.argv[2], "a")

    # copy each lines of FILE_SRC at the end of FILE_DST
    f_dst.write("\n\n")  # add 2 empty lines at the end
    for line in f_src:
        f_dst.write(line)

    # close the files
    f_src.close()
    f_dst.close()

def main():
    # stop the program if too few arguments
    assert (len(sys.argv) >= 2), f"Too few arguments.\n  Usage: python3 {sys.argv[0]} <src_file> <dst_file>"
    
    print(f"{sys.argv[0]}: Copying content of '{sys.argv[1]}' into '{sys.argv[2]}'...")
    copy_src_content_into_dst(sys.argv[1], sys.argv[2])
    print(f"{sys.argv[0]}: Done.")

if __name__ == "__main__":
    main()