import os
import pandas as pd
import sys
from sklearn.decomposition import PCA
stats_files = []
n_components = 100
log_components = 30
log_stats = 20

if len(sys.argv) < 1:
    print("fatal: you need at least one file")
    exit(1)
for i in range(1, len(sys.argv)):
    stats_files.append(sys.argv[i])

out_dir = "step5"
if not os.path.isdir(out_dir):
    os.mkdir(out_dir)
    
for f in sorted(stats_files):
    data = pd.read_csv(f, index_col=0)
    td = data.transpose()
    # Drop unnecessary stats
    td_clean = td.drop(["cpt_weight", "rel_ticks", "sim_insts", "sim_ops", "sim_seconds", "sim_ticks"], errors='ignore', axis=1)
    # Create a copy of the dataset and apply the PCA (first n_components)
    pca = PCA(n_components)
    pca_data = pd.DataFrame(pca.fit_transform(td_clean.to_numpy()), index=td_clean.index, columns=["PC" + str(i) for i in range (0, n_components)])
    pca_components = pd.DataFrame(pca.components_, index=["PC" + str(i) for i in range (0, n_components)], columns=td_clean.columns)
    # Save pca reduced data and components to output files
    out_filename = os.path.basename(f).replace(".csv", "_pca_data.csv")
    comp_filename = os.path.basename(f).replace(".csv", "_pca_comp.csv")
    final_filename = os.path.basename(f).replace(".csv", "_formatted.csv")
    pca_data.to_csv(os.path.join(out_dir, out_filename))
    pca_components.to_csv(os.path.join(out_dir, comp_filename))
    pca_final = pca_data
    if "rel_ticks" in data.index:
        pca_final.insert(0, "rel_ticks", data.loc["rel_ticks"])
    else:
        pca_final.insert(0, "rel_ticks", [0 for i in data.columns])
    pca_final.to_csv(os.path.join(out_dir, final_filename), index=False, sep=';')
    # Print statistical information in a separate file
    logname = os.path.basename(f).replace(".csv", "_pca_log.txt")
    logpath = os.path.join(out_dir, logname)
    with open(logpath, "w+") as log:
        log.write("--- Original data file: " + os.path.basename(f) + " ---\n\n")
        log.write("Percentage of information in all the " + str(n_components) +
                  " Principal Components:\n" + str(sum(pca.explained_variance_ratio_)) + "\n\n")
        for c in range(0, log_components):
            log.write("COMPONENT " + str(c) + " (WEIGHT = " + str(round(pca.explained_variance_ratio_[c], 5)) + ")\n")
            log.write("------------------------------------------\n")
            # Print metrics with highest weights for first component
            comp = pd.Series(pca.components_[c], index=td_clean.columns)
            # Sort components values by weight (in absolute value)
            comp = comp.reindex(comp.abs().sort_values(ascending=False).index)
            for v in range (0, log_stats):
                log.write(comp.index[v] + " = " + str(round(comp[v], 5)) + "\n")
            log.write("\n")
    