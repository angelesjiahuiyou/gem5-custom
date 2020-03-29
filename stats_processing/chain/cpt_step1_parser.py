from joblib import Parallel, parallel_backend, delayed
import multiprocessing
import sys
import re
import os

# Use the built-in version of scandir/walk if possible, otherwise
# use the scandir module version
try:
    from os import scandir, walk
except ImportError:
    from scandir import scandir, walk

cpu2017 = {
    "int":  ('602.gcc_s', '605.mcf_s', '623.xalancbmk_s', '625.x264_s', '641.leela_s'),
    "fp":   ('607.cactuBSSN_s', '628.pop2_s', '638.imagick_s', '649.fotonik3d_s', '654.roms_s')
}

# Parsing function
def process(file_list, cm, t, s, it):
    # Create empty support structures
    data     = {}
    weights  = []
    names    = []

    benchlist = cpu2017.get(it)
    target_list = [x for x in sorted(file_list) if cm in x and t in x and s in x and any(elm in x for elm in benchlist)]
    if target_list:
        for i, stats_path in enumerate(target_list):
            params = stats_path.split("/")
            b  = params[1]
            ss = params[3]
            c  = params[4]
            n  = params[7]

            if n == "full":
                weights.append("1.000000")
            else:
                weights.append(n.split("weight_")[1].split("_interval")[0])
            names.append(b + "." + ss + "." + c + "." + n.split("_inst")[0])

            in_file = open(os.path.join(base_path, stats_path), "r")

            sections = 0
            count_begins = 0

            # Count how many "begins" there are in the file
            for line in in_file.readlines():
                parsed = re.sub('\s+',',',line).split(',')
                if parsed[1].find("Begin") != -1:
                    sections += 1

            in_file.seek(0)
            for line in in_file.readlines():
                parsed = re.sub('\s+',',',line).split(',')
                if count_begins != sections:
                    if parsed[1].find("Begin") != -1:
                        count_begins += 1
                else:
                    if parsed[0].find("---") == -1 and parsed[0] != "":
                        m = parsed[0].replace("switch_cpus", "cpu")
                        if m not in data:
                            data[m] = ["N/A" for sf in range(0, len(target_list))]
                        data[m][i] = parsed[1]
            in_file.close()

        # Create the output file
        raw_file = open(os.path.join(out_dir, "raw_stats_" + it + "_" + cm + "_" + t + "_" + s + ".csv"), "w+")

        # Create header
        raw_file.write(',')
        for i, n in enumerate(names):
            raw_file.write(n)
            if i == len(names) - 1:
                raw_file.write('\n')
            else:
                raw_file.write(',')

        # Print simpoint weights
        raw_file.write('cpt_weight,')
        for i, w in enumerate(weights):
            raw_file.write(w)
            if i == len(weights) - 1:
                raw_file.write('\n')
            else:
                raw_file.write(',')

        # Print data from stats.txt files
        for key in sorted(data.keys()):
            raw_file.write(key + ',')
            for i, value in enumerate(data[key]):
                raw_file.write(value)
                if i == len(data[key]) - 1:
                    raw_file.write('\n')
                else:
                    raw_file.write(',')

        # Close the output file
        raw_file.close()


# Main program
base_path = sys.argv[1]
file_list = []

# List of parameters for separating the output data files
cpumodels = []
technologies = []
scenarios = []

out_dir = "step1"
if not os.path.isdir(out_dir):
    os.mkdir(out_dir)

# Scan the data folder to collect information about the files to read
for root, dirs, files in os.walk(base_path):
    for name in files:
        if name == "stats.txt":
            stats_path = os.path.join(os.path.relpath(root, base_path), name)
            params = stats_path.split("/")

            # Safety check
            if (len(params) == 9 and
                params[2] == "simulation" and
                not "err_" in params[7] and
                (any(params[1] in cpu2017.get(key) for key in cpu2017.keys()))):
                file_list.append(stats_path)

                if params[4] not in cpumodels:
                    cpumodels.append(params[4])
                if params[5] not in technologies:
                    technologies.append(params[5])
                if params[6] not in scenarios:
                    scenarios.append(params[6])

if not any(file_list):
    print("No files to process. Exiting")
    sys.exit(1)
else:
    print("Processing " + str(len(file_list)) + " files...")

with parallel_backend('multiprocessing', n_jobs=multiprocessing.cpu_count()):
    Parallel()(delayed(process)(file_list, cm, t, s, it) for cm in cpumodels for t in technologies for s in scenarios for it in cpu2017.keys())
