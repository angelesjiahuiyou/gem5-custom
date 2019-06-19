#!/bin/bash
mkdir -p ~/cp_data_arm
cd ~/cp_data_arm

# 453.povray
#echo "453.povray"
#mkdir -p 453.povray/checkpoint/train 453.povray/checkpoint/tmp_train
#cd 453.povray/checkpoint/tmp_train
#cp -r $SPEC/453.povray/data/all/input/* .
#cp -r $SPEC/453.povray/data/train/input/* .
#(time $GEM5/build/ARM/gem5.opt --outdir=../train $GEM5/configs/example/se.py --cpu-type=AtomicSimpleCPU --take-simpoint-checkpoint=$BENCH_DATA/arm/453.povray/simpoint/simpoint_train,$BENCH_DATA/arm/453.povray/simpoint/weight_train,100000000,0 --output=../train/povray.out --cmd=$SPEC/453.povray/exe/povray_base.arm --options="SPEC-benchmark-train.ini") &> ../train/gem5.453povray.log &
#cd ../../..

# 454.calculix
echo "454.calculix"
mkdir -p 454.calculix/checkpoint/train 454.calculix/checkpoint/tmp_train
cd 454.calculix/checkpoint/tmp_train
cp -r $SPEC/454.calculix/data/train/input/* .
(time $GEM5/build/ARM/gem5.opt --outdir=../train $GEM5/configs/example/se.py --cpu-type=AtomicSimpleCPU --take-simpoint-checkpoint=$BENCH_DATA/arm/454.calculix/simpoint/simpoint_train,$BENCH_DATA/arm/454.calculix/simpoint/weight_train,100000000,0 --output=../train/454calculix.out --cmd=$SPEC/454.calculix/exe/calculix_base.arm --options="-i stairs") &> ../train/gem5.454calculix.log &
cd ../../..

# 456.hmmer
echo "456.hmmer"
mkdir -p 456.hmmer/checkpoint/train 456.hmmer/checkpoint/tmp_train
cd 456.hmmer/checkpoint/tmp_train
cp -r $SPEC/456.hmmer/data/train/input/* .
(time $GEM5/build/ARM/gem5.opt --outdir=../train $GEM5/configs/example/se.py --cpu-type=AtomicSimpleCPU --take-simpoint-checkpoint=$BENCH_DATA/arm/456.hmmer/simpoint/simpoint_train,$BENCH_DATA/arm/456.hmmer/simpoint/weight_train,100000000,0 --output=../train/456hmmer.out --cmd=$SPEC/456.hmmer/exe/hmmer_base.arm --options="--fixed 0 --mean 425 --num 85000 --sd 300 --seed 0 leng100.hmm") &> ../train/gem5.456hmmer.log &
cd ../../..

# 458.sjeng
echo "458.sjeng"
mkdir -p 458.sjeng/checkpoint/train 458.sjeng/checkpoint/tmp_train
cd 458.sjeng/checkpoint/tmp_train
cp -r $SPEC/458.sjeng/data/train/input/* .
(time $GEM5/build/ARM/gem5.opt --outdir=../train $GEM5/configs/example/se.py --cpu-type=AtomicSimpleCPU --take-simpoint-checkpoint=$BENCH_DATA/arm/458.sjeng/simpoint/simpoint_train,$BENCH_DATA/arm/458.sjeng/simpoint/weight_train,100000000,0 --output=../train/458sjeng.out --cmd=$SPEC/458.sjeng/exe/sjeng_base.arm --options="train.txt") &> ../train/gem5.458sjeng.log &
cd ../../..

# 459.GemsFDTD
echo "459.GemsFDTD"
mkdir -p 459.GemsFDTD/checkpoint/train 459.GemsFDTD/checkpoint/tmp_train
cd 459.GemsFDTD/checkpoint/tmp_train
cp -r $SPEC/459.GemsFDTD/data/train/input/* .
(time $GEM5/build/ARM/gem5.opt --outdir=../train $GEM5/configs/example/se.py --cpu-type=AtomicSimpleCPU --take-simpoint-checkpoint=$BENCH_DATA/arm/459.GemsFDTD/simpoint/simpoint_train,$BENCH_DATA/arm/459.GemsFDTD/simpoint/weight_train,100000000,0 --output=../train/459GemsFDTD.out --mem-size=4GB --cmd=$SPEC/459.GemsFDTD/exe/GemsFDTD_base.arm ) &> ../train/gem5.459GemsFDTD.log &
cd ../../..

# 462.libquantum
echo "462.libquantum"
mkdir -p 462.libquantum/checkpoint/train 462.libquantum/checkpoint/tmp_train
cd 462.libquantum/checkpoint/tmp_train
(time $GEM5/build/ARM/gem5.opt --outdir=../train $GEM5/configs/example/se.py --cpu-type=AtomicSimpleCPU --take-simpoint-checkpoint=$BENCH_DATA/arm/462.libquantum/simpoint/simpoint_train,$BENCH_DATA/arm/462.libquantum/simpoint/weight_train,100000000,0 --output=../train/462libquantum.out --cmd=$SPEC/462.libquantum/exe/libquantum_base.arm --options="143 25") &> ../train/gem5.462libquantum.log &
cd ../../..

# 464.h264ref
echo "464.h264ref"
mkdir -p 464.h264ref/checkpoint/train 464.h264ref/checkpoint/tmp_train
cd 464.h264ref/checkpoint/tmp_train
cp -r $SPEC/464.h264ref/data/all/input/* .
cp -r $SPEC/464.h264ref/data/train/input/* .
(time $GEM5/build/ARM/gem5.opt --outdir=../train $GEM5/configs/example/se.py --cpu-type=AtomicSimpleCPU --take-simpoint-checkpoint=$BENCH_DATA/arm/464.h264ref/simpoint/simpoint_train,$BENCH_DATA/arm/464.h264ref/simpoint/weight_train,100000000,0 --output=../train/464h264ref.out --cmd=$SPEC/464.h264ref/exe/h264ref_base.arm --options="-d foreman_train_encoder_baseline.cfg") &> ../train/gem5.464h264ref.log &
cd ../../..

# 465.tonto
#echo "465.tonto"
#mkdir -p 465.tonto/checkpoint/train 465.tonto/checkpoint/tmp_train
#cd 465.tonto/checkpoint/tmp_train
#cp -r $SPEC/465.tonto/data/train/input/* .
#(time $GEM5/build/ARM/gem5.opt --outdir=../train $GEM5/configs/example/se.py --cpu-type=AtomicSimpleCPU --take-simpoint-checkpoint=$BENCH_DATA/arm/465.tonto/simpoint/simpoint_train,$BENCH_DATA/arm/465.tonto/simpoint/weight_train,100000000,0 --output=../train/465tonto.out --mem-size=64GB --cmd=$SPEC/465.tonto/exe/tonto_base.arm --options="< stdin") &> ../train/gem5.465tonto.log &
#cd ../../..

# 470.lbm
echo "470.lbm"
mkdir -p 470.lbm/checkpoint/train 470.lbm/checkpoint/tmp_train
cd 470.lbm/checkpoint/tmp_train
cp -r $SPEC/470.lbm/data/train/input/* .
(time $GEM5/build/ARM/gem5.opt --outdir=../train $GEM5/configs/example/se.py --cpu-type=AtomicSimpleCPU --take-simpoint-checkpoint=$BENCH_DATA/arm/470.lbm/simpoint/simpoint_train,$BENCH_DATA/arm/470.lbm/simpoint/weight_train,100000000,0 --output=../train/470lbm.out --cmd=$SPEC/470.lbm/exe/lbm_base.arm --options="300 reference.dat 0 1 100_100_130_cf_b.of") &> ../train/gem5.470lbm.log &
cd ../../..

# 471.omnetpp
echo "471.omnetpp"
mkdir -p 471.omnetpp/checkpoint/train 471.omnetpp/checkpoint/tmp_train
cd 471.omnetpp/checkpoint/tmp_train
cp -r $SPEC/471.omnetpp/data/train/input/* .
(time $GEM5/build/ARM/gem5.opt --outdir=../train $GEM5/configs/example/se.py --cpu-type=AtomicSimpleCPU --take-simpoint-checkpoint=$BENCH_DATA/arm/471.omnetpp/simpoint/simpoint_train,$BENCH_DATA/arm/471.omnetpp/simpoint/weight_train,100000000,0 --output=../train/471omnetpp.out --cmd=$SPEC/471.omnetpp/exe/omnetpp_base.arm --options="omnetpp.ini") &> ../train/gem5.471omnetpp.log &
cd ../../..

# 473.astar
echo "473.astar"
mkdir -p 473.astar/checkpoint/gem5_gen_BigLakes1024_train 473.astar/checkpoint/gem5_gen_rivers_train 473.astar/checkpoint/tmp_train
cd 473.astar/checkpoint/tmp_train
cp -r $SPEC/473.astar/data/train/input/* .
(time $GEM5/build/ARM/gem5.opt --outdir=../gem5_gen_BigLakes1024_train $GEM5/configs/example/se.py --cpu-type=AtomicSimpleCPU --take-simpoint-checkpoint=$BENCH_DATA/arm/473.astar/simpoint/simpoint_BigLakes1024_train,$BENCH_DATA/arm/473.astar/simpoint/weight_BigLakes1024_train,100000000,0 --output=../gem5_gen_BigLakes1024_train/473astar.out --cmd=$SPEC/473.astar/exe/astar_base.arm --options="BigLakes1024.cfg") &> ../gem5_gen_BigLakes1024_train/gem5.473astar.log &
(time $GEM5/build/ARM/gem5.opt --outdir=../gem5_gen_rivers_train $GEM5/configs/example/se.py --cpu-type=AtomicSimpleCPU --take-simpoint-checkpoint=$BENCH_DATA/arm/473.astar/simpoint/simpoint_rivers_train,$BENCH_DATA/arm/473.astar/simpoint/weight_rivers_train,100000000,0 --output=../gem5_gen_rivers_train/473astar.out --cmd=$SPEC/473.astar/exe/astar_base.arm --options="rivers1.cfg") &> ../gem5_gen_rivers_train/gem5.473astar.log &
cd ../../..

# 481.wrf
#echo "481.wrf"
#mkdir -p 481.wrf/checkpoint/train 481.wrf/checkpoint/tmp_train
#cd 481.wrf/checkpoint/tmp_train
#cp -r $SPEC/481.wrf/data/all/input/* .
#cp -r $SPEC/481.wrf/data/train/input/* .
#cp -r le/32/* .
#(time $GEM5/build/ARM/gem5.opt --outdir=../train $GEM5/configs/example/se.py --cpu-type=AtomicSimpleCPU --take-simpoint-checkpoint=$BENCH_DATA/arm/481.wrf/simpoint/simpoint_train,$BENCH_DATA/arm/481.wrf/simpoint/weight_train,100000000,0 --output=../train/481wrf.out --mem-size=64GB --cmd=$SPEC/481.wrf/exe/wrf_base.arm) &> ../train/gem5.481wrf.log &
#cd ../../..

# 482.sphinx3
echo "482.sphinx3"
mkdir -p 482.sphinx3/checkpoint/train 482.sphinx3/checkpoint/tmp_train
cd 482.sphinx3/checkpoint/tmp_train
cp -r $SPEC/482.sphinx3/data/all/input/* .
cp -r $SPEC/482.sphinx3/data/train/input/* .
rm *.be.raw
for file in *.le.raw
do
    mv "$file" "${file%.le.raw}.raw"
done
wc -c $(ls *.raw) | awk -F".raw" '{print $1}' | awk '{print $2 " " $1}' | head -n -1 > ctlfile
(time $GEM5/build/ARM/gem5.opt --outdir=../train $GEM5/configs/example/se.py --cpu-type=AtomicSimpleCPU --take-simpoint-checkpoint=$BENCH_DATA/arm/482.sphinx3/simpoint/simpoint_train,$BENCH_DATA/arm/482.sphinx3/simpoint/weight_train,100000000,0 --output=../train/482sphinx3.out --cmd=$SPEC/482.sphinx3/exe/sphinx_livepretend_base.arm --options="ctlfile . args.an4") &> ../train/gem5.482sphinx3.log &
cd ../../..

# 483.xalancbmk
echo "483.xalancbmk"
mkdir -p 483.xalancbmk/checkpoint/train 483.xalancbmk/checkpoint/tmp_train
cd 483.xalancbmk/checkpoint/tmp_train
cp -r $SPEC/483.xalancbmk/data/train/input/* .
(time $GEM5/build/ARM/gem5.opt --outdir=../train $GEM5/configs/example/se.py --cpu-type=AtomicSimpleCPU --take-simpoint-checkpoint=$BENCH_DATA/arm/483.xalancbmk/simpoint/simpoint_train,$BENCH_DATA/arm/483.xalancbmk/simpoint/weight_train,100000000,0 --output=../train/483xalancbmk.out --cmd=$SPEC/483.xalancbmk/exe/Xalan_base.arm --options="-v allbooks.xml xalanc.xsl") &> ../train/gem5.483xalancbmk.log &
cd ../../..
