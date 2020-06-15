import os
import sys
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from collections import OrderedDict
from matplotlib.ticker import ScalarFormatter
class ForceFormat(ScalarFormatter):
    def _set_format(self, vmin, vmax):
        self.format = "%1.1f"

benchmark_set = []
stats_files = []
legend = []
rel_ticks_test = []
rel_ticks_train = []
cpt_weight_test = []
cpt_weight_train = []
data_test = []
data_train = []
cpi_test = []
cpi_train = []
misses_l1_test = []
misses_l1_train = []
misses_l2_test = []
misses_l2_train = []
misses_l3_test = []
misses_l3_train = []
op_memrd_test = []
op_memwr_test = []
op_other_test = []
op_memrd_train = []
op_memwr_train = []
op_other_train = []
busyblk_cpuspwr_test = []
busyblk_cpusprd_test = []
busyblk_mshrfill_test = []
busyblk_cpuspwr_train = []
busyblk_cpusprd_train = []
busyblk_mshrfill_train = []
targetblk_cpuspwr_test = []
targetblk_cpusprd_test = []
targetblk_mshrfill_test = []
targetblk_cpuspwr_train = []
targetblk_cpusprd_train = []
targetblk_mshrfill_train = []
vlines_test = []
vlines_train = []
vlines_count_test = 0
vlines_count_train = 0

if len(sys.argv) < 1:
    print("fatal: you need at least one file")
    exit(1)
for i in range(1, len(sys.argv)):
    stats_files.append(sys.argv[i])

out_dir = "plots"
if not os.path.isdir(out_dir):
    os.mkdir(out_dir)

SMALL_SIZE = 10
MEDIUM_SIZE = 11
BIGGER_SIZE = 14
plt.rc('font', size=SMALL_SIZE)          # controls default text sizes
plt.rc('axes', titlesize=MEDIUM_SIZE)     # fontsize of the axes title
plt.rc('axes', labelsize=BIGGER_SIZE)    # fontsize of the x and y labels
plt.rc('xtick', labelsize=MEDIUM_SIZE)    # fontsize of the tick labels
plt.rc('ytick', labelsize=MEDIUM_SIZE)    # fontsize of the tick labels
plt.rc('legend', fontsize=MEDIUM_SIZE)    # legend fontsize
plt.rc('figure', titlesize=BIGGER_SIZE)  # fontsize of the figure title

# Plz don't ask
magic_number_test = 1
magic_number_train = 2

