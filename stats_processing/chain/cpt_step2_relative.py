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

baseline_data = pd.read_csv(baseline, index_col=0, keep_default_na=False, na_values="nan")
baseline_data.replace("N/A", 0, inplace=True)
baseline_data = baseline_data.apply(pd.to_numeric)
baseline_conf = baseline.replace("parsed_stats_", "").replace(".csv", "")

for f in stats_files:
    data_conf = f.replace("parsed_stats_", "").replace(".csv", "")
    data = pd.read_csv(f, index_col=0)
    # Treat the data as numeric
    data.replace("N/A", 0, inplace=True)
    data = data.apply(pd.to_numeric)
    # Perform the division w.r.t. baseline
    relative = pd.DataFrame.divide(data, baseline_data)
    # Append rel_slowdown to the new file
    #relative.rename(index={"sim_ticks": "rel_slowdown"}, inplace=True)
    relative.loc["rel_slowdown"] = relative.loc["sim_ticks"].apply(compute_slowdown)
    relative.sort_index(inplace=True)
    # Append rel_slowdown to the original file
    data.loc["rel_slowdown"] = relative.loc["rel_slowdown"]
    data.sort_index(inplace=True)
    # Save both files
    slowdown_filename = "slowdown.bl_" + baseline_conf + ".conf_" + data_conf + ".csv"
    relative_filename = "relative.bl_" + baseline_conf + ".conf_" + data_conf + ".csv"
    data.to_csv(slowdown_filename)
    relative.to_csv(relative_filename)