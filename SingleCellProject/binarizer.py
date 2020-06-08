import csv

binarizedfile = open('self_binarized_bdtnp.csv', 'w')
with open('bdtnp.txt') as csvfile:
	reader = csv.DictReader(csvfile, delimiter='\t')
	x = float(input("Please input the threshold for binarization (0-1): "))
	fieldnames = next(reader)
	fieldnames['CellID'] = 0
	writer = csv.DictWriter(binarizedfile, fieldnames=sorted(fieldnames, key=lambda s: s.casefold()), restval='0', extrasaction='raise', dialect='excel')
	writer.writeheader()
	row_number=0
	for row in reader:
		for item in row:
			if row[item] == str():
				continue
			elif float(row[item]) >= x: #0.40
				row[item] = 1
			elif float(row[item]) < x: #0.40
				row[item] = 0
		row_number+=1
		row['CellID']=row_number
		writer.writerow(row)
		
binarizedfile.close
