def makeStringList(stringListFileName):
	# Make a list of strings from a file
	stringList = []
	stringListFile = open(stringListFileName)
	for line in stringListFile:
		# Iterate through the lines of the file, and make an entry in the list for each
		stringList.append(line.strip())
	stringListFile.close()
	return stringList

def getGenotypesFromVcf(vcfFileName, individualsList, SNPLocationsListFileName, outputFileName):
	# ASSUMES THAT vcfFile AND SNPLocationsListFile ARE SORTED IN KARYOTYPIC ORDER AND HAVE NO chr
	# ASSUMES THAT ALL VARIANTS WITH LOCATIONS IN SNPLocationsListFile ARE IN vcfFile
	vcfFile = open(vcfFileName)
	vcfLine = vcfFile.readline()
	while vcfLine[0:2] == "##":
		# Iterate through the vcfFile until the line with the names of the individuals is reached
		vcfLine = vcfFile.readline()
	vcfLineElements = vcfLine.strip().split("\t")
	individualsIndexes = []
	for i in range(9, len(vcfLineElements)):
		# Iterate through the individuals and find those in the list
		if vcfLineElements[i] in individualsList:
			# At an individual in the list of individuals
			individualsIndexes.append(i)
	vcfLineElements = vcfFile.readline().strip().split("\t")
	SNPLocationsListFile = open(SNPLocationsListFileName)
	outputFile = open(outputFileName, 'w+')
	for line in SNPLocationsListFile:
		# Iterate through the variants and find the genotype of each individual in individualsList for each
		lineElements = line.strip().split("\t")
		SNPLocation = (int(lineElements[0]), int(lineElements[1]))
		while SNPLocation[0] > int(vcfLineElements[0]):
			# Iterate through the vcf file until a variant on the correct chromosome has been reached
			vcfLineElements = vcfFile.readline().strip().split("\t")
		while SNPLocation[1] > int(vcfLineElements[1]):
			# Iterate through the vcf file until a variant at the correct location has been reached
			vcfLineElements = vcfFile.readline().strip().split("\t")
		if (SNPLocation[0] != int(vcfLineElements[0])) or (SNPLocation[1] != int(vcfLineElements[1])):
			print SNPLocation[1]
			print vcfLineElements[1]
			print "Problem!"
		for index in individualsIndexes:
			# Iterate through the individuals and get each individual's genotype for the current variant
			alleles = vcfLineElements[index].split("|")
			genotype = float(int(alleles[0]) + int(alleles[1]))/float(2)
			outputFile.write(str(genotype) + "\t")
		outputFile.write("\n")
	vcfFile.close()
	SNPLocationsListFile.close()
	outputFile.close()
	
if __name__=="__main__":
	import sys
	# NOT DEBUGGED!
	vcfFileName = sys.argv[1]
	individualsListFileName = sys.argv[2]
	SNPLocationsListFileName = sys.argv[3]
	outputFileName = sys.argv[4]
	individualsList = makeStringList(individualsListFileName)
	getGenotypesFromVcf(vcfFileName, individualsList, SNPLocationsListFileName, outputFileName)
	
