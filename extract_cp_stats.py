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
data = {}

metrics = (
    "sim_insts",
    "sim_ticks",
    "ipc",
    "cpi",
    "overall_hits",
    "overall_misses",
    "overall_accesses",
    "overall_miss_rate",
    "overall_blocked_pkts",
    "overall_received_pkts",
    "blocked_pkts_ratio"
    #"l2cache.bank_blocked_cycles",
    #"l2cache.bank_blocked_reqs_cpusp_read",
    #"l2cache.bank_blocked_reqs_cpusp_write",
    #"l2cache.bank_blocked_reqs_memsp_mshr",
    #"l2cache.bank_blocked_retry_pkts",
    #"l2cache.bank_blocked_retry_ticks",
    #"l2cache.bank_blocked_ticks",
    #"l2cache.concurrent_banks_cycles",
    #"l2cache.concurrent_banks_ticks"
)

subfolders = sorted([f.path for f in scandir(path) if f.is_dir()])
names = sorted([f.name for f in scandir(path) if f.is_dir()])
names_short = [n.split("_inst")[0] for n in names]
for i, n in enumerate(names):
    if n == "full":
        weights.append("1.000000")
    else:
        weights.append(n.split("weight_")[1].split("_interval")[0])

for i, f in enumerate(subfolders):
    in_file = open(f + "/stats.txt", "r")

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
            for s in metrics:
                m = parsed[0].replace("switch_cpus", "cpu")
                if m.find(s) != -1:
                    if (m.find("::") == -1 or m.find("::total") != -1 or
                        m.find("concurrent_banks") != -1):
                        if m not in data:
                            data[m] = ["NA" for sf in subfolders]
                        data[m][i] = parsed[1]
    
    in_file.close()

out_file = open("parsed_stats.csv", "w+")

# Create header
out_file.write(',')
for i, n in enumerate(names_short):
    out_file.write(n)
    if i == len(names_short) - 1:
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
