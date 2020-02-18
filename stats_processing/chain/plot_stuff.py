import os
import sys
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
benchmark_set = ('602.gcc_s', '605.mcf_s', '607.cactuBSSN_s', '623.xalancbmk_s', '625.x264_s', '628.pop2_s', '638.imagick_s', '641.leela_s', '649.fotonik3d_s', '654.roms_s')
stats_files = []
names = []
slowdown_test = []
slowdown_train = []
cpt_weight_test = []
cpt_weight_train = []
data_test = []
data_train = []
op_memrd_test = []
op_memwr_test = []
op_other_test = []
op_memrd_train = []
op_memwr_train = []
op_other_train = []
vlines_test = []
vlines_train = []
vlines_count_test = 0
vlines_count_train = 0

if len(sys.argv) < 1:
    print("fatal: you need at least one file")
    exit(1)
for i in range(1, len(sys.argv)):
    stats_files.append(sys.argv[i])
 
for f in sorted(stats_files):
    data = pd.read_csv(f, index_col=0)
    if "rel_slowdown" in data.index:
        #names.append(os.path.basename(f).replace("slowdown", "").replace(".csv", "").replace("_", " "))
        names.append(os.path.basename(f).split('_')[-1].replace(".csv", ""))
        data_test = data.filter(like='test.', axis=1)
        data_train = data.filter(like='train.', axis=1)
        slowdown_test.append(data_test.loc['rel_slowdown'])
        slowdown_train.append(data_train.loc['rel_slowdown'])
        cpt_weight_test.append(data_test.loc['cpt_weight'])
        cpt_weight_train.append(data_train.loc['cpt_weight'])
        op_memrd_test.append(data_test.loc['system.cpu.op_class_0::MemRead'])
        op_memwr_test.append(data_test.loc['system.cpu.op_class_0::MemWrite'])
        op_other_test.append(
            data_test.loc['system.cpu.op_class_0::FloatAdd'] +
            data_test.loc['system.cpu.op_class_0::FloatCmp'] +
            data_test.loc['system.cpu.op_class_0::FloatCvt'] +
            data_test.loc['system.cpu.op_class_0::FloatDiv'] +
            data_test.loc['system.cpu.op_class_0::FloatMisc'] +
            data_test.loc['system.cpu.op_class_0::FloatMult'] +
            data_test.loc['system.cpu.op_class_0::FloatMultAcc'] +
            data_test.loc['system.cpu.op_class_0::FloatSqrt'] +
            data_test.loc['system.cpu.op_class_0::IntAlu'] +
            data_test.loc['system.cpu.op_class_0::IntDiv'] +
            data_test.loc['system.cpu.op_class_0::IntMult'] +
            data_test.loc['system.cpu.op_class_0::No_OpClass'] +
            data_test.loc['system.cpu.op_class_0::SimdAdd'] +
            data_test.loc['system.cpu.op_class_0::SimdAlu'] +
            data_test.loc['system.cpu.op_class_0::SimdCmp'] +
            data_test.loc['system.cpu.op_class_0::SimdCvt'] +
            data_test.loc['system.cpu.op_class_0::SimdFloatAdd'] +
            data_test.loc['system.cpu.op_class_0::SimdMisc'] +
            data_test.loc['system.cpu.op_class_0::SimdShift']
        )
        op_memrd_train.append(data_train.loc['system.cpu.op_class_0::MemRead'])
        op_memwr_train.append(data_train.loc['system.cpu.op_class_0::MemWrite'])
        op_other_train.append(
            data_train.loc['system.cpu.op_class_0::FloatAdd'] +
            data_train.loc['system.cpu.op_class_0::FloatCmp'] +
            data_train.loc['system.cpu.op_class_0::FloatCvt'] +
            data_train.loc['system.cpu.op_class_0::FloatDiv'] +
            data_train.loc['system.cpu.op_class_0::FloatMisc'] +
            data_train.loc['system.cpu.op_class_0::FloatMult'] +
            data_train.loc['system.cpu.op_class_0::FloatMultAcc'] +
            data_train.loc['system.cpu.op_class_0::FloatSqrt'] +
            data_train.loc['system.cpu.op_class_0::IntAlu'] +
            data_train.loc['system.cpu.op_class_0::IntDiv'] +
            data_train.loc['system.cpu.op_class_0::IntMult'] +
            data_train.loc['system.cpu.op_class_0::No_OpClass'] +
            data_train.loc['system.cpu.op_class_0::SimdAdd'] +
            data_train.loc['system.cpu.op_class_0::SimdAlu'] +
            data_train.loc['system.cpu.op_class_0::SimdCmp'] +
            data_train.loc['system.cpu.op_class_0::SimdCvt'] +
            data_train.loc['system.cpu.op_class_0::SimdFloatAdd'] +
            data_train.loc['system.cpu.op_class_0::SimdMisc'] +
            data_train.loc['system.cpu.op_class_0::SimdShift']
        )
        if not vlines_count_test:
            for f in benchmark_set[:-1]:
                num_cpts = len(data_test.filter(like=f, axis=1).loc['rel_slowdown'])
                if num_cpts:
                    vlines_count_test += num_cpts
                    vlines_test.append((f.split('.')[0], vlines_count_test))
        if not vlines_count_train:
            for f in benchmark_set[:-1]:
                num_cpts = len(data_train.filter(like=f, axis=1).loc['rel_slowdown'])
                if num_cpts:
                    vlines_count_train += num_cpts
                    vlines_train.append((f.split('.')[0], vlines_count_train))

