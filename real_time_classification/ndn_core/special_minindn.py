import argparse
import yaml
from typing import List
from mininet.topo import Topo
from minindn.minindn import Minindn
from minindn.helpers.nfdc import Nfdc

"""
This is a costumized class which inherits methods from Minindn class.
It contains methods that parse all the command line arguments and also the costumized topology file.
"""
class SpecialMinindn(Minindn):
	def __init__(self, parser,**mininetParams):

		parser = SpecialMinindn.parseArgs(parser)
		args = parser.parse_args()

		self.requestsFile = args.requestsFile
		self.topology_file = args.topology
		self.freshness = args.freshness
		self.length = args.length
		self.alpha = args.alpha
		self.sendingRate = args.sendingRate
		self.attackerTime = args.attackerTime
		self.attackerModel = args.attackerModel
		self.info = args.info
		self.dry = args.dry
		self.cacheStrategy = args.cacheStrategy
		self.cacheSize = args.cacheSize
		self.faceProtocol = args.faceProtocol
		self.routing = args.routingType

		topology, self.name_mapping, self.environments, self.groups = \
		  	SpecialMinindn.process_topology(self.topology_file)
	        super(SpecialMinindn, self).__init__( parser=parser, topo=topology, **mininetParams)

        @staticmethod
    	def parseArgs(parent):
			parser = argparse.ArgumentParser(parents=[parent], conflict_handler='resolve')
			parser.add_argument('-rf', '--requestsFile', help='File containing the requests')
			parser.add_argument('-t', '--topology', help='Customised topology file')
			parser.add_argument('-f', '--freshness', type=float, help='Data packet freshness in ms')
			parser.add_argument('-l', '--length', type=int, help='Max data length')
			parser.add_argument('-a', '--alpha', type=float, help="Alpha parameter for Zipf distribution")
			parser.add_argument("-sr", "--sendingRate", type=float, help="Consumer's sending rate interval") # from 1.0 to 25.0
			parser.add_argument("-at", "--attackerTime", type=float, help="Time for attacker's analysis (expressed in seconds)")
			parser.add_argument("-am","--attackerModel", type=str, help="Machine Learning model used by the attacker", choices = ["linear_1_500","linear_1_900",
		                                "linear_1_1300", "linear_1_1642", "linear_2_500", "linear_2_700","linear_2_900", "linear_2_1362",
		                                "linear_1and2_500", "linear_1and2_900", "linear_1and2_1300", "linear_1and2_1700","linear_1and2_2100", "linear_1and2_2500", "linear_1and2_3054",
		                                "multinomial_1_500","multinomial_1_900", "multinomial_1_1300", "multinomial_1_1642",
		                                "multinomial_2_500", "multinomial_2_700","multinomial_2_900", "multinomial_2_1362",
		                                "multinomial_1and2_500", "multinomial_1and2_900", "multinomial_1and2_1300", "multinomial_1and2_1700","multinomial_1and2_2100", "multinomial_1and2_2500", "multinomial_1and2_3054",
		                                "rf_1_500","rf_1_900", "rf_1_1300", "rf_1_1642",
		                                "rf_2_500", "rf_2_700","rf_2_900", "rf_2_1362",
		                                "rf_1and2_500", "rf_1and2_900", "rf_1and2_1300", "rf_1and2_1700","rf_1and2_2100", "rf_1and2_2500", "rf_1and2_3054",
		                                "svm_1_500","svm_1_900", "svm_1_1300", "svm_1_1642",
		                                "svm_2_500", "svm_2_700","svm_2_900", "svm_2_1362",
		                                "svm_1and2_500", "svm_1and2_900", "svm_1and2_1300", "svm_1and2_1700","svm_1and2_2100", "svm_1and2_2500", "svm_1and2_3054"])
			parser.add_argument("--info", action="store_true", help="Only print dataset info") # --INFO
			parser.add_argument("--dry", action="store_true", help="Only print requests") # --dry
			parser.add_argument("-cstrat", '--cacheStrategy', help="Strategy used by the router(s) during the simulation", choices=["lru", "lfu", 						"priority_fifo"],default="lru")
			parser.add_argument('-csize', '--cacheSize', type=int, help='Cache size of the router(s)', choices = [2000, 4000, 6000, 8000, 10000, 						12000, 14000, 1600] , default = 4000)
			parser.add_argument('--face-protocol', dest='faceProtocol', default=Nfdc.PROTOCOL_UDP, choices=[Nfdc.PROTOCOL_TCP, Nfdc.PROTOCOL_ETHER, 						Nfdc.PROTOCOL_UDP], help='Choose the face protocol to be used')
			parser.add_argument('--routing', dest='routingType', default='link-state', choices=['link-state','hr', 'dry'], help='Choose the routing 						type')

			return parser

	@staticmethod
	def process_topology(topology_file):
		topo = Topo()
        	with open(topology_file) as f:
            		topo_data = yaml.full_load(f)

        	name_mapping = {}
        	environments = {}
        	groups = {}

        	for group in topo_data.keys(): # topo_data = victims, attackers, producers, routers, links
            		if group == "links":
                		continue
            		groups[group] = []
            		if topo_data[group] is not None:
                		for node, env in topo_data[group].items():
                    			node_name = "%s_%s" % (group[:2].upper(), node)
                    			name_mapping[node] = node_name
                    			environments[node_name] = env
                    			groups[group].append(node_name)
                    			topo.addHost(node_name)

        	for node_name in name_mapping.values():
            		environments[node_name]["NODE_PREFIX"] = "/ndn/%s-site/%s" % (node_name, node_name)
            		environments[node_name]["DUMP_ENABLED"] = True

        	for couple in topo_data["links"]:
            		for node_A, node_B in couple.items():
                		if not isinstance(node_B, List) and node_A != node_B:
                    			topo.addLink(name_mapping[node_A], name_mapping[node_B], delay='10ms')

        	return topo, name_mapping, environments, groups
