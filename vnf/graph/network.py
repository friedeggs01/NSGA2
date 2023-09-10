from link import *
from node import *
from vnf import *

class Network():
    def __init__(self, input_path=None, ) -> None:
        self.input_path = input_path
        
        with open(self.input_path, "r") as f:
            lines = f.read().splitlines()
            
        self.N = dict()
        self.L = dict()
        self.adj = dict()
        self.num_nodes = 0
        self.num_links = 0
        self.num_servers = 0
        self.total_delay_link = 0
        self.total_delay_server = 0
        self.cost_servers = []
        self.cost_vnfs = []
        self.switch_ids = []
        self.server_ids = []
        
        line = list(map(int, lines[0].strip().split()))
        self.num_type_vnfs, self.num_vnfs_limit = line
        
        num_nodes = int(lines[1])
        
        for id in range(2, 2 + num_nodes):
            line = lines[id].strip().split()
            # line = 
            _id, _delay, _cost = line[0], line[1], line[2]
            if _cost == -1:
                self.add_node
        
    
    def create_network(self):
        ...
    
    def _update_adjacent(self, link: Link):
        sou, des = link.source, link.destination
    
    def add_node(self, node: Node):
        if node.id in self.N.keys():
            print("ID node is existed!")
        else:
            self.N[node.id] = node
            self.num_nodes += 1
    
    def add_link(self, link: Link):
        if link.id in self.L.keys():
            print("ID link is existed!")
        else:
            self.L[link.id] = link
            self._update_adjacent(link)
            self.num_links += 1   