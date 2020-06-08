# Import packages
# pandas is a module designed to help read in many different types of files and data types
import pandas as pd
import numpy as np
# mplot3d creates three dimensional plots
from mpl_toolkits import mplot3d
import matplotlib.pyplot as plt
import time
import sys
import argparse
import csv
import imageio
import os
import re

# The following is Mark Miloslavic

#Create dictionary for gene library
gene_dict = {
"01":"aay",
"02":"Ama",
"03":"Ance",
"04":"Antp",
"05":"apt",
"06":"Blimp-1",
"07":"bmm",
"08":"bowl",
"09":"brk",
"10":"Btk29A",
"11":"bun",
"12":"cad",
"13":"CenG1A",
"14":"CG10479",
"15":"CG11208",
"16":"CG14427",
"17":"CG17724",
"18":"CG17786",
"19":"CG43394",
"20":"CG8147",
"21":"cnc",
"22":"croc",
"23":"Cyp310a1",
"24":"D",
"25":"dan",
"26":"danr",
"27":"Dfd",
"28":"disco",
"29":"Doc2",
"30":"Doc3",
"31":"dpn",
"32":"edl",
"33":"ems",
"34":"erm",
"35":"Esp",
"36":"E(spl)m5-HLH",
"37":"eve",
"38":"exex",
"39":"fj",
"40":"fkh",
"41":"ftz",
"42":"gk",
"43":"gt",
"44":"h",
"45":"hb",
"46":"hkb",
"47":"htl",
"48":"Ilp4",
"49":"ImpE2",
"50":"ImpL2",
"51":"ken",
"52":"kni",
"53":"knrl",
"54":"Kr",
"55":"lok",
"56":"Mdr49",
"57":"Mes2",
"58":"MESR3",
"59":"mfas",
"60":"Nek2",
"61":"NetA",
"62":"noc",
"63":"nub",
"64":"numb",
"65":"oc",
"66":"odd",
"67":"peb",
"68":"prd",
"69":"pxb",
"70":"rau",
"71":"rho",
"72":"run",
"73":"sna",
"74":"srp",
"75":"tkv",
"76":"tll",
"77":"toc",
"78":"Traf4",
"79":"trn",
"80":"tsh",
"81":"twi",
"82":"zen",
"83":"zen2",
"84":"zfh1"}

gene_table = [['01 aay', '22 croc', '43 gt', '64 numb'],
              ['02 Ama', '23 Cyp310a1', '44 h', '65 oc'],
              ['03 Ance', '24 D', '45 hb', '66 odd'],
              ['04 Antp', '25 dan', '46 hkb', '67 peb'],
              ['05 apt', '26 danr', '47 htl', '68 prd'],
              ['06 Blimp-1', '27 Dfd', '48 Ilp4', '69 pxb'],
              ['07 bmm', '28 disco', '49 ImpE2', '70 rau'],
              ['08 bowl', '29 Doc2', '50 ImpL2', '71 rho'],
              ['09 brk', '30 Doc3', '51 ken', '72 run'],
              ['10 Btk29A', '31 dpn', '52 kni', '73 sna'],
              ['11 bun', '32 edl', '53 knrl', '74 srp'],
              ['12 cad', '33 ems', '54 Kr', '75 tkv'],
              ['13 CenG1A', '34 erm', '55 lok', '76 tll'],
              ['14 CG10479', '35 Esp', '56 Mdr49', '77 toc'],
              ['15 CG11208', '36 E(spl)m5-HLH', '57 Mes2', '78 Traf4'],
              ['16 CG14427', '37 eve', '58 MESR3', '79 trn'],
              ['17 CG17724', '38 exex', '59 mfas', '80 tsh'],
              ['18 CG17786', '39 fj', '60 Nek2', '81 twi'],
              ['19 CG43394', '40 fkh', '61 NetA', '82 zen'],
              ['20 CG8147', '41 ftz', '62 noc', '83 zen2'],
              ['21 cnc', '42 gk', '63 nub', '84 zfh1']]

#Print introductory message and gene list
print("Welcome to the Single Cell Transcriptomics Data Visualization Program!\n")
time.sleep(4)
print("This program will allow you to generate and display a 3D rotational model of the embryo with markers reflecting the gene expressions you select.\n")
time.sleep(7)
print("Lets get started!\n")
time.sleep(3)
for row in gene_table:
    print("{: <17} {: <17} {: <17} {: <17}".format(*row))

#Promt user to make a selection
while True:
    users_gene1_input = input("Select the first gene marker you wish to display by entering its corresponding number:")
    #If first input is incorrect value
    if users_gene1_input not in gene_dict:
        print("Enter a \033[1mtwo digit\033[0m number between 01 and 84.")
        time.sleep(5)
        continue
    #If input is correct value
    else:
        break
while True:
    users_gene2_input = input("Now select the second gene marker:")
    #If second input is incorrect value
    if users_gene2_input not in gene_dict:
        print("Enter a \033[1mtwo digit\033[0m number between 01 and 84.")
        time.sleep(5)
    elif users_gene2_input in users_gene1_input:
        print("Select a \033[1mdifferent\033[0m gene marker.")
        time.sleep(5)
        continue
    #If input is correct value
    else:
        break
number_images = ''
number_images = int(input("How many images (enter a number between 18 and 180) in the gif?\n"))
frames_duration = ''
frames_duration = int(input("How long should each image be displayed (frames per second: enter a number between 1 and 20)?\n"))

# The following is Connor Frasier    
    
bin1 = []
bin2 = []
bin3 = []
bin4 = []
bin5 = []
bin6 = []
bin7 = []
bin8 = []
bin9 = []

