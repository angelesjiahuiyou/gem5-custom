import os
import sys
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
benchmark_set = ('602.gcc_s', '605.mcf_s', '607.cactuBSSN_s', '623.xalancbmk_s', '625.x264_s', '628.pop2_s', '638.imagick_s', '641.leela_s', '649.fotonik3d_s', '654.roms_s')
stats_files = []
names = []
ticks_train = []
data_train = []
vlines_train = []
vlines_count_train = 0
cpt_weight_train = []

if len(sys.argv) < 1:
    print("fatal: you need at least one file")
    exit(1)
for i in range(1, len(sys.argv)):
    stats_files.append(sys.argv[i])
 
for f in sorted(stats_files):
    data = pd.read_csv(f, index_col=0)
    if "rel_ticks" in data.index:
        names.append(os.path.basename(f).replace("rel_ticks", "").replace(".csv", "").replace("_", " "))
        data_train = data.filter(like='train.', axis=1)
        ticks_train.append(data_train.loc['rel_ticks'])
        cpt_weight_train.append(data_train.loc['cpt_weight'])
        if not vlines_count_train:
            for f in benchmark_set[:-1]:
                num_cpts = len(data_train.filter(like=f, axis=1).loc['rel_ticks'])
                if num_cpts:
                    vlines_count_train += num_cpts
                    vlines_train.append((f.split('.')[0], vlines_count_train))
legend = [n.split()[1].split('-')[-1] for n in names]

# Ticks - Train
plt.xlabel('Simulation point - Train')
plt.ylabel('Relative execution time vs. SRAM cache')
for i, n in enumerate(names):
    ax = plt.gca()
    color=next(ax._get_lines.prop_cycler)['color']
    plt.plot(range(0, len(ticks_train[i])), ticks_train[i], color=color)
old_value = 0
for v in vlines_train:
    plt.axvline(x=v[1], color='k', linestyle='--')
    plt.text((v[1]+old_value)/2-4,plt.ylim()[1]+plt.ylim()[1]*0.02,v[0])
    old_value = v[1]
plt.text((len(ticks_train[0])+old_value)/2-4.4,plt.ylim()[1]+plt.ylim()[1]*0.02,'654')
plt.legend(legend, loc="upper right")
plt.margins(x=0)
plt.tight_layout(pad=4)
plt.show()
