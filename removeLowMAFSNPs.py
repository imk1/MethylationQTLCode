def getAlelleFreqs(genotypeStrList):
	# Get the allele frequencies for the current SNP
	numAlleles = 2 * len(genotypeStrList)
	numAllelesOne = 0
	for genotypeStr in genotypeStrList:
		# Iterate through the individuals and increment the allele counts appropriately
		numAllelesOne = numAllelesOne + float(genotypeStr)
	alleleFreqOne = float(numAllelesOne)/float(numAlleles)
	alleleFreqTwo = 1 - alleleFreqOne
	return [alleleFreqOne, alleleFreqTwo]

def removeLowMAFSNPs(genotypeFileName, outputFileName, MAFCutoff):
	# Remove the low MAF SNPs from a genotype file
	genotypeFile = open(genotypeFileName)
	outputFile = open(outputFileName, 'w+')
	for line in genotypeFile:
		# Iterate through the SNPs and removes those whose MAFs are too low
		lineElements = line.strip().split("\t")
		[alleleFreqOne, alleleFreqTwo] = getAlelleFreqs(lineElements[2:])
		if (alleleFreqOne > MAFCutoff) and (alleleFreqTwo > MAFCutoff):
			# Both allele frequencies are sufficiently high, so record the SNP
			outputFile.write(line)
	genotypeFile.close()
	outputFile.close()

if __name__=="__main__":
	import sys
	genotypeFileName = sys.argv[1]
	outputFileName = sys.argv[2]
	MAFCutoff = float(sys.argv[3])
	removeLowMAFSNPs(genotypeFileName, outputFileName, MAFCutoff)