# Average slowdown - Test
plt.figure(figsize=(9,7))
plt.subplot(2, 1, 1)
plt.xlabel('Benchmark - Test')
plt.ylabel('Average relative slowdown')
width = 0.65/len(names)
for i, n in enumerate(names):
    avg_slowdown = {}
    for b in benchmark_set:
        index = b.split('.')[0]
        avg_slowdown[index] = 0
        for cpt in data_test.filter(like=b, axis=1):
            avg_slowdown[index] = avg_slowdown[index] + (slowdown_test[i][cpt] * cpt_weight_test[i][cpt])
    ind_num = np.arange(len(avg_slowdown))
    plt.bar(ind_num + i*width, avg_slowdown.values(), width=width)
plt.xticks(ind_num + (len(names)-1)*width/2, avg_slowdown.keys())
plt.legend(names, loc="upper right")
plt.margins(x=0)

# Average slowdown - Train
plt.subplot(2, 1, 2)
plt.xlabel('Benchmark - Train')
plt.ylabel('Average relative slowdown')
width = 0.65/len(names)
for i, n in enumerate(names):
    avg_slowdown = {}
    for b in benchmark_set:
        index = b.split('.')[0]
        avg_slowdown[index] = 0
        for cpt in data_train.filter(like=b, axis=1):
            avg_slowdown[index] = avg_slowdown[index] + (slowdown_train[i][cpt] * cpt_weight_train[i][cpt])
    ind_num = np.arange(len(avg_slowdown))
    plt.bar(ind_num + i*width, avg_slowdown.values(), width=width)
plt.xticks(ind_num + (len(names)-1)*width/2, avg_slowdown.keys())
plt.legend(names, loc="upper right")
plt.margins(x=0)
plt.tight_layout(pad=4)
plt.show()

# Slowdown - Test
plt.figure(figsize=(9,7))
plt.subplot(2, 1, 1)
plt.xlabel('Simulation point - Test')
plt.ylabel('Relative slowdown')
for i, n in enumerate(names):
    plt.plot(range(0, len(slowdown_test[i])), slowdown_test[i])
old_value = 0
for v in vlines_test:
    plt.axvline(x=v[1], color='k', linestyle='--')
    plt.text((v[1]+old_value)/2-1.8,plt.ylim()[1]+plt.ylim()[1]*0.02,v[0])
    old_value = v[1]
plt.text((len(slowdown_test[0])+old_value)/2-2,plt.ylim()[1]+plt.ylim()[1]*0.02,'654')
plt.legend(names, loc="upper right")
plt.margins(x=0)

# Slowdown - Train
plt.subplot(2, 1, 2)
plt.xlabel('Simulation point - Train')
plt.ylabel('Relative slowdown')
for i, n in enumerate(names):
    plt.plot(range(0, len(slowdown_train[i])), slowdown_train[i])
old_value = 0
for v in vlines_train:
    plt.axvline(x=v[1], color='k', linestyle='--')
    plt.text((v[1]+old_value)/2-4,plt.ylim()[1]+plt.ylim()[1]*0.02,v[0])
    old_value = v[1]
plt.text((len(slowdown_train[0])+old_value)/2-4.4,plt.ylim()[1]+plt.ylim()[1]*0.02,'654')
plt.legend(names, loc="upper right")
plt.margins(x=0)
plt.tight_layout(pad=4)
plt.show()

# Instruction type - Test
plt.figure(figsize=(9,7))
plt.subplot(2, 1, 1)
plt.xlabel('Simulation point - Test')
plt.ylabel('Instruction mix')
tot_insts = op_other_test[0] + op_memrd_test[0] + op_memwr_test[0]
op_other_norm = op_other_test[0] / tot_insts
op_reads_norm = op_memrd_test[0] / tot_insts
op_writes_norm = op_memwr_test[0] / tot_insts
other = plt.bar(range(0, len(op_other_norm)), op_other_norm, 1)
reads = plt.bar(range(0, len(op_reads_norm)), op_reads_norm, 1, bottom=op_other_norm)
writes = plt.bar(range(0, len(op_writes_norm)), op_writes_norm, 1, bottom=(op_reads_norm + op_other_norm))
other.set_label('Other')
reads.set_label('MemRead')
writes.set_label('MemWrite')
old_value = 0
for v in vlines_test:
    plt.axvline(x=v[1], color='k', linestyle='--')
    plt.text((v[1]+old_value)/2-1.8,1.02,v[0])
    old_value = v[1]
plt.text((len(slowdown_test[0])+old_value)/2-2,1.02,'654')
plt.legend(loc='lower right')
plt.margins(x=0)
plt.ylim(0, 1)

# Instruction type - Train
plt.subplot(2, 1, 2)
plt.xlabel('Simulation point - Train')
plt.ylabel('Instruction mix')
tot_insts = op_other_train[0] + op_memrd_train[0] + op_memwr_train[0]
op_other_norm = op_other_train[0] / tot_insts
op_reads_norm = op_memrd_train[0] / tot_insts
op_writes_norm = op_memwr_train[0] / tot_insts
other = plt.bar(range(0, len(op_other_norm)), op_other_norm, 1)
reads = plt.bar(range(0, len(op_reads_norm)), op_reads_norm, 1, bottom=op_other_norm)
writes = plt.bar(range(0, len(op_writes_norm)), op_writes_norm, 1, bottom=(op_reads_norm + op_other_norm))
other.set_label('Other')
reads.set_label('MemRead')
writes.set_label('MemWrite')
old_value = 0
for v in vlines_train:
    plt.axvline(x=v[1], color='k', linestyle='--')
    plt.text((v[1]+old_value)/2-4,1.02,v[0])
    old_value = v[1]
plt.text((len(slowdown_train[0])+old_value)/2-4.4,1.02,'654')
plt.legend(loc='lower right')
plt.margins(x=0)
plt.ylim(0, 1)
plt.tight_layout(pad=4)
plt.show()
