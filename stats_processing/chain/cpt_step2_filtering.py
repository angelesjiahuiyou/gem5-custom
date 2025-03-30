import os
import pandas as pd
import sys
from joblib import Parallel, parallel_backend, delayed
import multiprocessing
stats_files = []

if len(sys.argv) < 1:
    print("fatal: you need at least one file")
    exit(1)
for i in range(1, len(sys.argv)):
    stats_files.append(sys.argv[i])

out_dir = "step2"
if not os.path.isdir(out_dir):
    os.mkdir(out_dir)

blacklist = (
    "rdQLenPdf", 
    "wrQLenPdf",
    "perBankRdBursts",
    "perBankWrBursts",
    "Energy",
    "final_tick",
    "host_",
    "avg",
    "rate",
    "ratio",
    "cycles",
    "overall_hit",
    "overall_miss",
    "overall_mshr",
    "overall_accesses"
)

whitelist = (
    "trans_dist",
    "op_class",
    "concurrent_banks_ticks"
)

def filter(f):
    data = pd.read_csv(f, index_col=0, na_values="inf").fillna(0)
    data_flt = pd.DataFrame
    field_list = []
    for field in data.index.values:
        if not (len(set(data.loc[field].dropna())) <= 1 or
            any(b in field for b in blacklist) or
            ("::" in field and "::total" not in field and not any(w in field for w in whitelist))):
            field_list.append(field)
    data_flt = data.loc[field_list]
    data_flt.to_csv(os.path.join(out_dir, os.path.basename(f).replace("raw_stats", "parsed_stats")))

with parallel_backend('multiprocessing', n_jobs=multiprocessing.cpu_count()):
    Parallel()(delayed(filter)(f) for f in stats_files)
