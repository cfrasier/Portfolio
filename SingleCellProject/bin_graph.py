# Import packages
# mplot3d creates three dimensional plots
from mpl_toolkits import mplot3d
import matplotlib.pyplot as plt

# pandas is a module designed to help read in many different types of files and data types
import pandas as pd
import numpy as np

# Read in the geometry.txt file as a data frame. Pandas data frames are called series, so the data type will need to be changed later. sep='\s+' refers to an unknown amount of white space used to delimit the data in file1.
with open('geometry.txt', 'r') as file1:
	df_coords = pd.read_table(file1, sep='\s+')

# Change the data type from a one column series to a list for each column in the series.
xdata = df_coords['xcoord'].tolist()
ydata = df_coords['ycoord'].tolist()
zdata = df_coords['zcoord'].tolist()

# Assign fig to call the plot
fig = plt.figure()
# Makes the projection in matplotlib three dimensional
ax = plt.axes(projection = '3d')

# Create scatterplot.  zdir is the data associated with the z direction. c is color
ax.scatter3D(xdata, ydata, zdata, zdir='zdata', c='gray')

# Need to mirror ycoord to get full embryo.
# May need to reference an Axes object to keep drawing on the same subplot.

# Assign axis labels
ax.set_xlabel('x')
ax.set_ylabel('y')
ax.set_zlabel('z')

# Plot the figure
fig
plt.show()

fig.savefig('figure1.png')

# Rotates plot and saves as png.  Degree must equal 360 at max i.
#for i  in range(10):
#	degree = i * 36	
#	ax.view_init(35, degree)
#	filename='figure' + '_' + str(degree) + '_' + 'rotation'
#	savefig(filename.png)
