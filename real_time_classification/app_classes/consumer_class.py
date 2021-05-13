from os.path import dirname, abspath

from minindn.apps.application import Application
from minindn.apps.app_manager import AppManager
from logging import debug

BASE_PATH = abspath(dirname(__file__) + "/../app_executables")

"""
Class for the costumized consumer application that inherits methods from Application class.
It gets the command line parameters for the consumer(s) node(s) and excecutes the application that should run in the consumer node.
"""

class ConsumerApp(Application):
	def __init__(self, node, **appParams):
		super(ConsumerApp, self).__init__(node)

		try:
			requestsFile = " -rf %s " % appParams.pop("requestsFile")
		except KeyError:
			requestsFile = ""

		try:
			prefixes = " -p %s " % appParams.pop("prefixes")

		except KeyError:
			prefixes = ""

		try:
			length = " -l %d " % appParams.pop("length")
		except KeyError:
			length = ""

		try:
			alpha = " -a %f " % appParams.pop("alpha")
		except KeyError:
			alpha = ""

		try:
			sendingRate = " -sr %f " % appParams.pop("sendingRate")
		except KeyError:
			sendingRate = ""

		try:
			if appParams.pop("dry"):
				dry = "--dry-run"
			else:
				dry = ""
		except KeyError:
			dry = ""

		try:
			self.logFile = appParams.pop("log")
		except KeyError:
			self.logFile = self.node.name + '.csv'

		self.prefix = prefixes
		self.cmd = "sudo python " + BASE_PATH + "/consumer_exe.py " + \
		requestsFile + prefixes + length + alpha + sendingRate + dry


	def start(self, command=None, logfile=None, envDict=None):
		if command is None:
			command = self.cmd
		if logfile is None:
			logfile = self.logFile
		if envDict is None:
			envDict = {}

		debug("%s executing %s\n" % (self.node.name, command))
		super(ConsumerApp, self).start(command, logfile=logfile, envDict=envDict)
