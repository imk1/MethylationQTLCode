def getSNPMethylationFDRs(SNPMethylEffectSizesFileName, SNPMethylEffectSizesRandFileNamePrefix, numIters, SNPMethylCutoffPlusFileName, corrCutoff):
	# Get the FDR for each SNP, C pair for a correlation cutoff
	# ASSUMES THAT LINES IN TRUE DATA FILE AND RANDOM DATA FILES COME FROM THE SAME (SNP, C) PAIRS
	# ASSUMES THAT ALL CHROMOSOMES ARE TOGETHER
	SNPMethylEffectSizesFile = open(SNPMethylEffectSizesFileName, 'rb')
	SNPMethylEffectSizesRandFileList = []
	numRealGreaterThanCorrCutoff = 0
	numGreaterThanCorrCutoff = []
	for i in range(numIters):
		# Open the file from each random iteration
		SNPMethylEffectSizesRandFileList.append(open(SNPMethylEffectSizesRandFileNamePrefix + str(i)))
		numGreaterThanCorrCutoff.append(0)
	SNPMethylCutoffPlusFile = open(SNPMethylCutoffPlusFileName, 'w+')

	for line in SNPMethylEffectSizesFile:
		# Iterate through the EffectSizeelations and compute the p-value for each
		lineElements = line.strip().split("\t")
		currentCorr = abs(float(lineElements[4])) # Use absolute value
		if currentCorr >= corrCutoff:
			# The current correlation is greater than the correlation cutoff, so record the SNP, C pair
			for le in lineElements:
				# Write the SNP and methylation location information to the output file
				SNPMethylCutoffPlusFile.write(le + "\t")
			SNPMethylCutoffPlusFile.write("\n")
			numRealGreaterThanCorrCutoff = numRealGreaterThanCorrCutoff + 1
		for i in range(numIters):
			# Find the EffectSizeelation for each random iteration and check if it is greater than the true EffectSizeelation
			randLineElements = SNPMethylEffectSizesRandFileList[i].readline().strip().split("\t")
			randCorr = abs(float(randLineElements[4])) # Use absolute value
			if randCorr >= corrCutoff:
				# The current random correlation is greater than the correlation cutoff
				numGreaterThanCorrCutoff[i] = numGreaterThanCorrCutoff[i] + 1
				
	SNPMethylEffectSizesFile.close()
	for SNPMethylEffectSizesRandFile in SNPMethylEffectSizesRandFileList:
		# Close the file from each random iteration
		SNPMethylEffectSizesRandFile.close()
	SNPMethylCutoffPlusFile.close()
	return [numRealGreaterThanCorrCutoff, numGreaterThanCorrCutoff]
	

def computeFDR(numRealGreaterThanCorrCutoff, numGreaterThanCorrCutoff, FDRFileName):
	# Compute and record the FDR
	FDRIters = []
	for num in numGreaterThanCorrCutoff:
		# Iterate through the numbers that are greater than the correlation cutoff and compute the fractions that are greater
		FDRIters.append(float(num)/float(numRealGreaterThanCorrCutoff))
	
	FDRFile = open(FDRFileName, 'w+')
	FDR = numpy.mean(FDRIters)
	FDRFile.write(str(FDR) + "\n")
	for Fi in FDRIters:
		# Write the fraction for each permuted data-set to the FDR file
		FDRFile.write(str(Fi) + "\n")
	FDRFile.close()


if __name__=="__main__":
	import sys
	import numpy
	SNPMethylEffectSizesFileName = sys.argv[1] # Should NOT end with .gz
	SNPMethylEffectSizesRandFileNamePrefix = sys.argv[2]
	numIters = int(sys.argv[3])
	SNPMethylCutoffPlusFileName = sys.argv[4] # Should NOT end with .gz
	corrCutoff = float(sys.argv[5])
	FDRFileName = sys.argv[6]

	[numRealGreaterThanCorrCutoff, numGreaterThanCorrCutoff] = getSNPMethylationFDRs(SNPMethylEffectSizesFileName, SNPMethylEffectSizesRandFileNamePrefix, numIters, SNPMethylCutoffPlusFileName, corrCutoff)
	computeFDR(numRealGreaterThanCorrCutoff, numGreaterThanCorrCutoff, FDRFileName)