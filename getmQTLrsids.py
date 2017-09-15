def getNextGenotype(genotypeLine):
	# Get the location and rsid number for the next genotype
	genotypeLineElements = genotypeLine.split("\t")
	rsidList = []
	if genotypeLineElements[2][0:2] == "rs":
		# At a SNP
		rsidList = genotypeLineElements[2].strip().split(";")
	else:
		rsidList = ["Indel"]
	genotypeInfo = (genotypeLineElements[0],  int(genotypeLineElements[1]), rsidList)
	return genotypeInfo

def getmQTLrsids(mQTLFileName, genotypeFileName, outputFileName):
	# Get the rsid numbers for mQTLs
	# ASSUMES THAT mQTLFileName AND genotypeFileName ARE SORTED BY SNP CHROMOSOME, POSITION IN NON-KARYOTYPIC ORDER
	# ASSUMES THAT ALL mQTLS ARE IN genotypeFile
	mQTLFile = open(mQTLFileName)
	genotypeFile = open(genotypeFileName)
	outputFile = open(outputFileName, 'w+')
	currentGenotypeInfo = getNextGenotype(genotypeFile.readline().strip())
	for line in mQTLFile:
		# Iterate through the lines of the mQTL file and find the rsid number of the location in each
		lineElements = line.strip().split("\t")
		position = (lineElements[0], int(lineElements[1])) # Chromosome has chr
		while position[0] > currentGenotypeInfo[0]:
			# Iterate through the genotype file until a SNP on the correct chromosome is reached
			currentGenotypeInfo = getNextGenotype(genotypeFile.readline().strip())
		while position[1] > currentGenotypeInfo[1]:
			# Iterate through the genotype file until a SNP at the correct position
			currentGenotypeInfo = getNextGenotype(genotypeFile.readline().strip())
		if (position[0] == currentGenotypeInfo[0]) and (position[1] == currentGenotypeInfo[1]):
			# At the mQTL in the genotype file, so record the rsid
			for rsid in currentGenotypeInfo[2]:
				# Print all rsids for the current SNP
				outputFile.write(rsid + "\t")
			outputFile.write("\n")
		else:
			print "Problem " + str(position[0]) + " " + str(position[1])
	mQTLFile.close()
	genotypeFile.close()
	outputFile.close()

if __name__=="__main__":
	import sys
	mQTLFileName = sys.argv[1]
	genotypeFileName = sys.argv[2]
	outputFileName = sys.argv[3]
	getmQTLrsids(mQTLFileName, genotypeFileName, outputFileName)