base_outpath = os.path.join(out_dir, os.path.basename(stats_files[0]).replace("slowdown_", "").replace(stats_files[0].split('_')[-1], ""))
for f in sorted(stats_files):
    data = pd.read_csv(f, index_col=0)
    if "rel_ticks" in data.index:
        legend.append(os.path.basename(f).split('_')[-1].split('.')[0])
        data_test = data.filter(like='test.', axis=1)
        data_train = data.filter(like='train.', axis=1)
        rel_ticks_test.append(data_test.loc['rel_ticks'])
        rel_ticks_train.append(data_train.loc['rel_ticks'])
        cpt_weight_test.append(data_test.loc['cpt_weight'])
        cpt_weight_train.append(data_train.loc['cpt_weight'])
        cpi_test.append(data_test.loc['system.cpu.cpi'])
        cpi_train.append(data_train.loc['system.cpu.cpi'])
        misses_l1_test.append(data_test.filter(regex='system.cpu.*cache.', axis=0).filter(like='_misses::', axis=0).filter(regex='^((?!mshr|demand).)*$', axis=0).sum())
        misses_l1_train.append(data_train.filter(regex='system.cpu.*cache.', axis=0).filter(like='_misses::', axis=0).filter(regex='^((?!mshr|demand).)*$', axis=0).sum())
        misses_l2_test.append(data_test.filter(like='system.l2cache.', axis=0).filter(like='_misses::', axis=0).filter(regex='^((?!mshr|demand).)*$', axis=0).sum())
        misses_l2_train.append(data_train.filter(like='system.l2cache.', axis=0).filter(like='_misses::', axis=0).filter(regex='^((?!mshr|demand).)*$', axis=0).sum())
        if "i7-6700" in os.path.basename(f):
            misses_l3_test.append(data_test.filter(like='system.l3cache.', axis=0).filter(like='_misses::', axis=0).filter(regex='^((?!mshr|demand).)*$', axis=0).sum())
            misses_l3_train.append(data_train.filter(like='system.l3cache.', axis=0).filter(like='_misses::', axis=0).filter(regex='^((?!mshr|demand).)*$', axis=0).sum())
            busyblk_cpusprd_test.append(data_test.filter(like='system.l3cache.bank_cfl_busyblk_cpusp_read_', axis=0).sum())
            busyblk_cpuspwr_test.append(data_test.filter(like='system.l3cache.bank_cfl_busyblk_cpusp_write_', axis=0).sum())
            busyblk_mshrfill_test.append(data_test.filter(like='system.l3cache.bank_cfl_busyblk_memsp_fill_', axis=0).sum())
            busyblk_cpusprd_train.append(data_train.filter(like='system.l3cache.bank_cfl_busyblk_cpusp_read_', axis=0).sum())
            busyblk_cpuspwr_train.append(data_train.filter(like='system.l3cache.bank_cfl_busyblk_cpusp_write_', axis=0).sum())
            busyblk_mshrfill_train.append(data_train.filter(like='system.l3cache.bank_cfl_busyblk_memsp_fill_', axis=0).sum())
            targetblk_cpusprd_test.append(data_test.filter(like='system.l3cache.bank_cfl_targetblk_cpusp_read_', axis=0).sum())
            targetblk_cpuspwr_test.append(data_test.filter(like='system.l3cache.bank_cfl_targetblk_cpusp_write_', axis=0).sum())
            targetblk_mshrfill_test.append(data_test.filter(like='system.l3cache.bank_cfl_targetblk_memsp_fill_', axis=0).sum())
            targetblk_cpusprd_train.append(data_train.filter(like='system.l3cache.bank_cfl_targetblk_cpusp_read_', axis=0).sum())
            targetblk_cpuspwr_train.append(data_train.filter(like='system.l3cache.bank_cfl_targetblk_cpusp_write_', axis=0).sum())
            targetblk_mshrfill_train.append(data_train.filter(like='system.l3cache.bank_cfl_targetblk_memsp_fill_', axis=0).sum())
        else:
            busyblk_cpusprd_test.append(data_test.filter(like='system.l2cache.bank_cfl_busyblk_cpusp_read_', axis=0).sum())
            busyblk_cpuspwr_test.append(data_test.filter(like='system.l2cache.bank_cfl_busyblk_cpusp_write_', axis=0).sum())
            busyblk_mshrfill_test.append(data_test.filter(like='system.l2cache.bank_cfl_busyblk_memsp_fill_', axis=0).sum())
            busyblk_cpusprd_train.append(data_train.filter(like='system.l2cache.bank_cfl_busyblk_cpusp_read_', axis=0).sum())
            busyblk_cpuspwr_train.append(data_train.filter(like='system.l2cache.bank_cfl_busyblk_cpusp_write_', axis=0).sum())
            busyblk_mshrfill_train.append(data_train.filter(like='system.l2cache.bank_cfl_busyblk_memsp_fill_', axis=0).sum())
            targetblk_cpusprd_test.append(data_test.filter(like='system.l2cache.bank_cfl_targetblk_cpusp_read_', axis=0).sum())
            targetblk_cpuspwr_test.append(data_test.filter(like='system.l2cache.bank_cfl_targetblk_cpusp_write_', axis=0).sum())
            targetblk_mshrfill_test.append(data_test.filter(like='system.l2cache.bank_cfl_targetblk_memsp_fill_', axis=0).sum())
            targetblk_cpusprd_train.append(data_train.filter(like='system.l2cache.bank_cfl_targetblk_cpusp_read_', axis=0).sum())
            targetblk_cpuspwr_train.append(data_train.filter(like='system.l2cache.bank_cfl_targetblk_cpusp_write_', axis=0).sum())
            targetblk_mshrfill_train.append(data_train.filter(like='system.l2cache.bank_cfl_targetblk_memsp_fill_', axis=0).sum())
        op_memrd_test.append(data_test.filter(regex='system.cpu.*op_class_0::', axis=0).filter(like='MemRead', axis=0).sum())
        op_memwr_test.append(data_test.filter(regex='system.cpu.*op_class_0::', axis=0).filter(like='MemWrite', axis=0).sum())
        op_other_test.append(data_test.filter(regex='system.cpu.*op_class_0::', axis=0).filter(regex='^((?!MemRead|MemWrite).)*$', axis=0).sum())
        op_memrd_train.append(data_train.filter(regex='system.cpu.*op_class_0::', axis=0).filter(like='MemRead', axis=0).sum())
        op_memwr_train.append(data_train.filter(regex='system.cpu.*op_class_0::', axis=0).filter(like='MemWrite', axis=0).sum())
        op_other_train.append(data_train.filter(regex='system.cpu.*op_class_0::', axis=0).filter(regex='^((?!MemRead|MemWrite).)*$', axis=0).sum())
        if not benchmark_set:
            benchmark_set = list(OrderedDict.fromkeys((v.split('.')[0] for v in data.columns.values)))
        if not vlines_count_test:
            for f in benchmark_set[:-1]:
                num_cpts = len(data_test.filter(like=f, axis=1).loc['rel_ticks'])
                if num_cpts:
                    vlines_count_test += num_cpts
                    vlines_test.append((f, vlines_count_test))
        if not vlines_count_train:
            for f in benchmark_set[:-1]:
                num_cpts = len(data_train.filter(like=f, axis=1).loc['rel_ticks'])
                if num_cpts:
                    vlines_count_train += num_cpts
                    vlines_train.append((f, vlines_count_train))


