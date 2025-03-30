#!/usr/bin/env python3
import os
import sys
from colour import Color
from itertools import repeat
import numpy as np
import pandas as pd
import seaborn as sns
from scipy import stats
import matplotlib.pyplot as plt
from collections import Counter
files = []

if sys.version_info[0] < 3:
    raise Exception("Python 3 or a more recent version is required.")

if len(sys.argv) < 1:
    print("fatal: you need at least one file")
    exit(1)
for i in range(1, len(sys.argv)):
    files.append(sys.argv[i])

if not os.path.isdir("figs"):
    os.makedirs("figs")
if not os.path.isdir("timelapse"):
    os.makedirs("timelapse")

for f in sorted(files):
    code = os.path.basename(f).rsplit('_', 1)[0]
    plotname = os.path.basename(f).replace('.txt', '')
    data = pd.read_csv(f, sep=';')
    data.columns = ['tick', 'bkid', 'tgtblk', 'busyblk', 'perbank', 'glob', 'pc', 'type']
    sys.stdout = open(os.path.join("figs", code + ".log"), "w")

    # Set time window
    #data = data[(data['tick'] <= 2140174632687) & (data['tick'] >= 2101792545027)]
    #code = code + "_window"

    blocks_unsorted = list(set().union(data['tgtblk'], data['busyblk']))
    blocks = sorted([b / 64 for b in blocks_unsorted])

    plt.figure(figsize=(16,8))
    plt.subplot(2, 1, 1)
    #plt.hist(data['perbank'], bins=len(set(data['perbank'])))
    plt.hist(data['perbank'], range=(0, 1000), bins=1000)
    #plt.autoscale(enable=True, axis='y', tight=True)
    plt.xlabel('Accesses to other blocks - per bank')
    plt.ylabel('Frequency')
    plt.subplot(2, 1, 2)
    #plt.hist(data['glob'], bins=len(set(data['glob'])))
    plt.hist(data['glob'], range=(0, 5000), bins=5000)
    #plt.autoscale(enable=True, axis='y', tight=True)
    plt.xlabel('Accesses to other blocks - global')
    plt.ylabel('Frequency')
    plt.tight_layout(pad=4)
    plt.savefig(os.path.join("figs", code + "_conflicts_otheracs.png"))
    plt.close()
    print("TEMPORAL LOCALITY")
    print("-----------------")
    print("Peaks per bank:")
    peak_list = Counter(data['perbank']).most_common(5)
    print(peak_list)
    print("Peaks globally:")
    peak_list = Counter(data['glob']).most_common(5)
    print(peak_list)
    print("")

    """
    peak_min = 130
    peak_max = 132
    data_pk = data[(data['perbank'] <= peak_max) & (data['perbank'] >= peak_min)]
    plt.figure(figsize=(16,8))
    for bank in range(4):
        plt.subplot(4, 1, bank + 1)
        pk_blocks = data_pk.loc[data_pk['bkid'] == bank]['tgtblk']
        plt.hist(pk_blocks, bins=len(set(pk_blocks)), rwidth=0.8)
        plt.xticks(rotation='vertical')
    plt.tight_layout(pad=0.5)
    plt.savefig(os.path.join("figs", code + "_conflicts_atpeak.png"))
    """

    x = [b / 64 for b in data['tgtblk']]
    y = [b / 64 for b in data['busyblk']]
    x_compact = [blocks.index(b) for b in x]
    y_compact = [blocks.index(b) for b in y]
    diff = [elx - ely for elx, ely in zip(x, y)]

    xy = np.vstack([x, y])
    z = stats.gaussian_kde(xy)(xy)
    plt.figure(figsize=(8,8))
    plt.scatter(x, y, c=z, s=8, edgecolor='')
    plt.xlabel("Target block (at bank conflict)")
    plt.ylabel("Block being written")
    plt.tight_layout(pad=4)
    plt.savefig(os.path.join("figs", code + "_pairs.png"))
    plt.close()

    xy_compact = np.vstack([x_compact, y_compact])
    z_compact = stats.gaussian_kde(xy_compact)(xy_compact)
    plt.figure(figsize=(8,8))
    plt.scatter(x_compact, y_compact, c=z_compact, s=8, edgecolor='')
    plt.xlabel("Target block (at bank conflict) - no distance")
    plt.ylabel("Block being written - no distance")
    plt.tight_layout(pad=4)
    plt.savefig(os.path.join("figs", code + "_pairs_compact.png"))
    plt.close()

    blue = Color("blue")
    colors = list(blue.range_to(Color("red"), len(x)))
    colors = [c.hex for c in colors]
    f, (a0, a1) = plt.subplots(2, 1, figsize=(8,8), gridspec_kw={'height_ratios': [10, 1]})
    a0.scatter(x_compact, y_compact, c=colors, s=8, edgecolor='')
    a0.set_xlabel("Target block (at bank conflict) - no distance")
    a0.set_ylabel("Block being written - no distance")
    ones = list(repeat(1, len(colors)))
    a1.bar(range(len(colors)), ones, width=1, color=colors)
    a1.axis("off")
    f.tight_layout(pad=2)
    f.savefig(os.path.join("figs", code + "_pairs_compact_colors.png"))
    plt.close()

    plt.figure(figsize=(8,8))
    sns.distplot(data['tick'] / 1000000000)
    plt.xlabel("Time (ms)")
    plt.ylabel("Conflict distribution")
    plt.tight_layout(pad=4)
    plt.savefig(os.path.join("figs", code + "_timedist.png"))
    plt.close()

    plt.figure(figsize=(8,8))
    plt.hist(diff, range=(-2000000, 2000000), bins=len(set(diff)))
    plt.autoscale(enable=True, axis='y', tight=True)
    plt.xlabel("Distance")
    plt.ylabel("Frequency")
    plt.tight_layout(pad=4)
    plt.savefig(os.path.join("figs", code + "_distance.png"))
    plt.close()
    print("SPATIAL LOCALITY")
    print("----------------")
    for dist in [i * 4 for i in range(4)]:
        count = len([i for i in diff if i == dist])
        print("Percentage of conflicts with distance", dist, ":", count / len(diff) * 100, "%")
    print("Conflict distance peaks:")
    peak_list = Counter(diff).most_common(5)
    print(peak_list)

    """
    for i in range(100):
        plt.figure(figsize=(8,8))
        plt.scatter(x[:i], y[:i], s=8)
        plt.xlabel("Target block (at bank conflict)")
        plt.ylabel("Block being written")
        plt.tight_layout(pad=4)
        plt.savefig(os.path.join("timelapse", str(i) + ".png"))
        plt.close()
    """

    sys.stdout.close()
