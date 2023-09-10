from problem import Problem 
from evolution import Evolution
import matplotlib.pyplot as plt
import math


def f1(x):
    return x[0]

def f2(x):
    s = 0
    for i in range(1, len(x)-1):
        s += x[i]
    g = 1 + (9/(len(x)-1))*s
    return 1 - math.sqrt(x[0]/g)

problem = Problem(num_of_variables=30, objectives=[f1, f2], variables_range =[(0, 1)], expand=False,  same_range=True)
evo = Evolution(problem, num_of_generations=100, mutation_param=20)
func = [i.objectives for i in evo.evolve()]

function1 = [i[0] for i in func]
function2 = [i[1] for i in func]

plt.xlabel('Function 1', fontsize=15)
plt.ylabel('Function 2', fontsize=15)
plt.scatter(function1, function2)
plt.show()