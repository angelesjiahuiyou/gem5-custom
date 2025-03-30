import os
import sys
import numpy as np
import pandas as pd
from scipy.cluster.hierarchy import dendrogram
from sklearn import linear_model, metrics, cluster, svm
from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt
stats_files = []

if len(sys.argv) < 1:
    print("fatal: you need at least one file")
    exit(1)
for i in range(1, len(sys.argv)):
    stats_files.append(sys.argv[i])

out_dir = "step6"
if not os.path.isdir(out_dir):
    os.mkdir(out_dir)

"""
# AFTER PCA
for f in sorted(stats_files):
    data = pd.read_csv(f, sep=';')
    lm = linear_model.LinearRegression()
    X = data.drop("rel_ticks", axis = 1)
    y = data.rel_ticks
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=0)
    lm.fit(X_train, y_train)
    print("File: ", f)
    print("Intercept: ", lm.intercept_)
    print("Number of coefficients: ", len(lm.coef_))
    print("Score: ", lm.score(X_train, y_train))
    cmat = pd.DataFrame(zip(X.columns, lm.coef_), columns = ['Features', 'Coefficients'])
    y_pred = lm.predict(X_test)
    print('Mean Absolute Error:', metrics.mean_absolute_error(y_test, y_pred))  
    print('Mean Squared Error:', metrics.mean_squared_error(y_test, y_pred))  
    print('Root Mean Squared Error:', np.sqrt(metrics.mean_squared_error(y_test, y_pred)))
    print("-----------------")
"""

# BEFORE PCA
for f in sorted(stats_files):
    data = pd.read_csv(f, index_col=0).transpose()
    data = data.drop(["cpt_weight", "sim_insts", "sim_ops", "sim_seconds", "sim_ticks"], errors='ignore', axis=1)
    data = data.dropna()
    X = data.drop("rel_ticks", axis = 1)
    y = data.rel_ticks

    # Divide in train and test
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=5)

    # Compute linear model coefficients
    lm = linear_model.RidgeCV()
    lm.fit(X_train, y_train)

    # Apply predictive model to test
    y_pred = lm.predict(X_test)
    
    # Plot real and predicted relative slowdown
    plt.figure(figsize=(7,4))
    plt.plot(range(len(y_test)), y_test, color='r', label='real')
    plt.plot(range(len(y_pred)), y_pred, color='b', label='predicted')
    plt.xlabel('Simulation point (subset)')
    plt.ylabel('Relative slowdown')
    plt.legend()
    plt.savefig(os.path.join(out_dir, os.path.basename(f).replace(".csv", ".png")), bbox_inches='tight', pad_inches=0.2)
    plt.close()
    
    # Create log
    logname = os.path.basename(f).replace(".csv", ".log")
    with open(os.path.join(out_dir, logname), 'w') as log:
        log.write("LINEAR MODEL DETAILS\n")
        log.write("-----------------" + "\n")
        log.write("Intercept: " + str(lm.intercept_) + "\n")
        log.write("Number of coefficients: " + str(len(lm.coef_)) + "\n")
        log.write("Score (R squared): " + str(lm.score(X_train, y_train)) + "\n")
        log.write("Train size: " + str(len(X_train.index)) + "\n\n")
        log.write("PREDICTION ACCURACY VS. TEST\n")
        log.write("-----------------" + "\n")
        log.write('Mean Absolute Error: ' + str(metrics.mean_absolute_error(y_test, y_pred)) + "\n")  
        log.write('Mean Squared Error: ' + str(metrics.mean_squared_error(y_test, y_pred)) + "\n")  
        log.write('Root Mean Squared Error: ' + str(np.sqrt(metrics.mean_squared_error(y_test, y_pred))) + "\n")
        log.write("Test size: " + str(len(X_test.index)) + "\n\n")
        cmat = pd.DataFrame(zip(X_train.columns, lm.coef_), columns = ['Features', 'Coefficients'])
        cmat = cmat.reindex(cmat['Coefficients'].abs().sort_values(ascending=False).index)
        log.write("LINEAR MODEL COEFFICIENTS\n")
        log.write("-----------------" + "\n")
        for c in cmat.values[:30]:
            log.write(str(round(c[1], 5)) + " -> " + c[0] + "\n")

    featname = os.path.basename(f).replace(".csv", "_features.log")
    agglo = cluster.FeatureAgglomeration(n_clusters=30)
    agglo.fit(X)
    with open(os.path.join(out_dir, featname), 'w') as feat:
        for i, label in enumerate(set(agglo.labels_)):
            features_with_label = [X.columns.values[j] for j, lab in enumerate(agglo.labels_) if lab == label]
            feat.write('Cluster {}:\n{}\n'.format(i, features_with_label))
