#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: enkeledabardhi
"""
import cPickle as pickle
from components.dataframe_preparation import Preprocessing
from components.ml_models import Models
from utils import configuration
from utils.plots import training_instances_plot, ocurrencies_plot, pca_plot


def main():
    prep = Preprocessing()
    df = prep.preparation()
    train_features, test_features, tf_idf, train_labels, test_labels = prep.tfidf_features()
    category_df, category_to_id, id_to_category = prep.label_dictionaries(df)

    model = Models(df, train_features, test_features, train_labels, test_labels, category_df)
    model.random_forests()
    model.linear_svc()
    model.multinomial_nb()
    model.support_vectors()
    model.cross_validating()

    #prep.most_correlated_terms()

    if configuration.PLOT_CON:

        training_instances_plot(df)
        print("Head of category dataframe: \n {} \n Category to ID dictionary: {} \n ID to category dictionary: {}".format(category_df, category_to_id, id_to_category))
        ocurrencies_plot(df)
        pca_plot(df, features)

if __name__ == "__main__":
    main()
