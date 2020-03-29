import os
import pandas as pd
import sys
stats_files = []

def compute_rel_ticks(x):
    if x < 1:
        return 1
    return x

if len(sys.argv) < 2:
    print("fatal: you need at least two files")
    exit(1)
baseline = sys.argv[1]
for i in range(2, len(sys.argv)):
    stats_files.append(sys.argv[i])

out_dir = "step3"
if not os.path.isdir(out_dir):
    os.mkdir(out_dir)

# Read and format data of the baseline configuration
baseline_data = pd.read_csv(baseline, index_col=0, keep_default_na=False, na_values="nan")
# Initially, set the common columns (= fields) equal to the baseline ones
common_cols = baseline_data.columns
# Scan the fields of the other files and find the common ones
for f in stats_files:
    data = pd.read_csv(f, index_col=0, keep_default_na=False, na_values="nan")
    common_cols = list(set(common_cols).intersection(data.columns))
# Sort common_cols
common_cols.sort()
# "Crop" the baseline data array
baseline_data = baseline_data[common_cols]
# Preprocess baseline data
baseline_data.replace("N/A", 0, inplace=True)
baseline_data = baseline_data.apply(pd.to_numeric)

# Process the other files
for f in stats_files:
    data = pd.read_csv(f, index_col=0, keep_default_na=False, na_values="nan")
    # "Crop" the data array
    data = data[common_cols]
    # Treat the data as numeric
    data.replace("N/A", 0, inplace=True)
    data = data.apply(pd.to_numeric)
    # Perform the division w.r.t. baseline
    relative = pd.DataFrame.divide(data, baseline_data)
    # Append rel_ticks to the new file
    relative.loc["rel_ticks"] = relative.loc["sim_ticks"].apply(compute_rel_ticks)
    relative.sort_index(inplace=True)
    # Append rel_ticks to the original file
    data.loc["rel_ticks"] = relative.loc["rel_ticks"]
    data.sort_index(inplace=True)
    # Save both files
    data_filename = os.path.basename(f)
    data_conf = data_filename.replace(".csv", "").replace("parsed_stats_", "")
    data.to_csv(os.path.join(out_dir, "slowdown_" + data_conf + ".csv"))
    relative.to_csv(os.path.join(out_dir, "relative_" + data_conf + ".csv"), na_rep="nan")

# Add the dummy relative slowdown to the baseline
if "rel_ticks" not in baseline_data.index:
    baseline_data.loc["rel_ticks"] = [0 for i in range(0, baseline_data.shape[1])]
    baseline_data.sort_index(inplace=True)
# Save the baseline .csv file
baseline_filename = os.path.basename(baseline)
baseline_conf = baseline_filename.replace("parsed_stats_", "").replace(".csv", "")
baseline_data.to_csv(os.path.join(out_dir, "baseline_" + baseline_conf + ".csv"), na_rep="nan")
