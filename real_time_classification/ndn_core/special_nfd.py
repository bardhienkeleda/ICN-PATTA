from pprint import pformat
from time import sleep
from mininet.log import setLogLevel, info, debug
from minindn.apps.nfd import Nfd
from minindn.apps.application import Application
from ndn_core.special_minindn import SpecialMinindn

"""
This is a NFD costumized class which inherits methods from native Nfd class.
"""

class SpecialNFD(Nfd):

	def __init__(self, node, environments=None, logLevel='NONE',csSize=65536, csPolicy="lru", csUnsolicitedPolicy="admit-all"):
	    super(SpecialNFD, self).__init__(node, logLevel, csSize, csPolicy, csUnsolicitedPolicy)
	    if environments is None:
	        environments = {}
	    environments[self.node.name]["DUMP_ENABLED"] = "%s/cs_dump.csv" % self.logDir
	    self.environments = environments

	def start(self):
	    #info(self.node.name + " = " + pformat(self.environments[self.node.name]) + "\n")
	    Application.start(self, 'nfd --config %s' % self.confFile,
		          logfile=self.logFile, envDict=self.environments[self.node.name])
	    SpecialMinindn.sleep(0.5)
