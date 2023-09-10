from graph import network, sfc_set
from problem import Problem 
from evolution import Evolution
import matplotlib.pyplot as plt
import math

names = ["nsf", "conus", "cogent"]
areas = ["center", "rural", "uniform", "urban"]
requests = [10, 20, 30]
TIMELIMIT = 300
i_s = [0, 1, 2, 3, 4]
for name in names:
    for area in areas:
        for request in requests:
            for i in i_s:
                name_folder = name+"_"+area+"_"+str(i)
                network = network.Network("./code/dataset/" + name_folder + "/input.txt")
                sfc_set = sfc_set.SFC_SET("./code/dataset/" + name_folder + "/request" + str(request) + ".txt")
                sfc_set.create_global_info(network)
                network.create_constraints_and_min_paths(sfc_set)

                # sol_mau = Solution(network, sfc_set)
                # sol_mau.name_folder_output = "./code/output/" + name_folder + "/request" + str(request)   