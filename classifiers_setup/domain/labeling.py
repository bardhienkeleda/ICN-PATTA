#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: enkeledabardhi
"""

import pandas as pd

if __name__ == '__main__':

    dataframe = pd.read_csv('labeled_dataset_1.csv')

    cs = ['baidu', 'apache', 'gnu', 'tapad', 'icio', 'tripod', 'wikidot']
    edu = ['mit', 'washington', 'ox', 'nyu', 'ufl', 'bu', 'lse', 'leeds', 'imperial', 'open', 'exeter', 'reading', 'uea', 'kit']
    entert = ['gohoi', 'itfactly', 'imageshack', 'alternativenation']
    news = ['sigonews', 'chinanews', 'palermotoday', 'tusciaweb', 'irishnews', 'asianews', 'senato', 'governo', 'rai']
    life = ['bizrate', 'salute', 'mapei', 'spuntiespuntini']
    culture = ['spettacolovivo', 'italia', 'treccani', 'tamilyogi']

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
    dataframe = dataframe.dropna()
    dataframe = dataframe.reset_index(drop=True)
    dataframe.to_csv("categorized_dataset.csv")
    print(dataframe)
