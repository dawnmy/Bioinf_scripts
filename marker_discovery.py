#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: Z.-L. Deng
# @Email: dawnmsg@gmail.com
# @Date:   2015-10-23 15:31:54
# @Last Modified by:   zde14
# @Last Modified time: 2015-11-16 15:44:43

import argparse
import data_processing as dp
from sklearn.ensemble import RandomForestClassifier
from sklearn.ensemble import ExtraTreesClassifier
from numpy import arange


class FS:

    def __init__(self, data, label):
        self.data = data
        # self.exp = self.data.genes
        self.label = label
        self.genes = list(self.data.columns)

    def edgeR(self, fdr=0.05):
        import rpy2.robjects as robjects
        import rpy2.robjects.numpy2ri
        robjects.r('library("edgeR")')
        count = self.data.T
        groups = self.label.unique()
        # params = {'group' : self.label, 'lib.size' : sizes}
        # dgelist = robjects.r.DGEList(data, **params)
        # au_raw <- read.table(file="./expression.txt", sep="\t", row.names=1)
        dgelist = robjects.r.DGEList(counts = count
                      , group = self.label
                      , genes = self.genes
        )
        # ms = robjects.r.deDGE(dgelist, doPoisson=True)

        norm = robjects.r.calcNormFactors(dgelist)
        comdis = robjects.r.estimateCommonDisp(norm)
        y = robjects.r.estimateTagwiseDisp(comdis)
        et = robjects.r.exactTest(y, pair=groups)
        robjects.r.write.table(robjects.r.topTags(et, n = "all"), "./AU_de_contig.txt", sep="\t")


    def testES(self, es=0.8, method='wilcoxon'):
        pass

    def mRMR(self):
        pass

    def fsRF(self, n_trees=10000):
        # from sklearn.ensemble import RandomForestClassifier
        estimator = RandomForestClassifier(n_estimators=n_trees, random_state=0)

        estimator.fit(self.data, self.label)
        importances = zip(self.genes, estimator.feature_importances_)
        return(sorted(importances, key=lambda x: x[1], reverse=True))

        # print("\t".join((gene, str(importance))))

    def fsDT(self, n_trees=10000):
        estimator = ExtraTreesClassifier(n_estimators=25000, random_state=0)
        estimator.fit(self.data, self.label)
        importances = zip(self.genes, estimator.feature_importances_)
        return(sorted(importances, key=lambda x: x[1], reverse=True))

        # return(clfrf.feature_importances_)

    def fsRFE(self, cv=5):
        from sklearn.svm import SVC
        # import matplotlib.pyplot as plt
        # from sklearn.cross_validation import StratifiedKFold
        from sklearn.feature_selection import RFECV
        estimator = SVC(kernel="linear")
        selector = RFECV(estimator, step=1, cv=cv)
        selector.fit(self.data, self.label)
        # markers = selector.get_support(indices=True)
        markers = selector.support_
        return(self.data.columns[markers])

        # print("Optimal number of features : %d" % selector.n_features_)
        # print(self.data.columns[markers])

        # # Plot number of features VS. cross-validation scores
        # plt.figure()
        # plt.xlabel("Number of features selected")
        # plt.ylabel("Cross validation score (nb of correct classifications)")
        # plt.plot(range(1, len(selector.grid_scores_) + 1), selector.grid_scores_)
        # plt.show()


        # clf = SVC(kernel="linear", C=1)
        # Recursive feature elimination with 4-fold cross validation
        # rfecv = RFECV(clf, step=1, cv=4)

        # selector1 = rfecv.fit(X_train, y_train)
        # pass


class Classifier:

    def __init__(self, training, test):
        self.training = training
        self.test = test
        self.training_label = self.training.index.get_level_values('class')


    def clfRF(self, n_trees=10000):
        rfc = RandomForestClassifier(n_estimators=n_trees)
        rfc.fit(self.training, self.training_label)
        # print y
        # print rfc.predict(X_test)
        # print rfc.predict_proba(X_test)
        # print rfc.predict_proba(Jx_test)
        # print Jy
        return(rfc.predict(self.test))

    def clfSVM(self, cv=5, c=[2**i for i in arange(-5, 7, 0.1)], g=[0, 10]):
        from sklearn.svm import SVC
        from sklearn.grid_search import GridSearchCV
        tuned_parameters = [
                   {'kernel': ['linear'], 'C': c}
                ]

        scores = ['precision', 'f1', 'accuracy', 'roc_auc']
        for score in scores:
            clf = GridSearchCV(SVC(C=1), tuned_parameters, cv=4, scoring=score)
            clf.fit(self.training, self.training_label)
            print(clf.best_estimator_)


    def clfLDA(self):
        pass


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("training",
                        help="the input expression table for \
                        training dataset with count or abundance of genes",
                        type=str)
    parser.add_argument("test",
                        help="the input expression table for \
                        test dataset with count or abundance of genes",
                        type=str)
    parser.add_argument("-s", "--subclass", action='store_true',
                        help="with subclass",
                        default=False
                        )

    args = parser.parse_args()

    training_file = args.training
    test_file = args.test
    training_dataset = dp.Data(training_file, subclass=args.subclass).df
    test_dataset = dp.Data(test_file, dataset='test', subclass=args.subclass).df
    training_label = training_dataset.index.get_level_values('class')
    test_label = test_dataset.index.get_level_values('class')
    # genes = list(training_dataset.df.genes.columns)
    frames = (training_dataset, test_dataset)
    whole_dataset = dp.pd.concat(frames)
    # data_scaled = min_max_scaler.fit_transform(datamatrix)
    whole_stand = dp.standardization(whole_dataset, method='max_min')
    # training_stand = whole_stand.xs(
    #                             'training',
    #                             level='dataset', drop_level=False
    #                             )

    training_stand = whole_stand.xs(
                        'training',
                        level='dataset',
                        drop_level=False
                    )
    test_stand = whole_stand.xs('test', level='dataset', drop_level=False)
    # print(training_label)

    fs1 = FS(training_stand, training_label)
    # print(fs1.data)
    # print(training_stand['samples'])
    fs1.edgeR()
    # markers = fs1.fsRFE(cv=4)
    # print(markers)
    # importance = fs1.fsDT(n_trees=10000)
    # for (gene, score) in importance:
    #     print(gene, score)
    
    # clf1 = Classifier(training_stand[markers], test_stand[markers])
    # print(clf1.clfRF(n_trees=10000))
    # clf1.clfSVM(cv=4)
    #data = dataset.ix[:, 1:]
    # samples = dataset.samples
    # label = dataset.phenotypes

    # print(samples, label)
    # for (gene, importance) in zip(genes, fs1.fsRF(n_trees=1000)):

    #     print("\t".join((gene, str(importance))))


if __name__ == '__main__':
    main()
