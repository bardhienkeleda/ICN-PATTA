# Real-time classification phase

This second part of the project aims to implement and evaluate the attack through a real tome classification in mini-NDN simulator.

## Usage

The repo contains three main modules:

 - app_classes: contains all the costumized applications for all nodes participating in the network: *victim(s)*, *attacker* and *producer(s)*.
 - app_executables: contains the executables that run in each node during simulation.
 - domain: contains the NDN dataset obtained during # Classifiers setup phase.
 - ndn_core: contains the costumized miniNDN and NFD classes.
 - Topologies: contain the yaml files representing the network topologies.

 Running  `python main.py` will do the job.

## Parameter Tuning

 In order to tune the scripts with the desired parameters, `utils/configuration.py` should be changed. You can change the number of the considered webpages for the analysis (`MAX_WEBPAGES` and `MIN_WEBPAGES`), TF-IDF tuning with respect to the number of features used and N-grams (`NUMBER_FEATURES` and `GRAMS`). Finally, for plotting the desired graphs and results, change `PLOT_CON` to True or False.
