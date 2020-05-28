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

if sys.version_info[0] < 3:
    raise Exception("Python 3 or a more recent version is required.")

if len(sys.argv) != 3:
    print("fatal: you need exactly two files")
    exit(1)

if not os.path.isdir("distribution"):
    os.makedirs("distribution")

_, trace, stats = sys.argv
code = os.path.basename(trace).rsplit('_', 1)[0]
plotname = os.path.basename(trace).replace('.txt', '')
data = pd.read_csv(trace, sep=';')
data.columns = ['tick', 'bkid', 'tgtblk', 'busyblk', 'perbank', 'glob', 'pc', 'type']

# Set time window
#data = data[(data['tick'] <= 2140174632687) & (data['tick'] >= 2101792545027)]
#code = code + "_window"

blocks_unsorted = list(set().union(data['tgtblk'], data['busyblk']))
blocks = sorted([int(b, 16) / 64 for b in blocks_unsorted])

time = []
ipc = []
softpf_hits = []
l2_accesses = []
iqfull = []
conflicts = []

with open(stats, 'r') as f:
    for line in f:
        if line.startswith("final_tick"):
            time.append(int(line.split()[1]))
        if line.startswith("system.switch_cpus.ipc"):
            ipc.append(float(line.split()[1]))
        if line.startswith("system.cpu.dcache.SoftPFReq_hits::total"):
            softpf_hits.append(float(line.split()[1]))
        if line.startswith("system.l2cache.ReadExReq_accesses::total"):
            l2_accesses.append(float(line.split()[1]))
        """if line.startswith("system.cpu.rename.IQFullEvents"):
            iqfull.append(float(line.split()[1]))"""
        if line.startswith("system.l2cache.bank_blocked_reqs_cpusp_write::total"):
            conflicts.append(float(line.split()[1]))

# Convert ticks to ms and crop conflict trace
conflict_time = data['tick'][lambda x: x >= time[0]] / 1000000000
time = [t / 1000000000 for t in time]

fig, ax1 = plt.subplots(figsize=(8,8))
color = 'tab:blue'
sns.distplot(conflict_time, ax=ax1, color=color)
ax1.set_xlabel('time (ms)')
ax1.set_ylabel('conflict distribution', color=color)
ax1.tick_params(axis='y', labelcolor=color)
ax2 = ax1.twinx()  # instantiate a second axes that shares the same x-axis
color = 'tab:red'
ax2.set_ylabel('ipc', color=color)  # we already handled the x-label with ax1
ax2.plot(time, ipc, color=color)
ax2.tick_params(axis='y', labelcolor=color)
fig.tight_layout()  # otherwise the right y-label is slightly clipped
plt.savefig(os.path.join("distribution", code + "_ipc.png"))

fig, ax1 = plt.subplots(figsize=(8,8))
color = 'tab:blue'
sns.distplot(conflict_time, ax=ax1, color=color)
ax1.set_xlabel('time (ms)')
ax1.set_ylabel('conflict distribution', color=color)
ax1.tick_params(axis='y', labelcolor=color)
ax2 = ax1.twinx()  # instantiate a second axes that shares the same x-axis
color = 'tab:red'
ax2.set_ylabel('dcache.SoftPFReq_hits', color=color)  # we already handled the x-label with ax1
ax2.plot(time, softpf_hits, color=color)
ax2.tick_params(axis='y', labelcolor=color)
fig.tight_layout()  # otherwise the right y-label is slightly clipped
plt.savefig(os.path.join("distribution", code + "_softpf.png"))

fig, ax1 = plt.subplots(figsize=(8,8))
color = 'tab:blue'
sns.distplot(conflict_time, ax=ax1, color=color)
ax1.set_xlabel('time (ms)')
ax1.set_ylabel('conflict distribution', color=color)
ax1.tick_params(axis='y', labelcolor=color)
ax2 = ax1.twinx()  # instantiate a second axes that shares the same x-axis
color = 'tab:red'
ax2.set_ylabel('l2cache.ReadExReq_accesses', color=color)  # we already handled the x-label with ax1
ax2.plot(time, l2_accesses, color=color)
ax2.tick_params(axis='y', labelcolor=color)
fig.tight_layout()  # otherwise the right y-label is slightly clipped
plt.savefig(os.path.join("distribution", code + "_l2acc.png"))

"""
fig, ax1 = plt.subplots(figsize=(8,8))
color = 'tab:blue'
sns.distplot(conflict_time, ax=ax1, color=color)
ax1.set_xlabel('time (ms)')
ax1.set_ylabel('conflict distribution', color=color)
ax1.tick_params(axis='y', labelcolor=color)
ax2 = ax1.twinx()  # instantiate a second axes that shares the same x-axis
color = 'tab:red'
ax2.set_ylabel('system.cpu.rename.IQFullEvents', color=color)  # we already handled the x-label with ax1
ax2.plot(time, iqfull, color=color)
ax2.tick_params(axis='y', labelcolor=color)
fig.tight_layout()  # otherwise the right y-label is slightly clipped
plt.savefig(os.path.join("distribution", code + "_iqfull.png"))
"""

fig, ax1 = plt.subplots(figsize=(8,8))
color = 'tab:blue'
sns.distplot(conflict_time, ax=ax1, color=color)
ax1.set_xlabel('time (ms)')
ax1.set_ylabel('conflict distribution', color=color)
ax1.tick_params(axis='y', labelcolor=color)
ax2 = ax1.twinx()  # instantiate a second axes that shares the same x-axis
color = 'tab:red'
ax2.set_ylabel('system.l2.bank_blocked_reqs_cpusp_write::total', color=color)  # we already handled the x-label with ax1
ax2.plot(time, conflicts, color=color)
ax2.tick_params(axis='y', labelcolor=color)
fig.tight_layout()  # otherwise the right y-label is slightly clipped
plt.savefig(os.path.join("distribution", code + "_conflicts.png"))
