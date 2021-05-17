#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: enkeledabardhi
"""
import pickle
import numpy as np
import configuration
import re
from sklearn.feature_extraction.text import TfidfVectorizer
from os.path import dirname, abspath

tfidf_vectors_path = (abspath(dirname(__file__)) + "/saved_tfidf_vectors")

def preprocessing(dataframe):
    """
    This method is used to perform the same preprocessing that is performed offline in the collected dataset.
    It allows to transform the sniffed traffic into BoW, filters and cleans.
    It returns the preprocessed data in form of a dataframe.
    """
    not_to_keep = []
    for webpg in range (len(configuration.webpages_list)):
        div = re.sub('[^A-Za-z0-9]+', ' ', str(configuration.webpages_list[webpg]))
        not_to_keep.append(div)
    for webpg in range (len(not_to_keep)):
        not_to_keep[webpg] = not_to_keep[webpg].split(" ")

    # prepare a list of words that should be droped
    words_to_delete = [item for sublist in not_to_keep for item in sublist]
    #words_to_delete = list(itertools.chain(*not_to_keep))
    words_to_delete.append('http')
    words_to_delete.append('wwwf')
    words_to_delete.append('co')
    words_to_delete.append('php')
    words_to_delete.append('html')
    words_to_delete.append('cn')
    words_to_delete.append('ndn')
    words_to_delete.append('PR')
    words_to_delete.append('P1')
    words_to_delete.append('site')

    words_to_delete = list(set(words_to_delete))

    # delete all the special characters from each url
    for row in range (len(dataframe)):
        dataframe['Interest_Request'][row] = re.sub('[^A-Za-z0-9]+', ' ', str(dataframe['Interest_Request'][row]))
        res = dataframe['Interest_Request'][row].split()

        for index, word in enumerate(res):
            if word in words_to_delete:
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
