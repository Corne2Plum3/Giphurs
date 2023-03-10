#!/bin/bash
set -e

# check if there's at least one argument
if [ $# -lt 1 ]
then
    echo -e $0":\x1b[1;31m Too few arguments.\x1b[0;0m"
    echo "Usage: ./build_fonts <format> [options]"
    echo "Where <format> can be: 'otf', 'ttf', 'woff2'/'webfonts' or 'all' ; and <options> ONLY ONE of the following arguments. Order is important!"
    echo "  -b : as a second argument to force (re)building sources."
    echo "  -i : idon't check UFO files. You shouldn't use it."
    exit 2
fi

# create sources if needed
case $2 in

    "-b" )  # force rebuild
        echo -e "\x1b[0;36mNew sources will be generated.\x1b[0;0m"
        USING_EXISTING_UFO=0
        ;;

    "-i" )  # ignore UFO check
        USING_EXISTING_UFO=1
        ;;

    * )  # invalid/no second argument : normal behaviour
        if [ -e ufo ]
        then
            echo -e "\x1b[0;36mufo folder found. ufo files inside them will be used.\x1b[0;0m"
            USING_EXISTING_UFO=1
        else
            echo -e "\x1b[0;36mNo ufo folder found. New sources will be generated.\x1b[0;0m"
            USING_EXISTING_UFO=0
        fi
        ;;
esac


if test $USING_EXISTING_UFO = 0
then
    ./build_sources.sh
fi

# Make font folder if needed
if [ ! -d ../fonts ]
then
    echo -e "\x1b[0;36mCreating 'fonts' folder...\x1b[0;0m"
    mkdir ../fonts
fi


# build fonts
case $1 in

    all )

        # otf + ttf + woff2
        echo -e "\x1b[0;36mThe following format will be generated: otf, ttf and woff2.\x1b[0;0m"
        ./$0 otf -i
        ./$0 ttf -i
        ./$0 woff2 -i

        ;;

    otf )

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

    ttf )

        # build ttf files
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
        echo -e "\x1b[0;36mPost-processing TTF files...\x1b[0;0m"

        TTF_LIST=$(ls ../fonts/ttf/*.ttf)
        for ttf_file in $TTF_LIST
        do
            mv $ttf_file temp
            gftools fix-nonhinting temp $ttf_file
            rm temp
        done

        echo -e "\x1b[1;32mTTF fonts has been generated with sucess! UwU\x1b[0;0m"

        ;;

    webfonts | woff2 )

        # build woff2 files by converting TTF files (woof woof)
        if [ ! -d ../fonts/ttf ]
        then  

            # NO TTF found. Ask to generate the TTF files.
            echo -e "\x1b[0;33m../fonts/ttf folder not found.\x1b[0;0m"
            echo -e "\x1b[0;33mWOFF2 webfont files are generated by using TTF files, and can't be generated if they are missing. but it seems that there isn't TTF files.\x1b[0;0m"
            
            yn=""
            while [ "$yn" != "y" ] && [ "$yn" != "n" ]
            do
                read -p "Would you like to generate the TTF files? (Y/N) " yn
                case $yn in 
                    [yY] )
                        # run the script to build ttf files
                        echo -e "TTF files will be generated first, then WOFF2 will be generated."
                        ./$0 ttf
                        ;;

                    [nN] )
                        echo -e "\x1b[1;31mCan't generate WOFF2 files without TTF files >_< !"
                        echo -e "Exiting program...\x1b[0;0m"
                        exit 1
                        ;;

                    * ) 
                        echo -e "\x1b[0;31mInvalid answer.\x1b[0;0m"
                        ;;
                esac
            done

        fi

        # really making the WOFF2 files
        echo -e "\x1b[0;36mConverting TTF files into WOFF2...\x1b[0;0m"

        rm -rf ../fonts/webfonts
        mkdir ../fonts/webfonts

        TTF_LIST=$(ls ../fonts/ttf/*.ttf)
        for ttf_file in $TTF_LIST
        do
            woff2_compress $ttf_file
        done

        # The woff2 has been generated inside the ttf folder bruh. Moving them into the right folder
        mv $(find ../fonts/ttf/*.woff2) ../fonts/webfonts/

        echo -e "\x1b[1;32mWOFF2 webfonts has been generated with sucess! UwU\x1b[0;0m"

        ;;
    
    *)

        echo -e $0":\x1b[1;31m Invalid font format '"$1"'."
        ;;

esac