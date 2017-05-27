#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: Z.-L. Deng
# @Email: dawnmsg@gmail.com
# @Date:   2015-10-23 18:21:59
# @Last Modified by:   zde14
# @Last Modified time: 2015-11-13 16:59:40

import pandas as pd


# class Data:

#     def __init__(self, data_file, dataset='training'):
#         self.dataset = dataset

#         self.data_file = data_file
#         self.df = pd.read_csv(
#             self.data_file,
#             delim_whitespace=True,
#             index_col=0)
#         if dataset == 'training':
#             self.df['']
#         else:


#         self.label = self.df.phenotypes
#         self.data = self.df.ix[:, 1:]

class Data:

    def __init__(self, data_file, dataset='training', subclass=False):
        self.dataset = dataset
        self.data_file = data_file
        self.df = pd.read_csv(
            self.data_file,
            delim_whitespace=True
        )
        self.df['dataset'] = dataset
        # if dataset == 'training':
        #     self.df['dataset'] = 'training'
            # n_cols = len(self.df.columns)
        if subclass:
            # self.df.columns = [
            #     ['phenotype'] * 2 + ['genes'] * (n_cols - 2),
            #     self.df.columns
            # ]
            self.df.set_index(['samples', 'dataset', 'class', 'subclass'], inplace=True)
        else:
            # self.df.columns = [
            #     ['phenotype'] + ['genes'] * (n_cols - 1), self.df.columns
            # ]
            self.df.set_index(['samples', 'dataset', 'class'], inplace=True)
        # else:
        #     self.df['dataset'] = 'test'

        #     # self.df.set_index(['samples', 'dataset'], inplace=True)
        #     n_cols = len(self.df.columns)
        #     if subclass:

        #         self.df.insert(0, 'class', 1)
        #         self.df.insert(1, 'subclass', 1)
        #         self.df.columns = [
        #             ['phenotype'] * 2 + ['genes'] * n_cols, self.df.columns
        #         ]
        #     else:

        #         self.df.insert(0, 'class', 1)
        #         self.df.columns = [
        #             ['phenotype'] + ['genes'] * n_cols, self.df.columns
        #         ]
        # self.df.set_index(['samples', 'dataset', 'phenotype'], inplace=True)


# percentage
def percentage(df):
    data = df.T
    data_norm = 100 * data / data.sum()
    data_norm = data_norm.T
    # frames = (label, data_norm)
    # df_norm = pd.concat(frames, axis=1)
    # n_cols = len(data_norm.columns)
    # df_norm.columns = [
    #                 ['phenotype'] + ['genes'] * n_cols, df_norm.columns
    #             ]

    return(data_norm)


# z-score
def standardization(df, method='max_min'):
    data = df
    # label = df.phenotype
    if method == 'max_min':
        data_st = (data - data.min()) / (data.max() - data.min())

    elif method == 'z_score':
        data_st = (data - data.mean()) / data.std()

    # frames = (label, data_st)
    # df_st = pd.concat(frames, axis=1)
    # n_cols = len(data.columns)
    # df_st.columns = [
    #                 ['phenotype'] + ['genes'] * n_cols, df_st.columns
    #             ]

    return(data_st)


# if __name__ == '__main__':
#     import sys, numpy, scipy
#     import scipy.cluster.hierarchy as hier
#     import scipy.spatial.distance as dist
#     dataset1 = Data('top100.txt')
#     # print(dataset1.df.index.get_level_values('class'))
#     # print(percentage(dataset1.df))

#     # distanceMatrix = dist.pdist(dataset1.df)
#     # distanceMatrix = dist.pdist(dataMatrix,'hamming') #use hamming function
#     distanceMatrix = dist.pdist(dataset1.df.T,'euclidean') #use euclidean function
#     distanceSquareMatrix = dist.squareform(distanceMatrix)
#     linkageMatrix = hier.linkage(distanceSquareMatrix)
#     print(linkageMatrix)

    # heatmapOrder = hier.leaves_list(linkageMatrix)

    # orderedDataMatrix = dataMatrix[heatmapOrder,:]

    # rowHeaders = numpy.array(rowHeaders)
    # orderedRowHeaders = rowHeaders[heatmapOrder,:]

    # matrixOutput = []
