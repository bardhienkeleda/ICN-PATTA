#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: enkeledabardhi
"""
import json
import pickle
import numpy as np
import pandas as pd
import re
import random
import glob
import os
from os.path import dirname, abspath
import matplotlib.pyplot as plt


BASIC_DIRECTORY = (abspath(dirname(__file__)))
domain_path = BASIC_DIRECTORY + "/domain/URL_Classification.csv"
tfidf_vector_path = BASIC_DIRECTORY + "/components/saved_tfidf_vectors/"
words = "x"
grams = "1gram_"


def top_tfidf_feats(row, features, top_n=25):
    ''' Get top n tfidf values in row and return them with their corresponding feature names.'''
    topn_ids = np.argsort(row)[::-1][:top_n]
    top_feats = [(features[i], row[i]) for i in topn_ids]
    df = pd.DataFrame(top_feats)
    df.columns = ['feature', 'tfidf']
    return df

def top_feats_in_doc(Xtr, features, row_id, top_n=25):
    ''' Top tfidf features in specific document (matrix row) '''
    row = np.squeeze(Xtr[row_id]) #.toarray())
    return top_tfidf_feats(row, features, top_n)

def top_mean_feats(Xtr, features, grp_ids=None, min_tfidf=0.1, top_n=25):
    ''' Return the top n features that on average are most important amongst documents in rows
        indentified by indices in grp_ids. '''
    if grp_ids:
        D = Xtr[grp_ids]#.toarray()
    else:
        D = Xtr#.toarray()

    D[D < min_tfidf] = 0
    tfidf_means = np.mean(D, axis=0)
    return top_tfidf_feats(tfidf_means, features, top_n)

def top_feats_by_class(Xtr, y, features, min_tfidf=0.1, top_n=25):
    ''' Return a list of dfs, where each df holds top_n features and their mean tfidf value
        calculated across documents with the same class label. '''
    dfs = []
    labels = np.unique(y)
    for label in labels:
        ids = np.where(y==label)
        feats_df = top_mean_feats(Xtr, features, ids, min_tfidf=min_tfidf, top_n=top_n)
        feats_df.label = label
        dfs.append(feats_df)
    return dfs

def plot_tfidf_classfeats_h(dfs):
    ''' Plot the data frames returned by the function plot_tfidf_classfeats(). '''
    fig = plt.figure(figsize=(12, 9), facecolor="w")
    x = np.arange(len(dfs[0]))
    for i, df in enumerate(dfs):
        ax = fig.add_subplot(1, len(dfs), i+1)
        ax.spines["top"].set_visible(False)
        ax.spines["right"].set_visible(False)
        ax.set_frame_on(False)
        ax.get_xaxis().tick_bottom()
        ax.get_yaxis().tick_left()
        ax.set_xlabel("Mean Tf-Idf Score", labelpad=16, fontsize=14)
        ax.set_title("label = " + str(df.label), fontsize=16)
        ax.ticklabel_format(axis='x', style='sci', scilimits=(-2,2))
        ax.barh(x, df.tfidf, align='center', color='#3F5D7D')
        ax.set_yticks(x)
        ax.set_ylim([-1, x[-1]+1])
        yticks = ax.set_yticklabels(df.feature)
        plt.subplots_adjust(bottom=0.09, right=0.97, left=0.15, top=0.95, wspace=0.52)
    plt.show()



if __name__ == "__main__":


    #### OLD CODE FOR KEYWORD PLOT ####
    with open(BASIC_DIRECTORY + "/" + "labels_dictionary.txt", "rb") as file:
        labels_dictionary = pickle.load(file)
    print(labels_dictionary)

    with open(tfidf_vector_path + "tfidf_vector_"+ grams + words +"feat.pk", "rb") as file:
        tfidf = pickle.load(file)

    with open(tfidf_vector_path + "train_features_"+ grams + words +"feat.pk", "rb") as file:
        train_features = pickle.load(file)

    with open(tfidf_vector_path + "train_labels_"+ grams + words +"feat.pk", "rb") as file:
        train_labels = pickle.load(file)


    feature_names = tfidf.get_feature_names()
    #print(feature_names)
    #df = top_tfidf_feats(train_features[1], feature_names, 5)
    #df = top_feats_in_doc(train_features, feature_names, 1, 5)
    #df = top_mean_feats(train_features, feature_names, None, 0.1, 1000)
    dfs = top_feats_by_class(train_features, train_labels, feature_names, 0.1, 50)
    print(dfs[4])
    #words = ['abadns42jd00', 'amico', 'news', 'www']
    #for word in words:
    #    print(word.isalpha())
    #plot_tfidf_classfeats_h(dfs)
