#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: enkeledabardhi
"""
import random
from utils import configuration
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.cm as cm
from sklearn.decomposition import PCA

"""
Functions used for plotting purposes.
"""
def training_instances_plot(dataframe):

    dataframe.Label.value_counts().plot(figsize=(12,5),kind='bar',color='green')
    plt.xlabel('Category')
    plt.ylabel('Total Number Of Individual Category for Training')
    plt.show()

def ocurrencies_plot(dataframe):
    fig = plt.figure(figsize=(8,6))
    colors = ['grey','grey','grey','grey','grey','grey','grey','grey','grey','grey','grey','grey','grey','grey','grey','grey','grey','grey','grey','grey','grey','grey','grey','grey','grey','grey','grey','grey','grey','grey','grey','darkblue','darkblue','darkblue','darkblue','darkblue','darkblue','darkblue','darkblue','darkblue','darkblue']
    dataframe.groupby('Label').Full_NDN_interest.count().sort_values().plot.barh(ylim=0, color=colors, title= 'Number of NDN interests requests in each NDN namespace category\n')
    plt.ylabel('Category',fontsize = 10)
    plt.xlabel('Number of ocurrences', fontsize = 10)
    plt.show()


def pca_plot(dataframe, features):
    pca = PCA(n_components = 2)
    components = pca.fit_transform(features)
    colors = ["#"+''.join([random.choice('0123456789ABCDEF') for j in range(6)]) for i in range(configuration.MAX_WEBPAGES)]
    dict_colors = {i: colors[i-1] for i in range(0,configuration.MAX_WEBPAGES)}
    dict_labels = {i: configuration.domains[i] for i in range(0,configuration.MAX_WEBPAGES)}
    cat_colors = [dict_colors[dataframe['Category_ID'][i]] for i in range(19520)]
    plt.scatter(components[:,0], components[:,1], c=cat_colors)
    plt.xlabel("First component", fontsize=12)
    plt.ylabel("Second component", fontsize=12)
    plt.title('PCA analysis for {} NDN namespaces and {} words considered'.format(configuration.MAX_WEBPAGES, configuration.NUMBER_FEATURES))
    #plt.legend()
    plt.show()
