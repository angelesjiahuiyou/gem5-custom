# Name of individual benchmarks
benchmarks = (
    "500.perlbench_r",
    "502.gcc_r",
    "503.bwaves_r",
    "505.mcf_r",
    "507.cactuBSSN_r",
    "508.namd_r",
    "510.parest_r",
    "511.povray_r",
    "519.lbm_r",
    "520.omnetpp_r",
    "521.wrf_r",
    "523.xalancbmk_r",
    "525.x264_r",
    "526.blender_r",
    "527.cam4_r",
    "531.deepsjeng_r",
    "538.imagick_r",
    "541.leela_r",
    "544.nab_r",
    "548.exchange2_r",
    "549.fotonik3d_r",
    "554.roms_r",
    "557.xz_r",
    "997.specrand_fr",
    "999.specrand_ir"
)

# If the executable binary name differs from the benchmark, note it here
exe_name = {
    "502.gcc_r"         : "cpugcc_r",
    "523.xalancbmk_r"   : "cpuxalan_r"

#    "482.sphinx3"       : "sphinx_livepretend",
#    "483.xalancbmk"     : "Xalan"
}

# Specify actions to take before launching benchmarks (from the perl (object.pm) script)
preprocessing = {
# TODO check 525, 511, 521, 526, 527, 538, 549 Done! but verify is there are problems
# Checked 525 (probably don't need any treatment, but there are extra functions apparently to fetch the parameters from the /data/[refrec|test|train]/input/control) file
# 511 (only fetching params perhamps)
# 521 (adds imagevalidate program, is it compulsory?)
# 526  same as 521
# 527  (adds cam4_validate program, is it compulsory?)
# 538  same as 521
# 549  sets for spec17/bin/specxz but not used the subroutine under invoke
##    "481.wrf"           : ("ln -s le/32/* .", "ln -s le/64/* ."),
##    "482.sphinx3"       : ("rm *.be.raw && for file in *.le.raw; do mv \"$file\" \"${file%.le.raw}.raw\"; done && wc -c $(ls *.raw) | awk -F\".raw\" \'{print $1}\' | awk \'{print $2 \" \" $1}\' | head -n -1 > ctlfile",
 ##                          "rm *.le.raw && for file in *.be.raw; do mv \"$file\" \"${file%.be.raw}.raw\"; done && wc -c $(ls *.raw) | awk -F\".raw\" \'{print $1}\' | awk \'{print $2 \" \" $1}\' | head -n -1 > ctlfile")
}


mem_size = {
# TODO not sure why is needed, gem5 memory size perhaps?
#    "434.zeusmp"        : 2,
#    "459.GemsFDTD"      : 4,
#    "465.tonto"         : 4,
#    "481.wrf"           : 4
}

# Define if there are several inputs for any benchmarks
subset = {
    "test" : {
        "500.perlbench_r"     : ("makerand", "test"),
        "503.bwaves_r"      : ("bwaves1", "bwaves2"),
        "557.xz_r"            :("1_0", "1_1", "1_2", "1_3e", "1_4", "1_4e", "4_0", "4_1", "4_2", "4_3e", "4_4", "4_4e", )

    },
    "train" : {
        "500.perlbench_r"   : ("diffmail", "perfect", "scrabbl", "splitmail", "suns"),
        "502.gcc_r"         :("200", "scilab", "train01"),
        "503.bwaves_r"     : ("bwaves1", "bwaves2"),
        "544.nab_r"         : ("aminos", "gcn4dna"),
        "557.xz_r"          :("combined", "IMG_2560")
    },
    "ref" : {
        # Yet to fill
        "500.perlbench_r"   :("checkspam", "diffmail", "splitmail"),
        "502.gcc_r"         :("gcc-ppo3", "gcc-ppo2", "gcc-smaller", "ref32o5", "ref32o3"),
        "503.bwaves_r"      : ("bwaves1", "bwaves2", "bwaves3", "bwaves4"),
        "525.x264_r"        :("pass1", "pass2", "seek"),
        "557.xz_r"          :("cld", "cpu2006docs", "combined")

    }
}

