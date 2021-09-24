#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Aug 30 22:22:07 2020

@author: enkeledabardhi
"""

import os
import glob
import pandas as pd
from sklearn.utils import shuffle

#os.chdir("/Users/enkeledabardhi/opt/MyProjects/MasterThesis/")

#all_files = glob.glob(os.path.join(path, "*.csv"))
#extension = 'csv'
#all_filenames = [i for i in glob.glob('*.{}'.format(extension))]
dfs = []
dfs = pd.DataFrame()
df1 = pd.read_csv("categorized_dataset.csv")
df1 = df1.drop("Unnamed: 0", axis = 1)
dfs = dfs.append(df1, ignore_index = True)

df2 = pd.read_csv("tech_dataset.csv")
df2 = df2.drop("Unnamed: 0", axis = 1)
dfs = dfs.append(df2, ignore_index = True)

df3 = pd.read_csv("news_dataset.csv")
df3 = df3.drop("Unnamed: 0", axis = 1)
#print(df3)
dfs = dfs.append(df3, ignore_index = True)
#print(dfs)
#dfs = dfs.drop_duplicates()
df4 = pd.read_csv("adult_dataset.csv")
df4 = df4.drop("Unnamed: 0", axis = 1)
dfs = dfs.append(df4, ignore_index = True)

df5 = pd.read_csv("artsentert_dataset.csv")
df5 = df5.drop("Unnamed: 0", axis = 1)
dfs = dfs.append(df5, ignore_index = True)

df6 = pd.read_csv("religion_dataset.csv")
df6 = df6.drop("Unnamed: 0", axis = 1)
dfs = dfs.append(df6, ignore_index = True)

df7 = pd.read_csv("education_dataset.csv")
df7 = df7.drop("Unnamed: 0", axis = 1)
dfs = dfs.append(df7, ignore_index = True)

df8 = pd.read_csv("health_dataset.csv")
df8 = df8.drop("Unnamed: 0", axis = 1)
dfs = dfs.append(df8, ignore_index = True)

print(df8)

dfs = dfs.drop_duplicates()
dfs = dfs.reset_index(drop=True)
print(dfs.groupby('Label').size())
print(dfs)
dfs.to_csv("updated_dataset.csv")

# shuffle dataframe for more randomness
dfs = shuffle(dfs)
dfs = dfs.reset_index()
#print(df.head(5))
# split 19504 instances of dataframe in train and test
df_train = dfs.iloc[:13738]
df_train.drop("index", axis=1, inplace=True)
#print(df_train.head(5))
#df_train.drop("Unnamed: 0", axis=1, inplace=True)
df_train = df_train.reset_index(drop=True)
#print(df_train.head(5))

df_test = dfs.iloc[13738:]
df_test.drop("index", axis=1, inplace=True)
df_test = df_test.reset_index(drop=True)

# write train and test dataframes into files for later use
with open("train_instances_new.csv" , "w") as file:
	df_train.to_csv(file)
with open("test_instances_new.csv" , "w") as file:
	df_test.to_csv(file)
