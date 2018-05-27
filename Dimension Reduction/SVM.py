import sys
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.datasets import load_svmlight_file
from sklearn.datasets import dump_svmlight_file
from sklearn.cross_validation import train_test_split
from sklearn import preprocessing
from sklearn.metrics import accuracy_score
from sklearn.metrics import precision_recall_fscore_support
from sklearn.svm import SVC
import matplotlib.pylab as plt
from sklearn.model_selection import GridSearchCV
from pandas import DataFrame

datapath = sys.argv[1]
# Load data
X, y = load_svmlight_file(datapath)
X = X.toarray()

# #特徵縮放
# sc = StandardScaler()
# sc.fit(X)
# X_std = sc.transform(X)

#######################################
#GridSearchCV
#######################################
# parameters = {'kernel': ['linear'], 'gamma': [0.1,0.01],
#                      'C': [0.1,1,10]}
# svm = SVC()
# clf = GridSearchCV(svm, parameters, scoring='f1_micro')
# clf.fit(X_train,Y_train)

# Pretty print GridSearch result
# df = DataFrame(data=clf.cv_results_)
# print(df)

# bst = clf.best_estimator_
# y_pred = bst.predict(X_test)
# print("Misclassified sample: %d" % (Y_test != y_pred).sum())
# print("Accuracy: %.2f" % accuracy_score(Y_test,y_pred))
# precision,recall,fscore,support = precision_recall_fscore_support(Y_test, y_pred, average='micro')
# print("precision: ", precision)
# print("recall: ", recall)
# print("fscore: ", fscore)
#######################################

# # Split data into training data and testing data
X_train, X_test, Y_train, Y_test = train_test_split(X, y, test_size=0.3, random_state=0)

svm = SVC(kernel='rbf', C=20, gamma=0.01)
svm.fit(X_train,Y_train)
#model評估
y_pred = svm.predict(X_test)
print("Misclassified sample: %d" % (Y_test != y_pred).sum())
print("Accuracy: %.2f" % accuracy_score(Y_test,y_pred))
precision,recall,fscore,support = precision_recall_fscore_support(Y_test, y_pred, average='micro')
print("precision: ", precision)
print("recall: ", recall)
print("fscore: ", fscore)
