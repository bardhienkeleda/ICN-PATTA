#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: enkeledabardhi
"""

import pandas as pd
import numpy as np
import random
import tldextract
from os.path import dirname, abspath

BASIC_DIRECTORY = (abspath(dirname(__file__)))
domain_path = BASIC_DIRECTORY + "/URL_Classification.csv"

def get_domains(df, label):
    domain_list = []
    for row in range(len(df)):
        if df['Label'][row] == label:
            #print(dataframe['Full request URI'][row])
            parse = tldextract.extract(df["Full request URI"][row])
            name = parse.domain
            domain_list.append(name)

    domain_list = list(set(domain_list))
    print(label)
    print(len(domain_list))
    updated_list = random.sample(domain_list, int(0.1 * len(domain_list)))
    print(len(updated_list))

    return updated_list

if __name__ == "__main__":

    dataframe = pd.read_csv(domain_path)
    dataframe.drop("1", axis=1, inplace=True)
    dataframe.dropna(inplace = True)
    dataframe = dataframe.reset_index(drop=True)
    dataframe.columns = ["Full request URI", "Label"]
    occ = dataframe.groupby('Label').size()
    print(dataframe.head(5))
    print(occ)

    url_occ = dataframe.groupby("Full request URI").size()
    categories = dataframe.Label.unique()
    #print(categories[0])
    #domains = get_domains(dataframe, "Business")
    #print(domains)

    list_domains = []

    for label in categories:
        mask = dataframe['Label'] == label
        pos = np.flatnonzero(mask)
        sub_df = dataframe.iloc[pos]
        sub_df = sub_df.reset_index()
        sub_df.drop('index', axis=1, inplace = True)
        #print(sub_df)
        label_domains = get_domains(sub_df, label)
        list_domains.append(label_domains)

    #flat_list_domains = [item for sublist in list_domains for item in sublist]

    #print(cat_dict.keys()[0])
    #dfs = []
    test_df = pd.DataFrame(columns = dataframe.columns)
    #print(df)

    for cat_number in range(len(list_domains)):
        df = pd.DataFrame(columns = dataframe.columns)
        cat_list = list_domains[cat_number]
        cat_name = categories[cat_number]
        print(cat_number)
        print(cat_name)
        print(len(cat_list))
        #print("\n\n")

        for row in range(len(dataframe)):
            if dataframe['Label'][row] == cat_name:
                parse = tldextract.extract(dataframe["Full request URI"][row])
                name = parse.domain
                #print("Dataframe reow {} and domain name {}:".format(dataframe["Full request URI"][row], name))
                if name in cat_list:
                    #print(name)
                    df = df.append(dataframe.iloc[row], ignore_index = True)
                    #dataframe.drop(dataframe.index[[row]], inplace=True)
                    #dataframe = dataframe.reset_index(drop=True)
        #print("Printing updated dataframe\n")
        #print(dataframe)
        test_df = test_df.append(df, ignore_index= True)
        print("Printing test dataframe\n")
        print(test_df)
        df.to_csv(cat_name + ".csv")
    test_df.to_csv("flex_test.csv")
    train_test_df = pd.concat([dataframe, test_df]).drop_duplicates(keep=False)
    train_test_df.to_csv("train_test_set.csv")
