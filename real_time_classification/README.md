# Real-time classification phase

This second part of the project aims to implement and evaluate the attack through a real tome classification in mini-NDN simulator.

## Usage

The repo contains three main modules:

 - app_classes: contains all the costumized applications for all nodes participating in the network: *victim(s)*, *attacker* and *producer(s)*.
 - app_executables: contains the executables that run in each node during simulation.
 - domain: contains the NDN dataset obtained during the first phase.
 - ndn_core: contains the costumized miniNDN and NFD classes.
 - Topologies: contain the yaml files representing the network topologies.

 To run a simualtion:  `sudo python exp.py -rf test_set.csv -t Topologies/topology_5_victims.yaml -f 5000.0 -l 1000 -a 0.95 -sr 1 -at 10.0000 -am "svm_1_1642"`.

## Parameter Tuning

Parameters for *topology*:
- Topologies/topology_1_victim.yaml
- Topologies/topology_5_victims.yaml

Parameters for *-am (attacker model)*:
- linear_1_500
- linear_1_900
- linear_1_1300
- linear_1_1642
- linear_2_500
- linear_2_700
- linear_2_900
- linear_2_1362
- linear_1and2_500
- linear_1and2_900
- linear_1and2_1300
- linear_1and2_1700
- linear_1and2_2100
- linear_1and2_2500
- linear_1and2_3004
- multinomial_1_500
- multinomial_1_900
- multinomial_1_1300
- multinomial_1_1642
- multinomial_2_500
- multinomial_2_700
- multinomial_2_900
- multinomial_2_1362
- multinomial_1and2_500
- multinomial_1and2_900
- multinomial_1and2_1300
- multinomial_1and2_1700
- multinomial_1and2_2100
- multinomial_1and2_2500
- multinomial_1and2_3004
- rf_1_500
- rf_1_900
- rf_1_1300
- rf_1_1642
- rf_2_500
- rf_2_700
- rf_2_900
- rf_2_1362
- rf_1and2_500
- rf_1and2_900
- rf_1and2_1300
- rf_1and2_1700
- rf_1and2_2100
- rf_1and2_2500
- rf_1and2_3004
- svm_1_500
- svm_1_900
- svm_1_1300
- svm_1_1642
- svm_2_500
- svm_2_700
- svm_2_900
- svm_2_1362
- svm_1and2_500
- svm_1and2_900
- svm_1and2_1300
- svm_1and2_1700
- svm_1and2_2100
- svm_1and2_2500
- svm_1and2_3004

The other parameters such as *-rf (requests file)*, *-f (freshness)*, *-l (name length)*, *-sr(sending rate)*, *-a(Zipf alpha parameter)* and *-at(attacker analysis time)* are kept constant during evaluation.
