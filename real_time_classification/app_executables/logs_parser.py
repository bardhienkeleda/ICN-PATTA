#!/usr/bin/env python2
import os
import glob
import pickle
import pandas as pd
import numpy as np
import logging
from mininet.log import info

logging.basicConfig(
    level=os.environ.get("LOGLEVEL", "INFO"),
    format="%(levelname)s [%(name)s] %(message)s"
)
"""
Parsing class is used by the attacker to simulate traffic sniffing task.
It picks a set of logs created from the victims traffic, the ML model and time interval used by the attacker for the analysis,
and it returns the issued interests by the victim(s) in the determined interval of time.
"""
class Parsing():

    def __init__(self, analysisModel, analysisTime):
        self.log = logging.getLogger("attacker:parsing")
        self.working_directory =  "/tmp/minindn/"
        self.basic_directory = "/home/bardhi/mini-ndn/examples/my_simulation/app_executables"
        self.mid_path_model = "/saved_models/"
        self.mid_path_vector = "/saved_tfidf_vectors/"
        self.start_analysis_pointer = 0
        self.stop_analysis_pointer = 0
        self.analysisTime = analysisTime
        self.last_analysed_request_time = 0
        self.analysisModel = analysisModel
        self.log.info("Attacker model {}".format(self.analysisModel))

    def ArgParser(self):
        """
        This method gets the command line parameters for the attacker node and parses them,
        loading the indicated ML model for the analysis and the respective TF-IDF vectorizer.
        It returns the model and the vectorizer.
        """
        with open(self.basic_directory + "/" + "labels_dictionary.txt", "rb") as file:
            labels_dictionary = pickle.load(file)
            #self.log.info(labels_dictionary)

        if self.analysisModel == "linear_1_500":
        	self.log.info("Attacker is using the Linear SVC model trained with 1-grams on 500-features\n")
        	loaded_model = pickle.load(open(self.basic_directory + self.mid_path_model + "linear_model_1gram_500feat.sav", "rb"))
        	loaded_tfidf = pickle.load(open(self.basic_directory + self.mid_path_vector + "tfidf_vector_1gram_500feat.pk", "rb"))

        elif self.analysisModel == "linear_1_900":
        	self.log.info("Attacker is using the Linear SVC model trained with 1-grams on 900-features\n")
        	loaded_model = pickle.load(open(self.basic_directory + self.mid_path_model + "linear_model_1gram_900feat.sav", "rb"))
        	loaded_tfidf = pickle.load(open(self.basic_directory + self.mid_path_vector + "tfidf_vector_1gram_900feat.pk", "rb"))

        elif self.analysisModel == "linear_1_1300":
        	self.log.info("Attacker is using the Linear SVC model trained with 1-grams on 1300-features\n")
        	loaded_model = pickle.load(open(self.basic_directory + self.mid_path_model +"linear_model_1gram_1300feat.sav", "rb"))
        	loaded_tfidf = pickle.load(open(self.basic_directory + self.mid_path_vector + "tfidf_vector_1gram_1300feat.pk", "rb"))

        elif self.analysisModel == "linear_1_1642":
        	self.log.info("Attacker is using the Linear SVC model trained with 1-grams on 1642-features\n")
        	loaded_model = pickle.load(open(self.basic_directory + self.mid_path_model +"linear_model_1gram_1642feat.sav", "rb"))
        	loaded_tfidf = pickle.load(open(self.basic_directory + self.mid_path_vector + "tfidf_vector_1gram_1642feat.pk", "rb"))

        elif self.analysisModel == "linear_2_500":
        	self.log.info("Attacker is using the Linear SVC model trained with 2-grams on 500-features\n")
        	loaded_model = pickle.load(open(self.basic_directory + self.mid_path_model +"linear_model_2gram_500feat.sav", "rb"))
        	loaded_tfidf = pickle.load(open(self.basic_directory + self.mid_path_vector + "tfidf_vector_2gram_500feat.pk", "rb"))

        elif self.analysisModel == "linear_2_700":
        	self.log.info("Attacker is using the Linear SVC model trained with 2-grams on 700-features\n")
        	loaded_model = pickle.load(open(self.basic_directory + self.mid_path_model +"linear_model_2gram_700feat.sav", "rb"))
        	loaded_tfidf = pickle.load(open(self.basic_directory + self.mid_path_vector + "tfidf_vector_2gram_700feat.pk", "rb"))

        elif self.analysisModel == "linear_2_900":
        	self.log.info("Attacker is using the Linear SVC model trained with 2-grams on 900-features\n")
        	loaded_model = pickle.load(open(self.basic_directory + self.mid_path_model +"linear_model_2gram_900feat.sav", "rb"))
        	loaded_tfidf = pickle.load(open(self.basic_directory + self.mid_path_vector + "tfidf_vector_2gram_900feat.pk", "rb"))

        elif self.analysisModel == "linear_2_1362":
        	self.log.info("Attacker is using the Linear SVC model trained with 2-grams on 1362-features\n")
        	loaded_model = pickle.load(open(self.basic_directory + self.mid_path_model +"linear_model_2gram_1362feat.sav", "rb"))
        	loaded_tfidf = pickle.load(open(self.basic_directory + self.mid_path_vector + "tfidf_vector_2gram_1362feat.pk", "rb"))

        elif self.analysisModel == "linear_1and2_500":
        	self.log.info("Attacker is using the Linear SVC model trained with both 1 and 2-grams on 500-features\n")
        	loaded_model = pickle.load(open(self.basic_directory + self.mid_path_model +"linear_model_1and2gram_500feat.sav", "rb"))
        	loaded_tfidf = pickle.load(open(self.basic_directory + self.mid_path_vector + "tfidf_vector_1and2gram_500feat.pk", "rb"))

        elif self.analysisModel == "linear_1and2_900":
        	self.log.info("Attacker is using the Linear SVC model trained with both 1 and 2-grams on 900-features\n")
        	loaded_model = pickle.load(open(self.basic_directory + self.mid_path_model + "linear_model_1and2gram_900feat.sav", "rb"))
        	loaded_tfidf = pickle.load(open(self.basic_directory + self.mid_path_vector + "tfidf_vector_1and2gram_900feat.pk", "rb"))

        elif self.analysisModel == "linear_1and2_1300":
        	self.log.info("Attacker is using the Linear SVC model trained with both 1 and 2-grams on 1300-features\n")
        	loaded_model = pickle.load(open(self.basic_directory + self.mid_path_model + "linear_model_1and2gram_1300feat.sav", "rb"))
        	loaded_tfidf = pickle.load(open(self.basic_directory + self.mid_path_vector + "tfidf_vector_1and2gram_1300feat.pk", "rb"))

        elif self.analysisModel == "linear_1and2_1700":
        	self.log.info("Attacker is using the Linear SVC model trained with both 1 and 2-grams on 1700-features\n")
        	loaded_model = pickle.load(open(self.basic_directory + self.mid_path_model + "linear_model_1and2gram_1700feat.sav", "rb"))
        	loaded_tfidf = pickle.load(open(self.basic_directory + self.mid_path_vector + "tfidf_vector_1and2gram_1700feat.pk", "rb"))

        elif self.analysisModel == "linear_1and2_2100":
        	self.log.info("Attacker is using the Linear SVC model trained with both 1 and 2-grams on 2100-features\n")
        	loaded_model = pickle.load(open(self.basic_directory + self.mid_path_model + "linear_model_1and2gram_2100feat.sav", "rb"))
        	loaded_tfidf = pickle.load(open(self.basic_directory + self.mid_path_vector + "tfidf_vector_1and2gram_2100feat.pk", "rb"))

        elif self.analysisModel == "linear_1and2_2500":
        	self.log.info("Attacker is using the Linear SVC model trained with both 1 and 2-grams on 2500-features\n")
        	loaded_model = pickle.load(open(self.basic_directory + self.mid_path_model + "linear_model_1and2gram_2500feat.sav", "rb"))
        	loaded_tfidf = pickle.load(open(self.basic_directory + self.mid_path_vector + "tfidf_vector_1and2gram_2500feat.pk", "rb"))

        elif self.analysisModel == "linear_1and2_3005":
        	self.log.info("Attacker is using the Linear SVC model trained with both 1 and 2-grams on 3005-features\n")
        	loaded_model = pickle.load(open(self.basic_directory + self.mid_path_model + "linear_model_1and2gram_3005feat.sav", "rb"))
        	loaded_tfidf = pickle.load(open(self.basic_directory + self.mid_path_vector + "tfidf_vector_1and2gram_3005feat.pk", "rb"))

        elif self.analysisModel == "multinomial_1_500":
        	self.log.info("Attacker is using the Multinomial NB model trained with 1-grams on 500-features\n")
        	loaded_model = pickle.load(open(self.basic_directory + self.mid_path_model + "multinomial_model_1gram_500feat.sav", "rb"))
        	loaded_tfidf = pickle.load(open(self.basic_directory + self.mid_path_vector + "tfidf_vector_1gram_500feat.pk", "rb"))

        elif self.analysisModel == "multinomial_1_900":
        	self.log.info("Attacker is using the MultinomialNB model trained with 1-grams on 900-features\n")
        	loaded_model = pickle.load(open(self.basic_directory + self.mid_path_model + "multinomial_model_1gram_900feat.sav", "rb"))
        	loaded_tfidf = pickle.load(open(self.basic_directory + self.mid_path_vector + "tfidf_vector_1gram_900feat.pk", "rb"))

        elif self.analysisModel == "multinomial_1_1300":
        	self.log.info("Attacker is using the MultinomialNB model trained with 1-grams on 1300-features\n")
        	loaded_model = pickle.load(open(self.basic_directory + self.mid_path_model + "multinomial_model_1gram_1300feat.sav", "rb"))
        	loaded_tfidf = pickle.load(open(self.basic_directory + self.mid_path_vector + "tfidf_vector_1gram_1300feat.pk", "rb"))

        elif self.analysisModel == "multinomial_1_1642":
        	self.log.info("Attacker is using the MultinomialNB model trained with 1-grams on 1642-features\n")
        	loaded_model = pickle.load(open(self.basic_directory + self.mid_path_model + "multinomial_model_1gram_1642feat.sav", "rb"))
        	loaded_tfidf = pickle.load(open(self.basic_directory + self.mid_path_vector + "tfidf_vector_1gram_1642feat.pk", "rb"))

        elif self.analysisModel == "multinomial_2_500":
        	self.log.info("Attacker is using the MultinomialNB model trained with 2-grams on 500-features\n")
        	loaded_model = pickle.load(open(self.basic_directory + self.mid_path_model + "multinomial_model_2gram_500feat.sav", "rb"))
        	loaded_tfidf = pickle.load(open(self.basic_directory + self.mid_path_vector + "tfidf_vector_2gram_500feat.pk", "rb"))

        elif self.analysisModel == "multinomial_2_700":
        	self.log.info("Attacker is using the MultinomialNB model trained with 2-grams on 700-features\n")
        	loaded_model = pickle.load(open(self.basic_directory + self.mid_path_model + "multinomial_model_2gram_700feat.sav", "rb"))
        	loaded_tfidf = pickle.load(open(self.basic_directory + self.mid_path_vector + "tfidf_vector_2gram_700feat.pk", "rb"))

        elif self.analysisModel == "multinomial_2_900":
        	self.log.info("Attacker is using the MultinomialNB model trained with 2-grams on 900-features\n")
        	loaded_model = pickle.load(open(self.basic_directory + self.mid_path_model + "multinomial_model_2gram_900feat.sav", "rb"))
        	loaded_tfidf = pickle.load(open(self.basic_directory + self.mid_path_vector + "tfidf_vector_2gram_900feat.pk", "rb"))

        elif self.analysisModel == "multinomial_2_1362":
        	self.log.info("Attacker is using the MultinomialNB model trained with 2-grams on 1362-features\n")
        	loaded_model = pickle.load(open(self.basic_directory + self.mid_path_model + "multinomial_model_2gram_1362feat.sav", "rb"))
        	loaded_tfidf = pickle.load(open(self.basic_directory + self.mid_path_vector + "tfidf_vector_2gram_1362feat.pk", "rb"))

        elif self.analysisModel == "multinomial_1and2_500":
        	self.log.info("Attacker is using the MultinomialNB model trained with both 1 and 2-grams on 500-features\n")
        	loaded_model = pickle.load(open(self.basic_directory + self.mid_path_model + "multinomial_model_1and2gram_500feat.sav", "rb"))
        	loaded_tfidf = pickle.load(open(self.basic_directory + self.mid_path_vector + "tfidf_vector_1and2gram_500feat.pk", "rb"))

        elif self.analysisModel == "multinomial_1and2_900":
        	self.log.info("Attacker is using the MultinomialNB model trained with both 1 and 2-grams on 900-features\n")
        	loaded_model = pickle.load(open(self.basic_directory + self.mid_path_model + "multinomial_model_1and2gram_900feat.sav", "rb"))
        	loaded_tfidf = pickle.load(open(self.basic_directory + self.mid_path_vector + "tfidf_vector_1and2gram_900feat.pk", "rb"))

        elif self.analysisModel == "multinomial_1and2_1300":
        	self.log.info("Attacker is using the MultinomialNB model trained with both 1 and 2-grams on 1300-features\n")
        	loaded_model = pickle.load(open(self.basic_directory + self.mid_path_model + "multinomial_model_1and2gram_1300feat.sav", "rb"))
        	loaded_tfidf = pickle.load(open(self.basic_directory + self.mid_path_vector + "tfidf_vector_1and2gram_1300feat.pk", "rb"))

        elif self.analysisModel == "multinomial_1and2_1700":
        	self.log.info("Attacker is using the MultinomialNB model trained with both 1 and 2-grams on 1700-features\n")
        	loaded_model = pickle.load(open(self.basic_directory + self.mid_path_model + "multinomial_model_1and2gram_1700feat.sav", "rb"))
        	loaded_tfidf = pickle.load(open(self.basic_directory + self.mid_path_vector + "tfidf_vector_1and2gram_1700feat.pk", "rb"))

        elif self.analysisModel == "multinomial_1and2_2100":
        	self.log.info("Attacker is using the MultinomialNB model trained with both 1 and 2-grams on 2100-features\n")
        	loaded_model = pickle.load(open(self.basic_directory + self.mid_path_model + "multinomial_model_1and2gram_2100feat.sav", "rb"))
        	loaded_tfidf = pickle.load(open(self.basic_directory + self.mid_path_vector + "tfidf_vector_1and2gram_2100feat.pk", "rb"))

        elif self.analysisModel == "multinomial_1and2_2500":
        	self.log.info("Attacker is using the MultinomialNB model trained with both 1 and 2-grams on 2500-features\n")
        	loaded_model = pickle.load(open(self.basic_directory + self.mid_path_model + "multinomial_model_1and2gram_2500feat.sav", "rb"))
        	loaded_tfidf = pickle.load(open(self.basic_directory + self.mid_path_vector + "tfidf_vector_1and2gram_2500feat.pk", "rb"))

        elif self.analysisModel == "multinomial_1and2_3005":
        	self.log.info("Attacker is using the MultinomialNB model trained with both 1 and 2-grams on 3005-features\n")
        	loaded_model = pickle.load(open(self.basic_directory + self.mid_path_model + "multinomial_model_1and2gram_3005feat.sav", "rb"))
        	loaded_tfidf = pickle.load(open(self.basic_directory + self.mid_path_vector + "tfidf_vector_1and2gram_3005feat.pk", "rb"))

        elif self.analysisModel == "rf_1_500":
            self.log.info("Attacker is using the RandomForestClassifier model trained with 1-grams on 500-features\n")
            loaded_model = pickle.load(open(self.basic_directory + self.mid_path_model + "rf_model_1gram_500feat.sav", "rb"))
            loaded_tfidf = pickle.load(open(self.basic_directory + self.mid_path_vector + "tfidf_vector_1gram_500feat.pk", "rb"))

        elif self.analysisModel == "rf_1_900":
            self.log.info("Attacker is using the RandomForestClassifier model trained with 1-grams on 900-features\n")
            loaded_model = pickle.load(open(self.basic_directory + self.mid_path_model + "rf_model_1gram_900feat.sav", "rb"))
            loaded_tfidf = pickle.load(open(self.basic_directory + self.mid_path_vector + "tfidf_vector_1gram_900feat.pk", "rb"))

        elif self.analysisModel == "rf_1_1300":
            self.log.info("Attacker is using the RandomForestClassifier model trained with 1-grams on 1300-features\n")
            loaded_model = pickle.load(open(self.basic_directory + self.mid_path_model + "rf_model_1gram_1300feat.sav", "rb"))
            loaded_tfidf = pickle.load(open(self.basic_directory + self.mid_path_vector + "tfidf_vector_1gram_1300feat.pk", "rb"))

        elif self.analysisModel == "rf_1_1642":
            self.log.info("Attacker is using the RandomForestClassifier model trained with 1-grams on 1642-features\n")
            loaded_model = pickle.load(open(self.basic_directory + self.mid_path_model + "rf_model_1gram_1642feat.sav", "rb"))
            loaded_tfidf = pickle.load(open(self.basic_directory + self.mid_path_vector + "tfidf_vector_1gram_1642feat.pk", "rb"))

        elif self.analysisModel == "rf_2_500":
            self.log.info("Attacker is using the RandomForestClassifier model trained with 2-grams on 500-features\n")
            loaded_model = pickle.load(open(self.basic_directory + self.mid_path_model + "rf_model_2gram_500feat.sav", "rb"))
            loaded_tfidf = pickle.load(open(self.basic_directory + self.mid_path_vector + "tfidf_vector_2gram_500feat.pk", "rb"))

        elif self.analysisModel == "rf_2_700":
            self.log.info("Attacker is using the RandomForestClassifier model trained with 2-grams on 700-features\n")
            loaded_model = pickle.load(open(self.basic_directory + self.mid_path_model + "rf_model_2gram_700feat.sav", "rb"))
            loaded_tfidf = pickle.load(open(self.basic_directory + self.mid_path_vector + "tfidf_vector_2gram_700feat.pk", "rb"))

        elif self.analysisModel == "rf_2_900":
            self.log.info("Attacker is using the RandomForestClassifier model trained with 2-grams on 900-features\n")
            loaded_model = pickle.load(open(self.basic_directory + self.mid_path_model + "rf_model_2gram_900feat.sav", "rb"))
            loaded_tfidf = pickle.load(open(self.basic_directory + self.mid_path_vector + "tfidf_vector_2gram_900feat.pk", "rb"))

        elif self.analysisModel == "rf_2_1362":
            self.log.info("Attacker is using the RandomForestClassifier model trained with 2-grams on 1362-features\n")
            loaded_model = pickle.load(open(self.basic_directory + self.mid_path_model + "rf_model_2gram_1362feat.sav", "rb"))
            loaded_tfidf = pickle.load(open(self.basic_directory + self.mid_path_vector + "tfidf_vector_2gram_1362feat.pk", "rb"))

        elif self.analysisModel == "rf_1and2_500":
            self.log.info("Attacker is using the RandomForestClassifier model trained with both 1 and 2-grams on 500-features\n")
            loaded_model = pickle.load(open(self.basic_directory + self.mid_path_model + "rf_model_1and2gram_500feat.sav", "rb"))
            loaded_tfidf = pickle.load(open(self.basic_directory + self.mid_path_vector + "tfidf_vector_1and2gram_500feat.pk", "rb"))

        elif self.analysisModel == "rf_1and2_900":
            self.log.info("Attacker is using the RandomForestClassifier model trained with both 1 and 2-grams on 900-features\n")
            loaded_model = pickle.load(open(self.basic_directory + self.mid_path_model + "rf_model_1and2gram_900feat.sav", "rb"))
            loaded_tfidf = pickle.load(open(self.basic_directory + self.mid_path_vector + "tfidf_vector_1and2gram_900feat.pk", "rb"))

        elif self.analysisModel == "rf_1and2_1300":
            self.log.info("Attacker is using the RandomForestClassifier model trained with both 1 and 2-grams on 1300-features\n")
            loaded_model = pickle.load(open(self.basic_directory + self.mid_path_model + "rf_model_1and2gram_1300feat.sav", "rb"))
            loaded_tfidf = pickle.load(open(self.basic_directory + self.mid_path_vector + "tfidf_vector_1and2gram_1300feat.pk", "rb"))

        elif self.analysisModel == "rf_1and2_1700":
            self.log.info("Attacker is using the RandomForestClassifier model trained with both 1 and 2-grams on 1700-features\n")
            loaded_model = pickle.load(open(self.basic_directory + self.mid_path_model + "rf_model_1and2gram_1700feat.sav", "rb"))
            loaded_tfidf = pickle.load(open(self.basic_directory + self.mid_path_vector + "tfidf_vector_1and2gram_1700feat.pk", "rb"))

        elif self.analysisModel == "rf_1and2_2100":
            self.log.info("Attacker is using the RandomForestClassifier model trained with both 1 and 2-grams on 2100-features\n")
            loaded_model = pickle.load(open(self.basic_directory + self.mid_path_model + "rf_model_1and2gram_2100feat.sav", "rb"))
            loaded_tfidf = pickle.load(open(self.basic_directory + self.mid_path_vector + "tfidf_vector_1and2gram_2100feat.pk", "rb"))

        elif self.analysisModel == "rf_1and2_2500":
            self.log.info("Attacker is using the RandomForestClassifier model trained with both 1 and 2-grams on 2500-features\n")
            loaded_model = pickle.load(open(self.basic_directory + self.mid_path_model + "rf_model_1and2gram_2500feat.sav", "rb"))
            loaded_tfidf = pickle.load(open(self.basic_directory + self.mid_path_vector + "tfidf_vector_1and2gram_2500feat.pk", "rb"))

        elif self.analysisModel == "rf_1and2_3005":
            self.log.info("Attacker is using the RandomForestClassifier model trained with both 1 and 2-grams on 3005-features\n")
            loaded_model = pickle.load(open(self.basic_directory + self.mid_path_model + "rf_model_1and2gram_3005feat.sav", "rb"))
            loaded_tfidf = pickle.load(open(self.basic_directory + self.mid_path_vector + "tfidf_vector_1and2gram_3005feat.pk", "rb"))

        elif self.analysisModel == "svm_1_500":
            self.log.info("Attacker is using the SVC model trained with 1-grams on 500-features\n")
            loaded_model = pickle.load(open(self.basic_directory + self.mid_path_model + "svm_model_1gram_500feat.sav", "rb"))
            loaded_tfidf = pickle.load(open(self.basic_directory + self.mid_path_vector + "tfidf_vector_1gram_500feat.pk", "rb"))

        elif self.analysisModel == "svm_1_900":
            self.log.info("Attacker is using the SVC model trained with 1-grams on 900-features\n")
            loaded_model = pickle.load(open(self.basic_directory + self.mid_path_model + "svm_model_1gram_900feat.sav", "rb"))
            loaded_tfidf = pickle.load(open(self.basic_directory + self.mid_path_vector + "tfidf_vector_1gram_900feat.pk", "rb"))

        elif self.analysisModel == "svm_1_1300":
            self.log.info("Attacker is using the SVC model trained with 1-grams on 1300-features\n")
            loaded_model = pickle.load(open(self.basic_directory + self.mid_path_model + "svm_model_1gram_1300feat.sav", "rb"))
            loaded_tfidf = pickle.load(open(self.basic_directory + self.mid_path_vector + "tfidf_vector_1gram_1300feat.pk", "rb"))

        elif self.analysisModel == "svm_1_1642":
            self.log.info("Attacker is using the SVC model trained with 1-grams on 1642-features\n")
            loaded_model = pickle.load(open(self.basic_directory + self.mid_path_model + "svm_model_1gram_1642feat.sav", "rb"))
            loaded_tfidf = pickle.load(open(self.basic_directory + self.mid_path_vector + "tfidf_vector_1gram_1642feat.pk", "rb"))

        elif self.analysisModel == "svm_2_500":
            self.log.info("Attacker is using the SVC model trained with 2-grams on 500-features\n")
            loaded_model = pickle.load(open(self.basic_directory + self.mid_path_model + "svm_model_2gram_500feat.sav", "rb"))
            loaded_tfidf = pickle.load(open(self.basic_directory + self.mid_path_vector + "tfidf_vector_2gram_500feat.pk", "rb"))

        elif self.analysisModel == "svm_2_700":
            self.log.info("Attacker is using the SVC model trained with 2-grams on 700-features\n")
            loaded_model = pickle.load(open(self.basic_directory + self.mid_path_model + "svm_model_2gram_700feat.sav", "rb"))
            loaded_tfidf = pickle.load(open(self.basic_directory + self.mid_path_vector + "tfidf_vector_2gram_700feat.pk", "rb"))

        elif self.analysisModel == "svm_2_900":
            self.log.info("Attacker is using the SVC model trained with 2-grams on 900-features\n")
            loaded_model = pickle.load(open(self.basic_directory + self.mid_path_model + "svm_model_2gram_900feat.sav", "rb"))
            loaded_tfidf = pickle.load(open(self.basic_directory + self.mid_path_vector + "tfidf_vector_2gram_900feat.pk", "rb"))

        elif self.analysisModel == "svm_2_1362":
            self.log.info("Attacker is using the SVC model trained with 2-grams on 1362-features\n")
            loaded_model = pickle.load(open(self.basic_directory + self.mid_path_model + "svm_model_2gram_1362feat.sav", "rb"))
            loaded_tfidf = pickle.load(open(self.basic_directory + self.mid_path_vector + "tfidf_vector_2gram_1362feat.pk", "rb"))

        elif self.analysisModel == "svm_1and2_500":
            self.log.info("Attacker is using the SVC model trained with both 1 and 2-grams on 500-features\n")
            loaded_model = pickle.load(open(self.basic_directory + self.mid_path_model + "svm_model_1and2gram_500feat.sav", "rb"))
            loaded_tfidf = pickle.load(open(self.basic_directory + self.mid_path_vector + "tfidf_vector_1and2gram_500feat.pk", "rb"))

        elif self.analysisModel == "svm_1and2_900":
            self.log.info("Attacker is using the SVC model trained with both 1 and 2-grams on 900-features\n")
            loaded_model = pickle.load(open(self.basic_directory + self.mid_path_model + "svm_model_1and2gram_900feat.sav", "rb"))
            loaded_tfidf = pickle.load(open(self.basic_directory + self.mid_path_vector + "tfidf_vector_1and2gram_900feat.pk", "rb"))

        elif self.analysisModel == "svm_1and2_1300":
            self.log.info("Attacker is using the SVC model trained with both 1 and 2-grams on 1300-features\n")
            loaded_model = pickle.load(open(self.basic_directory + self.mid_path_model + "svm_model_1and2gram_1300feat.sav", "rb"))
            loaded_tfidf = pickle.load(open(self.basic_directory + self.mid_path_vector + "tfidf_vector_1and2gram_1300feat.pk", "rb"))

        elif self.analysisModel == "svm_1and2_1700":
            self.log.info("Attacker is using the SVC model trained with both 1 and 2-grams on 1700-features\n")
            loaded_model = pickle.load(open(self.basic_directory + self.mid_path_model + "svm_model_1and2gram_1700feat.sav", "rb"))
            loaded_tfidf = pickle.load(open(self.basic_directory + self.mid_path_vector + "tfidf_vector_1and2gram_1700feat.pk", "rb"))

        elif self.analysisModel == "svm_1and2_2100":
            self.log.info("Attacker is using the SVC model trained with both 1 and 2-grams on 2100-features\n")
            loaded_model = pickle.load(open(self.basic_directory + self.mid_path_model + "svm_model_1and2gram_2100feat.sav", "rb"))
            loaded_tfidf = pickle.load(open(self.basic_directory + self.mid_path_vector + "tfidf_vector_1and2gram_2100feat.pk", "rb"))

        elif self.analysisModel == "svm_1and2_2500":
            self.log.info("Attacker is using the SVC model trained with both 1 and 2-grams on 2500-features\n")
            loaded_model = pickle.load(open(self.basic_directory + self.mid_path_model + "svm_model_1and2gram_2500feat.sav", "rb"))
            loaded_tfidf = pickle.load(open(self.basic_directory + self.mid_path_vector + "tfidf_vector_1and2gram_2500feat.pk", "rb"))

        elif self.analysisModel == "svm_1and2_3005":
            self.log.info("Attacker is using the SVC model trained with both 1 and 2-grams on 3005-features\n")
            loaded_model = pickle.load(open(self.basic_directory + self.mid_path_model + "svm_model_1and2gram_3005feat.sav", "rb"))
            loaded_tfidf = pickle.load(open(self.basic_directory + self.mid_path_vector + "tfidf_vector_1and2gram_3005feat.pk", "rb"))
        else:
        	self.log.info("None of the models is passed for analysis\n")

        return loaded_model, loaded_tfidf, labels_dictionary

    def LogParser(self):
        """
        This method navigates into the log files created by the victim(s) in the working directory
        and returns the loaded data in a dataframe format.
        """

        # create a list of directories containing the logs of interest
        directory_list = [os.path.join(self.working_directory, o) for o in os.listdir(self.working_directory)
        			if os.path.isdir(os.path.join(self.working_directory, o)) and 'VI' in o]

        # create a list of logs of interest
        self.log.info(directory_list)

        dfs = []
        for directory in directory_list:
            new_path = directory + '/log/'
            os.chdir(new_path)
            for filename in os.listdir(new_path):
                if filename.endswith('.csv'):
                    self.log.info("Name of file {}".format(filename))
                    df = pd.read_csv(filename, delimiter = ' ')

                    df = df.drop(['/usr/local/lib/python2.7/dist-packages/PyNDN-2.11b1-py2.7.egg/pyndn/interest.py:24:', 					'CryptographyDeprecationWarning:', 'is', 'longer', 'by', 'the', 'Python.1', 'core', 'team.',
                               				'Support', 'for', 'it', 'is.1', 'now', 'deprecated', 'in','cryptography,', 'and', 'will',
                               				'be', 'removed', 'in.1', 'the.1', 'next','release.'], 1)
                    # rename columns
                    df.columns = ['Request_Time', 'Delta_Time', 'Interest_Request', 'Data']
                    self.log.info(df.head(5))
                    to_be_deleted = ['Traceback', 'recent','File','32]']
                    for i in range(len(df)):
                        row_value = str(df['Request_Time'][i])
                        if row_value in to_be_deleted:
                            df.drop([i], inplace=True)
                            df.reset_index(drop=True)
                    dfs.append(df)

        dataframe = pd.concat(dfs)
        dataframe.reset_index(drop=True, inplace=True)
        os.chdir(self.basic_directory)
        #dataframe.to_csv("full_df.csv")

        """
        # drop all unwanted columns
        dataframe = dataframe.drop(['/usr/local/lib/python2.7/dist-packages/PyNDN-2.11b1-py2.7.egg/pyndn/interest.py:24:', 					'CryptographyDeprecationWarning:', 'is', 'longer', 'by', 'the', 'Python.1', 'core', 'team.',
           				'Support', 'for', 'it', 'is.1', 'now', 'deprecated', 'in','cryptography,', 'and', 'will',
           				'be', 'removed', 'in.1', 'the.1', 'next','release.'], 1)
           # rename columns
        dataframe.columns = ['Request_Time', 'Delta_Time', 'Interest_Request', 'Data']
        dataframe.to_csv("before_drop_df.csv")
        #self.log.info(dataframe.head(5))
        # drop unwanted rows

        to_be_deleted = ['Traceback', 'recent','File','32]']
        for i in range(len(dataframe)):
            #self.log.info("Row value is {} and i is {}".format(dataframe['Request_Time'][i], i))
            row_value = str(dataframe['Request_Time'][i])
            #self.log.info("Type of {} is {}".format(row_value, type(row_value)))
            if row_value in to_be_deleted:
                dataframe.drop([i], inplace=True)
                dataframe.reset_index(drop=True)
            #self.log.info(dataframe.head(5))
        #dataframe.drop(dataframe.tail(14).index, inplace=True)
        #dataframe.reset_index(drop=True)
        # write dataframe to csv
        #dataframe.to_csv("after_drop_df.csv")
        """
        return dataframe

    def ParseDataframe(self, dataframe):
        """
        This method loads the dataframe containing victim(s)
        and returns only the requests contained in the time interval for attacker's analysis.
        """

        if len(dataframe) == 0:
        	self.log.info("The victim has not made a request yet")
        	return None
        else:
            if (dataframe.iloc[-1]['Request_Time'] > self.last_analysed_request_time):
                if(dataframe.iloc[-1]['Request_Time']  - self.analysisTime > self.last_analysed_request_time):
                    self.start_analysis_pointer = dataframe.iloc[-1]['Request_Time']  - self.analysisTime
                    self.stop_analysis_pointer = dataframe.iloc[-1]['Request_Time']

                else:
                    self.start_analysis_pointer = self.last_analysed_request_time + 0.00001
                    self.stop_analysis_pointer = dataframe.iloc[-1]['Request_Time']
                self.last_analysed_request_time = dataframe.iloc[-1]['Request_Time']
            else:
                pass

        parsed_dataframe = dataframe.copy()
        rows_to_keep = []
        for row in range(len(parsed_dataframe)):
            row_value = parsed_dataframe['Request_Time'][row]

            if (row_value >= self.start_analysis_pointer).any() and (row_value <= self.stop_analysis_pointer).any():
        		rows_to_keep.append(row)
        parsed_dataframe = parsed_dataframe.iloc[rows_to_keep]
        parsed_dataframe.reset_index(drop=True, inplace=True)

        return parsed_dataframe
