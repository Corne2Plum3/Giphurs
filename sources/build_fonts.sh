#!/bin/bash
set -e

# check if there's at least one argument
if [ $# -lt 1 ]
then
    echo -e $0":\x1b[1;31m Too few arguments.\x1b[0;0m"
    echo "Usage: ./build_fonts <format>"
    echo "Where <format> can be: otf, ttf"
    echo "You can use '1' as a second argument to force (re)building sources."
    exit 2
fi

# create sources if needed
if [ $# -gt 1 ] && [ $2 = 1 ]
then 
    echo -e "\x1b[0;36mNew sources will be generated.\x1b[0;0m"
    USING_EXISTING_UFO=0
else
    echo -e "\x1b[0;36mChecking for ufo files...\x1b[0;0m"
    if [ -e ufo ]
    then
        echo -e "\x1b[0;36mufo folder found. ufo files inside them will be used.\x1b[0;0m"
        USING_EXISTING_UFO=1
    else
        echo -e "\x1b[0;36mNo ufo folder found. New sources will be generated.\x1b[0;0m"
        USING_EXISTING_UFO=0
    fi
fi


if test $USING_EXISTING_UFO = 0
then
    ./build_sources.sh
fi

# Make folders
echo -e "\x1b[0;36mInitializing fonts folder...\x1b[0;0m"

if [ ! -d ../fonts ]
then
    mkdir ../fonts
fi


# build fonts
case $1 in

    otf)

        # build otf files
        echo -e "\x1b[0;36mBuilding OTF files...\x1b[0;0m"

        rm -rf ../fonts/otf
        mkdir ../fonts/otf

        UFO_LIST=$(ls ufo)
        for ufo_file in $UFO_LIST
        do
            fontmake -u "ufo/"${ufo_file} -o otf --output-dir ../fonts/otf
            echo -e "\x1b[0;32m ../fonts/otf/"$ufo_file" generated!\x1b[0;0m"
        done

        # post-processing
        echo -e "\x1b[0;36mPost-processing OTF files...\x1b[0;0m"

        OTF_LIST=$(ls ../fonts/otf/*.otf)
        for otf_file in $OTF_LIST
        do
            mv $otf_file temp
            gftools fix-nonhinting temp $otf_file
            rm temp
        done

        echo -e "\x1b[1;32mOTF fonts has been generated with sucess! UwU\x1b[0;0m"

        ;;

    ttf)

        # build otf files
        echo -e "\x1b[0;36mBuilding TTF files...\x1b[0;0m"

        rm -rf ../fonts/ttf
        mkdir ../fonts/ttf

        UFO_LIST=$(ls ufo)
        for ufo_file in $UFO_LIST
        do
            fontmake -u "ufo/"${ufo_file} -o ttf --output-dir ../fonts/ttf
            echo -e "\x1b[0;32m ../fonts/ttf/"$ufo_file" generated!\x1b[0;0m"
        done

        # post-processing
        echo -e "\x1b[0;36mPost-processing OTF files...\x1b[0;0m"

        TTF_LIST=$(ls ../fonts/ttf/*.ttf)
        for ttf_file in $TTF_LIST
        do
            mv $ttf_file temp
            gftools fix-nonhinting temp $ttf_file
            rm temp
        done

        echo -e "\x1b[1;32mTTF fonts has been generated with sucess! UwU\x1b[0;0m"

        ;;

    
    *)

        echo -e $0":\x1b[1;31m Invalid font format '"$1"'."
        ;;

esac