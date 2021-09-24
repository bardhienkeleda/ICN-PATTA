# Real-time classification phase

This second part of the project aims to implement and evaluate the attack through a real tome classification in mini-NDN simulator.

## Usage

The repo contains three main modules:

 - app_classes: contains all the costumized applications for all nodes participating in the network: *victim(s)*, *attacker* and *producer(s)*.
 - app_executables: contains the executables that run in each node during simulation.
 - domain: contains the NDN dataset obtained during the first phase.
 - ndn_core: contains the costumized miniNDN and NFD classes.
 - Topologies: contain the yaml files representing the network topologies.

 To run a simualtion:  `sudo python exp.py -rf sim_test_set.csv -t Topologies/topology_5_victims.yaml -f 5000.0 -l 1000 -a 0.95 -sr 1 -at 10.0000 -am "svm_1_1785"`.

## Parameter Tuning

Parameters for *topology*:
- Topologies/topology_1_victim.yaml
- Topologies/topology_5_victims.yaml

Parameters for *-am (attacker model)*:
- linear_1_893
- linear_1_1785
- linear_2_460
- linear_2_917
- linear_1and2_1350
- linear_1and2_2700
- multinomial_1_893
- multinomial_1_1785
- multinomial_2_460
- multinomial_2_917
- multinomial_1and2_1350
- multinomial_1and2_2700
- svm_1_893
- svm_1_1785
- svm_2_460
- svm_2_917
- svm_1and2_1350
- svm_1and2_2700

The other parameters such as *-rf (requests file)*, *-f (freshness)*, *-l (name length)*, *-sr(sending rate)*, *-a(Zipf alpha parameter)* and *-at(attacker analysis time)* are kept constant during evaluation.
