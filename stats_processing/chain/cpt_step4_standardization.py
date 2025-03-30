import os
import pandas as pd
import sys
from sklearn.preprocessing import StandardScaler
stats_files = []

if len(sys.argv) < 1:
    print("fatal: you need at least one file")
    exit(1)
for i in range(1, len(sys.argv)):
    stats_files.append(sys.argv[i])

out_dir = "step4"
if not os.path.isdir(out_dir):
    os.mkdir(out_dir)

for f in stats_files:
    data = pd.read_csv(f, index_col=0, na_values="inf")
    rel_ticks = data.loc["rel_ticks"]
    data = data.drop("rel_ticks")
    # --- WAY WITHOUT TRANSPOSITION ---
    #std_data = data.sub(data.mean(1), axis=0).div(data.std(1), axis=0)
    #std_data = std_data.dropna()
    # --- WAY WITH TRANSPOSITION ---
    # Clean nan and inf values from original dataset
    data = data.dropna()
    # Transpose the dataset
    td = data.transpose()
    # Create a copy of the dataset and apply the standardization
    scaler = StandardScaler()
    std_td = pd.DataFrame(scaler.fit_transform(td.to_numpy()), columns=td.columns, index=td.index)
    # Re-transpose the dataset (ugly, inefficient but it works)
    std_data = std_td.transpose()
    # Remove "empty" rows
    std_data = std_data.loc[(std_data!=0).any(axis=1)]
    # Re-add relative slowdown
    std_data.loc["rel_ticks"] = rel_ticks
    std_data.sort_index(inplace=True)
    # Save to output file
    out_filename = os.path.basename(f).replace(".csv", "_std.csv")
    std_data.to_csv(os.path.join(out_dir, out_filename))
