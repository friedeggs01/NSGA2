import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

# Example data
func = [
    [1, 2, 3],
    [4, 5, 6],
    [7, 8, 9],
    [10, 11, 12]
]

function1 = [i[0] for i in func]
function2 = [i[1] for i in func]
function3 = [i[2] for i in func]

# Create the figure and axis objects
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

# Set the axis labels
ax.set_xlabel('DL', fontsize=15)
ax.set_ylabel('CS', fontsize=15)
ax.set_zlabel('CV', fontsize=15)

# Create the scatter plot
ax.scatter(function1, function2, function3)

# Show the plot
plt.show()