# Provide all the parameters needed for each execution
params = {
# Test runs
    "test" : {
        "500.perlbench_r" : ("-I. -I./lib makerand.pl", "-I. -I./lib test.pl"),
        "502.gcc_r"       : ("t1.c -O3 -finline-limit=50000 -o t1.opts-O3_-finline-limit_50000.s"),
        "503.bwaves_r"    : ("bwaves_1", "bwaves_2"),
        "505.mcf_r"       : ("inp.in"),
        "507.cactuBSSN_r" : ("spec_test.par"),
        "508.namd_r"      : ("--input apoa1.input --iterations 1 --output apoa1.test.output"),
        "510.parest_r"    : ("test.prm"),
        "511.povray_r"    : ("SPEC-benchmark-test.ini"),
        "519.lbm_r"       : ("20 reference.dat 0 1 100_100_130_cf_a.of"),
        "520.omnetpp_r"   : ("-c General -r 0"), 
##        "520.omnetpp_r"   : ("omnetpp.ini"), TODO this file exists as in spec2006
        "523.xalancbmk_r" : ("-v test.xml xalanc.xsl"),
        "525.x264_r"      : ("--dumpyuv 50 --frames 156 -o BuckBunny_New.264 BuckBunny.yuv 1280x720"),
        "526.blender_r"   : ("cube.blend --render-output cube_ --threads 1 -b -F RAWTGA -s 1 -e 1 -a"),
        "531.deepsjeng_r" : ("test.txt"),
        "538.imagick_r"   : ("-limit disk 0 test_input.tga -shear 25 -resize 640x480 -negate -alpha Off test_output.tga"),
        "541.leela_r"     : ("test.sgf"),
        "544.nab_r"       : ("hkrdenq 1930344093 1000"),
        "548.exchange2_r" : ("0"),
        "557.xz_r"        : ("cpu2006docs.tar.xz 1 055ce243071129412e9dd0b3b69a21654033a9b723d874b2015c774fac1553d9713be561ca86f74e4f16f22e664fc17a79f30caa5ad2c04fbc447549c2810fae 650156 -1 0",
                             "cpu2006docs.tar.xz 1 055ce243071129412e9dd0b3b69a21654033a9b723d874b2015c774fac1553d9713be561ca86f74e4f16f22e664fc17a79f30caa5ad2c04fbc447549c2810fae 639996 -1 1",
                             "cpu2006docs.tar.xz 1 055ce243071129412e9dd0b3b69a21654033a9b723d874b2015c774fac1553d9713be561ca86f74e4f16f22e664fc17a79f30caa5ad2c04fbc447549c2810fae 637616 -1 2",
                             "cpu2006docs.tar.xz 1 055ce243071129412e9dd0b3b69a21654033a9b723d874b2015c774fac1553d9713be561ca86f74e4f16f22e664fc17a79f30caa5ad2c04fbc447549c2810fae 628996 -1 3e",
                             "cpu2006docs.tar.xz 1 055ce243071129412e9dd0b3b69a21654033a9b723d874b2015c774fac1553d9713be561ca86f74e4f16f22e664fc17a79f30caa5ad2c04fbc447549c2810fae 631912 -1 4",
                             "cpu2006docs.tar.xz 1 055ce243071129412e9dd0b3b69a21654033a9b723d874b2015c774fac1553d9713be561ca86f74e4f16f22e664fc17a79f30caa5ad2c04fbc447549c2810fae 629064 -1 4e",
                             "cpu2006docs.tar.xz 4 055ce243071129412e9dd0b3b69a21654033a9b723d874b2015c774fac1553d9713be561ca86f74e4f16f22e664fc17a79f30caa5ad2c04fbc447549c2810fae 1548636 1555348 0",
                             "cpu2006docs.tar.xz 4 055ce243071129412e9dd0b3b69a21654033a9b723d874b2015c774fac1553d9713be561ca86f74e4f16f22e664fc17a79f30caa5ad2c04fbc447549c2810fae 1462248 -1 1",
                             "cpu2006docs.tar.xz 4 055ce243071129412e9dd0b3b69a21654033a9b723d874b2015c774fac1553d9713be561ca86f74e4f16f22e664fc17a79f30caa5ad2c04fbc447549c2810fae 1428548 -1 2",
                             "cpu2006docs.tar.xz 4 055ce243071129412e9dd0b3b69a21654033a9b723d874b2015c774fac1553d9713be561ca86f74e4f16f22e664fc17a79f30caa5ad2c04fbc447549c2810fae 1034828 -1 3e",
                             "cpu2006docs.tar.xz 4 055ce243071129412e9dd0b3b69a21654033a9b723d874b2015c774fac1553d9713be561ca86f74e4f16f22e664fc17a79f30caa5ad2c04fbc447549c2810fae 1061968 -1 4",
                             "cpu2006docs.tar.xz 4 055ce243071129412e9dd0b3b69a21654033a9b723d874b2015c774fac1553d9713be561ca86f74e4f16f22e664fc17a79f30caa5ad2c04fbc447549c2810fae 1034588 -1 4e"),
         "997.specrand_fr": ("324342 24239"),
         "999.specrand_ir": ("324342 24239")

    },
# Train runs
    "train" : {
        "500.perlbench_r" : ("-I./lib diffmail.pl 2 550 15 24 23 100", "-I./lib perfect.pl b 3", "-I. -I./lib scrabbl.pl", "-I./lib splitmail.pl 535 13 25 24 1091 1", "-I. -I./lib suns.pl"),
        "502.gcc_r"       : ("200.c -O3 -finline-limit=50000 -o 200.opts-O3_-finline-limit_50000.s",
                             "scilab.c -O3 -finline-limit=50000 -o scilab.opts-O3_-finline-limit_50000.s",
                             "train01.c -O3 -finline-limit=50000 -o train01.opts-O3_-finline-limit_50000.s"
                            ),
        "503.bwaves_r"    : ("bwaves_1", "bwaves_2"),
        "505.mcf_r"       : ("inp.in"),
        "507.cactuBSSN_r" : ("spec_train.par"),
        "508.namd_r"      : ("--input apoa1.input --iterations 7 --output apoa1.train.output"),
        "510.parest_r"    : ("train.prm"),
        "511.povray_r"    : ("SPEC-benchmark-train.ini"),
        "519.lbm_r"       : ("300 reference.dat 0 1 100_100_130_cf_b.of"),
        "520.omnetpp_r"   : ("-c General -r 0"),
##        "520.omnetpp_r"   : ("omnetpp.ini"), TODO this file exists as in spec2006
        "523.xalancbmk_r" : ("-v allbooks.xml xalanc.xsl "),
        "525.x264_r"      : ("--dumpyuv 50 --frames 142 -o BuckBunny_New.264 BuckBunny.yuv 1280x720"),
        "526.blender_r"   : ("sh5_reduced.blend --render-output sh5_reduced_ --threads 1 -b -F RAWTGA -s 234 -e 234 -a"),
        "531.deepsjeng_r" : ("train.txt"),
        "538.imagick_r"   : ("-limit disk 0 train_input.tga -resize 320x240 -shear 31 -edge 140 -negate -flop -resize 900x900 -edge 10 train_output.tga"),
        "541.leela_r"     : ("train.sgf"),
        "544.nab_r"       : ("aminos 391519156 1000", "gcn4dna 1850041461 300"),
        "548.exchange2_r" : ("1"),
        "557.xz_r"        : ("input.combined.xz 40 a841f68f38572a49d86226b7ff5baeb31bd19dc637a922a972b2e6d1257a890f6a544ecab967c313e370478c74f760eb229d4eef8a8d2836d233d3e9dd1430bf 6356684 -1 8",
                             "IMG_2560.cr2.xz 40 ec03e53b02deae89b6650f1de4bed76a012366fb3d4bdc791e8633d1a5964e03004523752ab008eff0d9e693689c53056533a05fc4b277f0086544c6c3cbbbf6 40822692 40824404 4",
                            ),
         "997.specrand_fr": ("1 11"),
         "999.specrand_ir": ("1 11")

    },
# Reference runs
    "ref" : {
        "500.perlbench_r" : ("-I./lib checkspam.pl 2500 5 25 11 150 1 1 1 1", "-I./lib diffmail.pl 4 800 10 17 19 300", "-I./lib splitmail.pl 6400 12 26 16 100 0"),
        "502.gcc_r"       : ("gcc-pp.c -O3 -finline-limit=0 -fif-conversion -fif-conversion2 -o gcc-pp.opts-O3_-finline-limit_0_-fif-conversion_-fif-conversion2.s",
                             "gcc-pp.c -O2 -finline-limit=36000 -fpic -o gcc-pp.opts-O2_-finline-limit_36000_-fpic.s",
                             "gcc-smaller.c -O3 -fipa-pta -o gcc-smaller.opts-O3_-fipa-pta.s > gcc-smaller.opts-O3_-fipa-pta.out",
                             "ref32.c -O5 -o ref32.opts-O5.s",
                             "ref32.c -O3 -fselective-scheduling -fselective-scheduling2 -o ref32.opts-O3_-fselective-scheduling_-fselective-scheduling2.s"
                            ),
        "503.bwaves_r"    : ("bwaves_1", "bwaves_2", "bwaves_3", "bwaves_4"),
        "505.mcf_r"       : ("inp.in"),
        "507.cactuBSSN_r" : ("spec_ref.par"),
        "508.namd_r"      : ("--input apoa1.input --output apoa1.ref.output --iterations 65"),
        "510.parest_r"    : ("ref.prm"),
        "511.povray_r"    : ("SPEC-benchmark-ref.ini"),
        "519.lbm_r"       : ("3000 reference.dat 0 0 100_100_130_ldc.of"),
        "520.omnetpp_r"   : ("-c General -r 0"),
##        "520.omnetpp_r"   : ("omnetpp.ini"), TODO this file exists as in spec2006
        "523.xalancbmk_r" : ("-v t5.xml xalanc.xsl"),
        "525.x264_r"      : ("--pass 1 --stats x264_stats.log --bitrate 1000 --frames 1000 -o BuckBunny_New.264 BuckBunny.yuv 1280x720",
                             "--pass 2 --stats x264_stats.log --bitrate 1000 --dumpyuv 200 --frames 1000 -o BuckBunny_New.264 BuckBunny.yuv 1280x720",
                             "--seek 500 --dumpyuv 200 --frames 1250 -o BuckBunny_New.264 BuckBunny.yuv 1280x720"
                            ),
        "526.blender_r"   : ("sh3_no_char.blend --render-output sh3_no_char_ --threads 1 -b -F RAWTGA -s 849 -e 849 -a"),
        "531.deepsjeng_r" : ("ref.txt"),
        "538.imagick_r"   : ("-limit disk 0 refrate_input.tga -edge 41 -resample 181% -emboss 31 -colorspace YUV -mean-shift 19x19+15% -resize 30% refrate_output.tga	"),
        "541.leela_r"     : ("ref.sgf"),
        "544.nab_r"       : ("1am0 1122214447 122"),
        "548.exchange2_r" : ("6"),
        "557.xz_r"        : ("cld.tar.xz 160 19cf30ae51eddcbefda78dd06014b4b96281456e078ca7c13e1c0c9e6aaea8dff3efb4ad6b0456697718cede6bd5454852652806a657bb56e07d61128434b474 59796407 61004416 6",
                             "cpu2006docs.tar.xz 250 055ce243071129412e9dd0b3b69a21654033a9b723d874b2015c774fac1553d9713be561ca86f74e4f16f22e664fc17a79f30caa5ad2c04fbc447549c2810fae 23047774 23513385 6e",
                             "input.combined.xz 250 a841f68f38572a49d86226b7ff5baeb31bd19dc637a922a972b2e6d1257a890f6a544ecab967c313e370478c74f760eb229d4eef8a8d2836d233d3e9dd1430bf 40401484 41217675 7"
                            ),
         "997.specrand_fr": ("1255432124 234923"),
         "999.specrand_ir": ("1255432124 234923")

#        "998.specrand"      : "1255432124 234923",
#        "999.specrand"      : "1255432124 234923"
    }
}

# Parameters provided via redirection command: : "/.[benchmark] < param "
input = {
    "test" : {
        "503.bwaves_r"    : ("bwaves_1.in", "bwaves_2.in"),
        "554.roms_r"      : ("ocean_benchmark0.in.x"),

    },
    "train" : {
        "500.perlbench_r" : ("", "", "scrabbl.in", "", ""),
        "503.bwaves_r"    : ("bwaves_1.in", "bwaves_2.in"),
        "554.roms_r"      : ("ocean_benchmark1.in.x"),
    },
    "ref" : {
        "503.bwaves_r"    : ("bwaves_1.in", "bwaves_2.in", "bwaves_3.in", "bwaves_4.in"),
        "554.roms_r"      : ("ocean_benchmark2.in.x"),
    }
}

# TODO not need to ask for these benchmarks, since no longer here
def get_preprocessing(b_name, arch_bits, endianness):
    if b_name == "481.wrf":
        if arch_bits == 32:
            return preprocessing[b_name][0]
        else:
            return preprocessing[b_name][1]
    elif b_name == "482.sphinx3":
        if endianness == "le":
            return preprocessing[b_name][0]
        else:
            return preprocessing[b_name][1]

    return preprocessing.get(b_name)
