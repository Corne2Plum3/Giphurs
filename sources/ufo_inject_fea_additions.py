"""
This script inject the content of src_file at the end of dst_file, both being path to text files.
"""

import os
import sys

def copy_src_content_into_dst(src_path, dst_path, mode="1"):
    """ Copy content of src_path at the end of src_dst. 
    Mode: 0 for the beginning, 1 for the end. """

    assert (mode in ["0","1"]), f"Invalid mode value '{mode}'. This can be either 0 or 1."

    # open the source file
    f_src = open(src_path, "r")

    if mode == "0":  # add lines at the beginning
        # store original content in another file
        temp_filename = "temp"
        with open(dst_path, "r") as f_dst, open(temp_filename, "a") as f_temp:
            # Write given content to the temp file
            for line in f_src:
                f_temp.write(line)
            f_temp.write("\n")
            # Read lines from original file one by one and append them to the dummy file
            for line in f_dst:
                f_temp.write(line)
        
        # remove original file
        os.remove(dst_path)
        os.rename(temp_filename, dst_path)

    else:  # add lines at the end
        with open(sys.argv[2], "a") as f_dst:  # open the dst file
            # copy each lines of FILE_SRC at the end of FILE_DST
            f_dst.write("\n\n")  # add 2 empty lines at the end
            for line in f_src:
                f_dst.write(line)
    
    f_src.close()

def main():
    # stop the program if too few arguments
    assert (len(sys.argv) >= 3), f"Too few arguments.\n  Usage: python3 {sys.argv[0]} <src_file> <dst_file> [<mode>]\n  Mode: 0 = add at the beginning ; 1 = add at the end (default)"
    
    print(f"{sys.argv[0]}: Copying content of '{sys.argv[1]}' into '{sys.argv[2]}'...")
    if(len(sys.argv) < 4):
        copy_src_content_into_dst(sys.argv[1], sys.argv[2])
    else:
        copy_src_content_into_dst(sys.argv[1], sys.argv[2], sys.argv[3])
    print(f"{sys.argv[0]}: Done.")

if __name__ == "__main__":
    main()
