#Import packages

#Welcomes user and describes program
def program_description():
	print("Welcome to the Single Cell Transcriptomics Data Visualization program!")
	sleep(3)
	print("This program allows you to generate and display a 3D model of the embryo with markers reflecting the gene expressions you select.")

#Displays all available genes for selection
def display_gene_library():

#Promp user to input gene selection
def get_user_input():
	users_selection = raw_input("Please select which genes you wish to display on the 3D model: ")
