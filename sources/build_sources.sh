#!/bin/bash
set -e

COMPILATION_START_TIME=$(date +%s)  # when the compilation started

# don't forget the '/' at the end!
SFD_DIR="sfd/"  # where the sfd source files are
SFD_LIST=$(ls $SFD_DIR)  # list of all files inside SFD_DIR

# make the folder to work in
rm -rf sfd_cleaned
mkdir sfd_cleaned
rm -rf ufo
mkdir ufo

echo -e "\x1b[0;36mBuilding the sources...\x1b[0;0m"

# build the ufo files from sfd
for sfd_file in $SFD_LIST
do
    # Clean the SFD file
    sfd_temp="sfd_cleaned/"${sfd_file%.*}"_temp.sfd"
    python3 sfd_cleanup.py $SFD_DIR$sfd_file $sfd_temp

    # Convert to UFO
    ufo_file="ufo/"${sfd_file%.*}".ufo"
    python3 -m sfdLib --ufo-kerning --ufo-anchors $sfd_temp $ufo_file

    # Apply some modifications to the UFO
    python3 ufo_force_flatten_components.py $ufo_file
    python3 ufo_add_stylistic_sets_descriptions_from_sfd.py $ufo_file $SFD_DIR/$sfd_file
    python3 ufo_inject_fea_additions.py "features_additions_beginning.fea" $ufo_file/features.fea 0
    python3 ufo_inject_fea_additions.py "features_additions_end.fea" $ufo_file/features.fea 1

    echo -e "\x1b[0;32m"$ufo_file" has been generated.\x1b[0;0m"
done

# sucess message
COMPILATION_END_TIME=$(date +%s)  # when the compilation finished
COMPILATION_DURATION=$(($COMPILATION_END_TIME-$COMPILATION_START_TIME))
echo -e "\x1b[1;32mAll ufo sources has been generated succesfully in "$COMPILATION_DURATION" second(s) ^^\x1b[0;0m"
