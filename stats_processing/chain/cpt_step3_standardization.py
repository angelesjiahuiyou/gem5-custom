import os
import pandas as pd
import sys
stats_files = []

if len(sys.argv) < 1:
    print("fatal: you need at least one file")
    exit(1)
for i in range(1, len(sys.argv)):
    stats_files.append(sys.argv[i])

out_dir = "step3"
if not os.path.isdir(out_dir):
    os.mkdir(out_dir)

for f in stats_files:
    data = pd.read_csv(f, index_col=0)
    std_data = data.sub(data.mean(1), axis=0).div(data.std(1), axis=0)
    std_data = std_data.dropna()
    out_filename = os.path.basename(f).replace(".csv", "_std.csv")
    std_data.to_csv(os.path.join(out_dir, out_filename))