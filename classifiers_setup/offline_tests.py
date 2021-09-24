#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: enkeledabardhi
"""

import os
import glob
import pandas as pd
import pickle
import re
from utils import new_configuration
from os.path import dirname, abspath

BASIC_DIRECTORY = (abspath(dirname(__file__)))
domain_path = BASIC_DIRECTORY + "/domain/computer_test_set.csv"
tfidf_vector_path = BASIC_DIRECTORY + "/components/saved_tfidf_vectors/"
models_path = BASIC_DIRECTORY + "/components/saved_models/"
words = "679"
grams = "1gram_"


def preprocessing(df):
    """
    Method used to preprocess the dataset performing cleansing and splitting of URLs into BoW.
    It returns the preprocessed dataframe.
    """
    not_to_keep = []

    """
    for webpg in range (len(new_configuration.webpages_list)):
        div = re.sub('[^A-Za-z0-9]+', ' ', str(new_configuration.webpages_list[webpg]))
        not_to_keep.append(div)
    for webpg in range (len(not_to_keep)):
        not_to_keep[webpg] = not_to_keep[webpg].split(" ")
    """

    # prepare a list of words that should be droped
    #words_to_delete = [item for sublist in not_to_keep for item in sublist]
    not_to_keep.append('http')
    not_to_keep.append('wwwf')
    #words_to_delete.append('co') #
    not_to_keep.append('php')
    not_to_keep.append('html')
    #words_to_delete.append('cn') #
    not_to_keep.append('www')

    #words_to_delete = list(set(words_to_delete))

    dataframe = df.copy()
    #print(dataframe.head(5))
    # delete all the special characters from each url
    for row in range (0, len(df)):
        word_pattern = re.compile('[^A-Za-z0-9]+')
        dataframe['Full request URI'][row] = word_pattern.sub(' ', str(df['Full request URI'][row]))
        res = dataframe['Full request URI'][row].split()
        #print("Res: {}".format(res))
        #results = []

        for index, word in enumerate(res):
            if (len(word) <= 3) or (word.isalpha == False) or (word in not_to_keep):
            #if word in not_to_keep:
                if index == 0:
                    dataframe['Full request URI'][row] = dataframe['Full request URI'][row].replace(word + ' ', ' ')
                    #print(value)
                    #print(dataframe['Full request URI'][row])
                elif index == (len(res) - 1):
                    dataframe['Full request URI'][row] = dataframe['Full request URI'][row].replace(' ' + word , ' ')
                else:
                    dataframe['Full request URI'][row] = dataframe['Full request URI'][row].replace(' ' + word + ' ', ' ')

    dataframe.columns = ['Full_NDN_interest', 'Label']

    return dataframe

if __name__ == '__main__':

    dataframe = pd.read_csv(domain_path)
    dataframe = dataframe.drop('Unnamed: 0', 1)
    print(dataframe.head(5))

    dataframe = preprocessing(dataframe)
    dataframe["Category_ID"] = 0
    print(dataframe.head(5))


    with open(BASIC_DIRECTORY + "/" + "labels_dictionary.txt", "rb") as file:
        labels_dictionary = pickle.load(file)
    print(labels_dictionary)
    loaded_model = pickle.load(open(models_path + "multinomial_model_1gram_679feat.sav", "rb"),  encoding="latin1")
    loaded_tfidf = pickle.load(open(tfidf_vector_path + "tfidf_vector_1gram_679feat.pk", "rb"),  encoding="latin1")

    test_features = loaded_tfidf.transform(dataframe['Full_NDN_interest']).toarray()
    print(test_features)
    test_labels = dataframe.Category_ID
    correct_prediction = 0

    for row in range(len(test_features)):
        print(dataframe['Full_NDN_interest'][row])
        prediction = loaded_model.predict([test_features[row]])
        print(prediction)
        if prediction == 0:
            correct_prediction += 1

    acc = correct_prediction / len(test_features)
    print(acc)
