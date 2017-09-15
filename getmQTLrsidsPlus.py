def getNextGenotype(genotypeLine, genotypersIDCol, genotypeChromCol, genotypePositionCol):
	# Get the location and rsid number for the next genotype
	if genotypeLine == "":
		# At the end of the genotype file, so stop
		return [("", 0, []), True]
	genotypeLineElements = genotypeLine.split("\t")
	rsidList = []
	if genotypeLineElements[genotypersIDCol][0:2] == "rs":
		# At a SNP
		rsidList = genotypeLineElements[genotypersIDCol].strip().split(";")
	else:
		rsidList = ["Indel"]
	genotypeInfo = (genotypeLineElements[genotypeChromCol],  int(genotypeLineElements[genotypePositionCol]), rsidList)
	return [genotypeInfo, False]

def getmQTLrsids(mQTLFileName, genotypeFileName, outputFileName, genotypersIDCol, genotypeChromCol, genotypePositionCol):
	# Get the rsid numbers for mQTLs
	# ASSUMES THAT mQTLFileName AND genotypeFileName ARE SORTED BY SNP CHROMOSOME, POSITION IN NON-KARYOTYPIC ORDER
	mQTLFile = open(mQTLFileName)
	genotypeFile = open(genotypeFileName)
	outputFile = open(outputFileName, 'w+')
	[currentGenotypeInfo, atGenotypeFileEnd] = getNextGenotype(genotypeFile.readline().strip(), genotypersIDCol, genotypeChromCol, genotypePositionCol)
	for line in mQTLFile:
		# Iterate through the lines of the mQTL file and find the rsid number of the location in each
		lineElements = line.strip().split("\t")
		position = (lineElements[0], int(lineElements[1])) # Chromosome has chr
		while position[0] > currentGenotypeInfo[0]:
			# Iterate through the genotype file until a SNP on the correct chromosome is reached
			[currentGenotypeInfo, atGenotypeFileEnd] = getNextGenotype(genotypeFile.readline().strip(), genotypersIDCol, genotypeChromCol, genotypePositionCol)
			if atGenotypeFileEnd == True:
				# At end of genotype file, so stop
				break
		if atGenotypeFileEnd == True:
				# At end of genotype file, so stop
				break
		while (position[1] > currentGenotypeInfo[1]) and (position[0] == currentGenotypeInfo[0]):
			# Iterate through the genotype file until a SNP at the correct position
			[currentGenotypeInfo, atGenotypeFileEnd] = getNextGenotype(genotypeFile.readline().strip(), genotypersIDCol, genotypeChromCol, genotypePositionCol)
			if atGenotypeFileEnd == True:
				# At end of genotype file, so stop
				break
		if atGenotypeFileEnd == True:
				# At end of genotype file, so stop
				break
		if (position[0] == currentGenotypeInfo[0]) and (position[1] == currentGenotypeInfo[1]):
			# At the mQTL in the genotype file, so record the rsid
			for rsid in currentGenotypeInfo[2]:
				# Print all rsids for the current SNP
				outputFile.write(rsid + "\t")
			outputFile.write("\n")
	mQTLFile.close()
	genotypeFile.close()
	outputFile.close()

if __name__=="__main__":
	import sys
	mQTLFileName = sys.argv[1]
	genotypeFileName = sys.argv[2]
	outputFileName = sys.argv[3]
	genotypersIDCol = int(sys.argv[4])
	genotypeChromCol = int(sys.argv[5])
	genotypePositionCol = int(sys.argv[6])
	getmQTLrsids(mQTLFileName, genotypeFileName, outputFileName, genotypersIDCol, genotypeChromCol, genotypePositionCol)
