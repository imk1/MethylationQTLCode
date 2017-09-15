def getSNPFromRead(readsSNPsLine):
	# Get the SNP location from a read
	if readsSNPsLine == "":
		# At the end of the file, so stop
		return [("", 0, ""), True]
	readsSNPsLineElements = readsSNPsLine.strip().split("\t")
	return [(readsSNPsLineElements[2], int(readsSNPsLineElements[3]), readsSNPsLineElements[4]), False]

def getNumReadsPerAllele(readsSNPsFileName, allelesSNPsFileName, outputFileName):
	# Gets the number reads for each allele of each SNP
	# Output file format:
	# Column 1: Chromosome
	# Column 2: Position
	# Column 3: Number of reads with reference allele
	# Column 4: Number of reads with alternate allele
	# Column 5: Total number of reads for the SNP
	# ASSUMES THAT readsSNPsFile and alleleSNPsFile ARE SORTED BY CHROMOSOME, POSITION (NON-KARYO.)
	# ASSUMES THAT EVERY SNP ON A READ IS IN THE ALLELES FILE
	readsSNPsFile = open(readsSNPsFileName)
	allelesSNPsFile = open(allelesSNPsFileName)
	outputFile = open(outputFileName, 'w+')
	[currentReadSNP, atEnd] = getSNPFromRead(readsSNPsFile.readline())
	for line in allelesSNPsFile:
		# Iterate through the SNPs and find the number of reads with each allele for each
		lineElements = line.strip().split("\t")
		currentAlleleSNP = (lineElements[0], int(lineElements[1]))
		ref = lineElements[3]
		alt = lineElements[4]
		numRef = 0
		numAlt = 0
		while (atEnd == False) and ((currentAlleleSNP[0] == currentReadSNP[0]) and (currentAlleleSNP[1] == currentReadSNP[1])):
			# Iterate through the reads with the current SNP
			if currentReadSNP[2] == ref:
				# The current read has the reference allele
				numRef = numRef + 1
			elif currentReadSNP[2] == alt:
				# The current read has the alternate allele
				numAlt = numAlt + 1
			[currentReadSNP, atEnd] = getSNPFromRead(readsSNPsFile.readline())
		if numRef + numAlt > 0:
			# The current SNP is in the data-set, so record its allele counts
			outputFile.write(currentAlleleSNP[0] + "\t" + str(currentAlleleSNP[1]) + "\t" + str(numRef) + "\t" + str(numAlt) + "\t" + str(numRef + numAlt) + "\n")
		if atEnd == True:
			# At the end of the reads file, so stop
			break
	readsSNPsFile.close()
	allelesSNPsFile.close()
	outputFile.close()
	
if __name__=="__main__":
   import sys
   readsSNPsFileName = sys.argv[1] 
   allelesSNPsFileName = sys.argv[2]
   outputFileName = sys.argv[3]
   getNumReadsPerAllele(readsSNPsFileName, allelesSNPsFileName, outputFileName)