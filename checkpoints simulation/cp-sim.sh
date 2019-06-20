#!/bin/bash

# Benchmark
benchmark="473.astar"
exe_name="astar_base.arm"
dataset="train"
subdata="rivers"
arguments="rivers1.cfg"
# Settings
num_cpus=1
num_banks=8

base_dir=$(pwd)
bench_dir=$BENCH_DATA/arm/$benchmark
exe_dir=$SPEC/$benchmark/exe
gem5_dir=$GEM5
mem_dir=$base_dir/mem_params
if [ ! -z "$subdata" ]
then
    data_dir=${subdata}_${dataset}
else
    data_dir=$dataset
fi

get_index() {
    index=0
    gi_value=$1
    shift
    gi_array=("$@")
    for i in "${!gi_array[@]}"; do
        if [ "${gi_array[$i]}" = "$gi_value" ]; then
            index=$i
        fi
    done
}

decode_config() {
    case $1 in
      "stt-all")
        dec_config=(1 1 1)
        ;;
      "stt-l1d")
        dec_config=(1 0 0)
        ;;
      "stt-l1d-l2")
        dec_config=(1 0 1)
        ;;
      "stt-l1i")
        dec_config=(0 1 0)
        ;;
      "stt-l2")
        dec_config=(0 0 1)
        ;;
      "stt-none")
        dec_config=(0 0 0)
        ;;
      *)
        dec_config=(0 0 0)
        ;;
    esac
}

mkdir -p simulations
cd simulations
mkdir -p $benchmark
cd $benchmark
mkdir -p $data_dir
cd $data_dir
for arch in "A7" "A15"
do
    lat_file=$mem_dir/latencies_$arch
    mkdir -p $arch
    cd $arch
    configs=("stt-all"  "stt-l1d"  "stt-l1d-l2"  "stt-l1i"  "stt-l2"  "stt-none")
    for config in "${configs[@]}"
    do
        mkdir -p $config
        cd $config
        cases=("typical" "worst")
        for case in "${cases[@]}"
        do
            # Get configuration in form of codes (0: SRAM, 1: STT-MRAM)
            decode_config $config
            # Transform configuration codes in indexes for the latency file
            get_index $case ${cases[@]}
            for i in "${!dec_config[@]}"
            do
                dec_config[$i]=$((dec_config[$i] + 1))
                if [ "${dec_config[$i]}" = "2" ]
                then
                    dec_config[$i]=$((dec_config[$i] + $index))
                fi
            done
            # Read and parse parameters from the latency file
            l1d=($(cat $lat_file | cut -d "," -f 1 | sed -n "${dec_config[0]}p" | tr '-' ' '))
            l1i=($(cat $lat_file | cut -d "," -f 1 | sed -n "${dec_config[1]}p" | tr '-' ' '))
            l2=($(cat $lat_file  | cut -d "," -f 2 | sed -n "${dec_config[2]}p" | tr '-' ' '))

            if [ "$config" != "stt-none" ] || [ "$case" = "typical" ]
            then
                mkdir -p $case
                cd $case
                sp=$(wc -l < $bench_dir/simpoint/simpoint_test)
                for cp in $(seq 1 $sp)
                do
                    mkdir -p cp$cp/tmp
                    cd cp$cp/tmp
                    ln -s $bench_dir/data/$dataset/input/* .
                    if [ -d "$bench_dir/data/all/input/" ]
                    then
                        ln -s $bench_dir/data/all/input/* .
                    fi
                    (time $gem5_dir/build/ARM/gem5.fast \
                    --outdir=.. \
                    $gem5_dir/configs/example/${arch}_multi.py \
                    --caches \
                    --l2cache \
                    --l2-enable-bank \
                    --l2-num-banks=${num_banks} \
                    --l1d-data-lat=${l1d[0]} \
                    --l1d-write-lat=${l1d[1]} \
                    --l1d-resp-lat=${l1d[2]} \
                    --l1d-tag-lat=${l1d[3]} \
                    --l1i-data-lat=${l1i[0]} \
                    --l1i-write-lat=${l1i[1]} \
                    --l1i-resp-lat=${l1i[2]} \
                    --l1i-tag-lat=${l1i[3]} \
                    --l2-data-lat=${l2[0]} \
                    --l2-write-lat=${l2[1]} \
                    --l2-resp-lat=${l2[2]} \
                    --l2-tag-lat=${l2[3]} \
                    --num-cpus=$num_cpus \
                    --maxinsts=100000000 \
                    --restore-simpoint-checkpoint \
                    --checkpoint-restore=$cp \
                    --checkpoint-dir=$bench_dir/checkpoint/$data_dir \
                    --cmd=$exe_dir/$exe_name \
                    --options="$arguments" \
                    --mem-type=NVMainMemory \
                    --nvmain-config=$mem_dir/LPDDR3_micron_512Meg_x32_qdp.config \
                    --nvmain-StatsFile=../nvmain_stats_${arch}_${config}_${case}_cp${cp}.log \
                    --nvmain-ConfigLog=../nvmain_config_${arch}_${config}_${case}_cp${cp}.log) \
                    &> ../${benchmark//./}_${arch}_${config}_${case}_cp${cp}.log &
                    cd ../..
                done
                cd ..
            fi
        done
        cd ..
    done
    cd ..
done
