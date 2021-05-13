from minindn.apps.application import Application
from minindn.apps.app_manager import AppManager
from os.path import abspath, dirname
from mininet.log import info, debug

BASE_PATH = abspath(dirname(__file__) + "/../app_executables")

"""
Class for the costumized producer application that inherits methods from Application class.
It gets the command line parameters for the producer node and excecutes the application that should run in the producer node.
"""

class ProducerApp(Application):

	def __init__(self, node, **appParams):
		super(ProducerApp, self).__init__(node)

		self.logfile = self.node.name+".csv"
		try:
			args_node = appParams.pop("nodes_args")[self.node.name]
			debug("%s => %s\n" % (self.node.name, args_node))

			try:
		    		prefix = "-p %s " % args_node["prefix"]
			except KeyError:
		    		prefix = ""
			try:
		    		requestsFile = "-rf %s " % args_node["requestsFile"]
			except KeyError:
		    		requestsFile = ""

			try:
				freshness = "-f %f " % args_node["freshness"]
			except KeyError:
				freshness = ""

			args_node = prefix + requestsFile + freshness


		except KeyError:
			args_node = ""


		self.cmd = "sudo python " + BASE_PATH + "/producer_exe.py " + args_node

	def start(self, command=None, logfile=None, envDict=None):
		if command is None:
			command = self.cmd
		if logfile is None:
			logfile = self.logfile
		if envDict is None:
			envDict = {}

		debug("%s executing %s\n" % (self.node.name, command))
		super(ProducerApp, self).start(command, logfile=logfile, envDict=envDict)
