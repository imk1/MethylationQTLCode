def getSNPMethylationRandpValues(SNPMethylEffectSizesFileName, SNPMethylEffectSizesRandFileNamePrefix, numIters, SNPMethylpValuesFileName, currentIter):
	# Get the EffectSizeelation p-values for each SNP, C pair
	# ASSUMES THAT LINES IN TRUE EffectSizeELATION FILE AND RANDOM EffectSizeELATION FILES COME FROM THE SAME (SNP, C) PAIRS
	SNPMethylEffectSizesFile = open(SNPMethylEffectSizesFileName, 'rb')
	SNPMethylEffectSizesRandFileList = []
	for i in range(0, numIters):
		# Open the file from each random iteration
		if i == currentIter:
			# At the random iteration that will be treated like real data, so skip it
			continue
		SNPMethylEffectSizesRandFileList.append(open(SNPMethylEffectSizesRandFileNamePrefix + str(i)))
	SNPMethylpValuesFile = open(SNPMethylpValuesFileName, 'w+')

	for line in SNPMethylEffectSizesFile:
		# Iterate through the EffectSizeelations and compute the p-value for each
		lineElements = line.strip().split("\t")
		currentEffectSize = abs(float(lineElements[4])) # Use absolute value
		numGreaterEqualEffectSize = 0
		for i in range(numIters-1):
			# Find the EffectSizeelation for each random iteration and check if it is greater than the true EffectSizeelation
			randLineElements = SNPMethylEffectSizesRandFileList[i].readline().strip().split("\t")
			randEffectSize = abs(float(randLineElements[4])) # Use absolute value
			if randEffectSize >= currentEffectSize:
				# The random EffectSizeelation is greater than or equal to the true EffectSizeelation
				numGreaterEqualEffectSize = numGreaterEqualEffectSize + 1
		pVal = float(numGreaterEqualEffectSize)/float(numIters-1)
		for le in lineElements[0:4]:
			# Write the SNP and methylation location information to the output file
			SNPMethylpValuesFile.write(le + "\t")
		SNPMethylpValuesFile.write(str(pVal) + "\n")

	SNPMethylEffectSizesFile.close()
	for SNPMethylEffectSizesRandFile in SNPMethylEffectSizesRandFileList:
		# Close the file from each random iteration
		SNPMethylEffectSizesRandFile.close()
	SNPMethylpValuesFile.close()


if __name__=="__main__":
	import sys
	SNPMethylEffectSizesRandFileNamePrefix = sys.argv[1]
	currentIter = int(sys.argv[2])
	SNPMethylEffectSizesFileName = SNPMethylEffectSizesRandFileNamePrefix + str(currentIter)
	numIters = int(sys.argv[3])
	SNPMethylpValuesFileName = sys.argv[4] # Should NOT end with .gz

	getSNPMethylationRandpValues(SNPMethylEffectSizesFileName, SNPMethylEffectSizesRandFileNamePrefix, numIters, SNPMethylpValuesFileName, currentIter)
