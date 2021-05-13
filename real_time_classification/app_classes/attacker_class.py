from os.path import dirname, abspath

from minindn.apps.application import Application
from minindn.apps.app_manager import AppManager
from logging import debug
from mininet.log import debug

BASE_PATH = abspath(dirname(__file__) + "/../app_executables")

"""
Class for the costumized attacker application that inherits methods from Application class.
It gets the command line parameters for the attacker node and excecutes the application that should run in the attacker node.
"""

class AttackerApp(Application):
	def __init__(self, node, **appParams):
		super(AttackerApp, self).__init__(node)

		try:
			attackerTime = " -at %f" % appParams.pop("attackerTime")
		except KeyError:
			attackerTime = ""
		try:
			attackerModel = " -am %s" % appParams.pop("attackerModel")
		except KeyError:
			attackerModel = ""
		try:
			self.logFile = appParams.pop("log")
		except KeyError:
			self.logFile = self.node.name + '.csv'

		self.cmd = "sudo python " + BASE_PATH + "/attacker_exe.py " + attackerTime + attackerModel
		debug("attacker is launching this command {}".format(self.cmd))

	def start(self, command=None, logfile=None, envDict=None):
		if command is None:
			command = self.cmd
		if logfile is None:
			logfile = self.logFile
		if envDict is None:
			envDict = {}

		debug("%s executing %s\n" % (self.node.name, command))
		super(AttackerApp, self).start(command, logfile=logfile, envDict=envDict)
