#!/bin/bash

function process_dir {
    cur_dir=${PWD##*/}
    cur_dir="${cur_dir//.}"

    if [ -d "valgrind" ]
    then
        # create the simpoint folder if not present
        if [ ! -d "simpoint" ]
        then
            mkdir "simpoint"
        fi

        # generate BBV file list
        file_list=$(ls valgrind | grep bb.out.$cur_dir)
        if [ $(echo $file_list | wc -w) == 0 ]
        then
            echo "No BBV file found in valgrind directory"
            return 1
        fi

        # process BBV files
        for bbv_file in $file_list
        do
            if [ $(sed '/^[[:blank:]]*#/d;s/#.*//' valgrind/$bbv_file | wc -w) == 0 ]
            then
                printf '%s\n' "The file $bbv_file is empty! Skipping..."
            else
                name=${bbv_file#bb.out.$cur_dir.}
                name=${name//./_}
                simpoint -loadFVFile valgrind/$bbv_file -maxK 30 -saveSimpoints simpoint/simpoint_$name -saveSimpointWeights simpoint/weight_$name > simpoint/simpoint_creation_$name
                echo "SimPoints successfully generated from file $bbv_file"
            fi
        done
    else
        echo "Missing valgrind folder"
        return 1
    fi
}

if [ "$1" == "-a" ]
then
    if [ -z $2 ] || [ ! -d $2 ]
    then
        echo "Directory not set or badly set!"
        exit 1
    fi
    for f in $(ls -d $2/*/)
    do
	echo "-- $(basename $f) --"
        cd $f
        process_dir
    done
elif [ "$1" == "-d" ]
then
    if [ -z $2 ] || [ ! -d $2 ]
    then
        echo "Directory not set or badly set!"
	exit 1
    fi
    cd $2
    process_dir
elif [ "$1" == "-t" ]
then
    process_dir
else
    echo "Usage:      sp-gen.sh <option>"
    echo
    echo "Options:"
    echo "-t :        'This', process current folder"
    echo "-d <path>:  'Dir',  process given folder"
    echo "-a <path> : 'All',  process all the subfolders in a given path"
fi

