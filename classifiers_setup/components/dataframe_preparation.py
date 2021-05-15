#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: enkeledabardhi
"""
from os.path import abspath, dirname
from utils import configuration
import pandas as pd
import re
import sklearn
import numpy as np
import pickle
from sklearn.utils import shuffle
from sklearn.feature_selection import chi2
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn import preprocessing

"""
This class preprocess the dataset by filling some missing values, dropping NaN labeled rows,
deleting domain names and very frequently used words such as http, co, php etc.
Furthermore, it calculates TF-IDF features.
"""
class Preprocessing():

    def __init__(self):
        self.domain_path = abspath(dirname(__file__)  + '/../domain')
        self.tfidf_vectors_path = (abspath(dirname(__file__)) + "/saved_tfidf_vectors/saved_full_vectors")

    def preprocessing(self, df):
        """
        Method used to preprocess the dataset performing cleansing and splitting of URLs into BoW.
        It returns the preprocessed dataframe.
        """
        not_to_keep = []
        for webpg in range (len(configuration.webpages_list)):
            div = re.sub('[^A-Za-z0-9]+', ' ', str(configuration.webpages_list[webpg]))
            not_to_keep.append(div)
        for webpg in range (len(not_to_keep)):
            not_to_keep[webpg] = not_to_keep[webpg].split(" ")

        # prepare a list of words that should be droped
        words_to_delete = [item for sublist in not_to_keep for item in sublist]
        words_to_delete.append('http')
        words_to_delete.append('wwwf')
        words_to_delete.append('co')
        words_to_delete.append('php')
        words_to_delete.append('html')
        words_to_delete.append('cn')
        words_to_delete = list(set(words_to_delete))

        # delete all the special characters from each url
        for row in range (0, len(df)):
            df['Full request URI'][row] = re.sub('[^A-Za-z0-9]+', ' ', str(df['Full request URI'][row]))
            res = df['Full request URI'][row].split()
            for index, word in enumerate(res):
                if word in words_to_delete:
                    if index == 0:
                        df['Full request URI'][row] = df['Full request URI'][row].replace(word + ' ', ' ')
                    elif index == (len(res) - 1):
                        df['Full request URI'][row] = df['Full request URI'][row].replace(' ' + word , ' ')
                    else:
                        df['Full request URI'][row] = df['Full request URI'][row].replace(' ' + word + ' ', ' ')
        df.columns = ['Full_NDN_interest', 'Label']

        return df


    def preparation(self):
        """
        Method used to prepare the final dataset by invoking the preprocessing method.
        Furthermore, it splits the dataset into train, test and also the label dictionary for later use.
        It returns the final dataframe.
        """

        df = pd.read_csv(self.domain_path + '/' + 'categorized_dataset.csv')
        """
        for row in range(len(df)):
            if df['Full request URI'][row] == 'http://baidu.com/':
                df['Label'][row] = 'baidu'
            elif df['Full request URI'][row] in ['http://www.tapad.com/', 'http://www.tapad.com/humans.txt']:
                df['Label'][row] = 'tapad'
            elif df['Full request URI'][row] in ['http://www.nyu.edu/', 'http://home.nyu.edu/']:
                df['Label'][row] = 'nyu'
            elif df['Full request URI'][row] == 'http://www.exeter.ac.uk/':
                df['Label'][row] = 'exeter'
            elif df['Full request URI'][row] == 'http://uea.ac.uk/':
                df['Label'][row] = 'uea'

        df = df.dropna()
        df = df.reset_index(drop=True)
        """

        if configuration.WRITE_TEST_TRAIN:
            # shuffle dataframe for more randomness
            df = shuffle(df)
            df = df.reset_index()
            # split 19504 instances of dataframe in train and test
            df_train = df.iloc[:13653]

            df_train.drop("index", axis=1, inplace=True)
            df_train = df_train.reset_index(drop=True)

            df_test = df.iloc[13653:]
            df_test.drop("index", axis=1, inplace=True)
            df_test = df_test.reset_index(drop=True)

            # write train and test dataframes into files for later use
            with open(self.domain_path + "/" + "train_instances_new.csv" , "w") as file:
            	df_train.to_csv(file)
            with open(self.domain_path + "/" + "test_instances_new.csv" , "w") as file:
            	df_test.to_csv(file)

        # call preprocessing method and preprocess dataframe
        df = df.reset_index(drop=True)
        df = self.preprocessing(df)

        # encode the labels
        self.label_encoder = preprocessing.LabelEncoder()
        df['Category_ID'] = self.label_encoder.fit_transform(df['Label'].tolist())
        # create a dictionary for later use
        labels_dictionary = dict(zip(self.label_encoder.classes_, self.label_encoder.transform(self.label_encoder.classes_)))
        # save labels for latter use in online analysis
    	with open("labels_dictionary.txt", "wb") as file:
    		file.write(pickle.dumps(labels_dictionary))

        return df

    def tfidf_features(self):
        """
        Method used to calculate the TF-IDF features for training and testing phase.
        It returnsboth train and test features and labels, tfidf vectorizer.
        """
         # load train and test instances into dataframes
         train_df = pd.read_csv(self.domain_path + "/" + "train_instances_new.csv")
         train_df.drop("Unnamed: 0", axis=1, inplace=True)
         train_df = self.preprocessing(train_df)
         train_df['Category_ID'] = self.label_encoder.transform(train_df['Label'].tolist())

         test_df = pd.read_csv(self.domain_path + "/" + "test_instances_new.csv")
         test_df.drop("Unnamed: 0", axis=1, inplace=True)
         test_df = self.preprocessing(test_df)
         test_df['Category_ID'] = self.label_encoder.transform(test_df['Label'].tolist())

         # calculate tfidf for both train and test
         self.tfidf = TfidfVectorizer(sublinear_tf=True, min_df =5,  ngram_range=configuration.GRAMS, max_features= configuration.NUMBER_FEATURES, stop_words='english') #
         self.train_features = self.tfidf.fit_transform(train_df.Full_NDN_interest).toarray()
         self.test_features = self.tfidf.transform(test_df.Full_NDN_interest).toarray()
         # calculate labels for both train and test
         self.train_labels = train_df.Category_ID
         self.test_labels = test_df.Category_ID

         # save tfidf test vectors which will be used for online analysis
         if configuration.WRITE_MODELS:
    	     with open(self.tfidf_vectors_path + "/" + "tfidf_vector_1and2gram_maxfeat.pk" , "wb") as file:
    	     	pickle.dump(self.tfidf, file)
         print("Each of the %d training NDN interest names is represented by %d features" % (self.train_features.shape))
         print("Each of the %d test NDN interest names is represented by %d features" % (self.test_features.shape))

         return self.train_features, self.test_features, self.tfidf, self.train_labels, self.test_labels

    def most_correlated_terms(self):

        """
        Function used to calculate and print the most N correlated terms for a certain N
        """
        N = 3
        for Label, category_id in sorted(self.category_to_id.items()):

            features_chi2 = chi2(self.train_features, self.train_labels == category_id)
            indices = np.argsort(features_chi2[0])
            feature_names = np.array(self.tfidf.get_feature_names())[indices]
            unigrams = [v for v in feature_names if len(v.split(' ')) == 1]
            bigrams = [v for v in feature_names if len(v.split(' ')) == 2]
            print("\n==> %s:" %(Label))
            print("  * Most Correlated Unigrams are: %s" %(', '.join(unigrams[-N:])))
            print("  * Most Correlated Bigrams are: %s" %(', '.join(bigrams[-N:])))

    def label_dictionaries(self, dataframe):

        # create dictionaries of labels
        category_id_df = dataframe[['Label', 'Category_ID']].drop_duplicates()
        self.category_to_id = dict(category_id_df.values)
        self.id_to_category = dict(category_id_df[['Category_ID', 'Label']].values)

        return category_id_df, self.category_to_id, self.id_to_category
