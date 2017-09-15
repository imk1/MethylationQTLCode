def combineGenotypeFiles(genotypeFileNameListFileName, outputFileName):
	# Combine the genotype data from files in Hapmap format to be in one file in the following format:
	# 1.  Chromosome
	# 2.  Position on chromosome
	# 3.  rsid
	# 4.  First allele
	# 5.  Second allele
	genotypeFileNameListFile = open(genotypeFileNameListFileName)
	outputFile = open(outputFileName, 'w+')
	for genotypeFileName in genotypeFileNameListFile:
		# Iterate through the files with genotypes and add the appropriate information from each to the output file
		genotypeFile = open(genotypeFileName.strip())
		genotypeFile.readline() # Remove the header
		for line in genotypeFile:
			# Iterate through the lines of the genotype file and record the appropriate information from each line
			lineElements = line.strip().split(" ")
			alleleElements = lineElements[1].split("/")
			outputFile.write(lineElements[2] + "\t" + lineElements[3] + "\t" + lineElements[0] + "\t" + alleleElements[0] + "\t" + alleleElements[1] + "\n")
		genotypeFile.close()
	genotypeFileNameListFile.close()
	outputFile.close()
	
if __name__=="__main__":
	import sys
	genotypeFileNameListFileName = sys.argv[1]
	outputFileName = sys.argv[2]
	combineGenotypeFiles(genotypeFileNameListFileName, outputFileName)