# MPKI - Test
num_plots = 2 if "i7-6700" not in base_outpath else 3
plt.figure(figsize=(7,8))
plt.subplot(num_plots, 1, 1)
plt.xlabel('Simulation point - Test')
plt.ylabel('MPKI L1')
ax = plt.gca()
color=next(ax._get_lines.prop_cycler)['color']
plt.plot(range(0, len(misses_l1_test[0])), misses_l1_test[0]/100000, color=color)
overall = {}
plot_overall = []
for b in benchmark_set:
    index = b.split('.')[0]
    overall[index] = 0
    sum_weights = 0
    sum_values = 0
    flt_data = data_test.filter(like=b, axis=1)
    if len(flt_data.columns):
        for cpt in flt_data:
            overall[index] = overall[index] + (misses_l1_test[0][cpt]/100000 * cpt_weight_test[0][cpt])
            sum_weights = sum_weights + cpt_weight_test[0][cpt]
            sum_values = sum_values + misses_l1_test[0][cpt]/100000
        overall[index] = overall[index] + sum_values / len(flt_data.columns) * (1 - sum_weights)
        for cpt in flt_data:
            plot_overall.append(overall[index])
plt.bar(np.arange(0.5, len(plot_overall)-1, 1), plot_overall[:-1], width=1, alpha=0.3)
old_value = 0
for v in vlines_test:
    plt.axvline(x=v[1], color='k', linestyle='--')
    plt.text((v[1]+old_value)/2-magic_number_test, plt.ylim()[1]+plt.ylim()[1]*0.02, v[0])
    old_value = v[1]
plt.text((len(rel_ticks_test[0])+old_value)/2-magic_number_test, plt.ylim()[1]+plt.ylim()[1]*0.02, benchmark_set[-1])
plt.margins(x=0)
plt.subplot(num_plots, 1, 2)
plt.xlabel('Simulation point - Test')
plt.ylabel('MPKI L2')
ax = plt.gca()
color=next(ax._get_lines.prop_cycler)['color']
plt.plot(range(0, len(misses_l2_test[0])), misses_l2_test[0]/100000, color=color)
overall = {}
plot_overall = []
for b in benchmark_set:
    index = b.split('.')[0]
    overall[index] = 0
    sum_weights = 0
    sum_values = 0
    flt_data = data_test.filter(like=b, axis=1)
    if len(flt_data.columns):
        for cpt in flt_data:
            overall[index] = overall[index] + (misses_l2_test[0][cpt]/100000 * cpt_weight_test[0][cpt])
            sum_weights = sum_weights + cpt_weight_test[0][cpt]
            sum_values = sum_values + misses_l2_test[0][cpt]/100000
        overall[index] = overall[index] + sum_values / len(flt_data.columns) * (1 - sum_weights)
        for cpt in flt_data:
            plot_overall.append(overall[index])
plt.bar(np.arange(0.5, len(plot_overall)-1, 1), plot_overall[:-1], width=1, alpha=0.3)
old_value = 0
for v in vlines_test:
    plt.axvline(x=v[1], color='k', linestyle='--')
    plt.text((v[1]+old_value)/2-magic_number_test, plt.ylim()[1]+plt.ylim()[1]*0.02, v[0])
    old_value = v[1]
plt.text((len(rel_ticks_test[0])+old_value)/2-magic_number_test, plt.ylim()[1]+plt.ylim()[1]*0.02, benchmark_set[-1])
plt.margins(x=0)
if num_plots == 3:
    plt.subplot(3, 1, 3)
    plt.xlabel('Simulation point - Test')
    plt.ylabel('MPKI L3')
    ax = plt.gca()
    color=next(ax._get_lines.prop_cycler)['color']
    plt.plot(range(0, len(misses_l3_test[0])), misses_l3_test[0]/100000, color=color)
    overall = {}
    plot_overall = []
    for b in benchmark_set:
        index = b.split('.')[0]
        overall[index] = 0
        sum_weights = 0
        sum_values = 0
        flt_data = data_test.filter(like=b, axis=1)
        if len(flt_data.columns):
            for cpt in flt_data:
                overall[index] = overall[index] + (misses_l3_test[0][cpt]/100000 * cpt_weight_test[0][cpt])
                sum_weights = sum_weights + cpt_weight_test[0][cpt]
                sum_values = sum_values + misses_l3_test[0][cpt]/100000
            overall[index] = overall[index] + sum_values / len(flt_data.columns) * (1 - sum_weights)
            for cpt in flt_data:
                plot_overall.append(overall[index])
    plt.bar(np.arange(0.5, len(plot_overall)-1, 1), plot_overall[:-1], width=1, alpha=0.3)
    old_value = 0
    for v in vlines_test:
        plt.axvline(x=v[1], color='k', linestyle='--')
        plt.text((v[1]+old_value)/2-magic_number_test, plt.ylim()[1]+plt.ylim()[1]*0.02, v[0])
        old_value = v[1]
    plt.text((len(rel_ticks_test[0])+old_value)/2-magic_number_test, plt.ylim()[1]+plt.ylim()[1]*0.02, benchmark_set[-1])
    plt.margins(x=0)
