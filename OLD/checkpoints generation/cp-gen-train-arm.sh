#!/bin/bash
mkdir -p ~/cp_data_arm
cd ~/cp_data_arm

# 400.perlbench
echo "400.perlbench"
mkdir -p 400.perlbench/checkpoint/{scrabbl,suns,tmp}_train
cd 400.perlbench/checkpoint/tmp_train
ln -s $SPEC/400.perlbench/data/all/input/* .
ln -s $SPEC/400.perlbench/data/train/input/* .
(time $GEM5/build/ARM/gem5.fast --outdir=../scrabbl_train $GEM5/configs/example/se.py --cpu-type=AtomicSimpleCPU --take-simpoint-checkpoint=$BENCH_DATA/arm/400.perlbench/simpoint/simpoint_scrabbl_train,$BENCH_DATA/arm/400.perlbench/simpoint/weight_scrabbl_train,100000000,0 --output=../scrabbl_train/400perlbench.out --cmd=$SPEC/400.perlbench/exe/perlbench_base.arm --options="-I. -I./lib scrabbl.pl") &> ../scrabbl_train/gem5.400perlbench.log &
(time $GEM5/build/ARM/gem5.fast --outdir=../suns_train $GEM5/configs/example/se.py --cpu-type=AtomicSimpleCPU --take-simpoint-checkpoint=$BENCH_DATA/arm/400.perlbench/simpoint/simpoint_suns_train,$BENCH_DATA/arm/400.perlbench/simpoint/weight_suns_train,100000000,0 --output=../suns_train/400perlbench.out --cmd=$SPEC/400.perlbench/exe/perlbench_base.arm --options="-I. -I./lib suns.pl") &> ../suns_train/gem5.400perlbench.log &
cd ../../..

# 401.bzip2
echo "401.bzip2"
mkdir -p 401.bzip2/checkpoint/{byoudoin_5,input_combined_80,input_program_10,tmp}_train
cd 401.bzip2/checkpoint/tmp_train
ln -s $SPEC/401.bzip2/data/all/input/* .
ln -s $SPEC/401.bzip2/data/train/input/* .
(time $GEM5/build/ARM/gem5.fast --outdir=../byoudoin_5_train $GEM5/configs/example/se.py --cpu-type=AtomicSimpleCPU --take-simpoint-checkpoint=$BENCH_DATA/arm/401.bzip2/simpoint/simpoint_byoudoin_5_train,$BENCH_DATA/arm/401.bzip2/simpoint/weight_byoudoin_5_train,100000000,0 --output=../byoudoin_5_train/401bzip.out --cmd=$SPEC/401.bzip2/exe/bzip2_base.arm --options="byoudoin.jpg 5") &> ../byoudoin_5_train/gem5.401bzip2.log &
(time $GEM5/build/ARM/gem5.fast --outdir=../input_combined_80_train $GEM5/configs/example/se.py --cpu-type=AtomicSimpleCPU --take-simpoint-checkpoint=$BENCH_DATA/arm/401.bzip2/simpoint/simpoint_input_combined_80_train,$BENCH_DATA/arm/401.bzip2/simpoint/weight_input_combined_80_train,100000000,0 --output=../input_combined_80_train/401bzip.out --cmd=$SPEC/401.bzip2/exe/bzip2_base.arm --options="input.combined 80") &> ../input_combined_80_train/gem5.401bzip2.log &
(time $GEM5/build/ARM/gem5.fast --outdir=../input_program_10_train $GEM5/configs/example/se.py --cpu-type=AtomicSimpleCPU --take-simpoint-checkpoint=$BENCH_DATA/arm/401.bzip2/simpoint/simpoint_input_program_10_train,$BENCH_DATA/arm/401.bzip2/simpoint/weight_input_program_10_train,100000000,0 --output=../input_program_10_train/401bzip.out --cmd=$SPEC/401.bzip2/exe/bzip2_base.arm --options="input.program 10") &> ../input_program_10_train/gem5.401bzip2.log &
cd ../../..

# 403.gcc
echo "403.gcc"
mkdir -p 403.gcc/checkpoint/{train,tmp_train}
cd 403.gcc/checkpoint/tmp_train
ln -s $SPEC/403.gcc/data/train/input/* .
(time $GEM5/build/ARM/gem5.fast --outdir=../train $GEM5/configs/example/se.py --cpu-type=AtomicSimpleCPU --take-simpoint-checkpoint=$BENCH_DATA/arm/403.gcc/simpoint/simpoint_train,$BENCH_DATA/arm/403.gcc/simpoint/weight_train,100000000,0 --output=../train/403gcc.out --cmd=$SPEC/403.gcc/exe/gcc_base.arm --options="integrate.in -o integrate.s") &> ../train/gem5.403gcc.log &
cd ../../..

# 410.bwaves
echo "410.bwaves"
mkdir -p 410.bwaves/checkpoint/{train,tmp_train}
cd 410.bwaves/checkpoint/tmp_train
ln -s $SPEC/410.bwaves/data/train/input/* .
(time $GEM5/build/ARM/gem5.fast --outdir=../train $GEM5/configs/example/se.py --cpu-type=AtomicSimpleCPU --take-simpoint-checkpoint=$BENCH_DATA/arm/410.bwaves/simpoint/simpoint_train,$BENCH_DATA/arm/410.bwaves/simpoint/weight_train,100000000,0 --output=../train/410bwaves.out --cmd=$SPEC/410.bwaves/exe/bwaves_base.arm --options="bwaves.in") &> ../train/gem5.410bwaves.log &
cd ../../..

# 416.gamess
#echo "416.gamess"
#mkdir -p 416.gamess/checkpoint/{train,tmp_train}
#cd 416.gamess/checkpoint/tmp_train
#ln -s $SPEC/416.gamess/data/train/input/* .
#(time $GEM5/build/ARM/gem5.fast --outdir=../train $GEM5/configs/example/se.py --cpu-type=AtomicSimpleCPU --take-simpoint-checkpoint=$BENCH_DATA/arm/416.gamess/simpoint/simpoint_train,$BENCH_DATA/arm/416.gamess/simpoint/weight_train,100000000,0 --output=../train/416gamess.out --mem-size=2GB --cmd=$SPEC/416.gamess/exe/gamess_base.arm --input="h2ocu2+_energy.config") &> ../train/gem5.416gamess.log &
#cd ../../..

# 429.mcf
echo "429.mcf"
mkdir -p 429.mcf/checkpoint/{train,tmp_train}
cd 429.mcf/checkpoint/tmp_train
ln -s $SPEC/429.mcf/data/train/input/* .
(time $GEM5/build/ARM/gem5.fast --outdir=../train $GEM5/configs/example/se.py --cpu-type=AtomicSimpleCPU --take-simpoint-checkpoint=$BENCH_DATA/arm/429.mcf/simpoint/simpoint_train,$BENCH_DATA/arm/429.mcf/simpoint/weight_train,100000000,0 --output=../train/429mcf.out --cmd=$SPEC/429.mcf/exe/mcf_base.arm --options="inp.in") &> ../train/gem5.429mcfb.log &
cd ../../..

# 433.milc
echo "433.milc"
mkdir -p 433.milc/checkpoint/{train,tmp_train}
cd 433.milc/checkpoint/tmp_train
ln -s $SPEC/433.milc/data/train/input/* .
(time $GEM5/build/ARM/gem5.fast --outdir=../train $GEM5/configs/example/se.py --cpu-type=AtomicSimpleCPU --take-simpoint-checkpoint=$BENCH_DATA/arm/433.milc/simpoint/simpoint_train,$BENCH_DATA/arm/433.milc/simpoint/weight_train,100000000,0 --output=../train/433milc.out --cmd=$SPEC/433.milc/exe/milc_base.arm --input="su3imp.in") &> ../train/gem5.429mcf.log &
cd ../../..

# 434.zeusmp
echo "434.zeusmp"
mkdir -p 434.zeusmp/checkpoint/{train,tmp_train}
cd 434.zeusmp/checkpoint/tmp_train
ln -s $SPEC/434.zeusmp/data/train/input/* .
(time $GEM5/build/ARM/gem5.fast --outdir=../train $GEM5/configs/example/se.py --cpu-type=AtomicSimpleCPU --take-simpoint-checkpoint=$BENCH_DATA/arm/434.zeusmp/simpoint/simpoint_train,$BENCH_DATA/arm/434.zeusmp/simpoint/weight_train,100000000,0 --output=../train/434zeusmp.out --mem-size=2GB --cmd=$SPEC/434.zeusmp/exe/zeusmp_base.arm) &> ../train/gem5.434zeusmp.log &
cd ../../..

# 435.gromacs
echo "435.gromacs"
mkdir -p 435.gromacs/checkpoint/{train,tmp_train}
cd 435.gromacs/checkpoint/tmp_train
ln -s $SPEC/435.gromacs/data/train/input/* .
(time $GEM5/build/ARM/gem5.fast --outdir=../train $GEM5/configs/example/se.py --cpu-type=AtomicSimpleCPU --take-simpoint-checkpoint=$BENCH_DATA/arm/435.gromacs/simpoint/simpoint_train,$BENCH_DATA/arm/435.gromacs/simpoint/weight_train,100000000,0 --output=../train/435gromacs.out --cmd=$SPEC/435.gromacs/exe/gromacs_base.arm --options="-silent -deffnm gromacs -nice 0") &> ../train/gem5.435gromacs.log &
cd ../../..

# 436.cactusADM
echo "436.cactusADM"
mkdir -p 436.cactusADM/checkpoint/{train,tmp_train}
cd 436.cactusADM/checkpoint/tmp_train
ln -s $SPEC/436.cactusADM/data/train/input/* .
(time $GEM5/build/ARM/gem5.fast --outdir=../train $GEM5/configs/example/se.py --cpu-type=AtomicSimpleCPU --take-simpoint-checkpoint=$BENCH_DATA/arm/436.cactusADM/simpoint/simpoint_train,$BENCH_DATA/arm/436.cactusADM/simpoint/weight_train,100000000,0 --output=../train/436cactusADM.out --mem-size=2GB --cmd=$SPEC/436.cactusADM/exe/cactusADM_base.arm --options="benchADM.par") &> ../train/gem5.436cactusADM.log &
cd ../../..

# 437.leslie3d
echo "437.leslie3d"
mkdir -p 437.leslie3d/checkpoint/{train,tmp_train}
cd 437.leslie3d/checkpoint/tmp_train
ln -s $SPEC/437.leslie3d/data/train/input/* .
(time $GEM5/build/ARM/gem5.fast --outdir=../train $GEM5/configs/example/se.py --cpu-type=AtomicSimpleCPU --take-simpoint-checkpoint=$BENCH_DATA/arm/437.leslie3d/simpoint/simpoint_train,$BENCH_DATA/arm/437.leslie3d/simpoint/weight_train,100000000,0 --output=../train/437leslie3d.out --cmd=$SPEC/437.leslie3d/exe/leslie3d_base.arm --input="leslie3d.in") &> ../train/gem5.437leslie3d.log &
cd ../../..

# 444.namd
echo "444.namd"
mkdir -p 444.namd/checkpoint/{train,tmp_train}
cd 444.namd/checkpoint/tmp_train
ln -s $SPEC/444.namd/data/all/input/* .
ln -s $SPEC/444.namd/data/train/input/* .
(time $GEM5/build/ARM/gem5.fast --outdir=../train $GEM5/configs/example/se.py --cpu-type=AtomicSimpleCPU --take-simpoint-checkpoint=$BENCH_DATA/arm/444.namd/simpoint/simpoint_train,$BENCH_DATA/arm/444.namd/simpoint/weight_train,100000000,0 --output=../train/444namd.out --cmd=$SPEC/444.namd/exe/namd_base.arm --options="--input namd.input --iterations 1 --output ../train/namd.out") &> ../train/gem5.444namd.log &
cd ../../..

# 445.gobmk
echo "445.gobmk"
mkdir -p 445.gobmk/checkpoint/{arb,arend,arion,atari,blunder,buzco,nicklas2,nicklas4,tmp}_train
cd 445.gobmk/checkpoint/tmp_train
ln -s $SPEC/445.gobmk/data/all/input/* .
ln -s $SPEC/445.gobmk/data/train/input/* .
(time $GEM5/build/ARM/gem5.fast --outdir=../arb_train $GEM5/configs/example/se.py --cpu-type=AtomicSimpleCPU --take-simpoint-checkpoint=$BENCH_DATA/arm/445.gobmk/simpoint/simpoint_arb_train,$BENCH_DATA/arm/445.gobmk/simpoint/weight_arb_train,100000000,0 --output=../arb_train/445gobmk.out --cmd=$SPEC/445.gobmk/exe/gobmk_base.arm --options="--quiet --mode gtp" --input="arb.tst") &> ../arb_train/gem5.445gobmk.log &
(time $GEM5/build/ARM/gem5.fast --outdir=../arend_train $GEM5/configs/example/se.py --cpu-type=AtomicSimpleCPU --take-simpoint-checkpoint=$BENCH_DATA/arm/445.gobmk/simpoint/simpoint_arend_train,$BENCH_DATA/arm/445.gobmk/simpoint/weight_arend_train,100000000,0 --output=../arend_train/445gobmk.out --cmd=$SPEC/445.gobmk/exe/gobmk_base.arm --options="--quiet --mode gtp" --input="arend.tst") &> ../arend_train/gem5.445gobmk.log &
(time $GEM5/build/ARM/gem5.fast --outdir=../arion_train $GEM5/configs/example/se.py --cpu-type=AtomicSimpleCPU --take-simpoint-checkpoint=$BENCH_DATA/arm/445.gobmk/simpoint/simpoint_arion_train,$BENCH_DATA/arm/445.gobmk/simpoint/weight_arion_train,100000000,0 --output=../arion_train/445gobmk.out --cmd=$SPEC/445.gobmk/exe/gobmk_base.arm --options="--quiet --mode gtp" --input="arion.tst") &> ../arion_train/gem5.445gobmk.log &
(time $GEM5/build/ARM/gem5.fast --outdir=../atari_train $GEM5/configs/example/se.py --cpu-type=AtomicSimpleCPU --take-simpoint-checkpoint=$BENCH_DATA/arm/445.gobmk/simpoint/simpoint_atari_train,$BENCH_DATA/arm/445.gobmk/simpoint/weight_atari_train,100000000,0 --output=../atari_train/445gobmk.out --cmd=$SPEC/445.gobmk/exe/gobmk_base.arm --options="--quiet --mode gtp" --input="atari.tst") &> ../atari_train/gem5.445gobmk.log &
(time $GEM5/build/ARM/gem5.fast --outdir=../blunder_train $GEM5/configs/example/se.py --cpu-type=AtomicSimpleCPU --take-simpoint-checkpoint=$BENCH_DATA/arm/445.gobmk/simpoint/simpoint_blunder_train,$BENCH_DATA/arm/445.gobmk/simpoint/weight_blunder_train,100000000,0 --output=../blunder_train/445gobmk.out --cmd=$SPEC/445.gobmk/exe/gobmk_base.arm --options="--quiet --mode gtp" --input="blunder.tst") &> ../blunder_train/gem5.445gobmk.log &
(time $GEM5/build/ARM/gem5.fast --outdir=../buzco_train $GEM5/configs/example/se.py --cpu-type=AtomicSimpleCPU --take-simpoint-checkpoint=$BENCH_DATA/arm/445.gobmk/simpoint/simpoint_buzco_train,$BENCH_DATA/arm/445.gobmk/simpoint/weight_buzco_train,100000000,0 --output=../buzco_train/445gobmk.out --cmd=$SPEC/445.gobmk/exe/gobmk_base.arm --options="--quiet --mode gtp" --input="buzco.tst") &> ../buzco_train/gem5.445gobmk.log &
(time $GEM5/build/ARM/gem5.fast --outdir=../nicklas2_train $GEM5/configs/example/se.py --cpu-type=AtomicSimpleCPU --take-simpoint-checkpoint=$BENCH_DATA/arm/445.gobmk/simpoint/simpoint_nicklas2_train,$BENCH_DATA/arm/445.gobmk/simpoint/weight_nicklas2_train,100000000,0 --output=../nicklas2_train/445gobmk.out --cmd=$SPEC/445.gobmk/exe/gobmk_base.arm --options="--quiet --mode gtp" --input="nicklas2.tst") &> ../nicklas2_train/gem5.445gobmk.log &
(time $GEM5/build/ARM/gem5.fast --outdir=../nicklas4_train $GEM5/configs/example/se.py --cpu-type=AtomicSimpleCPU --take-simpoint-checkpoint=$BENCH_DATA/arm/445.gobmk/simpoint/simpoint_nicklas4_train,$BENCH_DATA/arm/445.gobmk/simpoint/weight_nicklas4_train,100000000,0 --output=../nicklas4_train/445gobmk.out --cmd=$SPEC/445.gobmk/exe/gobmk_base.arm --options="--quiet --mode gtp" --input="nicklas4.tst") &> ../nicklas4_train/gem5.445gobmk.log &
cd ../../..

# 447.dealII
echo "447.dealII"
mkdir -p 447.dealII/checkpoint/{train,tmp_train}
cd 447.dealII/checkpoint/tmp_train
ln -s $SPEC/447.dealII/data/all/input/* .
(time $GEM5/build/ARM/gem5.fast --outdir=../train $GEM5/configs/example/se.py --cpu-type=AtomicSimpleCPU --take-simpoint-checkpoint=$BENCH_DATA/arm/447.dealII/simpoint/simpoint_train,$BENCH_DATA/arm/447.dealII/simpoint/weight_train,100000000,0 --output=../train/447dealII.out --cmd=$SPEC/447.dealII/exe/dealII_base.arm --options="10") &> ../train/gem5.447dealII.log &
cd ../../..

# 450.soplex
echo "450.soplex"
mkdir -p 450.soplex/checkpoint/{pds-20,train,tmp}_train
cd 450.soplex/checkpoint/tmp_train
ln -s $SPEC/450.soplex/data/train/input/* .
(time $GEM5/build/ARM/gem5.fast --outdir=../pds-20_train $GEM5/configs/example/se.py --cpu-type=AtomicSimpleCPU --take-simpoint-checkpoint=$BENCH_DATA/arm/450.soplex/simpoint/simpoint_pds-20_train,$BENCH_DATA/arm/450.soplex/simpoint/weight_pds-20_train,100000000,0 --output=../pds-20_train/450soplex.out --cmd=$SPEC/450.soplex/exe/soplex_base.arm --options="-s1 -e -m5000 pds-20.mps") &> ../pds-20_train/gem5.450soplex.log &
(time $GEM5/build/ARM/gem5.fast --outdir=../train_train $GEM5/configs/example/se.py --cpu-type=AtomicSimpleCPU --take-simpoint-checkpoint=$BENCH_DATA/arm/450.soplex/simpoint/simpoint_train_train,$BENCH_DATA/arm/450.soplex/simpoint/weight_train_train,100000000,0 --output=../train_train/450soplex.out --cmd=$SPEC/450.soplex/exe/soplex_base.arm --options="-m1200 train.mps") &> ../train_train/gem5.450soplex.log &
cd ../../..

# 453.povray
#echo "453.povray"
#mkdir -p 453.povray/checkpoint/train 453.povray/checkpoint/tmp_train
#cd 453.povray/checkpoint/tmp_train
#ln -s $SPEC/453.povray/data/all/input/* .
#ln -s $SPEC/453.povray/data/train/input/* .
#(time $GEM5/build/ARM/gem5.fast --outdir=../train $GEM5/configs/example/se.py --cpu-type=AtomicSimpleCPU --take-simpoint-checkpoint=$BENCH_DATA/arm/453.povray/simpoint/simpoint_train,$BENCH_DATA/arm/453.povray/simpoint/weight_train,100000000,0 --output=../train/povray.out --cmd=$SPEC/453.povray/exe/povray_base.arm --options="SPEC-benchmark-train.ini") &> ../train/gem5.453povray.log &
#cd ../../..

# 454.calculix
echo "454.calculix"
mkdir -p 454.calculix/checkpoint/train 454.calculix/checkpoint/tmp_train
cd 454.calculix/checkpoint/tmp_train
ln -s $SPEC/454.calculix/data/train/input/* .
(time $GEM5/build/ARM/gem5.fast --outdir=../train $GEM5/configs/example/se.py --cpu-type=AtomicSimpleCPU --take-simpoint-checkpoint=$BENCH_DATA/arm/454.calculix/simpoint/simpoint_train,$BENCH_DATA/arm/454.calculix/simpoint/weight_train,100000000,0 --output=../train/454calculix.out --cmd=$SPEC/454.calculix/exe/calculix_base.arm --options="-i stairs") &> ../train/gem5.454calculix.log &
cd ../../..

# 456.hmmer
echo "456.hmmer"
mkdir -p 456.hmmer/checkpoint/train 456.hmmer/checkpoint/tmp_train
cd 456.hmmer/checkpoint/tmp_train
ln -s $SPEC/456.hmmer/data/train/input/* .
(time $GEM5/build/ARM/gem5.fast --outdir=../train $GEM5/configs/example/se.py --cpu-type=AtomicSimpleCPU --take-simpoint-checkpoint=$BENCH_DATA/arm/456.hmmer/simpoint/simpoint_train,$BENCH_DATA/arm/456.hmmer/simpoint/weight_train,100000000,0 --output=../train/456hmmer.out --cmd=$SPEC/456.hmmer/exe/hmmer_base.arm --options="--fixed 0 --mean 425 --num 85000 --sd 300 --seed 0 leng100.hmm") &> ../train/gem5.456hmmer.log &
cd ../../..

# 458.sjeng
echo "458.sjeng"
mkdir -p 458.sjeng/checkpoint/train 458.sjeng/checkpoint/tmp_train
cd 458.sjeng/checkpoint/tmp_train
ln -s $SPEC/458.sjeng/data/train/input/* .
(time $GEM5/build/ARM/gem5.fast --outdir=../train $GEM5/configs/example/se.py --cpu-type=AtomicSimpleCPU --take-simpoint-checkpoint=$BENCH_DATA/arm/458.sjeng/simpoint/simpoint_train,$BENCH_DATA/arm/458.sjeng/simpoint/weight_train,100000000,0 --output=../train/458sjeng.out --cmd=$SPEC/458.sjeng/exe/sjeng_base.arm --options="train.txt") &> ../train/gem5.458sjeng.log &
cd ../../..

# 459.GemsFDTD
echo "459.GemsFDTD"
mkdir -p 459.GemsFDTD/checkpoint/train 459.GemsFDTD/checkpoint/tmp_train
cd 459.GemsFDTD/checkpoint/tmp_train
ln -s $SPEC/459.GemsFDTD/data/train/input/* .
(time $GEM5/build/ARM/gem5.fast --outdir=../train $GEM5/configs/example/se.py --cpu-type=AtomicSimpleCPU --take-simpoint-checkpoint=$BENCH_DATA/arm/459.GemsFDTD/simpoint/simpoint_train,$BENCH_DATA/arm/459.GemsFDTD/simpoint/weight_train,100000000,0 --output=../train/459GemsFDTD.out --mem-size=4GB --cmd=$SPEC/459.GemsFDTD/exe/GemsFDTD_base.arm ) &> ../train/gem5.459GemsFDTD.log &
cd ../../..

# 462.libquantum
echo "462.libquantum"
mkdir -p 462.libquantum/checkpoint/train 462.libquantum/checkpoint/tmp_train
cd 462.libquantum/checkpoint/tmp_train
(time $GEM5/build/ARM/gem5.fast --outdir=../train $GEM5/configs/example/se.py --cpu-type=AtomicSimpleCPU --take-simpoint-checkpoint=$BENCH_DATA/arm/462.libquantum/simpoint/simpoint_train,$BENCH_DATA/arm/462.libquantum/simpoint/weight_train,100000000,0 --output=../train/462libquantum.out --cmd=$SPEC/462.libquantum/exe/libquantum_base.arm --options="143 25") &> ../train/gem5.462libquantum.log &
cd ../../..

# 464.h264ref
echo "464.h264ref"
mkdir -p 464.h264ref/checkpoint/train 464.h264ref/checkpoint/tmp_train
cd 464.h264ref/checkpoint/tmp_train
ln -s $SPEC/464.h264ref/data/all/input/* .
ln -s $SPEC/464.h264ref/data/train/input/* .
(time $GEM5/build/ARM/gem5.fast --outdir=../train $GEM5/configs/example/se.py --cpu-type=AtomicSimpleCPU --take-simpoint-checkpoint=$BENCH_DATA/arm/464.h264ref/simpoint/simpoint_train,$BENCH_DATA/arm/464.h264ref/simpoint/weight_train,100000000,0 --output=../train/464h264ref.out --cmd=$SPEC/464.h264ref/exe/h264ref_base.arm --options="-d foreman_train_encoder_baseline.cfg") &> ../train/gem5.464h264ref.log &
cd ../../..

# 465.tonto
#echo "465.tonto"
#mkdir -p 465.tonto/checkpoint/train 465.tonto/checkpoint/tmp_train
#cd 465.tonto/checkpoint/tmp_train
#ln -s $SPEC/465.tonto/data/train/input/* .
#(time $GEM5/build/ARM/gem5.fast --outdir=../train $GEM5/configs/example/se.py --cpu-type=AtomicSimpleCPU --take-simpoint-checkpoint=$BENCH_DATA/arm/465.tonto/simpoint/simpoint_train,$BENCH_DATA/arm/465.tonto/simpoint/weight_train,100000000,0 --output=../train/465tonto.out --mem-size=64GB --cmd=$SPEC/465.tonto/exe/tonto_base.arm --options="< stdin") &> ../train/gem5.465tonto.log &
#cd ../../..

# 470.lbm
echo "470.lbm"
mkdir -p 470.lbm/checkpoint/train 470.lbm/checkpoint/tmp_train
cd 470.lbm/checkpoint/tmp_train
ln -s $SPEC/470.lbm/data/train/input/* .
(time $GEM5/build/ARM/gem5.fast --outdir=../train $GEM5/configs/example/se.py --cpu-type=AtomicSimpleCPU --take-simpoint-checkpoint=$BENCH_DATA/arm/470.lbm/simpoint/simpoint_train,$BENCH_DATA/arm/470.lbm/simpoint/weight_train,100000000,0 --output=../train/470lbm.out --cmd=$SPEC/470.lbm/exe/lbm_base.arm --options="300 reference.dat 0 1 100_100_130_cf_b.of") &> ../train/gem5.470lbm.log &
cd ../../..

# 471.omnetpp
echo "471.omnetpp"
mkdir -p 471.omnetpp/checkpoint/train 471.omnetpp/checkpoint/tmp_train
cd 471.omnetpp/checkpoint/tmp_train
ln -s $SPEC/471.omnetpp/data/train/input/* .
(time $GEM5/build/ARM/gem5.fast --outdir=../train $GEM5/configs/example/se.py --cpu-type=AtomicSimpleCPU --take-simpoint-checkpoint=$BENCH_DATA/arm/471.omnetpp/simpoint/simpoint_train,$BENCH_DATA/arm/471.omnetpp/simpoint/weight_train,100000000,0 --output=../train/471omnetpp.out --cmd=$SPEC/471.omnetpp/exe/omnetpp_base.arm --options="omnetpp.ini") &> ../train/gem5.471omnetpp.log &
cd ../../..

# 473.astar
echo "473.astar"
mkdir -p 473.astar/checkpoint/BigLakes1024_train 473.astar/checkpoint/rivers_train 473.astar/checkpoint/tmp_train
cd 473.astar/checkpoint/tmp_train
ln -s $SPEC/473.astar/data/train/input/* .
(time $GEM5/build/ARM/gem5.fast --outdir=../BigLakes1024_train $GEM5/configs/example/se.py --cpu-type=AtomicSimpleCPU --take-simpoint-checkpoint=$BENCH_DATA/arm/473.astar/simpoint/simpoint_BigLakes1024_train,$BENCH_DATA/arm/473.astar/simpoint/weight_BigLakes1024_train,100000000,0 --output=../BigLakes1024_train/473astar.out --cmd=$SPEC/473.astar/exe/astar_base.arm --options="BigLakes1024.cfg") &> ../BigLakes1024_train/gem5.473astar.log &
(time $GEM5/build/ARM/gem5.fast --outdir=../rivers_train $GEM5/configs/example/se.py --cpu-type=AtomicSimpleCPU --take-simpoint-checkpoint=$BENCH_DATA/arm/473.astar/simpoint/simpoint_rivers_train,$BENCH_DATA/arm/473.astar/simpoint/weight_rivers_train,100000000,0 --output=../rivers_train/473astar.out --cmd=$SPEC/473.astar/exe/astar_base.arm --options="rivers1.cfg") &> ../rivers_train/gem5.473astar.log &
cd ../../..

# 481.wrf
#echo "481.wrf"
#mkdir -p 481.wrf/checkpoint/train 481.wrf/checkpoint/tmp_train
#cd 481.wrf/checkpoint/tmp_train
#ln -s $SPEC/481.wrf/data/all/input/* .
#ln -s $SPEC/481.wrf/data/train/input/* .
#ln -s le/32/* .
#(time $GEM5/build/ARM/gem5.fast --outdir=../train $GEM5/configs/example/se.py --cpu-type=AtomicSimpleCPU --take-simpoint-checkpoint=$BENCH_DATA/arm/481.wrf/simpoint/simpoint_train,$BENCH_DATA/arm/481.wrf/simpoint/weight_train,100000000,0 --output=../train/481wrf.out --mem-size=64GB --cmd=$SPEC/481.wrf/exe/wrf_base.arm) &> ../train/gem5.481wrf.log &
#cd ../../..

# 482.sphinx3
echo "482.sphinx3"
mkdir -p 482.sphinx3/checkpoint/train 482.sphinx3/checkpoint/tmp_train
cd 482.sphinx3/checkpoint/tmp_train
ln -s $SPEC/482.sphinx3/data/all/input/* .
ln -s $SPEC/482.sphinx3/data/train/input/* .
rm *.be.raw
for file in *.le.raw
do
    mv "$file" "${file%.le.raw}.raw"
done
wc -c $(ls *.raw) | awk -F".raw" '{print $1}' | awk '{print $2 " " $1}' | head -n -1 > ctlfile
(time $GEM5/build/ARM/gem5.fast --outdir=../train $GEM5/configs/example/se.py --cpu-type=AtomicSimpleCPU --take-simpoint-checkpoint=$BENCH_DATA/arm/482.sphinx3/simpoint/simpoint_train,$BENCH_DATA/arm/482.sphinx3/simpoint/weight_train,100000000,0 --output=../train/482sphinx3.out --cmd=$SPEC/482.sphinx3/exe/sphinx_livepretend_base.arm --options="ctlfile . args.an4") &> ../train/gem5.482sphinx3.log &
cd ../../..

# 483.xalancbmk
echo "483.xalancbmk"
mkdir -p 483.xalancbmk/checkpoint/train 483.xalancbmk/checkpoint/tmp_train
cd 483.xalancbmk/checkpoint/tmp_train
ln -s $SPEC/483.xalancbmk/data/train/input/* .
(time $GEM5/build/ARM/gem5.fast --outdir=../train $GEM5/configs/example/se.py --cpu-type=AtomicSimpleCPU --take-simpoint-checkpoint=$BENCH_DATA/arm/483.xalancbmk/simpoint/simpoint_train,$BENCH_DATA/arm/483.xalancbmk/simpoint/weight_train,100000000,0 --output=../train/483xalancbmk.out --cmd=$SPEC/483.xalancbmk/exe/Xalan_base.arm --options="-v allbooks.xml xalanc.xsl") &> ../train/gem5.483xalancbmk.log &
cd ../../..
