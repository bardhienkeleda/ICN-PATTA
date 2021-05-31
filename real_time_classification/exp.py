#!/usr/bin/env python2

import os
from datetime import datetime, timedelta
from os.path import dirname, abspath

#from argparse import ArgumentParser
import argparse
import yaml
import sys
from typing import List
import pandas as pd
from pprint import pformat
from time import sleep

from mininet.log import setLogLevel, info, debug
from mininet.topo import Topo

from minindn.minindn import Minindn
from minindn.util import MiniNDNCLI
from minindn.apps.app_manager import AppManager
from minindn.apps.application import Application
from minindn.apps.nfd import Nfd
from minindn.apps.nlsr import Nlsr
from minindn.apps.tshark import Tshark

from app_classes.consumer_class import ConsumerApp
from app_classes.producer_class import ProducerApp
from app_classes.attacker_class import AttackerApp

from ndn_core.special_minindn import SpecialMinindn
from ndn_core.special_nfd import SpecialNFD

isCLIEnabled = False
SimulationDuration = 600 # expressed in seconds

"""
This is the overall experiment.
"""

if __name__ == '__main__':

	setLogLevel('info')

	SpecialMinindn.cleanUp()
	SpecialMinindn.verifyDependencies()

	parser = argparse.ArgumentParser()
	ndn = SpecialMinindn(parser=parser)
	args = ndn.args

	#start ndn
	ndn.start()

	all_hosts = ndn.net.hosts
	producers = [i for i in ndn.net.hosts if i.name in ndn.groups["producers"]]
	victims = [i for i in ndn.net.hosts if i.name in ndn.groups["victims"]]
	attacker = [i for i in ndn.net.hosts if i.name in ndn.groups["attacker"]]
	routers = [i for i in ndn.net.hosts if i.name in ndn.groups["routers"]]
	sub_hosts = victims+attacker+producers


	info('Starting NFD on all the hosts (consumers, producers, attacker)\n')
	nfds = AppManager(ndn, sub_hosts, SpecialNFD, environments=ndn.environments)

	info("Starting NFD on routers\n")
        nfds = AppManager(ndn, routers, SpecialNFD,
                          environments=ndn.environments,
                          csPolicy=ndn.args.cacheStrategy,
                          csSize=ndn.args.cacheSize,
                          csUnsolicitedPolicy="admit-all")

	info('Starting NLSR on nodes\n')
	nlsrs = AppManager(ndn, ndn.net.hosts, Nlsr)

	info("Starting NDN producer application on %s\n" % ndn.groups["producers"])
	nodes_args = {}
	for i, node_name in enumerate(sorted(ndn.groups["producers"])):
		nodes_args[node_name] = {
    			"requestsFile": ndn.requestsFile,
    			"prefix": "/ndn/%s-site/%s" % (node_name, node_name),
    			"freshness": ndn.freshness}
	producers_s = AppManager(ndn, producers, ProducerApp, nodes_args = nodes_args)

	info("Starting NDN attacker application on %s\n" % attacker)
	attacker_s = AppManager(ndn, attacker, AttackerApp, attackerTime = ndn.attackerTime, attackerModel=ndn.attackerModel)

	info("Starting NDN consumer application on %s\n" % victims)
	consumers_s = AppManager(
		    ndn, victims, ConsumerApp,
		    requestsFile=ndn.requestsFile,
		    length=ndn.length,
		    sendingRate=ndn.sendingRate,
		    alpha=ndn.alpha,
		    prefixes=' '.join(["/ndn/%s-site/%s" % (p, p) for p in sorted(ndn.groups["producers"])]))
	#sleep(40)

	if isCLIEnabled:
		MiniNDNCLI(ndn.net)
	else:
		info("Simulation started:\t%s\n" % datetime.now())
		info("Estimated time of simulation end:\t%s\n" % (datetime.now() + timedelta(seconds=SimulationDuration)))

		sleep(SimulationDuration)
	ndn.stop()