plt.tight_layout(pad=4/(num_plots-1))
plt.savefig(base_outpath + "mpki_test.png", bbox_inches = 'tight', pad_inches = 0.2)
plt.close()

# MPKI - Train
num_plots = 2 if "i7-6700" not in base_outpath else 3
plt.figure(figsize=(7,8))
plt.subplot(num_plots, 1, 1)
plt.xlabel('Simulation point - Train')
plt.ylabel('MPKI L1')
ax = plt.gca()
color=next(ax._get_lines.prop_cycler)['color']
plt.plot(range(0, len(misses_l1_train[0])), misses_l1_train[0]/100000, color=color)
overall = {}
plot_overall = []
for b in benchmark_set:
    index = b.split('.')[0]
    overall[index] = 0
    sum_weights = 0
    sum_values = 0
    flt_data = data_train.filter(like=b, axis=1)
    if len(flt_data.columns):
        for cpt in flt_data:
            overall[index] = overall[index] + (misses_l1_train[0][cpt]/100000 * cpt_weight_train[0][cpt])
            sum_weights = sum_weights + cpt_weight_train[0][cpt]
            sum_values = sum_values + misses_l1_train[0][cpt]/100000
        overall[index] = overall[index] + sum_values / len(flt_data.columns) * (1 - sum_weights)
        for cpt in flt_data:
            plot_overall.append(overall[index])
plt.bar(np.arange(0.5, len(plot_overall)-1, 1), plot_overall[:-1], width=1, alpha=0.3)
old_value = 0
for v in vlines_train:
    plt.axvline(x=v[1], color='k', linestyle='--')
    plt.text((v[1]+old_value)/2-magic_number_train, plt.ylim()[1]+plt.ylim()[1]*0.02, v[0])
    old_value = v[1]
plt.text((len(rel_ticks_train[0])+old_value)/2-magic_number_train, plt.ylim()[1]+plt.ylim()[1]*0.02, benchmark_set[-1])
plt.margins(x=0)
plt.subplot(num_plots, 1, 2)
plt.xlabel('Simulation point - Train')
plt.ylabel('MPKI L2')
ax = plt.gca()
color=next(ax._get_lines.prop_cycler)['color']
plt.plot(range(0, len(misses_l2_train[0])), misses_l2_train[0]/100000, color=color)
overall = {}
plot_overall = []
for b in benchmark_set:
    index = b.split('.')[0]
    overall[index] = 0
    sum_weights = 0
    sum_values = 0
    flt_data = data_train.filter(like=b, axis=1)
    if len(flt_data.columns):
        for cpt in flt_data:
            overall[index] = overall[index] + (misses_l2_train[0][cpt]/100000 * cpt_weight_train[0][cpt])
            sum_weights = sum_weights + cpt_weight_train[0][cpt]
            sum_values = sum_values + misses_l2_train[0][cpt]/100000
        overall[index] = overall[index] + sum_values / len(flt_data.columns) * (1 - sum_weights)
        for cpt in flt_data:
            plot_overall.append(overall[index])
plt.bar(np.arange(0.5, len(plot_overall)-1, 1), plot_overall[:-1], width=1, alpha=0.3)
old_value = 0
for v in vlines_train:
    plt.axvline(x=v[1], color='k', linestyle='--')
    plt.text((v[1]+old_value)/2-magic_number_train, plt.ylim()[1]+plt.ylim()[1]*0.02, v[0])
    old_value = v[1]
plt.text((len(rel_ticks_train[0])+old_value)/2-magic_number_train, plt.ylim()[1]+plt.ylim()[1]*0.02, benchmark_set[-1])
plt.margins(x=0)
if num_plots == 3:
    plt.subplot(3, 1, 3)
    plt.xlabel('Simulation point - Train')
    plt.ylabel('MPKI L3')
    ax = plt.gca()
    color=next(ax._get_lines.prop_cycler)['color']
    plt.plot(range(0, len(misses_l3_train[0])), misses_l3_train[0]/100000, color=color)
    overall = {}
    plot_overall = []
    for b in benchmark_set:
        index = b.split('.')[0]
        overall[index] = 0
        sum_weights = 0
        sum_values = 0
        flt_data = data_train.filter(like=b, axis=1)
        if len(flt_data.columns):
            for cpt in flt_data:
                overall[index] = overall[index] + (misses_l3_train[0][cpt]/100000 * cpt_weight_train[0][cpt])
                sum_weights = sum_weights + cpt_weight_train[0][cpt]
                sum_values = sum_values + misses_l3_train[0][cpt]/100000
            overall[index] = overall[index] + sum_values / len(flt_data.columns) * (1 - sum_weights)
            for cpt in flt_data:
                plot_overall.append(overall[index])
    plt.bar(np.arange(0.5, len(plot_overall)-1, 1), plot_overall[:-1], width=1, alpha=0.3)
    old_value = 0
    for v in vlines_train:
        plt.axvline(x=v[1], color='k', linestyle='--')
        plt.text((v[1]+old_value)/2-magic_number_train, plt.ylim()[1]+plt.ylim()[1]*0.02, v[0])
        old_value = v[1]
    plt.text((len(rel_ticks_train[0])+old_value)/2-magic_number_train, plt.ylim()[1]+plt.ylim()[1]*0.02, benchmark_set[-1])
    plt.margins(x=0)
