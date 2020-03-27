import os
import sys
import numpy as np
import pandas as pd
from sklearn import linear_model
from sklearn import metrics
from sklearn.model_selection import train_test_split
from sklearn import svm
import matplotlib.pyplot as plt
stats_files = []

if len(sys.argv) < 1:
    print("fatal: you need at least one file")
    exit(1)
for i in range(1, len(sys.argv)):
    stats_files.append(sys.argv[i])

out_dir = "step5"
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
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.15, random_state=5)

    # Compute linear model coefficients
    lm = linear_model.Ridge()
    lm.fit(X_train, y_train)

    # Print linear model details
    print("File: ", f)
    print("Intercept: ", lm.intercept_)
    print("Number of coefficients: ", len(lm.coef_))
    print("Score (R squared): ", lm.score(X_train, y_train))

    # Apply predictive model to test
    y_pred = lm.predict(X_test)
    print('Mean Absolute Error:', metrics.mean_absolute_error(y_test, y_pred))  
    print('Mean Squared Error:', metrics.mean_squared_error(y_test, y_pred))  
    print('Root Mean Squared Error:', np.sqrt(metrics.mean_squared_error(y_test, y_pred)))
    print("")
    
    # Plot real and predicted relative slowdown
    plt.figure(figsize=(9,7))
    plt.plot(range(len(y[X_test.index])), y[X_test.index], color='r')
    plt.plot(range(len(y_pred)), y_pred, color='b')
    plt.show()
    
    # Show coefficients
    cmat = pd.DataFrame(zip(X_train.columns, lm.coef_), columns = ['Features', 'Coefficients'])
    cmat = cmat.reindex(cmat['Coefficients'].abs().sort_values(ascending=False).index)  
    for c in cmat.values[:30]:
        print(str(round(c[1], 5)) + " -> " + c[0])
    print("-----------------")
