#!/usr/bin/env python2
import os
import logging
import ast
import time
import sys
from datetime import datetime
from os.path import dirname, abspath
import argparse
import pandas as pd
import numpy as np
from logs_parser import Parsing
from prep import preprocessing, tfidf_features
from mininet.log import setLogLevel, info, debug

base_path = (abspath(dirname(__file__)))
logs_path = os.path.join(base_path, '..', 'logs_results/')

logging.basicConfig(
    level=os.environ.get("LOGLEVEL", "INFO"),
    format="%(levelname)s [%(name)s] %(message)s"
)
if __name__ == '__main__':

    log = logging.getLogger("attacker:main")
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument("-at", "--attackerTime", type=float, help="Time for attacker's analysis (expressed in seconds)")
    arg_parser.add_argument("-am", "--attackerModel", type=str, help="Machine Learning model used by the attacker",
                                choices = ["linear_1_893","linear_1_1785",
                                "linear_2_460", "linear_2_917",
                                "linear_1and2_1350", "linear_1and2_2700",
                                "multinomial_1_893","multinomial_1_1785",
                                "multinomial_2_500", "multinomial_2_917",
                                "multinomial_1and2_1350", "multinomial_1and2_2700",
                                "svm_1_893","svm_1_1785",
                                "svm_2_460", "svm_2_917",
                                "svm_1and2_1350", "svm_1and2_2700"])
    args = arg_parser.parse_args()

    # time variables for triggering the attacker
    simulation_duration = 600
    time_pointer = time.time()
    time_start_simulation_permanent = time.time()

    # prepare the data
    parsing_df= Parsing(args.attackerModel, args.attackerTime)
    loaded_model, loaded_tfidf, labels_dictionary = parsing_df.ArgParser()
    out_file = open(logs_path  + "multinomial_1_1785/" + "5victims/" + "multinomial_1_1785_4.txt", "w")
    # start analysis
    while True:
        if time.time() >= time_pointer + args.attackerTime:
            time_pointer = time.time()
            dataframe = parsing_df.LogParser()
            parsed_dataframe = parsing_df.ParseDataframe(dataframe)

            if parsed_dataframe is None or len(parsed_dataframe)==0:
                pass
            else:
                prep_dataframe = preprocessing(parsed_dataframe)
                prep_dataframe = prep_dataframe.drop(['Request_Time', 'Delta_Time', 'Data'], 1)

                features = tfidf_features(prep_dataframe, loaded_tfidf)
                for row in range(len(features)):
                    start_pred_time = time.time()
                    prediction = loaded_model.predict([features[row]])
                    stop_pred_time = time.time()
                    prediction_time = stop_pred_time - start_pred_time
                    predicted = int(prediction)
                    inverse_labels_dictionary = {value:key for key, value in labels_dictionary.items()}

                    # make prediction on requested content and write results
                    if predicted in inverse_labels_dictionary.keys():
                        name = inverse_labels_dictionary.get(predicted)
                        log.info("Victim requested content from: {}".format(name))
                        out_file.write("Real request: {}, Attacker's prediction: {}, Prediction time: {}\n".format(prep_dataframe['Interest_Request'][row], name, prediction_time))

        if time.time() >= time_start_simulation_permanent + float(simulation_duration):
            break
    # write results
    out_file.write("Number of legitime requests from victim(s): {}".format(len(dataframe)))
    out_file.close()
