#!/usr/bin/env python3
import os
import sys
import re
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from collections import Counter
console = sys.stdout
conflict_traces = []

if sys.version_info[0] < 3:
    raise Exception("Python 3 or a more recent version is required.")

if len(sys.argv) < 2:
    print("fatal: you need at least one file")
    exit(1)
for i in range(1, len(sys.argv)):
    conflict_traces.append(sys.argv[i])

if not os.path.isdir("memory"):
    os.makedirs("memory")

for trace in sorted(conflict_traces):
    sys.stdout = console
    print("- Processing", trace, "...")
    code = os.path.basename(trace).split('.')[0]
    benchnum = code[:3]
    data = pd.read_csv(trace, sep=';')
    data.columns = ['tick', 'bkid', 'tgtblk', 'busyblk', 'perbank', 'glob', 'pc', 'tgtmemreg', 'updmemreg', 'type']
    sys.stdout = open(os.path.join("memory", code + ".log"), "w")

    # Set time window
    #data = data[(data['tick'] <= 2140174632687) & (data['tick'] >= 2101792545027)]
    #code = code + "_window"

    blocks_unsorted = list(set().union(data['tgtblk'], data['busyblk']))
    blocks = sorted([int(b, 16) / 64 for b in blocks_unsorted])

    for i in Counter(data['type']).most_common(3):
        print(str(i[0]))
        print("Total:\t\t\t\t", i[1]),
        print("Target block in stack:\t\t", len(data[(data['type'] == i[0]) & (data['tgtmemreg'] == 1)]))
        print("Target block out of stack:\t", len(data[(data['type'] == i[0]) & (data['tgtmemreg'] == 0)]))
        print("Update block in stack:\t\t", len(data[(data['type'] == i[0]) & (data['updmemreg'] == 1)]))
        print("Update block out of stack:\t", len(data[(data['type'] == i[0]) & (data['updmemreg'] == 0)]))
        print("Either block in stack:\t\t", len(data[(data['type'] == i[0]) & ((data['tgtmemreg'] == 1) | (data['updmemreg'] == 1))]))
        print("")

    f_dict = {}
    print("Program counters:")
    with open(os.path.join("dumps", benchnum + "_disassembly.txt"), 'r') as f:
        for i in Counter(data['pc']).most_common(10):
            f.seek(0)
            function = ""
            pc = int(i[0], 16)
            for line in f:
                if re.match(r'\S', line):
                    function = line.split()[1][:-1]
                elif line.strip() and re.match(r'\s', line) and len(line.split()) > 1 and int(line.split()[0][:-1], 16) == pc:
                    break
            if function not in f_dict:
                f_dict[function] = i[1]
            else:
                f_dict[function] = f_dict[function] + i[1]
            print(i[0], "\t\t", i[1])
    print("")

    print("Functions:")
    f_dict = {k: v for k, v in sorted(f_dict.items(), key=lambda item: item[1], reverse=True)}
    max_len = max([len(s) for s in f_dict]) + 5
    for i in f_dict:
        print(f"{i:<{max_len}}{f_dict[i]:<10}")
    print("")

    ranges = {}
    confl_per_sec = {}
    with open(os.path.join("dumps", benchnum + "_sections.txt"), 'r') as f:
        for line in f:
            if re.match(r'\s*\[\s*\d+\]', line):
                no_index = re.split(r'\s*\[\s*\d+\]', line)[1].split()
                if no_index[0] != "NULL" and int(no_index[2], 16) != 0:
                    ranges[no_index[0]] = (int(no_index[2], 16), int(no_index[2], 16) + int(no_index[4], 16))

    for i, row in data.iterrows():
        section = "(unknown)"
        for r in ranges:
            tgtblk = int(row['tgtblk'], 16)
            tgtmemreg = int(row['tgtmemreg'])
            if tgtmemreg == 1:
                section = "stack"
            elif tgtmemreg == 2:
                section = "mmap"
            elif tgtmemreg == 3:
                section = "heap"
            elif tgtblk >= ranges[r][0] and tgtblk < ranges[r][1]:
                section = r
                break
        if section not in confl_per_sec:
            confl_per_sec[section] = 1
        else:
            confl_per_sec[section] = confl_per_sec[section] + 1

    print("Target data regions:")
    confl_per_sec = {k: v for k, v in sorted(confl_per_sec.items(), key=lambda item: item[1], reverse=True)}
    max_len = max([len(s) for s in confl_per_sec]) + 5
    for i in confl_per_sec:
        print(f"{i:<{max_len}}{confl_per_sec[i]:<10}")
    print("")

    conflict_time_reads = data[data['type'] == "WritebackDirty"]['tick'] / 1000000000
    conflict_time_writes = data[data['type'] != "WritebackDirty"]['tick'] / 1000000000

    fig, ax1 = plt.subplots(figsize=(8,8))
    color = 'tab:blue'
    sns.distplot(conflict_time_reads, ax=ax1, color=color)
    ax1.set_xlabel('time (ms)')
    ax1.set_ylabel('conflict distribution - reads', color=color)
    ax1.tick_params(axis='y', labelcolor=color)
    ax2 = ax1.twinx()  # instantiate a second axes that shares the same x-axis
    color = 'tab:red'
    ax2.set_ylabel('conflict distribution - writes', color=color)  # we already handled the x-label with ax1
    sns.distplot(conflict_time_writes, ax=ax2, color=color)
    ax2.tick_params(axis='y', labelcolor=color)
    fig.tight_layout()  # otherwise the right y-label is slightly clipped
    plt.savefig(os.path.join("memory", code + "_rw.png"))
    plt.close()

    sys.stdout.close()
