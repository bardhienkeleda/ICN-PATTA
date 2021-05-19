#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: enkeledabardhi
"""
import pickle
import pandas as pd
import seaborn as sns
import matplotlib
import matplotlib.pyplot as plt
from utils import configuration
from os.path import dirname, abspath

from sklearn.naive_bayes import MultinomialNB
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import LinearSVC
from sklearn.svm import SVC

from sklearn import metrics
from sklearn.metrics import confusion_matrix
from sklearn.model_selection import cross_val_score
from sklearn.model_selection import train_test_split

"""
This class is used to train different ML models and save them for later use.
Each method trains a certain model and plots its results.
Furthermore, the cross_validating method is used for CV of selected models.
"""

class Models():
    def __init__(self, dataframe, train_feat, test_feat, train_lab, test_lab, category_df):
        self.models_path = abspath(dirname(__file__) + "/saved_models")
        self.cv_models_path = abspath(dirname(__file__)  + '/saved_models/saved_cv_models/mindf_5')
        self.train_features = train_feat
        self.test_features = test_feat
        self.train_labels = train_lab
        self.test_labels = test_lab
        self.df = dataframe
        self.cat_df = category_df
        self.models = [
            RandomForestClassifier(n_estimators=200, max_depth=5, random_state=0), #class_weight = 'balanced'
            LinearSVC(),
            MultinomialNB(),
            SVC(C = 10.0, kernel = 'rbf', gamma = 'scale')
        ]

        self.X_train = self.train_features
        self.y_train = self.train_labels
        self.X_test = self.test_features
        self.y_test = self.test_labels

    def random_forests(self):
        rf_model = self.models[0]
        rf_model.fit(self.X_train, self.y_train)
        y_pred = rf_model.predict(self.X_test)

        if configuration.PLOT_CON:
            print(self.df['Label'].unique())
            print('\t\t\t\tCLASSIFICATIION METRICS RF\n')
            print(metrics.classification_report(self.y_test, y_pred, target_names= self.df['Label'].unique()))
        if configuration.PLOT_CM:
            print('\t\t\t\tCONFUSION MATRIX FOR RF\n')
            conf_mat = confusion_matrix(self.y_test, y_pred)
            fig, ax = plt.subplots(figsize=(8,8))
            sns.heatmap(conf_mat, annot=True, cmap="Blues", fmt='d',
                        xticklabels=self.cat_df.Label.values,
                        yticklabels=self.cat_df.Label.values)
            plt.ylabel('Actual')
            plt.xlabel('Predicted')
            plt.title("CONFUSION MATRIX - RF\n", size=16);
            plt.show()
        if configuration.WRITE_MODELS:
	    	rf_filename = "rf_model_1gram_653feat.sav"
	    	pickle.dump(rf_model, open(self.models_path + '/' + rf_filename, 'wb'))
        return rf_model

    def linear_svc(self):
        linear_model = self.models[1]
        linear_model.fit(self.X_train, self.y_train)
        y_pred = linear_model.predict(self.X_test)

        if configuration.PLOT_CON:
            print('\t\t\t\tCLASSIFICATIION METRICS LINEAR SVC\n')
            print(metrics.classification_report(self.y_test, y_pred, target_names= self.df['Label'].unique()))
        if configuration.PLOT_CM:
            conf_mat = confusion_matrix(self.y_test, y_pred)
            fig, ax = plt.subplots(figsize=(8,8))
            sns.heatmap(conf_mat, annot=True, cmap="Blues", fmt='d',
                        xticklabels=self.cat_df.Label.values,
                        yticklabels=self.cat_df.Label.values)
            plt.ylabel('Actual')
            plt.xlabel('Predicted')
            plt.title("CONFUSION MATRIX - LinearSVC\n", size=16);
            plt.show()
        if configuration.WRITE_MODELS:
	     	linear_filename = "linear_model_1gram_653feat.sav"
	    	pickle.dump(linear_model, open(self.models_path + '/' + linear_filename, 'wb'))
        return linear_model

    def multinomial_nb(self):
        multinomial_model = self.models[2]
        multinomial_model.fit(self.X_train, self.y_train)
        y_pred = multinomial_model.predict(self.X_test)

        if configuration.PLOT_CON:
            print('\t\t\t\tCLASSIFICATIION METRICS MNB\n')
            print(metrics.classification_report(self.y_test, y_pred, target_names= self.df['Label'].unique()))
        if configuration.PLOT_CM:
            conf_mat = confusion_matrix(self.y_test, y_pred)
            fig, ax = plt.subplots(figsize=(8,8))
            sns.heatmap(conf_mat, annot=True, cmap="Blues", fmt='d',
                        xticklabels=self.cat_df.Label.values,
                        yticklabels=self.cat_df.Label.values)
            plt.ylabel('Actual')
            plt.xlabel('Predicted')
            plt.title("CONFUSION MATRIX - MNB\n", size=16);
            plt.show()
        if configuration.WRITE_MODELS:
            multinomial_filename = "multinomial_model_1gram_653feat_dom.sav"
            pickle.dump(multinomial_model, open(self.models_path + '/' + multinomial_filename, 'wb'))
        return multinomial_model

    def support_vectors(self):
        svc_model = self.models[3]
        svc_model.fit(self.X_train, self.y_train)
        y_pred = svc_model.predict(self.X_test)

        if configuration.PLOT_CON:
            print('\t\t\t\tCLASSIFICATIION METRICS SVC\n')
            print(metrics.classification_report(self.y_test, y_pred, target_names= self.df['Label'].unique()))
        if configuration.PLOT_CM:
            conf_mat = confusion_matrix(self.y_test, y_pred)
            fig, ax = plt.subplots(figsize=(8,8))
            sns.heatmap(conf_mat, annot=True, cmap="Blues", fmt='d',
                        xticklabels=self.cat_df.Label.values,
                        yticklabels=self.cat_df.Label.values)
            plt.ylabel('Actual')
            plt.xlabel('Predicted')
            plt.title("CONFUSION MATRIX - SVC\n", size=16);
            plt.show()
        if configuration.WRITE_MODELS:
            svm_filename = "svm_model_1gram_653feat.sav"
            pickle.dump(svc_model, open(self.models_path + '/' + svm_filename, 'wb'))
        return svc_model

    def cross_validating(self):
        CV = 5
        cv_df = pd.DataFrame(index=range(CV * len(self.models)))
        entries = []
        self.cv_models = [
            RandomForestClassifier(n_estimators=200, max_depth=5, random_state=0), #class_weight = 'balanced'
            LinearSVC(),
            MultinomialNB(),
            SVC(C = 10.0, kernel = 'rbf', gamma = 'scale')
        ]
        for model in self.cv_models:
            model_name = model.__class__.__name__
            accuracies = cross_val_score(model, self.X_train, self.y_train, scoring='accuracy', cv=CV)
            for fold_idx, accuracy in enumerate(accuracies):
                entries.append((model_name, fold_idx, accuracy))

            cv_df = pd.DataFrame(entries, columns=['model_name', 'fold_idx', 'accuracy'])
            mean_accuracy = cv_df.groupby('model_name').accuracy.mean()
            std_accuracy = cv_df.groupby('model_name').accuracy.std()
            acc = pd.concat([mean_accuracy, std_accuracy], axis= 1,
                  ignore_index=True)
            acc.columns = ['Mean Accuracy', 'Standard deviation']
        print(acc)
