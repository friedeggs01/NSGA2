from individual import Individual
from graph.network import Network
from graph.sfc_set import SFC_SET
from graph.sfc import SFC

import random
import copy
import heapq

class Problem:

    def __init__(self, network: Network, sfcs: SFC_SET):
        self.network = network
        self.sfcs = sfcs
        
    def generate_individual(self):
        individual = Individual()
        vnf_pool = list(range(1, self.network.num_type_vnfs+1))
        for _ in range(self.network.num_servers):
            group = random.sample(vnf_pool, self.network.num_vnfs_limit)
            individual.features.extend(group)
        return individual
    
    def calculate_objectives(self, individual):
        network_copy = copy.deepcopy(self.network)
        self._kichhoatNodes(individual, network_copy)
        for sfc in self.sfcs.sfc_set:
            for i in sfc.vnf_list:
                ser = self.find_servers_have_vnf_i(i, individual, network_copy)
                ser = self.remove_servers_invalid(ser, sfc)
                self.find_path_dijkstra(ser,network_copy, sfc)
            #FIXME - link_to_des = network_copy.L[].delay
            self.network.total_delay_link += link_to_des.delay 
            sfc.path.append(sfc.destination)        
        
        individual.objectives = self._obj_func(network_copy)
    
    def _kichhoatNodes(self, individual: Individual, network_copy: Network) -> None:
        for node_server_id in range(self.network.num_servers):
            for vnf_id in range(self.network.num_vnfs_limit):
                network_copy.cost_servers_use += network_copy.N[network_copy.server_ids[node_server_id]].cost
                network_copy.cost_vnfs_use += network_copy.N[network_copy.server_ids[node_server_id]].vnf_cost[individual.features[node_server_id * network_copy.num_servers + vnf_id]]
                        
    def _obj_func(self, network_copy: Network):
        fitness = []
        # delay of all sfcs
        fitness.append((network_copy.delay_link + network_copy.delay_server)/(network_copy.total_delay_link + network_copy.total_delay_server))
        # cost of install servers
        fitness.append(network_copy.cost_servers_use/network_copy.sum_cost_servers)
        # cost of install vnfs
        fitness.append(network_copy.cost_vnfs_use/network_copy.max_cost_vnfs)
        return fitness
    
    # return list of Node (class)
    def find_servers_have_vnf_i(self, i: int, individual: Individual, network_copy: Network):
        positions = [index for index, value in enumerate(individual.features) if value == i]
        server_id = [positions[index] // self.network.num_vnfs_limit  for index in range(len(positions))]
        server_node = [network_copy.N[i].values for i in server_id]
        return server_node
        
    def remove_servers_invalid(self, ser, sfc: SFC):
        valid_ser = []
        for server_node in ser:
            if sfc.cpu < server_node.cpu_available:
                valid_ser.append(server_node)
        return valid_ser
    
    # find path have min bandwidth, then update constraint    
    def find_path_dijkstra(self, end_nodes, network_copy: Network, sfc: SFC):
        distances = {node: float('inf') for node in network_copy.N.values} 
        distances[sfc.path[-1]] = 0
        previous_nodes = {node: None for node in network_copy.N.values} 
        unvisited_nodes = [(0, sfc.path[-1])]

        while unvisited_nodes:
        
            current_distance, current_node = heapq.heappop(unvisited_nodes)

            if current_node in end_nodes:
                end_nodes.remove(current_node)
                if len(end_nodes) == 0:
                    break 

            if current_distance > distances[current_node]:
                continue 
            
            for neighbor, weight in network_copy.adj[current_node].keys(), network_copy.adj[current_node].values().delay:
                distance = current_distance + weight
                # checking constraint
                if sfc.bw > network_copy.L[current][neighbor].bw_available:
                    continue
                if neighbor.type == True and sfc.cpu > network_copy.N[neighbor.id].cpu_available:
                    continue
                if neighbor.type == False and sfc.memory > network_copy.N[neighbor.id].mem_available:
                    continue
                if distance < distances[neighbor]:
                    distances[neighbor] = distance
                    previous_nodes[neighbor] = current_node
                    heapq.heappush(unvisited_nodes, (distance, neighbor))

        smallest_weight = float('inf')
        smallest_end_node = None
        for end_node in end_nodes:
            if distances[end_node] < smallest_weight:
                smallest_weight = distances[end_node]
                smallest_end_node = end_node

        current = smallest_end_node
        sfc.path.insert(-1,current)
        current.cpu_available -= sfc.cpu
        position = -1
        while current:
            current = previous_nodes[current]
            if current.type == False:
                current.mem_available -= sfc.memory
            else:
                current.cpu_available -= sfc.cpu
            network_copy.L[current.id][sfc.path[-1]].bw_available -= sfc.bw
            
            sfc.path.insert(position, current)
            position -= 1        
    
    # check vnf not used and then calculate again the fitness of individual