from graph.network import Network
from graph.sfc_set import SFC_SET
from evolution import Evolution
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import csv
import os


# names = ["nsf", "conus", "cogent"]
# areas = ["center", "rural", "uniform", "urban"]
# requests = [10, 20, 30]
# i_s = [0, 1, 2, 3, 4]

names = ["cogent"]
areas = ["center"]
requests = [10]
i_s = [0]
# folder_path = 'NSGA2\vnf\graph\output'
folder_path = 'graph\output'
os.makedirs(folder_path, exist_ok=True)
for name in names:
    for area in areas:
        for request in requests:
            for i in i_s:
                name_folder = name+"_"+area+"_"+str(i)
                network = Network("dataset/" + name_folder + "/input.txt")
                sfc_set = SFC_SET("dataset/" + name_folder + "/request" + str(request) + ".txt")
                evo = Evolution(network, sfc_set, mutation_param=20)
                func = [i.objectives for i in evo.evolve()]
                file_path = os.path.join(folder_path, f'{name_folder}_request_{str(request)}_result.csv')
                result = {}
                for i in func:
                    result['fitness_1'] = i[0]
                    result['fitness_2'] = i[1]
                    result['fitness_3'] = i[2]
                    
                # function1 = [i[0] for i in func]
                # function2 = [i[1] for i in func]
                # function3 = [i[2] for i in func]

                # fig = plt.figure()
                # ax = fig.add_subplot(111, projection='3d')

                # ax.set_xlabel('DL', fontsize=15)
                # ax.set_ylabel('CS', fontsize=15)
                # ax.set_zlabel('CV', fontsize=15)

                # ax.scatter(function1, function2, function3)

                # plt.show()
                    with open(file_path, 'a') as file:
                        fieldnames = ['fitness_1', 'fitness_2', 'fitness_3']
                        writer = csv.DictWriter(file, fieldnames=fieldnames)
                        writer.writerow(result)
                    