def getNextGenotypeInfo(genotypeLine):
	# Get the SNP location (chromosome, position), SNP, reference, and non-reference alleles from the genotype file
	# The reference allele is listed first
	if genotypeLine == "":
		# At the end of the genotype file, so stop
		return [(0, 0, "", "", ""), True]
	genotypeLineElements = genotypeLine.split("\t")
	return [int(genotypeLineElements[0][3:]), int(genotypeLineElements[1]), genotypeLineElements[2], genotypeLineElements[3], genotypeLineElements[4], False]

def getUpDownAllelesGeuvadis(GeuvadisFileName, genotypeFileName, outputFileName):
	# Get the up-regulating and down-regulating alleles from Geuvadis
	# From Guevadis README: "The sign denotes the direction of the nonreference allele (i.e. rvalue<0 means that nonreference allele has lower expression)"
	# ASSUMES THAT THE Geuvadis AND GENOTYPE FILES ARE SORTED BY CHROMOSOME, POSITION IN KARYOTYPIC ORDER
	# outputFile will contain:
	# 1.  Gene name
	# 2.  rsid (number with no "rs")
	# 3.  Chromosome
	# 4.  Position
	# 5.  Up-regulating allele
	# 6.  Down-regulating allele
	GeuvadisFile = open(GeuvadisFileName)
	genotypeFile = open(genotypeFileName)
	outputFile = open(outputFileName, 'w+')
	basesDict = {}
	basesDict["A"] = 1
	basesDict["C"] = 2
	basesDict["G"]= 3
	basesDict["T"] = 4
	[currentGenotypeChrom, currentGenotypePosition, currentGenotypeSNP, currentGenotypeRef, currentGenotypeAlt, atGenotypeFileEnd] = getNextGenotypeInfo(genotypeFile.readline().strip())
	for line in GeuvadisFile:
		# Iterate through the Geuvadis SNPs and find those that are up and down regulating
		lineElements = line.strip().split("\t")
		while int(lineElements[4]) > currentGenotypeChrom:
			# Iterate through the genotypes until one on the correct chromosome has been reached
			[currentGenotypeChrom, currentGenotypePosition, currentGenotypeSNP, currentGenotypeRef, currentGenotypeAlt, atGenotypeFileEnd] = getNextGenotypeInfo(genotypeFile.readline().strip())
			if atGenotypeFileEnd == True:
				# At the end of the genotype file, so stop
				break
		if atGenotypeFileEnd == True:
			# At the end of the genotype file, so stop
			break
		while (float(lineElements[6]) > currentGenotypePosition) and (int(lineElements[4]) == currentGenotypeChrom):
			# Iterate through the genotypes until one on the correct chromosome has been reached
			[currentGenotypeChrom, currentGenotypePosition, currentGenotypeSNP, currentGenotypeRef, currentGenotypeAlt, atGenotypeFileEnd] = getNextGenotypeInfo(genotypeFile.readline().strip())
			if atGenotypeFileEnd == True:
				# At the end of the genotype file, so stop
				break
		if atGenotypeFileEnd == True:
			# At the end of the genotype file, so stop
			break
		if lineElements[0] == currentGenotypeSNP:
			# At the correct SNP in the genotype file
			if (currentGenotypeRef not in basesDict) or (currentGenotypeAlt not in basesDict):
				# At an indel, so skip it
				continue
			corr = float(lineElements[9])
			upAllele = basesDict[currentGenotypeAlt]
			downAllele = basesDict[currentGenotypeRef]
			if corr < 0:
				# The reference allele is up-regulating
				upAllele = basesDict[currentGenotypeRef]
				downAllele = basesDict[currentGenotypeAlt]
			outputFile.write(lineElements[2] + "\t" + lineElements[0][2:] + "\t" + lineElements[4] + "\t" + lineElements[6] + "\t" + str(upAllele) + "\t" + str(downAllele) + "\n")
	GeuvadisFile.close()
	genotypeFile.close()
	outputFile.close()

if __name__=="__main__":
   import sys
   GeuvadisFileName = sys.argv[1] 
   genotypeFileName = sys.argv[2]
   outputFileName = sys.argv[3]
   getUpDownAllelesGeuvadis(GeuvadisFileName, genotypeFileName, outputFileName)