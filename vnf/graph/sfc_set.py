import os
import numpy as np
from network import *
from sfc import *

class SFC_SET():
    def __init__(self, input_path=None):
        self.input_path = input_path
        
        with open(self.input_path, "r") as f:
            lines = f.read().splitlines()
            
        self.name = os.path.split(self.input_path)[-1].split(".")[0]
        self.num_sfc = int(lines[0])
        self.sfc_set = []
        for id in range(1, self.num_sfc + 1):
            line = lines[id].strip().split()
            self.sfc_set.append(SFC(id-1, line))
        
        for sfc in self.sfc_set: 
            self.total_re 
        
        self.capmax = np.sum()   
        self.memmax = np.sum()
        self.cpumax = np.sum()
        
        self.max_delay_server = 0
        
    def create_global_info(self, network: Network):
        self._delaymax(network)
        self.network_name = network.name
        
        self.keypoint_consume = dict()
        for sfc in self.sfc_set:
            value = sfc.memory
            if sfc.source not in self.keypoint_consume.keys():
                self.keypoint_consume[] 
            else:
            
            value = 
            if 
            else:
                
        
    def _delaymax(self, network: Network):
        number_used_vnfs = 0
        for sfc in self.sfc_set:
            number_used_vnfs += sfc.num_vnfs
        self.max_delay_server = number_used_vnfs * network.max_delay_server
        
    def sort(self):
        self.sfc_set = sorted(self.sfc_set, key=lambda x: -x.density)

    def total_type_vnf_require(self):
        lst = []
        for sfc in self.sfc_set:
            lst.extend(sfc.vnf_list)
        return set(lst)

    def __len__(self):
        return len(self.sfc_set)