#!/bin/bash
if [ ! -d ~/spec_data ]
then
    mkdir ~/spec_data
fi
cd ~/spec_data

# 453.povray
echo "453.povray"
if [ ! -d 453.povray ]
then
    mkdir -p 453.povray/valgrind
fi
cd 453.povray
ln -s $SPEC/453.povray/data/all/input/* .
ln -s $SPEC/453.povray/data/test/input/SPEC-benchmark-test.pov .
valgrind --tool=exp-bbv --bb-out-file=valgrind/bb.out.453povray.test --pc-out-file=valgrind/pc.453povray.test $SPEC/453.povray/exe/povray_base.x86 $SPEC/453.povray/data/test/input/SPEC-benchmark-test.ini &> valgrind/453povray_test.out
wait
echo "- generated test bbv"
rm SPEC-benchmark-test.pov SPEC-benchmark.tga SPEC-benchmark.log
ln -s $SPEC/453.povray/data/train/input/SPEC-benchmark-train.pov .
valgrind --tool=exp-bbv --bb-out-file=valgrind/bb.out.453povray.train --pc-out-file=valgrind/pc.453povray.train $SPEC/453.povray/exe/povray_base.x86 $SPEC/453.povray/data/train/input/SPEC-benchmark-train.ini &> valgrind/453povray_train.out
wait
echo "- generated train bbv"
rm SPEC-benchmark-train.pov SPEC-benchmark.tga SPEC-benchmark.log
rm *.ttf *.inc
cd ..

# 454.calculix
echo "454.calculix"
if [ ! -d 454.calculix ]
then
    mkdir -p 454.calculix/valgrind
fi
cd 454.calculix
valgrind --tool=exp-bbv --bb-out-file=valgrind/bb.out.454calculix.test --pc-out-file=valgrind/pc.454calculix.test $SPEC/454.calculix/exe/calculix_base.x86 -i $SPEC/454.calculix/data/test/input/beampic &> valgrind/454calculix_test.out
wait
echo "- generated test bbv"
valgrind --tool=exp-bbv --bb-out-file=valgrind/bb.out.454calculix.train --pc-out-file=valgrind/pc.454calculix.train $SPEC/454.calculix/exe/calculix_base.x86 -i $SPEC/454.calculix/data/train/input/stairs &> valgrind/454calculix_train.out
wait
echo "- generated train bbv"
rm spooles.out
rm SPECtestformatmodifier_z.txt
cd ..

# 456.hmmer
echo "456.hmmer"
if [ ! -d 456.hmmer ]
then
    mkdir -p 456.hmmer/valgrind
fi
cd 456.hmmer
valgrind --tool=exp-bbv --bb-out-file=valgrind/bb.out.456hmmer.test --pc-out-file=valgrind/pc.456hmmer.test $SPEC/456.hmmer/exe/hmmer_base.x86 --fixed 0 --mean 325 --num 45000 --sd 200 --seed 0 $SPEC/456.hmmer/data/test/input/bombesin.hmm &> valgrind/456hmmer_test.out
wait
echo "- generated test bbv"
valgrind --tool=exp-bbv --bb-out-file=valgrind/bb.out.456hmmer.train --pc-out-file=valgrind/pc.456hmmer.train $SPEC/456.hmmer/exe/hmmer_base.x86 --fixed 0 --mean 425 --num 85000 --sd 300 --seed 0 $SPEC/456.hmmer/data/train/input/leng100.hmm &> valgrind/456hmmer_train.out
wait
echo "- generated train bbv"
cd ..

# 458.sjeng
echo "458.sjeng"
if [ ! -d 458.sjeng ]
then
    mkdir -p 458.sjeng/valgrind
fi
cd 458.sjeng
valgrind --tool=exp-bbv --bb-out-file=valgrind/bb.out.458sjeng.test --pc-out-file=valgrind/pc.458sjeng.test $SPEC/458.sjeng/exe/sjeng_base.x86 $SPEC/458.sjeng/data/test/input/test.txt &> valgrind/458sjeng_test.out
wait
echo "- generated test bbv"
valgrind --tool=exp-bbv --bb-out-file=valgrind/bb.out.458sjeng.train --pc-out-file=valgrind/pc.458sjeng.train $SPEC/458.sjeng/exe/sjeng_base.x86 $SPEC/458.sjeng/data/train/input/train.txt &> valgrind/458sjeng_train.out
wait
echo "- generated train bbv"
cd ..

# 459.GemsFDTD
echo "459.GemsFDTD"
if [ ! -d 459.GemsFDTD ]
then
    mkdir -p 459.GemsFDTD/valgrind
fi
cd 459.GemsFDTD
ln -s $SPEC/459.GemsFDTD/data/test/input/* .
valgrind --tool=exp-bbv --bb-out-file=valgrind/bb.out.459GemsFDTD.test --pc-out-file=valgrind/pc.459GemsFDTD.test $SPEC/459.GemsFDTD/exe/GemsFDTD_base.x86 &> valgrind/459GemsFDTD_test.out
wait
echo "- generated test bbv"
rm sphere.pec test.in yee.dat sphere_td.nft
ln -s $SPEC/459.GemsFDTD/data/train/input/* .
valgrind --tool=exp-bbv --bb-out-file=valgrind/bb.out.459GemsFDTD.train --pc-out-file=valgrind/pc.459GemsFDTD.train $SPEC/459.GemsFDTD/exe/GemsFDTD_base.x86 &> valgrind/459GemsFDTD_train.out
wait
echo "- generated train bbv"
rm sphere.pec train.in yee.dat sphere_td.nft
cd ..

# 462.libquantum
echo "462.libquantum"
if [ ! -d 462.libquantum ]
then
    mkdir -p 462.libquantum/valgrind
fi
cd 462.libquantum
valgrind --tool=exp-bbv --bb-out-file=valgrind/bb.out.462libquantum.test --pc-out-file=valgrind/pc.462libquantum.test $SPEC/462.libquantum/exe/libquantum_base.x86 33 5 &> valgrind/462libquantum_test.out
wait
echo "- generated test bbv"
valgrind --tool=exp-bbv --bb-out-file=valgrind/bb.out.462libquantum.train --pc-out-file=valgrind/pc.462libquantum.train $SPEC/462.libquantum/exe/libquantum_base.x86 143 25 &> valgrind/462libquantum_train.out
wait
echo "- generated train bbv"
cd ..

# 464.h264ref
echo "464.h264ref"
if [ ! -d 464.h264ref ]
then
    mkdir -p 464.h264ref/valgrind
fi
cd 464.h264ref
ln -s $SPEC/464.h264ref/data/all/input/foreman_qcif.yuv .
valgrind --tool=exp-bbv --bb-out-file=valgrind/bb.out.464h264ref.test --pc-out-file=valgrind/pc.464h264ref.test $SPEC/464.h264ref/exe/h264ref_base.x86 -d $SPEC/464.h264ref/data/test/input/foreman_test_encoder_baseline.cfg &> valgrind/464h264ref_test.out
wait
echo "- generated test bbv"
rm foreman_qcif.264 foreman_test_baseline_leakybucketparam.cfg
valgrind --tool=exp-bbv --bb-out-file=valgrind/bb.out.464h264ref.train --pc-out-file=valgrind/pc.464h264ref.train $SPEC/464.h264ref/exe/h264ref_base.x86 -d $SPEC/464.h264ref/data/train/input/foreman_train_encoder_baseline.cfg &> valgrind/464h264ref_train.out
wait
echo "- generated train bbv"
rm foreman_qcif.264 foreman_train_baseline_leakybucketparam.cfg
rm foreman_qcif.yuv
cd ..

# 465.tonto
echo "465.tonto"
if [ ! -d 465.tonto ]
then
    mkdir -p 465.tonto/valgrind
fi
cd 465.tonto
ln -s $SPEC/465.tonto/data/test/input/stdin .
valgrind --tool=exp-bbv --bb-out-file=valgrind/bb.out.465tonto.test --pc-out-file=valgrind/pc.465tonto.test $SPEC/465.tonto/exe/tonto_base.x86 &> valgrind/465tonto_test.out
wait
echo "- generated test bbv"
rm stdin stdout
ln -s $SPEC/465.tonto/data/train/input/stdin .
valgrind --tool=exp-bbv --bb-out-file=valgrind/bb.out.465tonto.train --pc-out-file=valgrind/pc.465tonto.train $SPEC/465.tonto/exe/tonto_base.x86 &> valgrind/465tonto_train.out
wait
echo "- generated train bbv"
rm stdin stdout
cd ..

# 470.lbm
echo "470.lbm"
if [ ! -d 470.lbm ]
then
    mkdir -p 470.lbm/valgrind
fi
cd 470.lbm
ln -s $SPEC/470.lbm/data/test/input/100_100_130_cf_a.of .
valgrind --tool=exp-bbv --bb-out-file=valgrind/bb.out.470lbm.test --pc-out-file=valgrind/pc.470lbm.test $SPEC/470.lbm/exe/lbm_base.x86 20 reference.dat 0 1 100_100_130_cf_a.of &> valgrind/470lbm_test.out
wait
echo "- generated test bbv"
rm 100_100_130_cf_a.of
ln -s $SPEC/470.lbm/data/train/input/100_100_130_cf_b.of .
valgrind --tool=exp-bbv --bb-out-file=valgrind/bb.out.470lbm.train --pc-out-file=valgrind/pc.470lbm.train $SPEC/470.lbm/exe/lbm_base.x86 300 reference.dat 0 1 100_100_130_cf_b.of &> valgrind/470lbm_train.out
wait
echo "- generated train bbv"
rm 100_100_130_cf_b.of
cd ..

# 471.omnetpp
echo "471.omnetpp"
if [ ! -d 471.omnetpp ]
then
    mkdir -p 471.omnetpp/valgrind
fi
cd 471.omnetpp
ln -s $SPEC/471.omnetpp/data/test/input/omnetpp.ini .
valgrind --tool=exp-bbv --bb-out-file=valgrind/bb.out.471omnetpp.test --pc-out-file=valgrind/pc.471omnetpp.test $SPEC/471.omnetpp/exe/omnetpp_base.x86 &> valgrind/471omnetpp_test.out
wait
echo "- generated test bbv"
rm omnetpp.ini omnetpp.sca
ln -s $SPEC/471.omnetpp/data/train/input/omnetpp.ini .
valgrind --tool=exp-bbv --bb-out-file=valgrind/bb.out.471omnetpp.train --pc-out-file=valgrind/pc.471omnetpp.train $SPEC/471.omnetpp/exe/omnetpp_base.x86 &> valgrind/471omnetpp_train.out
wait
echo "- generated train bbv"
rm omnetpp.ini omnetpp.sca
cd ..

# 473.astar
echo "473.astar"
if [ ! -d 473.astar ]
then
    mkdir -p 473.astar/valgrind
fi
cd 473.astar
ln -s $SPEC/473.astar/data/test/input/lake.bin .
valgrind --tool=exp-bbv --bb-out-file=valgrind/bb.out.473astar.test --pc-out-file=valgrind/pc.473astar.test $SPEC/473.astar/exe/astar_base.x86 $SPEC/473.astar/data/test/input/lake.cfg &> valgrind/473astar_test.out
wait
echo "- generated test bbv"
rm lake.bin
ln -s $SPEC/473.astar/data/train/input/BigLakes1024.bin .
ln -s $SPEC/473.astar/data/train/input/rivers.bin .
valgrind --tool=exp-bbv --bb-out-file=valgrind/bb.out.473astar.BigLakes1024.train --pc-out-file=valgrind/pc.473astar.BigLakes1024.train $SPEC/473.astar/exe/astar_base.x86 $SPEC/473.astar/data/train/input/BigLakes1024.cfg &> valgrind/473astar_BigLakes1024_train.out
wait
valgrind --tool=exp-bbv --bb-out-file=valgrind/bb.out.473astar.rivers.train --pc-out-file=valgrind/pc.473astar.rivers.train $SPEC/473.astar/exe/astar_base.x86 $SPEC/473.astar/data/train/input/rivers1.cfg &> valgrind/473astar_rivers_train.out
wait
echo "- generated train bbv"
rm BigLakes1024.bin rivers.bin
cd ..

# 481.wrf
echo "481.wrf"
if [ ! -d 481.wrf ]
then
    mkdir -p 481.wrf/valgrind
fi
cd 481.wrf
ln -s $SPEC/481.wrf/data/all/input/* .
ln -s le/64/RRTM_DATA .
ln -s $SPEC/481.wrf/data/test/input/* .
valgrind --tool=exp-bbv --bb-out-file=valgrind/bb.out.481wrf.test --pc-out-file=valgrind/pc.481wrf.test $SPEC/481.wrf/exe/wrf_base.x86 &> valgrind/481wrf_test.out
wait
echo "- generated test bbv"
rm namelist.input  wrfbdy_d01  wrfinput_d01
ln -s $SPEC/481.wrf/data/train/input/* .
valgrind --tool=exp-bbv --bb-out-file=valgrind/bb.out.481wrf.train --pc-out-file=valgrind/pc.481wrf.train $SPEC/481.wrf/exe/wrf_base.x86 &> valgrind/481wrf_train.out
wait
echo "- generated train bbv"
rm namelist.input  wrfbdy_d01  wrfinput_d01
rm GENPARM.TBL LANDUSE.TBL RRTM_DATA SOILPARM.TBL VEGPARM.TBL wrf.in
rm -rf be le
cd ..

# 482.sphinx3
echo "482.sphinx3"
if [ ! -d 482.sphinx3 ]
then
    mkdir -p 482.sphinx3/valgrind
fi
cd 482.sphinx3
ln -s $SPEC/482.sphinx3/data/all/input/* .
ln -s $SPEC/482.sphinx3/data/test/input/* .
rm *.be.raw
for file in *.le.raw
do
    mv "$file" "${file%.le.raw}.raw"
done
wc -c $(ls *.raw) | awk -F".raw" '{print $1}' | awk '{print $2 " " $1}' | head -n -1 > ctlfile
valgrind --tool=exp-bbv --bb-out-file=valgrind/bb.out.482sphinx3.test --pc-out-file=valgrind/pc.482sphinx3.test $SPEC/482.sphinx3/exe/sphinx_livepretend_base.x86 ctlfile . args.an4 &> valgrind/482sphinx3_test.out
wait
echo "- generated test bbv"
rm an406-fcaw-b.raw an407-fcaw-b.raw args.an4 beams.dat ctlfile considered.out total_considered.out
ln -s $SPEC/482.sphinx3/data/train/input/* .
rm *.be.raw
for file in *.le.raw
do
    mv "$file" "${file%.le.raw}.raw"
done
wc -c $(ls *.raw) | awk -F".raw" '{print $1}' | awk '{print $2 " " $1}' | head -n -1 > ctlfile
valgrind --tool=exp-bbv --bb-out-file=valgrind/bb.out.482sphinx3.train --pc-out-file=valgrind/pc.482sphinx3.train $SPEC/482.sphinx3/exe/sphinx_livepretend_base.x86 ctlfile . args.an4 &> valgrind/482sphinx3_train.out
wait
echo "- generated train bbv"
rm an406-fcaw-b.raw an407-fcaw-b.raw an408-fcaw-b.raw an409-fcaw-b.raw an410-fcaw-b.raw args.an4 beams.dat ctlfile considered.out total_considered.out
rm -rf model
cd ..

# 483.xalancbmk
echo "483.xalancbmk"
if [ ! -d 483.xalancbmk ]
then
    mkdir -p 483.xalancbmk/valgrind
fi
cd 483.xalancbmk
ln -s $SPEC/483.xalancbmk/data/test/input/100mb.xsd .
valgrind --tool=exp-bbv --bb-out-file=valgrind/bb.out.483xalancbmk.test --pc-out-file=valgrind/pc.483xalancbmk.test $SPEC/483.xalancbmk/exe/Xalan_base.x86 -v $SPEC/483.xalancbmk/data/test/input/test.xml $SPEC/483.xalancbmk/data/test/input/xalanc.xsl &> valgrind/483xalancbmk_test.out
wait
echo "- generated test bbv"
rm 100mb.xsd
ln -s $SPEC/483.xalancbmk/data/train/input/train.xsd .
valgrind --tool=exp-bbv --bb-out-file=valgrind/bb.out.483xalancbmk.train --pc-out-file=valgrind/pc.483xalancbmk.train $SPEC/483.xalancbmk/exe/Xalan_base.x86 -v $SPEC/483.xalancbmk/data/train/input/allbooks.xml $SPEC/483.xalancbmk/data/train/input/xalanc.xsl &> valgrind/483xalancbmk_train.out
wait
rm train.xsd
cd ..

# 998.specrand
echo "998.specrand"
if [ ! -d 998.specrand ]
then
    mkdir -p 998.specrand/valgrind
fi
cd 998.specrand
valgrind --tool=exp-bbv --bb-out-file=valgrind/bb.out.998specrand.ref --pc-out-file=valgrind/pc.998specrand.ref $SPEC/998.specrand/exe/specrand_base.x86 1255432124 234923 &> valgrind/998specrand_ref.out
wait
echo "- generated ref bbv"
cd ..

# 999.specrand
echo "999.specrand"
if [ ! -d 999.specrand ]
then
    mkdir -p 999.specrand/valgrind
fi
cd 999.specrand
valgrind --tool=exp-bbv --bb-out-file=valgrind/bb.out.999specrand.ref --pc-out-file=valgrind/pc.999specrand.ref $SPEC/999.specrand/exe/specrand_base.x86 1255432124 234923 &> valgrind/999specrand_ref.out
wait
echo "- generated ref bbv"
cd ..