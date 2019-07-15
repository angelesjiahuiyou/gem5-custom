#!/bin/bash

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
        exit 1
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
    exit 1
fi
