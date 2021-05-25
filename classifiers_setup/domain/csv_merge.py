#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Aug 30 22:22:07 2020

@author: enkeledabardhi
"""

import os
import glob
import pandas as pd

#os.chdir("/Users/enkeledabardhi/opt/MyProjects/MasterThesis/")

#all_files = glob.glob(os.path.join(path, "*.csv"))
extension = 'csv'
all_filenames = [i for i in glob.glob('*.{}'.format(extension))]
dfs = pd.DataFrame()
for file in all_filenames:
    df = pd.read_csv(file, encoding='latin-1')
    df.columns = ['Full request URI']
    print(df)
    dfs = dfs.append(df, ignore_index = True)
dfs['Label'] = 'Technology'
dfs.to_csv("tech_dataset.csv")
"""
#combine all files in the list
combined_csv = pd.concat([pd.read_csv(f, encoding='latin-1') for f in all_filenames ]) #
#export to csv
combined_csv.to_csv( "tech_dataset.csv", index=False, encoding='utf-8-sig')
"""
