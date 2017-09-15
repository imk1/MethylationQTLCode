def combineGenotypeProbs(genotypeProbsFileName, genotypesFileName, colsToRemove):
	# Combine genotype probabilities to get genotypes
	genotypeProbsFile = open(genotypeProbsFileName)
	genotypesFile = open(genotypesFileName, 'w+')
	for line in genotypeProbsFile:
		# Iterate through the genotype probability information and combine it to get genotypes
		# First genotype probability will be multiplied by 2, second by 1, and third by 0
		lineElements = line.strip().split()
		genotypesFile.write(lineElements[0])
		numGenotypes = (len(lineElements) - 1) / 3
		for j in range(numGenotypes):
			# Iterate through the genotypes and combine the genotype probabilities into a single number in [0, 2]
			if j in colsToRemove:
				# The individual in column j should be removed
				continue
			index = (3 * j) + 1
			genotype = (2.0 * float(lineElements[index])) + float(lineElements[index + 1])
			genotypesFile.write("\t" + str(genotype))
		genotypesFile.write("\n")
	genotypeProbsFile.close()
	genotypesFile.close()

if __name__=="__main__":
	import sys
	genotypeProbsFileName = sys.argv[1]
	genotypesFileName = sys.argv[2]
	colsToRemove = []
	for colStr in sys.argv[3:len(sys.argv)]:
		# Iterate through the remaining arguments and add them to the list of columns to remove
		colsToRemove.append(float(colStr))
	combineGenotypeProbs(genotypeProbsFileName, genotypesFileName, colsToRemove)