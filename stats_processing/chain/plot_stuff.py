import os
import sys
import pandas as pd
import matplotlib.pyplot as plt
benchmark_set = ('602', '605', '607', '623', '625', '628', '638', '641', '649', '654')
stats_files = []
names_vector = []
slowdown_vector = []
crop_vector = []
vlines = []
vlines_count = 0

if len(sys.argv) < 1:
    print("fatal: you need at least one file")
    exit(1)
for i in range(1, len(sys.argv)):
    stats_files.append(sys.argv[i])
 
for f in sorted(stats_files):
    data = pd.read_csv(f, index_col=0)
    if "rel_slowdown" in data.index:
        names_vector.append(os.path.basename(f).replace("slowdown_", "").replace(".csv", "").replace("_", " "))
        slowdown_vector.append(data.loc['rel_slowdown'])
        crop_vector.append(data.filter(like='605', axis=1).loc['rel_slowdown'])

        if not vlines_count:
            for f in benchmark_set[:-1]:
                num_cpts = len(data.filter(like=f, axis=1).loc['rel_slowdown'])
                if num_cpts:
                    vlines_count += num_cpts
                    vlines.append(vlines_count)

# All the points
plt.figure(figsize=(20,5))
plt.xlabel('Simulation point - Full benchmark set')
plt.ylabel('Relative slowdown')
for i, n in enumerate(names_vector):
    plt.plot(range(0, len(slowdown_vector[i])), slowdown_vector[i])
for v in vlines:
    plt.axvline(x=v, color='k', linestyle='--')
plt.legend(names_vector)
plt.margins(x=0)
plt.show()

# 605.mcf
plt.figure(figsize=(10,5))
plt.xlabel('Simulation point - 605.mcf')
plt.ylabel('Relative slowdown')
for i, n in enumerate(names_vector):
    plt.plot(range(0, len(crop_vector[i])), crop_vector[i])
plt.legend(names_vector)
plt.margins(x=0)
plt.show()
    