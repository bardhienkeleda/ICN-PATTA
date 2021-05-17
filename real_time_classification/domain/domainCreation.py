#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: enkeledabardhi
"""

import os
import glob
import pandas as pd

if __name__ == '__main__':

    dataframe = pd.read_csv('test_instances_new.csv')
    dataframe = dataframe.drop('Label', 1)
    dataframe = dataframe.drop('Unnamed: 0', 1)
    print(dataframe.head(5))
    dataframe['Full request URI'] = dataframe['Full request URI'].str[6:]
    print(dataframe.head(5))

    for i in range(len(dataframe)):
        string = dataframe['Full request URI'][i]
        for j in range(0,len(string)):
            if (string[j]=="?" or string[j]=="="):
                print("String before removal %s " % string)
                string = string[:j] + "/" + string[j+1:]
                print("String after removal %s" % string)
                dataframe['Full request URI'][i] = string
                print("Dataframe entry %s" % dataframe['Full request URI'][i])

    dataframe.to_csv('test_set_new.csv')
