import sys
import re
import os

# Use the built-in version of scandir/walk if possible, otherwise
# use the scandir module version
try:
    from os import scandir, walk
except ImportError:
    from scandir import scandir, walk

path = sys.argv[1]
weights = []
names = []
data = {}
max_cols = 0
col = 0

# Count the configurations (which will be one per column)
for root, dirs, files in os.walk(path):
    depth = root[len(path) + len(os.path.sep):].count(os.path.sep)
    if depth == 6:
        max_cols += 1

# Read all the stats.txt files and add the information to a dictionary
benchmarks = sorted([(f.name, f.path) for f in scandir(path) if f.is_dir()])
for b in benchmarks:
    sim_dir = os.path.join(b[1], "simulation")
    if os.path.isdir(sim_dir):
        subset = sorted([(f.name, f.path) for f in scandir(sim_dir) if f.is_dir()])
        for ss in subset:
            cpu = sorted([(f.name, f.path) for f in scandir(ss[1]) if f.is_dir()])
            for c in cpu:
                tech = sorted([(f.name, f.path) for f in scandir(c[1]) if f.is_dir()])
                for t in tech:
                    scenario = sorted([(f.name, f.path) for f in scandir(t[1]) if f.is_dir()])
                    for s in scenario:
                        subfolders = sorted([(f.name, f.path) for f in scandir(s[1]) if f.is_dir()])
                        for n in subfolders:
                            if n[0] == "full":
                                weights.append("1.000000")
                            else:
                                weights.append(n[0].split("weight_")[1].split("_interval")[0])
                            names.append(b[0] + "." + ss[0] + "." + c[0] + "." + t[0] + "." + s[0] + "." + n[0].split("_inst")[0])

                            in_file = open(os.path.join(n[1], "stats.txt"), "r")

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
                                            data[m] = ["NA" for sf in range(0, max_cols)]
                                        data[m][col] = parsed[1]

                            in_file.close()
                            col += 1
                            print(col)

out_file = open("parsed_stats.csv", "w+")

# Create header
out_file.write(',')
for i, n in enumerate(names):
    out_file.write(n)
    if i == len(names) - 1:
        out_file.write('\n')
    else:
        out_file.write(',')

# Print simpoint weights
out_file.write('sp_weight,')
for i, w in enumerate(weights):
    out_file.write(w)
    if i == len(weights) - 1:
        out_file.write('\n')
    else:
        out_file.write(',')

# Print data from stats.txt files
for key in sorted(data.keys()):
    out_file.write(key + ',')
    for i, value in enumerate(data[key]):
        out_file.write(value)
        if i == len(data[key]) - 1:
            out_file.write('\n')
        else:
            out_file.write(',')

out_file.close()
