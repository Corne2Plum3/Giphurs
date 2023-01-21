#!/bin/bash
set -e

# don't forget the '/' at the end!
SFD_DIR="sfd/"  # where the sfd source files are

SFD_LIST=$(ls $SFD_DIR)

# initialisation: set python stuff
echo -e "\x1b[0;36mSetting up Python environnement...\x1b[0;0m"
export PYTHONV=$(python3 -c 'import sys; v=sys.version_info; print(f"python{v.major}.{v.minor}")')
export PYTHONPATH="py/local/lib/$PYTHONV/dist-packages:$(python3 -c "import sys; print(':'.join(sys.path)[1:])")"
if [ ! -d py ]; then
  pip install -U --prefix=py git+https://github.com/MFEK/sfdLib.py
fi

# make the folder to work in
rm -rf sfd_cleaned
mkdir sfd_cleaned
rm -rf ufo
mkdir ufo

echo -e "\x1b[0;36mBuilding the sources...\x1b[0;0m"

for sfd_file in $SFD_LIST
do
    # Clean the SFD file
    sfd_temp="sfd_cleaned/"${sfd_file%.*}"_temp.sfd"
    python3 fontforge_cleanup.py $SFD_DIR$sfd_file $sfd_temp

    # Convert to UFO
    ufo_file="ufo/"${sfd_file%.*}
    python3 -m sfdLib --ufo-kerning --ufo-anchors $sfd_temp $ufo_file

    echo -e "\x1b[0;32m"$ufo_file" has been generated.\x1b[0;0m"
done

echo -e "\x1b[0;32mAll sources has been generated succesfully! ^^\x1b[0;0m"