plt.tight_layout(pad=4/(num_plots-1))
plt.savefig(base_outpath + "mpki_train.png", bbox_inches = 'tight', pad_inches = 0.2)
plt.close()

# Slowdown - Test
plt.figure(figsize=(7,8))
plt.subplot(2, 1, 1)
plt.xlabel('Simulation point - Test')
plt.ylabel('Relative slowdown')
for i, n in enumerate(legend):
    ax = plt.gca()
    color=next(ax._get_lines.prop_cycler)['color']
    plt.plot(range(0, len(rel_ticks_test[i])), rel_ticks_test[i], color=color)
    average = {}
    plot_average = []
    for b in benchmark_set:
        index = b.split('.')[0]
        average[index] = 0
        sum_weights = 0
        sum_values = 0
        flt_data = data_test.filter(like=b, axis=1)
        if len(flt_data.columns):
            for cpt in flt_data:
                average[index] = average[index] + (rel_ticks_test[i][cpt] * cpt_weight_test[i][cpt])
                sum_weights = sum_weights + cpt_weight_test[i][cpt]
                sum_values = sum_values + rel_ticks_test[i][cpt]
            average[index] = average[index] + sum_values / len(flt_data.columns) * (1 - sum_weights)
            for cpt in flt_data:
                plot_average.append(average[index])
    plt.bar(np.arange(0.5, len(plot_average)-1, 1), plot_average[:-1], width=1, alpha=0.3)
old_value = 0
for v in vlines_test:
    plt.axvline(x=v[1], color='k', linestyle='--')
    plt.text((v[1]+old_value)/2-magic_number_test, plt.ylim()[1]+plt.ylim()[1]*0.003, v[0])
    old_value = v[1]
plt.text((len(rel_ticks_test[0])+old_value)/2-magic_number_test, plt.ylim()[1]+plt.ylim()[1]*0.003, benchmark_set[-1])
plt.legend(legend, loc="upper right")
plt.margins(x=0)
plt.ylim(ymin=1)

# Slowdown - Train
plt.subplot(2, 1, 2)
plt.xlabel('Simulation point - Train')
plt.ylabel('Relative slowdown')
for i, n in enumerate(legend):
    ax = plt.gca()
    color=next(ax._get_lines.prop_cycler)['color']
    plt.plot(range(0, len(rel_ticks_train[i])), rel_ticks_train[i], color=color)
    average = {}
    plot_average = []
    for b in benchmark_set:
        index = b.split('.')[0]
        average[index] = 0
        sum_weights = 0
        sum_values = 0
        flt_data = data_train.filter(like=b, axis=1)
        if len(flt_data.columns):
            for cpt in flt_data:
                average[index] = average[index] + (rel_ticks_train[i][cpt] * cpt_weight_train[i][cpt])
                sum_weights = sum_weights + cpt_weight_train[i][cpt]
                sum_values = sum_values + rel_ticks_train[i][cpt]
            average[index] = average[index] + sum_values / len(flt_data.columns) * (1 - sum_weights)
            for cpt in flt_data:
                plot_average.append(average[index])
    plt.bar(np.arange(0.5, len(plot_average)-1, 1), plot_average[:-1], width=1, alpha=0.3)
old_value = 0
for v in vlines_train:
    plt.axvline(x=v[1], color='k', linestyle='--')
    plt.text((v[1]+old_value)/2-magic_number_train, plt.ylim()[1]+plt.ylim()[1]*0.003, v[0])
    old_value = v[1]
plt.text((len(rel_ticks_train[0])+old_value)/2-magic_number_train, plt.ylim()[1]+plt.ylim()[1]*0.003, benchmark_set[-1])
plt.legend(legend, loc="upper right")
plt.margins(x=0)
plt.ylim(ymin=1)
plt.tight_layout(pad=4)
plt.savefig(base_outpath + "slowdown.png", bbox_inches = 'tight', pad_inches = 0.2)
plt.close()

