#!/usr/bin/env python
# coding=utf-8

# Author: Z.-L. Deng
 
# This script is used to perform a feature selection for selecting biomarkers 
# based on gene expression by using recursive feature elimination implemented  
# by Support Vector Machine and Random Forest.
#
# 

"""
Selecting the important features as potential biomarkers from metatranscriptome data using RF and SVM
"""
import numpy as np
from sklearn import preprocessing
from sklearn.svm import SVC
from sklearn.feature_selection import RFECV
from sklearn.ensemble import ExtraTreesClassifier

print(__doc__)


# For loading the data from tab delimited file
def read_data_table(inf,ing):
    inputfile = inf
    gene_name = ing

    datamatrix = np.array([map(float,line.split()[1:]) for line in open(inputfile).readlines()])
    min_max_scaler = preprocessing.MinMaxScaler()
    
    # Scaling the value into the range of [0,1]
    data_scaled = min_max_scaler.fit_transform(datamatrix)

    label = np.array(map(int,[line.split()[0] for line in open(inputfile).readlines()]))
    var = np.array(open(gene_name,'r').readline().strip().split("\t"))

    dataform = {"data":data_scaled,"label":label,"var":var}

    return(dataform)

if __name__=="__main__":
    # Load the data from tab delimited file
    top100 = read_data_table("top100.txt","gene_name.txt")
    X,y = top100["data"],top100["label"]
    X_train, X_test, y_train, y_test = X,X,y,y

    # Support vector classifier with linear kernel for recursive feature elimination
    clf = SVC(kernel="linear", C=1)

    # Recursive feature elimination with 4-fold cross validation
    rfecv = RFECV(clf, step=1, cv=4)

    selector1 = rfecv.fit(X_train, y_train)

    # Random forest classifier for feature selection
    clfrf = ExtraTreesClassifier(n_estimators=25000,random_state=0)

    clfrf.fit(X_train, y_train)


##--- The features selected by recursive feature elimination method
    print "#################################################################################"
    print "#       RFECV: Recursive feature elimination using Support Vector Machine       #"
    print "#################################################################################"


    fs1 = list(selector1.get_support(indices=True))
    print fs1

    print top100["var"][fs1]
    print "\n\n"


##--- The top 5 features ranked by Random Forest
    print "##############################################################"
    print "#     RF: Feature importance ranking with Random Forest      #"
    print "##############################################################"

    rfl = {}
    j = 0
    for i in clfrf.feature_importances_:
        j += 1

        if i > 0:
            rfl[j] = i

    rf_rank = sorted(rfl.iteritems(), key=lambda d:d[1], reverse = True)

    for id,score in rf_rank[:5]:

        print id -1 ,score
        print top100["var"][id-1]
