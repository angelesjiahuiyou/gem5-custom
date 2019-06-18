#!/bin/bash
mkdir -p ~/cp_data_x86
cd ~/cp_data_x86

# 453.povray
echo "453.povray"
mkdir -p 453.povray/checkpoint/test 453.povray/checkpoint/tmp_test
cd 453.povray/checkpoint/tmp_test
cp -r $SPEC/453.povray/data/all/input/* .
cp -r $SPEC/453.povray/data/test/input/* .
(time $GEM5/build/X86/gem5.opt --outdir=../test $GEM5/configs/example/se.py --cpu-type=AtomicSimpleCPU --take-simpoint-checkpoint=$BENCH_DATA/x86/453.povray/simpoint/simpoint_test,$BENCH_DATA/x86/453.povray/simpoint/weight_test,100000000,0 --output=../test/453povray.out --cmd=$SPEC/453.povray/exe/povray_base.x86 --options="SPEC-benchmark-test.ini") &> ../test/gem5.453povray.log &
cd ../../..

# 454.calculix
# ...NOPE!

# 456.hmmer
echo "456.hmmer"
mkdir -p 456.hmmer/checkpoint/test 456.hmmer/checkpoint/tmp_test
cd 456.hmmer/checkpoint/tmp_test
cp -r $SPEC/456.hmmer/data/test/input/* .
(time $GEM5/build/X86/gem5.opt --outdir=../test $GEM5/configs/example/se.py --cpu-type=AtomicSimpleCPU --take-simpoint-checkpoint=$BENCH_DATA/x86/456.hmmer/simpoint/simpoint_test,$BENCH_DATA/x86/456.hmmer/simpoint/weight_test,100000000,0 --output=../test/456hmmer.out --cmd=$SPEC/456.hmmer/exe/hmmer_base.x86 --options="--fixed 0 --mean 325 --num 45000 --sd 200 --seed 0 bombesin.hmm") &> ../test/gem5.456hmmer.log &
cd ../../..

# 458.sjeng
echo "458.sjeng"
mkdir -p 458.sjeng/checkpoint/test 458.sjeng/checkpoint/tmp_test
cd 458.sjeng/checkpoint/tmp_test
cp -r $SPEC/458.sjeng/data/test/input/* .
(time $GEM5/build/X86/gem5.opt --outdir=../test $GEM5/configs/example/se.py --cpu-type=AtomicSimpleCPU --take-simpoint-checkpoint=$BENCH_DATA/x86/458.sjeng/simpoint/simpoint_test,$BENCH_DATA/x86/458.sjeng/simpoint/weight_test,100000000,0 --output=../test/458sjeng.out --cmd=$SPEC/458.sjeng/exe/sjeng_base.x86 --options="test.txt") &> ../test/gem5.458sjeng.log &
cd ../../..

# 459.GemsFDTD
echo "459.GemsFDTD"
mkdir -p 459.GemsFDTD/checkpoint/test 459.GemsFDTD/checkpoint/tmp_test
cd 459.GemsFDTD/checkpoint/tmp_test
cp -r $SPEC/459.GemsFDTD/data/test/input/* .
(time $GEM5/build/X86/gem5.opt --outdir=../test $GEM5/configs/example/se.py --cpu-type=AtomicSimpleCPU --take-simpoint-checkpoint=$BENCH_DATA/x86/459.GemsFDTD/simpoint/simpoint_test,$BENCH_DATA/x86/459.GemsFDTD/simpoint/weight_test,100000000,0 --output=../test/459GemsFDTD.out --mem-size=4GB --cmd=$SPEC/459.GemsFDTD/exe/GemsFDTD_base.x86 ) &> ../test/gem5.459GemsFDTD.log &
cd ../../..

# 462.libquantum
echo "462.libquantum"
mkdir -p 462.libquantum/checkpoint/test 462.libquantum/checkpoint/tmp_test
cd 462.libquantum/checkpoint/tmp_test
(time $GEM5/build/X86/gem5.opt --outdir=../test $GEM5/configs/example/se.py --cpu-type=AtomicSimpleCPU --take-simpoint-checkpoint=$BENCH_DATA/x86/462.libquantum/simpoint/simpoint_test,$BENCH_DATA/x86/462.libquantum/simpoint/weight_test,100000000,0 --output=../test/462libquantum.out --cmd=$SPEC/462.libquantum/exe/libquantum_base.x86 --options="33 5") &> ../test/gem5.462libquantum.log &
cd ../../..

# 464.h264ref
echo "464.h264ref"
mkdir -p 464.h264ref/checkpoint/test 464.h264ref/checkpoint/tmp_test
cd 464.h264ref/checkpoint/tmp_test
cp -r $SPEC/464.h264ref/data/all/input/* .
cp -r $SPEC/464.h264ref/data/test/input/* .
(time $GEM5/build/X86/gem5.opt --outdir=../test $GEM5/configs/example/se.py --cpu-type=AtomicSimpleCPU --take-simpoint-checkpoint=$BENCH_DATA/x86/464.h264ref/simpoint/simpoint_test,$BENCH_DATA/x86/464.h264ref/simpoint/weight_test,100000000,0 --output=../test/464h264ref.out --cmd=$SPEC/464.h264ref/exe/h264ref_base.x86 --options="-d foreman_test_encoder_baseline.cfg") &> ../test/gem5.464h264ref.log &
cd ../../..

# 465.tonto
echo "465.tonto"
mkdir -p 465.tonto/checkpoint/test 465.tonto/checkpoint/tmp_test
cd 465.tonto/checkpoint/tmp_test
cp -r $SPEC/465.tonto/data/test/input/* .
(time $GEM5/build/X86/gem5.opt --outdir=../test $GEM5/configs/example/se.py --cpu-type=AtomicSimpleCPU --take-simpoint-checkpoint=$BENCH_DATA/x86/465.tonto/simpoint/simpoint_test,$BENCH_DATA/x86/465.tonto/simpoint/weight_test,100000000,0 --output=../test/465tonto.out --cmd=$SPEC/465.tonto/exe/tonto_base.x86 --options="< stdin") &> ../test/gem5.465tonto.log &
cd ../../..

# 470.lbm
echo "470.lbm"
mkdir -p 470.lbm/checkpoint/test 470.lbm/checkpoint/tmp_test
cd 470.lbm/checkpoint/tmp_test
cp -r $SPEC/470.lbm/data/test/input/* .
(time $GEM5/build/X86/gem5.opt --outdir=../test $GEM5/configs/example/se.py --cpu-type=AtomicSimpleCPU --take-simpoint-checkpoint=$BENCH_DATA/x86/470.lbm/simpoint/simpoint_test,$BENCH_DATA/x86/470.lbm/simpoint/weight_test,100000000,0 --output=../test/470lbm.out --cmd=$SPEC/470.lbm/exe/lbm_base.x86 --options="20 reference.dat 0 1 100_100_130_cf_a.of") &> ../test/gem5.470lbm.log &
cd ../../..

# 471.omnetpp
echo "471.omnetpp"
mkdir -p 471.omnetpp/checkpoint/test 471.omnetpp/checkpoint/tmp_test
cd 471.omnetpp/checkpoint/tmp_test
cp -r $SPEC/471.omnetpp/data/test/input/* .
(time $GEM5/build/X86/gem5.opt --outdir=../test $GEM5/configs/example/se.py --cpu-type=AtomicSimpleCPU --take-simpoint-checkpoint=$BENCH_DATA/x86/471.omnetpp/simpoint/simpoint_test,$BENCH_DATA/x86/471.omnetpp/simpoint/weight_test,100000000,0 --output=../test/471omnetpp.out --cmd=$SPEC/471.omnetpp/exe/omnetpp_base.x86 --options="omnetpp.ini") &> ../test/gem5.471omnetpp.log &
cd ../../..

# 473.astar
echo "473.astar"
mkdir -p 473.astar/checkpoint/test 473.astar/checkpoint/tmp_test
cd 473.astar/checkpoint/tmp_test
cp -r $SPEC/473.astar/data/test/input/* .
(time $GEM5/build/X86/gem5.opt --outdir=../test $GEM5/configs/example/se.py --cpu-type=AtomicSimpleCPU --take-simpoint-checkpoint=$BENCH_DATA/x86/473.astar/simpoint/simpoint_test,$BENCH_DATA/x86/473.astar/simpoint/weight_test,100000000,0 --output=../test/473astar.out --cmd=$SPEC/473.astar/exe/astar_base.x86 --options="lake.cfg") &> ../test/gem5.473astar.log &
cd ../../..

# 481.wrf
echo "481.wrf"
mkdir -p 481.wrf/checkpoint/test 481.wrf/checkpoint/tmp_test
cd 481.wrf/checkpoint/tmp_test
cp -r $SPEC/481.wrf/data/all/input/* .
cp -r $SPEC/481.wrf/data/test/input/* .
cp -r le/64/* .
(time $GEM5/build/X86/gem5.opt --outdir=../test $GEM5/configs/example/se.py --cpu-type=AtomicSimpleCPU --take-simpoint-checkpoint=$BENCH_DATA/x86/481.wrf/simpoint/simpoint_test,$BENCH_DATA/x86/481.wrf/simpoint/weight_test,100000000,0 --output=../test/481wrf.out --cmd=$SPEC/481.wrf/exe/wrf_base.x86) &> ../test/gem5.481wrf.log &
cd ../../..

# 482.sphinx3
echo "482.sphinx3"
mkdir -p 482.sphinx3/checkpoint/test 482.sphinx3/checkpoint/tmp_test
cd 482.sphinx3/checkpoint/tmp_test
cp -r $SPEC/482.sphinx3/data/all/input/* .
cp -r $SPEC/482.sphinx3/data/test/input/* .
rm *.be.raw
for file in *.le.raw
do
    mv "$file" "${file%.le.raw}.raw"
done
wc -c $(ls *.raw) | awk -F".raw" '{print $1}' | awk '{print $2 " " $1}' | head -n -1 > ctlfile
(time $GEM5/build/X86/gem5.opt --outdir=../test $GEM5/configs/example/se.py --cpu-type=AtomicSimpleCPU --take-simpoint-checkpoint=$BENCH_DATA/x86/482.sphinx3/simpoint/simpoint_test,$BENCH_DATA/x86/482.sphinx3/simpoint/weight_test,100000000,0 --output=../test/482sphinx3.out --cmd=$SPEC/482.sphinx3/exe/sphinx_livepretend_base.x86 --options="ctlfile . args.an4") &> ../test/gem5.482sphinx3.log &
cd ../../..

# 483.xalancbmk
echo "483.xalancbmk"
mkdir -p 483.xalancbmk/checkpoint/test 483.xalancbmk/checkpoint/tmp_test
cd 483.xalancbmk/checkpoint/tmp_test
cp -r $SPEC/483.xalancbmk/data/test/input/* .
(time $GEM5/build/X86/gem5.opt --outdir=../test $GEM5/configs/example/se.py --cpu-type=AtomicSimpleCPU --take-simpoint-checkpoint=$BENCH_DATA/x86/483.xalancbmk/simpoint/simpoint_test,$BENCH_DATA/x86/483.xalancbmk/simpoint/weight_test,100000000,0 --output=../test/483xalancbmk.out --cmd=$SPEC/483.xalancbmk/exe/Xalan_base.x86 --options="-v test.xml xalanc.xsl") &> ../test/gem5.483xalancbmk.log &
cd ../../..

# 998.specrand
echo "998.specrand"
mkdir -p 998.specrand/checkpoint/ref 998.specrand/checkpoint/tmp_ref
cd 998.specrand/checkpoint/tmp_ref
(time $GEM5/build/X86/gem5.opt --outdir=../ref $GEM5/configs/example/se.py --cpu-type=AtomicSimpleCPU --take-simpoint-checkpoint=$BENCH_DATA/x86/998.specrand/simpoint/simpoint_ref,$BENCH_DATA/x86/998.specrand/simpoint/weight_ref,100000000,0 --output=../ref/998specrand.out --cmd=$SPEC/998.specrand/exe/specrand_base.x86 --options="1255432124 234923") &> ../ref/gem5.998specrand.log &
cd ../../..

# 999.specrand
echo "999.specrand"
mkdir -p 999.specrand/checkpoint/ref 999.specrand/checkpoint/tmp_ref
cd 999.specrand/checkpoint/tmp_ref
(time $GEM5/build/X86/gem5.opt --outdir=../ref $GEM5/configs/example/se.py --cpu-type=AtomicSimpleCPU --take-simpoint-checkpoint=$BENCH_DATA/x86/999.specrand/simpoint/simpoint_ref,$BENCH_DATA/x86/999.specrand/simpoint/weight_ref,100000000,0 --output=../ref/999specrand.out --cmd=$SPEC/999.specrand/exe/specrand_base.x86 --options="1255432124 234923") &> ../ref/gem5.999specrand.log &
cd ../../..