# CPI - Test
plt.figure(figsize=(7,8))
plt.subplot(2, 1, 1)
plt.xlabel('Simulation point - Test')
plt.ylabel('Cycles per instruction')
for i, n in enumerate(legend):
    ax = plt.gca()
    color=next(ax._get_lines.prop_cycler)['color']
    plt.plot(range(0, len(cpi_test[i])), cpi_test[i], color=color)
    average = {}
    plot_average = []
    for b in benchmark_set:
        index = b.split('.')[0]
        average[index] = 0
        sum_weights = 0
        sum_values = 0
        flt_data = data_test.filter(like=b, axis=1)
        if len(flt_data.columns):
            for cpt in flt_data:
                average[index] = average[index] + (cpi_test[i][cpt] * cpt_weight_test[i][cpt])
                sum_weights = sum_weights + cpt_weight_test[i][cpt]
                sum_values = sum_values + cpi_test[i][cpt]
            average[index] = average[index] + sum_values / len(flt_data.columns) * (1 - sum_weights)
            for cpt in flt_data:
                plot_average.append(average[index])
    plt.bar(np.arange(0.5, len(plot_average)-1, 1), plot_average[:-1], width=1, alpha=0.3)
old_value = 0
for v in vlines_test:
    plt.axvline(x=v[1], color='k', linestyle='--')
    plt.text((v[1]+old_value)/2-magic_number_test, plt.ylim()[1]+plt.ylim()[1]*0.02, v[0])
    old_value = v[1]
plt.text((len(cpi_test[0])+old_value)/2-magic_number_test, plt.ylim()[1]+plt.ylim()[1]*0.02, benchmark_set[-1])
plt.legend(legend, loc="upper right")
plt.margins(x=0)
plt.ylim(ymin=1)

# CPI - Train
plt.subplot(2, 1, 2)
plt.xlabel('Simulation point - Train')
plt.ylabel('Cycles per instruction')
for i, n in enumerate(legend):
    ax = plt.gca()
    color=next(ax._get_lines.prop_cycler)['color']
    plt.plot(range(0, len(cpi_train[i])), cpi_train[i], color=color)
    average = {}
    plot_average = []
    for b in benchmark_set:
        index = b.split('.')[0]
        average[index] = 0
        sum_weights = 0
        sum_values = 0
        flt_data = data_train.filter(like=b, axis=1)
        if len(flt_data.columns):
            for cpt in flt_data:
                average[index] = average[index] + (cpi_train[i][cpt] * cpt_weight_train[i][cpt])
                sum_weights = sum_weights + cpt_weight_train[i][cpt]
                sum_values = sum_values + cpi_train[i][cpt]
            average[index] = average[index] + sum_values / len(flt_data.columns) * (1 - sum_weights)
            for cpt in flt_data:
                plot_average.append(average[index])
    plt.bar(np.arange(0.5, len(plot_average)-1, 1), plot_average[:-1], width=1, alpha=0.3)
old_value = 0
for v in vlines_train:
    plt.axvline(x=v[1], color='k', linestyle='--')
    plt.text((v[1]+old_value)/2-magic_number_train ,plt.ylim()[1]+plt.ylim()[1]*0.02, v[0])
    old_value = v[1]
plt.text((len(cpi_train[0])+old_value)/2-magic_number_train,plt.ylim()[1]+plt.ylim()[1]*0.02, benchmark_set[-1])
plt.legend(legend, loc="upper right")
plt.margins(x=0)
plt.ylim(ymin=1)
plt.tight_layout(pad=4)
plt.savefig(base_outpath + "cpi.png", bbox_inches = 'tight', pad_inches = 0.2)
plt.close()

# Instruction type - Test
plt.figure(figsize=(7,8))
plt.subplot(2, 1, 1)
plt.xlabel('Simulation point - Test')
plt.ylabel('Operation mix (%)')
tot_insts = op_other_test[0] + op_memrd_test[0] + op_memwr_test[0]
op_other_norm = op_other_test[0] / tot_insts
op_reads_norm = op_memrd_test[0] / tot_insts
op_writes_norm = op_memwr_test[0] / tot_insts
other = plt.bar(np.arange(0.5, len(op_other_norm), 1), op_other_norm, 1)
reads = plt.bar(np.arange(0.5, len(op_reads_norm), 1), op_reads_norm, 1, bottom=op_other_norm)
writes = plt.bar(np.arange(0.5, len(op_writes_norm), 1), op_writes_norm, 1, bottom=(op_reads_norm + op_other_norm))
other.set_label('Other')
reads.set_label('MemRead')
writes.set_label('MemWrite')
old_value = 0
for v in vlines_test:
    plt.axvline(x=v[1], color='k', linestyle='--')
    plt.text((v[1]+old_value)/2-magic_number_test, 1.02, v[0])
    old_value = v[1]
plt.text((len(rel_ticks_test[0])+old_value)/2-magic_number_test, 1.02, benchmark_set[-1])
plt.legend(loc='lower right')
plt.margins(x=0)
plt.ylim(0, 1)

