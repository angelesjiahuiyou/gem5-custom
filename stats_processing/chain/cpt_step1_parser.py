import sys
import re
import os

# Use the built-in version of scandir/walk if possible, otherwise
# use the scandir module version
try:
    from os import scandir, walk
except ImportError:
    from scandir import scandir, walk

base_path = sys.argv[1]
file_list = []

# List of parameters for separating the output data files
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
            if (len(params) == 8 and params[1] == "simulation" and
                not "err_" in params[6]):
                file_list.append(stats_path)

                if params[4] not in technologies:
                    technologies.append(params[4])
                if params[5] not in scenarios:
                    scenarios.append(params[5])   

if not any(file_list):
    print("No files to process. Exiting")
    sys.exit(1)
else:
    print("Processing " + str(len(file_list)) + " files...")

for t in technologies:
    for s in scenarios:

        # Create empty support structures
        data     = {}
        data_flt = {}
        weights  = []
        names    = []

        target_list = [x for x in sorted(file_list) if t in x and s in x]
        if target_list:
            for i, stats_path in enumerate(target_list):
                params = stats_path.split("/")
                b  = params[0]
                ss = params[2]
                c  = params[3]
                n  = params[6]

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

            # Filtering
            for key in data:
                if not (data[key] == ["0" for sf in range(0, len(target_list))] or
                data[key] == ["inf" for sf in range(0, len(target_list))] or
                data[key] == ["nan" for sf in range(0, len(target_list))] or
                "final_tick" in key or
                "host_" in key or
                "avg" in key or
                "rate" in key or
                "ratio" in key or
                "cycles" in key or
                "overall_hit" in key or
                "overall_miss" in key or
                "overall_mshr" in key or
                "overall_accesses" in key or
                "::total" in key):
                    data_flt[key] = data[key]

            # Create the output file
            out_file = open(os.path.join(out_dir, "parsed_stats_" + t + "_" + s + ".csv"), "w+")

            # Create header
            out_file.write(',')
            for i, n in enumerate(names):
                out_file.write(n)
                if i == len(names) - 1:
                    out_file.write('\n')
                else:
                    out_file.write(',')

            # Print simpoint weights
            """ out_file.write('sp_weight,')
            for i, w in enumerate(weights):
                out_file.write(w)
                if i == len(weights) - 1:
                    out_file.write('\n')
                else:
                    out_file.write(',') """

            # Print data from stats.txt files
            for key in sorted(data_flt.keys()):
                out_file.write(key + ',')
                for i, value in enumerate(data_flt[key]):
                    out_file.write(value)
                    if i == len(data_flt[key]) - 1:
                        out_file.write('\n')
                    else:
                        out_file.write(',')

            out_file.close()
