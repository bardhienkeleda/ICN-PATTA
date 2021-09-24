# Classifiers setup phase

This first part of the project aims to perform an offline analysis of a dataset collected performing website scrapping. It is mainly divided in three parts:

1. STEP 1: Web scraping for 6 webpage categories, visiting both main pages and all links this main page contains. The collected dataset is placed in module `dataset`.
2. STEP 2: Use the dataset to train different ML models.
3. STEP 3: Use the trained models from STEP 2 to predict which is the requested page from a certain user.

## Usage

The repo contains three main modules:

 - Components: contains all scripts for the preprocessing part from dataframe preparation to calculation of TF-IDF scores. It also contains the class of all ML models used for training and cross-validation part.
 - Domain: contains the collected dataset from STEP 1.
 - Utils: contains a configuration file and the scripts for obtaining all the plots and metrics.

 Running  `python main.py` will do the job.