#bin1checkers = set(input("Please provide the genes to be checked for bin number 1: ").split(", "))
#bin2checkers = set(input("Please provide the genes to be checked for bin number 2: ").split(", "))
bin1checkers = set(gene_dict[users_gene1_input].split(", "))
bin2checkers = set(gene_dict[users_gene2_input].split(", "))
bin3checkers = {}
bin4checkers = {}
bin5checkers = {}
bin6checkers = {}
bin7checkers = {}
bin8checkers = {}
bin9checkers = {}

with open("self_binarized_bdtnp.csv") as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
                #print row
                total_on = 0
                genes_on = []
                dgenes_on = {}
                CellID = row['CellID']
                for item in row:
                        if row[item] == '1':
                                genes_on.append(item)
                                total_on += 1
                #print(row['CellID'],total_on)
                #print(row['CellID'] +"\t"+str(genes_on)+"\t" + str(total_on))
                dgenes_on[CellID] = set(genes_on)
                #print(dgenes_on)
                if bin2checkers.issubset(dgenes_on[CellID]):
                        bin2.append(int(CellID))
                #for item in dgenes_on[CellID]:
                        #if item in bin1checkers:
                                #bin1.append(CellID)
                if bin1checkers.issubset(dgenes_on[CellID]):
                        bin1.append(int(CellID))

# The following is David Brown

# Read in the geometry.txt file as a Pandas data frame. sep='\s+' refers to an unknown amount of white space used to delimit the data in file1.
with open('geometry.txt', 'r') as file1:
    df_coords = pd.read_table(file1, sep='\s+')

# Create a list to mark all possible cell positions. Should be a list indexed from 0:3038. 
list_all_pos = []
for x in range(3039):
    list_all_pos.append(int(x))

# Create empty lists for the data from Connor's work.  Each list will be the position of an "ON" or "TRUE" value from the self_binarized file.
list_gene1 = []
list_only_gene1 = []
list_gene2 = []
list_only_gene2 = []
list_both = []
list_none = []

# Assign the lists to the outputs of Connor's work.
list_gene1 = bin1
list_gene2 = bin2

# Create list comprehensions to subdivide the data for visualization.  Only gene1, only gene2, both genes, and neither genes.
list_both = [item for item in list_gene2 if item in list_gene1]
list_only_gene1 = [item for item in list_gene1 if item not in list_both]
list_only_gene2 = [item for item in list_gene2 if item not in list_both]
list_none = [item for item in list_all_pos if item not in list_both or not list_only_gene1 or not list_only_gene2]

# Assign new empty variables for the coordinates of only gene1, only gene2, both, and none.
gene1x = []
gene1y = []
gene1z = []

gene2x = []
gene2y = []
gene2z = []

bothx = []
bothy = []
bothz = []

nonex = []
noney = []
nonez = []

# Append the x, y, and z coordinates from the df_coords (geometry.txt) to the appropriate subset of the data: only gene1, only gene2, both, or none.
for object in list_gene1:
    gene1x.append(df_coords.at[object,'xcoord'].tolist())
    gene1y.append(df_coords.at[object,'ycoord'].tolist())
    gene1z.append(df_coords.at[object,'zcoord'].tolist())
for object in list_gene2:
    gene2x.append(df_coords.at[object,'xcoord'].tolist())
    gene2y.append(df_coords.at[object,'ycoord'].tolist())
    gene2z.append(df_coords.at[object,'zcoord'].tolist())
for object in list_both:
    bothx.append(df_coords.at[object,'xcoord'].tolist())
    bothy.append(df_coords.at[object,'ycoord'].tolist())
    bothz.append(df_coords.at[object,'zcoord'].tolist())
for object in list_none:
    nonex.append(df_coords.at[object,'xcoord'].tolist())
    noney.append(df_coords.at[object,'ycoord'].tolist())
    nonez.append(df_coords.at[object,'zcoord'].tolist())

# Draws and rotates plot and saves as png.  Work with i and degree to generate right amount of images.
for i in range((number_images+1)):
    fig = plt.figure()
    ax1 = plt.axes(projection = '3d')
    ax1.scatter3D(nonex, noney, nonez, zdir='nonez', c='#a6a6a6', alpha=0.5, s=0.5)
    ax1.scatter3D(gene1x, gene1y, gene1z, zdir='gene1z', c='#ff0000', alpha=0.9, s=1.5)
    ax1.scatter3D(gene2x, gene2y, gene2z, zdir='gene2z', c='#0000ff', alpha=0.9, s=1.5)
    ax1.scatter3D(bothx, bothy, bothz, zdir='bothz', c='#00ff00', alpha=0.9, s=1.75)
    ax1.set_xlabel('x')
    ax1.set_ylabel('y')
    ax1.set_zlabel('z')
    degree = int(i * (180 / number_images))
    ax1.view_init(35, degree)
    fig.savefig("file_" + str(degree) + ".png")
    plt.close("all")
    print(degree)

# The following is Sayal Guirales

cwd = os.getcwd()
 #Gets the directory path of the current directory that you run the program in

image_folder = os.fsencode(cwd)

filenames = []

#Organize images that are to be used for gif into dictionary
for file in os.listdir(image_folder):
    filename = os.fsdecode(file)
    if filename.endswith( ('.jpeg', '.png') ):
        filenames.append(filename)

filenames.sort(key=lambda var:[int(x) if x.isdigit() else x for x in re.findall(r'[^0-9]|[0-9]+', var)]) #Cannot use .sort() alone, needs function to organize numbers correctly

images = list(map(lambda filename: imageio.imread(filename), filenames)) #save images into readable list

imageio.mimsave(os.path.join('transcriptome.gif'), images, duration = (1/frames_duration)) # modify duration as needed
print("Thank you for using the Single Cell Transcriptomics Data Visualization Program!")
