def convertGenotypeProbsToGenotypes(genotypeProbsFileName, outputFileName):
	# Convert genotype probabilities to genotypes
	# Genotype: 0 means homozygous reference allele, .5 means heterozygous, 1 means homozygous alternate allele
	# ASSUMES THAT THE FIRST COLUMN FOR EACH INDIVIDUAL IS THE REFERENCE ALLELE PROB. AND THE LAST IS THE ALTERNATE ALLELE PROB.
	genotypeProbsFile = open(genotypeProbsFileName)
	outputFile = open(outputFileName, 'w+')
	for line in genotypeProbsFile:
		# Iterate through the genotype probabilities and convert each to a genotype
		lineElements = line.split()
		outputFile.write(lineElements[0] + "\t" + lineElements[1])
		indivCount = 0
		while indivCount < (len(lineElements) - 2) / 3:
			# Iterate through the individuals and compute each of their genotypes
			probAlt = float(lineElements[(indivCount * 3) + 4])
			probHet = float(lineElements[(indivCount * 3) + 3])
			genotype = probAlt + (.5 * probHet)
			outputFile.write("\t" + str(genotype))
			indivCount = indivCount + 1
		outputFile.write("\n")
	genotypeProbsFile.close()
	outputFile.close()

if __name__=="__main__":
   import sys
   genotypeProbsFileName = sys.argv[1] 
   outputFileName = sys.argv[2]
   convertGenotypeProbsToGenotypes(genotypeProbsFileName, outputFileName)