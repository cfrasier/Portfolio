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

# Create list to receive boolean bin data.
# Should be a list indexed from 0:3038, with values of 0 or 1.  Then tell which positions are on.
# Then pull those coordinate values from the df_coords table.
list_gene1 = []
list_gene2 = []

# Assign the lists to the outputs of Connor's work.
list_gene1 = bin1
list_gene2 = bin2

# Use pandas to read the csv file
with open('binarized_bdtnp.csv', 'r') as file2:
	gene_coords = pd.read_csv(file2)

# Assign new empty variables for the coordinates of gene 1 and gene 2.
gene1x = []
gene1y = []
gene1z = []

gene2x = []
gene2y = []
gene2z = []

# The below should return the coordinates for the rows we selected as TRUE from running Connor's script.
# Need his input as list. Object is a reference to the index position of the boolean true values generated
# in a list from his binning script. Might need to switch the boolean == True to == 1.
for object in list_gene1:
	for object in list_gene1:
#	if object == True:
		gene1x.append(df_coords[object,0].tolist())
		gene1y.append(df_coords[object,1].tolist())
        	gene1z.append(df_coords[object,2].tolist())
	else
		continue
for object in list_gene2:
	for object in list_gene2:
#	if object == True:
		gene2x.append(df_coords[object,0].tolist())
		gene2y.append(df_coords[object,1].tolist())
		gene2z.append(df_coords[object,2].tolist())
	else
		continue

# Assign fig to call the plot
fig = plt.figure()
# Makes the projection in matplotlib three dimensional
ax1 = plt.axes(projection = '3d')

# Create scatterplot for bin framework.  zdir is the data associated with the z direction. c is color
ax1.scatter3D(xdata, ydata, zdata, zdir='zdata', c='grays')

# Create scatterplot for designated genes.
ax1.scatter3D(gene1x, gene1y, gene1z, zdir='gene1z', c='red')
ax1.scatter3D(gene2x, gene2y, gene2z, zdir='gene2z', c='blue')

# Assign axis labels
ax1.set_xlabel('x')
ax1.set_ylabel('y')
ax1.set_zlabel('z')

# Plot the figure
# plt.show()

# Rotates plot and saves as png.  Work with i and degree to generate right amount of images.
for i in range(11):
	degree = i * 18
	ax1.view_init(35, degree)
#	fig.savefig("/" + str(path) + "/" + "file_" + str(degree) + ".png")
	fig.savefig("file_" + str(degree) + ".png")
