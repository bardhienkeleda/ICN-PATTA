#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: enkeledabardhi
"""
import pickle
import numpy as np
import configuration
import re
import wordninja
from sklearn.feature_extraction.text import TfidfVectorizer
from os.path import dirname, abspath


def preprocessing(dataframe):
    """
    This method is used to perform the same preprocessing that is performed offline in the collected dataset.
    It allows to transform the sniffed traffic into BoW, filters and cleans.
    It returns the preprocessed data in form of a dataframe.
    """
    not_to_keep = []
    """
    for webpg in range (len(configuration.webpages_list)):
        div = re.sub('[^A-Za-z0-9]+', ' ', str(configuration.webpages_list[webpg]))
        not_to_keep.append(div)
    for webpg in range (len(not_to_keep)):
        not_to_keep[webpg] = not_to_keep[webpg].split(" ")
    """

    # prepare a list of words that should be droped
    #words_to_delete = [item for sublist in not_to_keep for item in sublist]
    not_to_keep.append('http')
    not_to_keep.append('https')
    not_to_keep.append('ftp')
    not_to_keep.append('www')
    not_to_keep.append('wwwf')
    not_to_keep.append('www2')
    not_to_keep.append('www3')
    not_to_keep.append('co') #
    not_to_keep.append('php')
    not_to_keep.append('html')
    not_to_keep.append('cn')
    not_to_keep.append('ndn')
    not_to_keep.append('PR')
    not_to_keep.append('P1')
    not_to_keep.append('site')

    #words_to_delete = list(set(words_to_delete))

    # delete all the special characters from each url
    for row in range (len(dataframe)):
        dataframe['Interest_Request'][row] = re.sub('[^A-Za-z0-9]+', ' ', str(dataframe['Interest_Request'][row]))
        res = dataframe['Interest_Request'][row].split()
        results = []
        for word in res:
            #print("Printing word {}".format(word))
            word_list = wordninja.split(word)
            #print("Printing word list {}".format(word_list))
            results.append(word_list)
        flat_results = [item for sublist in results for item in sublist]

        for index, word in enumerate(flat_results):
            if (len(word) <= 3) or (word.isalpha == False) or (word in not_to_keep):
                if index == 0:
                    dataframe['Interest_Request'][row] = dataframe['Interest_Request'][row].replace(word + ' ', ' ')
                elif index == (len(res) - 1):
                    dataframe['Interest_Request'][row] = dataframe['Interest_Request'][row].replace(' ' + word , ' ')
                else:
                    dataframe['Interest_Request'][row] = dataframe['Interest_Request'][row].replace(' ' + word + ' ', ' ')

    return dataframe

def tfidf_features(dataframe, tfidf):
    """
    This method used the TF-IDF vectorizer used during training for the model on use for analysis
    and transform the sniffed data, preparing this way the features for prediction.
    It returns these features.
    """
    features = tfidf.transform(dataframe.Interest_Request).toarray()
    return features