# Instruction type - Train
plt.subplot(2, 1, 2)
plt.xlabel('Simulation point - Train')
plt.ylabel('Operation mix (%)')
tot_insts = op_other_train[0] + op_memrd_train[0] + op_memwr_train[0]
op_other_norm = op_other_train[0] / tot_insts
op_reads_norm = op_memrd_train[0] / tot_insts
op_writes_norm = op_memwr_train[0] / tot_insts
other = plt.bar(np.arange(0.5, len(op_other_norm), 1), op_other_norm, 1)
reads = plt.bar(np.arange(0.5, len(op_reads_norm), 1), op_reads_norm, 1, bottom=op_other_norm)
writes = plt.bar(np.arange(0.5, len(op_writes_norm), 1), op_writes_norm, 1, bottom=(op_reads_norm + op_other_norm))
other.set_label('Other')
reads.set_label('MemRead')
writes.set_label('MemWrite')
old_value = 0
for v in vlines_train:
    plt.axvline(x=v[1], color='k', linestyle='--')
    plt.text((v[1]+old_value)/2-magic_number_train, 1.02, v[0])
    old_value = v[1]
plt.text((len(rel_ticks_train[0])+old_value)/2-magic_number_train, 1.02, benchmark_set[-1])
plt.legend(loc='lower right')
plt.margins(x=0)
plt.ylim(0, 1)
plt.tight_layout(pad=4)
plt.savefig(base_outpath + "opmix.png", bbox_inches = 'tight', pad_inches = 0.2)
plt.close()

