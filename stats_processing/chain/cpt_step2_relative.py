import os
import pandas as pd
import sys
stats_files = []

def compute_slowdown(x):
    return (x - 1)

if len(sys.argv) < 2:
    print("fatal: you need at least two files")
    exit(1)
baseline = sys.argv[1]
for f in range(2, len(sys.argv)):
    stats_files.append(sys.argv[f])

out_dir = "step2"
if not os.path.isdir(out_dir):
    os.mkdir(out_dir)

baseline_data = pd.read_csv(baseline, index_col=0, keep_default_na=False, na_values="nan")
baseline_data.replace("N/A", 0, inplace=True)
baseline_data = baseline_data.apply(pd.to_numeric)
if "rel_slowdown" not in baseline_data.index:
    baseline_data.loc["rel_slowdown"] = [0 for i in range(0, baseline_data.shape[1])]
    baseline_data.sort_index(inplace=True)
baseline_filename = os.path.basename(baseline)
baseline_conf = baseline_filename.replace("parsed_stats_", "").replace(".csv", "")
baseline_data.to_csv(os.path.join(out_dir, "baseline_" + baseline_conf + ".csv"))

for f in stats_files:
    data = pd.read_csv(f, index_col=0)
    # Treat the data as numeric
    data.replace("N/A", 0, inplace=True)
    data = data.apply(pd.to_numeric)
    # Perform the division w.r.t. baseline
    relative = pd.DataFrame.divide(data, baseline_data)
    # Append rel_slowdown to the new file
    relative.loc["rel_slowdown"] = relative.loc["sim_ticks"].apply(compute_slowdown)
    relative.sort_index(inplace=True)
    # Append rel_slowdown to the original file
    data.loc["rel_slowdown"] = relative.loc["rel_slowdown"]
    data.sort_index(inplace=True)
    # Save both files
    data_filename = os.path.basename(f)
    data_conf = data_filename.replace(".csv", "").replace("parsed_stats_", "")
    data.to_csv(os.path.join(out_dir, "slowdown_" + data_conf + ".csv"))
    relative.to_csv(os.path.join(out_dir, "relative_" + data_conf + ".csv"))
