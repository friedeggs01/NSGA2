from __future__ import print_function 
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import plotly.graph_objects as go
D = 30
x = np.random.rand(D)
print(x)

def ZDT1(x):
    f1 = x[0]
    g = 1 + 9 * np.sum(x[1:D]/(D-1))
    h = 1 - np.sqrt(f1/g)
    f2 = g*h
    return[f1, f2]

objective_values = ZDT1(x)
print(objective_values)

true_front = np.empty((0, 2))

for f1 in np.linspace(0, 1, num=20):
    f2 = 1 - np.sqrt(f1)
    true_front = np.vstack([true_front, [f1, f2]])  

true_front = pd.DataFrame(true_front, columns=['f1', 'f2'])  # convert to DataFrame
true_front

fig = go.Figure(layout=dict(xaxis=dict(title='f1'),yaxis=dict(title='f2')))

fig.add_scatter(x=true_front.f1, y=true_front.f2, mode='markers')

fig.show()

objective_values = np.empty((0, 2))

for i in range(50):
    x = np.random.rand(D)
    y = ZDT1(x)
    objective_values = np.vstack([objective_values, y])

# convert to DataFrame
objective_values = pd.DataFrame(objective_values, columns=['f1', 'f2'])
objective_values.head()

fig = go.Figure(layout=dict(xaxis=dict(title='f1'), yaxis=dict(title='f2')))

fig.add_scatter(x=objective_values.f1, y=objective_values.f2,
                name='Solutions', mode='markers')

fig.add_scatter(x=true_front.f1, y=true_front.f2, name='True Front')

fig.show()