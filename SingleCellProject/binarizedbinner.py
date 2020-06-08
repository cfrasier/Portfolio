import csv

bin1 = []
bin2 = []
bin3 = []


bin1checkers = set(input("Please provide the genes to be checked for bin number 1: ").split(", "))
bin2checkers = set(input("Please provide the genes to be checked for bin number 2: ").split(", "))
bin3checkers = set(input("Please provide the genes to be checked for bin number 3: ").split(", "))

with open('self_binarized_bdtnp.csv') as csvfile:
	reader = csv.DictReader(csvfile)
	for row in reader:
		genes_on = []
		dgenes_on = {}
		CellID = row['CellID']
		for item in row:
			if row[item] == '1':
				genes_on.append(item)
		dgenes_on[CellID] = set(genes_on)
		if bin1checkers.issubset(dgenes_on[CellID]):
			bin1.append(CellID)
		elif bin2checkers.issubset(dgenes_on[CellID]):
			bin2.append(CellID)
		elif bin3checkers.issubset(dgenes_on[CellID]):
			bin3.append(CellID)

print(bin1)
print(bin2)
print(bin3)