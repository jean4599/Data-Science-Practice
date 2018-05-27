import sys
import numpy as np
from sklearn.datasets import load_svmlight_file
from sklearn.datasets import dump_svmlight_file
from sklearn import preprocessing
from sklearn.preprocessing import StandardScaler

import time
tt = time.time()
# from libsvm.python.svm import *
# from libsvm.python.svmutil import *

def pca(X):
	#Standardize the data (mean = 0 and variance = 1)
	X_std = preprocessing.scale(X, with_mean=False)

	# Calculate covariance matrix
	covariance_matrix = np.cov(np.transpose(X_std))
	
	# Calculate the eigenvectors and eigenvalues of the covariave matrix
	eig_val, eig_vec = np.linalg.eig(covariance_matrix)

	# Sort eig_value based on eig_val from highest to lowest
	abs_eig_val = np.abs(eig_val)
	indices = np.argsort(-abs_eig_val)
	abs_eig_val = abs_eig_val[indices]
	
	# Find top K eigen values that cover 85% variance
	K = abs_eig_val.shape[0]-1
	eig_sum = 0
	for i in range(abs_eig_val.shape[0]):
		eig_sum = eig_sum+abs_eig_val[i]
	#print("sum of eig value: ", eig_sum)

	eig_val_percent = abs_eig_val/eig_sum
	
	eig_percent_sum = 0
	for i in range(eig_val.shape[0]):
		eig_percent_sum = eig_percent_sum+eig_val_percent[i]
		if eig_percent_sum>=0.90:
			K = i
			print("K: ", K," %=", eig_percent_sum)
			break

	eig_vec = eig_vec[indices]

	eig_pairs = [(abs_eig_val[i], eig_vec[:,i]) for i in range(abs_eig_val.shape[0])]
	#print(eig_pairs)

	# Select the top K eig_vec
	selected_feature=np.array([ele[1] for ele in eig_pairs[:K]])
	
	# Get new data: Project original data to new dimension
	project_matrix = np.transpose(selected_feature)
	data=np.dot(X_std, project_matrix)
	# print("X_std.shape", X_std.shape, "project_matrix.shape", project_matrix.shape, "After PCA X shape: ", data.shape)

	return data

datapath = sys.argv[1]
# Load data
X, y = load_svmlight_file(datapath)
X = X.toarray()

# PCA
pca_X = pca(X)

# Standardize data
sc = StandardScaler()
sc.fit(pca_X)
X_std = sc.transform(pca_X)

# Output data
output_datapath = datapath.split(".")[0]+'_out.txt'
dump_svmlight_file(X_std, y, output_datapath)
print("Output data to ", output_datapath)

tf = time.time()
print("run time ", tf-tt)
