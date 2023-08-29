from main.problem import Problem 
from main.evolution import Evolution
import matplotlib.pyplot as plt
import math

def f1(x):
    return x[0]

def f2(x):
    s = 0
    for i in range(1, len(x)):
        s += x[i]
    g = 1 + (9/(len(x)-1))*s
    return 1 - math.sqrt(x[0]/g)

problem = Problem(num_of_variables=30, objectives=[f1, f2], variables_range =[()], expand=False,  same_range=True)
evo = Evolution(problem, mutation_param=20)
func = [i.objectives for i in evo.evolve()]

function1 = [i[0] for i in func]
function2 = [i[1] for i in func]

plt.xlabel('Function 1', fontsize=15)
plt.ylabel('Function 2', fontsize=15)
plt.scatter(function1, function2)
plt.show()