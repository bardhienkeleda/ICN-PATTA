#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: enkeledabardhi
"""

import pandas as pd
from sklearn.utils import shuffle
Write= True

if __name__ == '__main__':

    dataframe = pd.read_csv('labeled_dataset_1.csv')

    cs = ['baidu', 'apache', 'gnu', 'lycos', 'icio', 'tripod', 'wikidot']
    edu = ['mit', 'washington', 'ox', 'nyu', 'ufl', 'bu', 'lse', 'leeds', 'imperial', 'open', 'exeter', 'reading', 'uea', 'kit']
    entert = ['gohoi', 'itfactly', 'imageshack', 'alternativenation', 'tamilyogi', 'bizrate']
    news = ['sigonews', 'chinanews', 'palermotoday', 'tusciaweb', 'irishnews', 'asianews','rai']
    life = ['salute', 'mapei', 'spuntiespuntini']
    culture = ['spettacolovivo', 'italia', 'treccani']
    politics = ['governo', 'senato']

    for i in range(0, len(dataframe)):
        if dataframe['Label'][i] in cs:
            dataframe['Label'][i] = 'computer science'
        elif dataframe['Label'][i] in edu:
            dataframe['Label'][i] = 'education'
        elif dataframe['Label'][i] in entert:
            dataframe['Label'][i] = 'entertainment'
        elif dataframe['Label'][i] in news:
            dataframe['Label'][i] = 'news'
        elif dataframe['Label'][i] in life:
            dataframe['Label'][i] = 'life care'
        elif dataframe['Label'][i] in culture:
            dataframe['Label'][i] = 'culture'
        elif dataframe['Label'][i] in politics:
            dataframe['Label'][i] = 'politics'

    dataframe = dataframe.dropna()
    dataframe = dataframe.reset_index(drop=True)
    dataframe.to_csv("categorized_dataset.csv")

    if Write:
        # shuffle dataframe for more randomness
        dataframe = shuffle(dataframe)
        dataframe = dataframe.reset_index()
        #print(df.head(5))
        # split 19504 instances of dataframe in train and test
        df_train = dataframe.iloc[:13653]
        df_train.drop("index", axis=1, inplace=True)
        #print(df_train.head(5))
        #df_train.drop("Unnamed: 0", axis=1, inplace=True)
        df_train = df_train.reset_index(drop=True)
        #print(df_train.head(5))

        df_test = dataframe.iloc[13653:]
        df_test.drop("index", axis=1, inplace=True)
        df_test = df_test.reset_index(drop=True)

        # write train and test dataframes into files for later use
        with open("train_instances_new.csv" , "w") as file:
        	df_train.to_csv(file)
        with open("test_instances_new.csv" , "w") as file:
        	df_test.to_csv(file)
    print(dataframe)
