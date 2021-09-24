#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Aug 30 22:22:07 2020

@author: enkeledabardhi
"""

import os
import glob
import pandas as pd

extension = 'csv'
all_filenames = [i for i in glob.glob('*.{}'.format(extension))]
print(all_filenames)
dfs = pd.DataFrame()
for file in all_filenames:
    df = pd.read_csv(file, encoding='latin-1')
    df.columns = ['Full request URI']
    dfs = dfs.append(df, ignore_index = True)
dfs['Label'] = 'Health'
dfs.to_csv("health_dataset.csv")
