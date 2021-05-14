# ICN-PATTA

This repo contains the source code for the implementation of our paper entitled *ICN PATTA: ICN Privacy Attack Through Traffic Analysis*.
The project contains two main modules:
1. Classifiers setup: used for classifiers training phase.
2. Real time classification: used for mini-NDN simulations and real time classification by the attacker.

## Usage
Documentation in order reproduce our work can be found in:
- [Classifiers setup phase:] (https://github.com/bardhienkeleda/ICN-PATTA/blob/main/classifiers_setup/README.md)
- [Real-time classification phase:] (https://github.com/bardhienkeleda/ICN-PATTA/blob/main/real_time_classification/README.md)

## Setup

MiniNDN uses the local installed binaries of NDN therefore a complete installation of ndn-cxx and NFD is necessary. For simpler and faster topology setup install NLSR, a service discovery service. For the full list of required libraries and the corresponding version, check `system_requirements.txt`.
