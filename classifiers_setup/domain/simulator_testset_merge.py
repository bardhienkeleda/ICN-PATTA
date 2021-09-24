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
df1 = pd.read_csv("sunporno.csv")
df1.columns = ['Full request URI']
df1['Label'] = 'Adult'
#print(df1)
dfs = dfs.append(df1, ignore_index = True)

df2 = pd.read_csv("rollingstone.csv")
df2.columns = ['Full request URI']
df2['Label'] = 'Arts & Entertainment'
#print(df2)
dfs = dfs.append(df2, ignore_index = True)

df3 = pd.read_csv("harvard.csv")
df3.columns = ['Full request URI']
df3['Label'] = 'Education'
#print(df3)
dfs = dfs.append(df3, ignore_index = True)

df4 = pd.read_csv("astrology-zodiac-signs.csv")
df4.columns = ['Full request URI']
df4['Label'] = 'Faith & Beliefs'
#print(df4)
dfs = dfs.append(df4, ignore_index = True)

df5 = pd.read_csv("rxlist.csv")
df5.columns = ['Full request URI']
df5['Label'] = 'Health'
#print(df5)
dfs = dfs.append(df5, ignore_index = True)

df6 = pd.read_csv("nytimes.csv")
df6.columns = ['Full request URI']
df6['Label'] = 'News'
#print(df5)
dfs = dfs.append(df6, ignore_index = True)

df7 = pd.read_csv("galeon.csv")
df7.columns = ['Full request URI']
df7['Label'] = 'Technology'
#print(df7)
dfs = dfs.append(df7, ignore_index = True)

df8 = pd.read_csv("test_instances_new.csv")
df8 = df8.drop("Unnamed: 0", axis = 1)
dfs = dfs.append(df8, ignore_index = True)
#print(df8)

dfs = dfs.drop_duplicates()
dfs = dfs.reset_index(drop=True)
print(dfs.groupby('Label').size())
dfs = shuffle(dfs)
dfs = dfs.reset_index()
dfs = dfs.drop("index", axis = 1)
print(dfs)
dfs.to_csv("sim_test_set_lab.csv")

dfs['Full request URI'] = dfs['Full request URI'].str[7:]
#dfs = dfs.drop("index", axis = 1)
#print(dfs.head(10))

for i in range(len(dfs)):
    string = dfs['Full request URI'][i]
    for j in range(0, len(string)):
        if (string[j]=="?" or string[j]=="="):
            #print("String before removal %s " % string)
            string = string[:j] + "/" + string[j+1:]
            #print("String after removal %s" % string)
            dfs['Full request URI'][i] = string
            #print("Dataframe entry %s" % dfs['Full request URI'][i])

#dfs = dfs.drop("index", axis = 1)
dfs = dfs.drop('Label', axis=1)
#print(dfs)
dfs.to_csv("sim_test_set.csv")
