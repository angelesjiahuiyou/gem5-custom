#!/bin/bash
mkdir -p ~/cp_data_x86
cd ~/cp_data_x86

# 400.perlbench
echo "400.perlbench"
mkdir -p 400.perlbench/checkpoint/{makerand,pack,tmp}_test
cd 400.perlbench/checkpoint/tmp_test
ln -s $SPEC/400.perlbench/data/all/input/* .
ln -s $SPEC/400.perlbench/data/test/input/* .
(time $GEM5/build/X86/gem5.fast --outdir=../makerand_test $GEM5/configs/example/se.py --cpu-type=AtomicSimpleCPU --take-simpoint-checkpoint=$BENCH_DATA/x86/400.perlbench/simpoint/simpoint_makerand_test,$BENCH_DATA/x86/400.perlbench/simpoint/weight_makerand_test,100000000,0 --output=../makerand_test/400perlbench.out --cmd=$SPEC/400.perlbench/exe/perlbench_base.x86 --options="-I. -I./lib makerand.pl") &> ../makerand_test/gem5.400perlbench.log &
(time $GEM5/build/X86/gem5.fast --outdir=../pack_test $GEM5/configs/example/se.py --cpu-type=AtomicSimpleCPU --take-simpoint-checkpoint=$BENCH_DATA/x86/400.perlbench/simpoint/simpoint_pack_test,$BENCH_DATA/x86/400.perlbench/simpoint/weight_pack_test,100000000,0 --output=../pack_test/400perlbench.out --cmd=$SPEC/400.perlbench/exe/perlbench_base.x86 --options="-I. -I./lib pack.pl") &> ../pack_test/gem5.400perlbench.log &
cd ../../..

# 401.bzip2
echo "401.bzip2"
mkdir -p 401.bzip2/checkpoint/{dryer_2,input_program_5,tmp}_test
cd 401.bzip2/checkpoint/tmp_test
ln -s $SPEC/401.bzip2/data/all/input/* .
ln -s $SPEC/401.bzip2/data/test/input/* .
(time $GEM5/build/X86/gem5.fast --outdir=../dryer_2_test $GEM5/configs/example/se.py --cpu-type=AtomicSimpleCPU --take-simpoint-checkpoint=$BENCH_DATA/x86/401.bzip2/simpoint/simpoint_dryer_2_test,$BENCH_DATA/x86/401.bzip2/simpoint/weight_dryer_2_test,100000000,0 --output=../dryer_2_test/401bzip.out --cmd=$SPEC/401.bzip2/exe/bzip2_base.x86 --options="dryer.jpg 2") &> ../dryer_2_test/gem5.401bzip2.log &
(time $GEM5/build/X86/gem5.fast --outdir=../input_program_5_test $GEM5/configs/example/se.py --cpu-type=AtomicSimpleCPU --take-simpoint-checkpoint=$BENCH_DATA/x86/401.bzip2/simpoint/simpoint_input_program_5_test,$BENCH_DATA/x86/401.bzip2/simpoint/weight_input_program_5_test,100000000,0 --output=../input_program_5_test/401bzip.out --cmd=$SPEC/401.bzip2/exe/bzip2_base.x86 --options="input.program 5") &> ../input_program_5_test/gem5.401bzip2.log &
cd ../../..

# 403.gcc
echo "403.gcc"
mkdir -p 403.gcc/checkpoint/{test,tmp_test}
cd 403.gcc/checkpoint/tmp_test
ln -s $SPEC/403.gcc/data/test/input/* .
(time $GEM5/build/X86/gem5.fast --outdir=../test $GEM5/configs/example/se.py --cpu-type=AtomicSimpleCPU --take-simpoint-checkpoint=$BENCH_DATA/x86/403.gcc/simpoint/simpoint_test,$BENCH_DATA/x86/403.gcc/simpoint/weight_test,100000000,0 --output=../test/403gcc.out --cmd=$SPEC/403.gcc/exe/gcc_base.x86 --options="cccp.in -o cccp.s") &> ../test/gem5.403gcc.log &
cd ../../..

# 410.bwaves
echo "410.bwaves"
mkdir -p 410.bwaves/checkpoint/{test,tmp_test}
cd 410.bwaves/checkpoint/tmp_test
ln -s $SPEC/410.bwaves/data/test/input/* .
(time $GEM5/build/X86/gem5.fast --outdir=../test $GEM5/configs/example/se.py --cpu-type=AtomicSimpleCPU --take-simpoint-checkpoint=$BENCH_DATA/x86/410.bwaves/simpoint/simpoint_test,$BENCH_DATA/x86/410.bwaves/simpoint/weight_test,100000000,0 --output=../test/410bwaves.out --cmd=$SPEC/410.bwaves/exe/bwaves_base.x86 --options="bwaves.in") &> ../test/gem5.410bwaves.log &
cd ../../..

# 416.gamess
#echo "416.gamess"
#mkdir -p 416.gamess/checkpoint/{test,tmp_test}
#cd 416.gamess/checkpoint/tmp_test
#ln -s $SPEC/416.gamess/data/test/input/* .
#(time $GEM5/build/X86/gem5.fast --outdir=../test $GEM5/configs/example/se.py --cpu-type=AtomicSimpleCPU --take-simpoint-checkpoint=$BENCH_DATA/x86/416.gamess/simpoint/simpoint_test,$BENCH_DATA/x86/416.gamess/simpoint/weight_test,100000000,0 --output=../test/416gamess.out --mem-size=2GB --cmd=$SPEC/416.gamess/exe/gamess_base.x86 --input="exam29.config") &> ../test/gem5.416gamess.log &
#cd ../../..

# 429.mcf
echo "429.mcf"
mkdir -p 429.mcf/checkpoint/{test,tmp_test}
cd 429.mcf/checkpoint/tmp_test
ln -s $SPEC/429.mcf/data/test/input/* .
(time $GEM5/build/X86/gem5.fast --outdir=../test $GEM5/configs/example/se.py --cpu-type=AtomicSimpleCPU --take-simpoint-checkpoint=$BENCH_DATA/x86/429.mcf/simpoint/simpoint_test,$BENCH_DATA/x86/429.mcf/simpoint/weight_test,100000000,0 --output=../test/429mcf.out --cmd=$SPEC/429.mcf/exe/mcf_base.x86 --options="inp.in") &> ../test/gem5.429mcfb.log &
cd ../../..

# 433.milc
echo "433.milc"
mkdir -p 433.milc/checkpoint/{test,tmp_test}
cd 433.milc/checkpoint/tmp_test
ln -s $SPEC/433.milc/data/test/input/* .
(time $GEM5/build/X86/gem5.fast --outdir=../test $GEM5/configs/example/se.py --cpu-type=AtomicSimpleCPU --take-simpoint-checkpoint=$BENCH_DATA/x86/433.milc/simpoint/simpoint_test,$BENCH_DATA/x86/433.milc/simpoint/weight_test,100000000,0 --output=../test/433milc.out --cmd=$SPEC/433.milc/exe/milc_base.x86 --input="su3imp.in") &> ../test/gem5.429mcf.log &
cd ../../..

# 434.zeusmp
echo "434.zeusmp"
mkdir -p 434.zeusmp/checkpoint/{test,tmp_test}
cd 434.zeusmp/checkpoint/tmp_test
ln -s $SPEC/434.zeusmp/data/test/input/* .
(time $GEM5/build/X86/gem5.fast --outdir=../test $GEM5/configs/example/se.py --cpu-type=AtomicSimpleCPU --take-simpoint-checkpoint=$BENCH_DATA/x86/434.zeusmp/simpoint/simpoint_test,$BENCH_DATA/x86/434.zeusmp/simpoint/weight_test,100000000,0 --output=../test/434zeusmp.out --mem-size=2GB --cmd=$SPEC/434.zeusmp/exe/zeusmp_base.x86) &> ../test/gem5.434zeusmp.log &
cd ../../..

# 435.gromacs
echo "435.gromacs"
mkdir -p 435.gromacs/checkpoint/{test,tmp_test}
cd 435.gromacs/checkpoint/tmp_test
ln -s $SPEC/435.gromacs/data/test/input/* .
(time $GEM5/build/X86/gem5.fast --outdir=../test $GEM5/configs/example/se.py --cpu-type=AtomicSimpleCPU --take-simpoint-checkpoint=$BENCH_DATA/x86/435.gromacs/simpoint/simpoint_test,$BENCH_DATA/x86/435.gromacs/simpoint/weight_test,100000000,0 --output=../test/435gromacs.out --cmd=$SPEC/435.gromacs/exe/gromacs_base.x86 --options="-silent -deffnm gromacs -nice 0") &> ../test/gem5.435gromacs.log &
cd ../../..

# 436.cactusADM
echo "436.cactusADM"
mkdir -p 436.cactusADM/checkpoint/{test,tmp_test}
cd 436.cactusADM/checkpoint/tmp_test
ln -s $SPEC/436.cactusADM/data/test/input/* .
(time $GEM5/build/X86/gem5.fast --outdir=../test $GEM5/configs/example/se.py --cpu-type=AtomicSimpleCPU --take-simpoint-checkpoint=$BENCH_DATA/x86/436.cactusADM/simpoint/simpoint_test,$BENCH_DATA/x86/436.cactusADM/simpoint/weight_test,100000000,0 --output=../test/436cactusADM.out --cmd=$SPEC/436.cactusADM/exe/cactusADM_base.x86 --options="benchADM.par") &> ../test/gem5.436cactusADM.log &
cd ../../..

# 437.leslie3d
echo "437.leslie3d"
mkdir -p 437.leslie3d/checkpoint/{test,tmp_test}
cd 437.leslie3d/checkpoint/tmp_test
ln -s $SPEC/437.leslie3d/data/test/input/* .
(time $GEM5/build/X86/gem5.fast --outdir=../test $GEM5/configs/example/se.py --cpu-type=AtomicSimpleCPU --take-simpoint-checkpoint=$BENCH_DATA/x86/437.leslie3d/simpoint/simpoint_test,$BENCH_DATA/x86/437.leslie3d/simpoint/weight_test,100000000,0 --output=../test/437leslie3d.out --cmd=$SPEC/437.leslie3d/exe/leslie3d_base.x86 --input="leslie3d.in") &> ../test/gem5.437leslie3d.log &
cd ../../..

# 444.namd
echo "444.namd"
mkdir -p 444.namd/checkpoint/{test,tmp_test}
cd 444.namd/checkpoint/tmp_test
ln -s $SPEC/444.namd/data/all/input/* .
ln -s $SPEC/444.namd/data/test/input/* .
(time $GEM5/build/X86/gem5.fast --outdir=../test $GEM5/configs/example/se.py --cpu-type=AtomicSimpleCPU --take-simpoint-checkpoint=$BENCH_DATA/x86/444.namd/simpoint/simpoint_test,$BENCH_DATA/x86/444.namd/simpoint/weight_test,100000000,0 --output=../test/444namd.out --cmd=$SPEC/444.namd/exe/namd_base.x86 --options="--input namd.input --iterations 1 --output ../test/namd.out") &> ../test/gem5.444namd.log &
cd ../../..

# 445.gobmk
echo "445.gobmk"
mkdir -p 445.gobmk/checkpoint/{capture,connection,connect,cutstone,dniwog,tmp}_test
cd 445.gobmk/checkpoint/tmp_test
ln -s $SPEC/445.gobmk/data/all/input/* .
ln -s $SPEC/445.gobmk/data/test/input/* .
(time $GEM5/build/X86/gem5.fast --outdir=../capture_test $GEM5/configs/example/se.py --cpu-type=AtomicSimpleCPU --take-simpoint-checkpoint=$BENCH_DATA/x86/445.gobmk/simpoint/simpoint_capture_test,$BENCH_DATA/x86/445.gobmk/simpoint/weight_capture_test,100000000,0 --output=../capture_test/445gobmk.out --cmd=$SPEC/445.gobmk/exe/gobmk_base.x86 --options="--quiet --mode gtp" --input="capture.tst") &> ../capture_test/gem5.445gobmk.log &
(time $GEM5/build/X86/gem5.fast --outdir=../connection_test $GEM5/configs/example/se.py --cpu-type=AtomicSimpleCPU --take-simpoint-checkpoint=$BENCH_DATA/x86/445.gobmk/simpoint/simpoint_connection_test,$BENCH_DATA/x86/445.gobmk/simpoint/weight_connection_test,100000000,0 --output=../connection_test/445gobmk.out --cmd=$SPEC/445.gobmk/exe/gobmk_base.x86 --options="--quiet --mode gtp" --input="connection.tst") &> ../connection_test/gem5.445gobmk.log &
(time $GEM5/build/X86/gem5.fast --outdir=../connect_test $GEM5/configs/example/se.py --cpu-type=AtomicSimpleCPU --take-simpoint-checkpoint=$BENCH_DATA/x86/445.gobmk/simpoint/simpoint_connect_test,$BENCH_DATA/x86/445.gobmk/simpoint/weight_connect_test,100000000,0 --output=../connect_test/445gobmk.out --cmd=$SPEC/445.gobmk/exe/gobmk_base.x86 --options="--quiet --mode gtp" --input="connect.tst") &> ../connect_test/gem5.445gobmk.log &
(time $GEM5/build/X86/gem5.fast --outdir=../cutstone_test $GEM5/configs/example/se.py --cpu-type=AtomicSimpleCPU --take-simpoint-checkpoint=$BENCH_DATA/x86/445.gobmk/simpoint/simpoint_cutstone_test,$BENCH_DATA/x86/445.gobmk/simpoint/weight_cutstone_test,100000000,0 --output=../cutstone_test/445gobmk.out --cmd=$SPEC/445.gobmk/exe/gobmk_base.x86 --options="--quiet --mode gtp" --input="cutstone.tst") &> ../cutstone_test/gem5.445gobmk.log &
(time $GEM5/build/X86/gem5.fast --outdir=../dniwog_test $GEM5/configs/example/se.py --cpu-type=AtomicSimpleCPU --take-simpoint-checkpoint=$BENCH_DATA/x86/445.gobmk/simpoint/simpoint_dniwog_test,$BENCH_DATA/x86/445.gobmk/simpoint/weight_dniwog_test,100000000,0 --output=../dniwog_test/445gobmk.out --cmd=$SPEC/445.gobmk/exe/gobmk_base.x86 --options="--quiet --mode gtp" --input="dniwog.tst") &> ../dniwog_test/gem5.445gobmk.log &
cd ../../..

# 447.dealII
echo "447.dealII"
mkdir -p 447.dealII/checkpoint/{test,tmp_test}
cd 447.dealII/checkpoint/tmp_test
ln -s $SPEC/447.dealII/data/all/input/* .
(time $GEM5/build/X86/gem5.fast --outdir=../test $GEM5/configs/example/se.py --cpu-type=AtomicSimpleCPU --take-simpoint-checkpoint=$BENCH_DATA/x86/447.dealII/simpoint/simpoint_test,$BENCH_DATA/x86/447.dealII/simpoint/weight_test,100000000,0 --output=../test/447dealII.out --cmd=$SPEC/447.dealII/exe/dealII_base.x86 --options="8") &> ../test/gem5.447dealII.log &
cd ../../..

# 450.soplex
echo "450.soplex"
mkdir -p 450.soplex/checkpoint/{test,tmp_test}
cd 450.soplex/checkpoint/tmp_test
ln -s $SPEC/450.soplex/data/test/input/* .
(time $GEM5/build/X86/gem5.fast --outdir=../test $GEM5/configs/example/se.py --cpu-type=AtomicSimpleCPU --take-simpoint-checkpoint=$BENCH_DATA/x86/450.soplex/simpoint/simpoint_test,$BENCH_DATA/x86/450.soplex/simpoint/weight_test,100000000,0 --output=../test/450soplex.out --cmd=$SPEC/450.soplex/exe/soplex_base.x86 --options="-m10000 test.mps") &> ../test/gem5.450soplex.log &
cd ../../..

# 453.povray
echo "453.povray"
mkdir -p 453.povray/checkpoint/test 453.povray/checkpoint/tmp_test
cd 453.povray/checkpoint/tmp_test
ln -s $SPEC/453.povray/data/all/input/* .
ln -s $SPEC/453.povray/data/test/input/* .
(time $GEM5/build/X86/gem5.fast --outdir=../test $GEM5/configs/example/se.py --cpu-type=AtomicSimpleCPU --take-simpoint-checkpoint=$BENCH_DATA/x86/453.povray/simpoint/simpoint_test,$BENCH_DATA/x86/453.povray/simpoint/weight_test,100000000,0 --output=../test/453povray.out --cmd=$SPEC/453.povray/exe/povray_base.x86 --options="SPEC-benchmark-test.ini") &> ../test/gem5.453povray.log &
cd ../../..

# 456.hmmer
echo "456.hmmer"
mkdir -p 456.hmmer/checkpoint/test 456.hmmer/checkpoint/tmp_test
cd 456.hmmer/checkpoint/tmp_test
ln -s $SPEC/456.hmmer/data/test/input/* .
(time $GEM5/build/X86/gem5.fast --outdir=../test $GEM5/configs/example/se.py --cpu-type=AtomicSimpleCPU --take-simpoint-checkpoint=$BENCH_DATA/x86/456.hmmer/simpoint/simpoint_test,$BENCH_DATA/x86/456.hmmer/simpoint/weight_test,100000000,0 --output=../test/456hmmer.out --cmd=$SPEC/456.hmmer/exe/hmmer_base.x86 --options="--fixed 0 --mean 325 --num 45000 --sd 200 --seed 0 bombesin.hmm") &> ../test/gem5.456hmmer.log &
cd ../../..

# 458.sjeng
echo "458.sjeng"
mkdir -p 458.sjeng/checkpoint/test 458.sjeng/checkpoint/tmp_test
cd 458.sjeng/checkpoint/tmp_test
ln -s $SPEC/458.sjeng/data/test/input/* .
(time $GEM5/build/X86/gem5.fast --outdir=../test $GEM5/configs/example/se.py --cpu-type=AtomicSimpleCPU --take-simpoint-checkpoint=$BENCH_DATA/x86/458.sjeng/simpoint/simpoint_test,$BENCH_DATA/x86/458.sjeng/simpoint/weight_test,100000000,0 --output=../test/458sjeng.out --cmd=$SPEC/458.sjeng/exe/sjeng_base.x86 --options="test.txt") &> ../test/gem5.458sjeng.log &
cd ../../..

# 459.GemsFDTD
echo "459.GemsFDTD"
mkdir -p 459.GemsFDTD/checkpoint/test 459.GemsFDTD/checkpoint/tmp_test
cd 459.GemsFDTD/checkpoint/tmp_test
ln -s $SPEC/459.GemsFDTD/data/test/input/* .
(time $GEM5/build/X86/gem5.fast --outdir=../test $GEM5/configs/example/se.py --cpu-type=AtomicSimpleCPU --take-simpoint-checkpoint=$BENCH_DATA/x86/459.GemsFDTD/simpoint/simpoint_test,$BENCH_DATA/x86/459.GemsFDTD/simpoint/weight_test,100000000,0 --output=../test/459GemsFDTD.out --mem-size=4GB --cmd=$SPEC/459.GemsFDTD/exe/GemsFDTD_base.x86 ) &> ../test/gem5.459GemsFDTD.log &
cd ../../..

# 462.libquantum
echo "462.libquantum"
mkdir -p 462.libquantum/checkpoint/test 462.libquantum/checkpoint/tmp_test
cd 462.libquantum/checkpoint/tmp_test
(time $GEM5/build/X86/gem5.fast --outdir=../test $GEM5/configs/example/se.py --cpu-type=AtomicSimpleCPU --take-simpoint-checkpoint=$BENCH_DATA/x86/462.libquantum/simpoint/simpoint_test,$BENCH_DATA/x86/462.libquantum/simpoint/weight_test,100000000,0 --output=../test/462libquantum.out --cmd=$SPEC/462.libquantum/exe/libquantum_base.x86 --options="33 5") &> ../test/gem5.462libquantum.log &
cd ../../..

# 464.h264ref
echo "464.h264ref"
mkdir -p 464.h264ref/checkpoint/test 464.h264ref/checkpoint/tmp_test
cd 464.h264ref/checkpoint/tmp_test
ln -s $SPEC/464.h264ref/data/all/input/* .
ln -s $SPEC/464.h264ref/data/test/input/* .
(time $GEM5/build/X86/gem5.fast --outdir=../test $GEM5/configs/example/se.py --cpu-type=AtomicSimpleCPU --take-simpoint-checkpoint=$BENCH_DATA/x86/464.h264ref/simpoint/simpoint_test,$BENCH_DATA/x86/464.h264ref/simpoint/weight_test,100000000,0 --output=../test/464h264ref.out --cmd=$SPEC/464.h264ref/exe/h264ref_base.x86 --options="-d foreman_test_encoder_baseline.cfg") &> ../test/gem5.464h264ref.log &
cd ../../..

# 465.tonto
#echo "465.tonto"
#mkdir -p 465.tonto/checkpoint/test 465.tonto/checkpoint/tmp_test
#cd 465.tonto/checkpoint/tmp_test
#ln -s $SPEC/465.tonto/data/test/input/* .
#(time $GEM5/build/X86/gem5.fast --outdir=../test $GEM5/configs/example/se.py --cpu-type=AtomicSimpleCPU --take-simpoint-checkpoint=$BENCH_DATA/x86/465.tonto/simpoint/simpoint_test,$BENCH_DATA/x86/465.tonto/simpoint/weight_test,100000000,0 --output=../test/465tonto.out --cmd=$SPEC/465.tonto/exe/tonto_base.x86 --options="< stdin") &> ../test/gem5.465tonto.log &
#cd ../../..

# 470.lbm
echo "470.lbm"
mkdir -p 470.lbm/checkpoint/test 470.lbm/checkpoint/tmp_test
cd 470.lbm/checkpoint/tmp_test
ln -s $SPEC/470.lbm/data/test/input/* .
(time $GEM5/build/X86/gem5.fast --outdir=../test $GEM5/configs/example/se.py --cpu-type=AtomicSimpleCPU --take-simpoint-checkpoint=$BENCH_DATA/x86/470.lbm/simpoint/simpoint_test,$BENCH_DATA/x86/470.lbm/simpoint/weight_test,100000000,0 --output=../test/470lbm.out --cmd=$SPEC/470.lbm/exe/lbm_base.x86 --options="20 reference.dat 0 1 100_100_130_cf_a.of") &> ../test/gem5.470lbm.log &
cd ../../..

# 471.omnetpp
echo "471.omnetpp"
mkdir -p 471.omnetpp/checkpoint/test 471.omnetpp/checkpoint/tmp_test
cd 471.omnetpp/checkpoint/tmp_test
ln -s $SPEC/471.omnetpp/data/test/input/* .
(time $GEM5/build/X86/gem5.fast --outdir=../test $GEM5/configs/example/se.py --cpu-type=AtomicSimpleCPU --take-simpoint-checkpoint=$BENCH_DATA/x86/471.omnetpp/simpoint/simpoint_test,$BENCH_DATA/x86/471.omnetpp/simpoint/weight_test,100000000,0 --output=../test/471omnetpp.out --cmd=$SPEC/471.omnetpp/exe/omnetpp_base.x86 --options="omnetpp.ini") &> ../test/gem5.471omnetpp.log &
cd ../../..

# 473.astar
echo "473.astar"
mkdir -p 473.astar/checkpoint/test 473.astar/checkpoint/tmp_test
cd 473.astar/checkpoint/tmp_test
ln -s $SPEC/473.astar/data/test/input/* .
(time $GEM5/build/X86/gem5.fast --outdir=../test $GEM5/configs/example/se.py --cpu-type=AtomicSimpleCPU --take-simpoint-checkpoint=$BENCH_DATA/x86/473.astar/simpoint/simpoint_test,$BENCH_DATA/x86/473.astar/simpoint/weight_test,100000000,0 --output=../test/473astar.out --cmd=$SPEC/473.astar/exe/astar_base.x86 --options="lake.cfg") &> ../test/gem5.473astar.log &
cd ../../..

# 481.wrf
echo "481.wrf"
mkdir -p 481.wrf/checkpoint/test 481.wrf/checkpoint/tmp_test
cd 481.wrf/checkpoint/tmp_test
ln -s $SPEC/481.wrf/data/all/input/* .
ln -s $SPEC/481.wrf/data/test/input/* .
ln -s le/64/* .
(time $GEM5/build/X86/gem5.fast --outdir=../test $GEM5/configs/example/se.py --cpu-type=AtomicSimpleCPU --take-simpoint-checkpoint=$BENCH_DATA/x86/481.wrf/simpoint/simpoint_test,$BENCH_DATA/x86/481.wrf/simpoint/weight_test,100000000,0 --output=../test/481wrf.out --cmd=$SPEC/481.wrf/exe/wrf_base.x86) &> ../test/gem5.481wrf.log &
cd ../../..

# 482.sphinx3
echo "482.sphinx3"
mkdir -p 482.sphinx3/checkpoint/test 482.sphinx3/checkpoint/tmp_test
cd 482.sphinx3/checkpoint/tmp_test
ln -s $SPEC/482.sphinx3/data/all/input/* .
ln -s $SPEC/482.sphinx3/data/test/input/* .
rm *.be.raw
for file in *.le.raw
do
    mv "$file" "${file%.le.raw}.raw"
done
wc -c $(ls *.raw) | awk -F".raw" '{print $1}' | awk '{print $2 " " $1}' | head -n -1 > ctlfile
(time $GEM5/build/X86/gem5.fast --outdir=../test $GEM5/configs/example/se.py --cpu-type=AtomicSimpleCPU --take-simpoint-checkpoint=$BENCH_DATA/x86/482.sphinx3/simpoint/simpoint_test,$BENCH_DATA/x86/482.sphinx3/simpoint/weight_test,100000000,0 --output=../test/482sphinx3.out --cmd=$SPEC/482.sphinx3/exe/sphinx_livepretend_base.x86 --options="ctlfile . args.an4") &> ../test/gem5.482sphinx3.log &
cd ../../..

# 483.xalancbmk
echo "483.xalancbmk"
mkdir -p 483.xalancbmk/checkpoint/test 483.xalancbmk/checkpoint/tmp_test
cd 483.xalancbmk/checkpoint/tmp_test
ln -s $SPEC/483.xalancbmk/data/test/input/* .
(time $GEM5/build/X86/gem5.fast --outdir=../test $GEM5/configs/example/se.py --cpu-type=AtomicSimpleCPU --take-simpoint-checkpoint=$BENCH_DATA/x86/483.xalancbmk/simpoint/simpoint_test,$BENCH_DATA/x86/483.xalancbmk/simpoint/weight_test,100000000,0 --output=../test/483xalancbmk.out --cmd=$SPEC/483.xalancbmk/exe/Xalan_base.x86 --options="-v test.xml xalanc.xsl") &> ../test/gem5.483xalancbmk.log &
cd ../../..

# 998.specrand
echo "998.specrand"
mkdir -p 998.specrand/checkpoint/ref 998.specrand/checkpoint/tmp_ref
cd 998.specrand/checkpoint/tmp_ref
(time $GEM5/build/X86/gem5.fast --outdir=../ref $GEM5/configs/example/se.py --cpu-type=AtomicSimpleCPU --take-simpoint-checkpoint=$BENCH_DATA/x86/998.specrand/simpoint/simpoint_ref,$BENCH_DATA/x86/998.specrand/simpoint/weight_ref,100000000,0 --output=../ref/998specrand.out --cmd=$SPEC/998.specrand/exe/specrand_base.x86 --options="1255432124 234923") &> ../ref/gem5.998specrand.log &
cd ../../..

# 999.specrand
echo "999.specrand"
mkdir -p 999.specrand/checkpoint/ref 999.specrand/checkpoint/tmp_ref
cd 999.specrand/checkpoint/tmp_ref
(time $GEM5/build/X86/gem5.fast --outdir=../ref $GEM5/configs/example/se.py --cpu-type=AtomicSimpleCPU --take-simpoint-checkpoint=$BENCH_DATA/x86/999.specrand/simpoint/simpoint_ref,$BENCH_DATA/x86/999.specrand/simpoint/weight_ref,100000000,0 --output=../ref/999specrand.out --cmd=$SPEC/999.specrand/exe/specrand_base.x86 --options="1255432124 234923") &> ../ref/gem5.999specrand.log &
cd ../../..