# Bank conflicts
yfmt = ForceFormat()
yfmt.set_powerlimits((0,0))
for i, n in enumerate(legend):
    # Busy block - Test
    plt.figure(figsize=(7,8))
    plt.subplot(2, 1, 1)
    ax = plt.gca()
    #ax.yaxis.set_major_formatter(yfmt)
    plt.xlabel('Simulation point - Test [' + legend[i] + ']')
    plt.ylabel('Bank conflicts - Busy Block')
    plt.gca().set_prop_cycle('color', plt.rcParams['axes.prop_cycle'].by_key()['color'][1:])
    #cpusprd = plt.bar(np.arange(0.5, len(busyblk_cpusprd_test[i]), 1), busyblk_cpusprd_test[i], 1)
    #cpuspwr = plt.bar(np.arange(0.5, len(busyblk_cpuspwr_test[i]), 1), busyblk_cpuspwr_test[i], 1, bottom=busyblk_cpusprd_test[i])
    cpuspwr = plt.bar(np.arange(0.5, len(busyblk_cpuspwr_test[i]), 1), busyblk_cpuspwr_test[i], 1)
    #mshrfill = plt.bar(np.arange(0.5, len(busyblk_mshrfill_test[i]), 1), busyblk_mshrfill_test[i], 1, bottom=(busyblk_cpusprd_test[i] + busyblk_cpuspwr_test[i]))
    mshrfill = plt.bar(np.arange(0.5, len(busyblk_mshrfill_test[i]), 1), busyblk_mshrfill_test[i], 1, bottom=busyblk_cpuspwr_test[i])
    #cpusprd.set_label('Read request')
    cpuspwr.set_label('Writeback')
    mshrfill.set_label('Write fill')
    old_value = 0
    for v in vlines_test:
        plt.axvline(x=v[1], color='k', linestyle='--')
        plt.text((v[1]+old_value)/2-magic_number_test, plt.ylim()[1]+plt.ylim()[1]*0.02, v[0])
        old_value = v[1]
    plt.text((len(rel_ticks_test[0])+old_value)/2-magic_number_test, plt.ylim()[1]+plt.ylim()[1]*0.02, benchmark_set[-1])
    plt.legend(loc='upper right')
    plt.margins(x=0)

    # Busy block - Train
    plt.subplot(2, 1, 2)
    ax = plt.gca()
    #ax.yaxis.set_major_formatter(yfmt)
    plt.xlabel('Simulation point - Train [' + legend[i] + ']')
    plt.ylabel('Bank conflicts - Busy Block')
    plt.gca().set_prop_cycle('color', plt.rcParams['axes.prop_cycle'].by_key()['color'][1:])
    #cpusprd = plt.bar(np.arange(0.5, len(busyblk_cpusprd_train[i]), 1), busyblk_cpusprd_train[i], 1)
    #cpuspwr = plt.bar(np.arange(0.5, len(busyblk_cpuspwr_train[i]), 1), busyblk_cpuspwr_train[i], 1, bottom=busyblk_cpusprd_train[i])
    cpuspwr = plt.bar(np.arange(0.5, len(busyblk_cpuspwr_train[i]), 1), busyblk_cpuspwr_train[i], 1)
    #mshrfill = plt.bar(np.arange(0.5, len(busyblk_mshrfill_train[i]), 1), busyblk_mshrfill_train[i], 1, bottom=(busyblk_cpusprd_train[i] + busyblk_cpuspwr_train[i]))
    mshrfill = plt.bar(np.arange(0.5, len(busyblk_mshrfill_train[i]), 1), busyblk_mshrfill_train[i], 1, bottom=busyblk_cpuspwr_train[i])
    #cpusprd.set_label('Read request')
    cpuspwr.set_label('Writeback')
    mshrfill.set_label('Write fill')
    old_value = 0
    for v in vlines_train:
        plt.axvline(x=v[1], color='k', linestyle='--')
        plt.text((v[1]+old_value)/2-magic_number_train, plt.ylim()[1]+plt.ylim()[1]*0.02, v[0])
        old_value = v[1]
    plt.text((len(rel_ticks_train[0])+old_value)/2-magic_number_train, plt.ylim()[1]+plt.ylim()[1]*0.02, benchmark_set[-1])
    plt.legend(loc='upper right')
    plt.margins(x=0)
    plt.tight_layout(pad=4)
    plt.savefig(base_outpath + legend[i] + "_conflicts_busyblk.png", bbox_inches = 'tight', pad_inches = 0.2)
    plt.close()

    # Target block - Test
    plt.figure(figsize=(7,8))
    plt.subplot(2, 1, 1)
    ax = plt.gca()
    #ax.yaxis.set_major_formatter(yfmt)
    plt.xlabel('Simulation point - Test [' + legend[i] + ']')
    plt.ylabel('Bank conflicts - Target block')
    plt.gca().set_prop_cycle('color', plt.rcParams['axes.prop_cycle'].by_key()['color'][1:])
    cpusprd  = plt.bar(np.arange(0.5, len(targetblk_cpusprd_test[i]), 1), targetblk_cpusprd_test[i], 1)
    #cpuspwr  = plt.bar(np.arange(0.5, len(targetblk_cpuspwr_test[i]), 1), targetblk_cpuspwr_test[i], 1, bottom=targetblk_cpusprd_test[i])
    #cpuspwr  = plt.bar(np.arange(0.5, len(targetblk_cpuspwr_test[i]), 1), targetblk_cpuspwr_test[i], 1)
    #mshrfill = plt.bar(np.arange(0.5, len(targetblk_mshrfill_test[i]), 1), targetblk_mshrfill_test[i], 1, bottom=(targetblk_cpusprd_test[i] + targetblk_cpuspwr_test[i]))
    #mshrfill = plt.bar(np.arange(0.5, len(targetblk_mshrfill_test[i]), 1), targetblk_mshrfill_test[i], 1, bottom=targetblk_cpuspwr_test[i])
    cpusprd.set_label('Read request')
    #cpuspwr.set_label('Writeback')
    #mshrfill.set_label('Write fill')
    old_value = 0
    for v in vlines_test:
        plt.axvline(x=v[1], color='k', linestyle='--')
        plt.text((v[1]+old_value)/2-magic_number_test, plt.ylim()[1]+plt.ylim()[1]*0.02, v[0])
        old_value = v[1]
    plt.text((len(rel_ticks_test[0])+old_value)/2-magic_number_test, plt.ylim()[1]+plt.ylim()[1]*0.02, benchmark_set[-1])
    plt.legend(loc='upper right')
    plt.margins(x=0)

    # Target block - Train
    plt.subplot(2, 1, 2)
    ax = plt.gca()
    #ax.yaxis.set_major_formatter(yfmt)
    plt.xlabel('Simulation point - Train [' + legend[i] + ']')
    plt.ylabel('Bank conflicts - Target block')
    plt.gca().set_prop_cycle('color', plt.rcParams['axes.prop_cycle'].by_key()['color'][1:])
    cpusprd  = plt.bar(np.arange(0.5, len(targetblk_cpusprd_train[i]), 1), targetblk_cpusprd_train[i], 1)
    #cpuspwr  = plt.bar(np.arange(0.5, len(targetblk_cpuspwr_train[i]), 1), targetblk_cpuspwr_train[i], 1, bottom=targetblk_cpusprd_train[i])
    #cpuspwr  = plt.bar(np.arange(0.5, len(targetblk_cpuspwr_train[i]), 1), targetblk_cpuspwr_train[i], 1)
    #mshrfill = plt.bar(np.arange(0.5, len(targetblk_mshrfill_train[i]), 1), targetblk_mshrfill_train[i], 1, bottom=(targetblk_cpusprd_train[i] + targetblk_cpuspwr_train[i]))
    #mshrfill = plt.bar(np.arange(0.5, len(targetblk_mshrfill_train[i]), 1), targetblk_mshrfill_train[i], 1, bottom=targetblk_cpuspwr_train[i])
    cpusprd.set_label('Read request')
    #cpuspwr.set_label('Writeback')
    #mshrfill.set_label('Write fill')
    old_value = 0
    for v in vlines_train:
        plt.axvline(x=v[1], color='k', linestyle='--')
        plt.text((v[1]+old_value)/2-magic_number_train, plt.ylim()[1]+plt.ylim()[1]*0.02, v[0])
        old_value = v[1]
    plt.text((len(rel_ticks_train[0])+old_value)/2-magic_number_train, plt.ylim()[1]+plt.ylim()[1]*0.02, benchmark_set[-1])
    plt.legend(loc='upper right')
    plt.margins(x=0)
    plt.tight_layout(pad=4)
    plt.savefig(base_outpath + legend[i] + "_conflicts_targetblk.png", bbox_inches = 'tight', pad_inches = 0.2)
    plt.close()
