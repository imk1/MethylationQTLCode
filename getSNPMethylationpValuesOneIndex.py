def getSNPMethylationpValues(SNPMethylEffectSizesFileName, SNPMethylEffectSizesRandFileNamePrefix, numIters, SNPMethylpValuesFileName):
	# Get the EffectSizeelation p-values for each SNP, C pair
	# ASSUMES THAT LINES IN TRUE EffectSizeELATION FILE AND RANDOM EffectSizeELATION FILES COME FROM THE SAME (SNP, C) PAIRS
	SNPMethylEffectSizesFile = open(SNPMethylEffectSizesFileName, 'rb')
	SNPMethylEffectSizesRandFileList = []
	for i in range(1, numIters + 1):
		# Open the file from each random iteration
		SNPMethylEffectSizesRandFileList.append(open(SNPMethylEffectSizesRandFileNamePrefix + str(i)))
	SNPMethylpValuesFile = open(SNPMethylpValuesFileName, 'w+')

	for line in SNPMethylEffectSizesFile:
		# Iterate through the EffectSizeelations and compute the p-value for each
		lineElements = line.strip().split("\t")
		currentEffectSize = abs(float(lineElements[4])) # Use absolute value
		numGreaterEqualEffectSize = 0
		for i in range(numIters):
			# Find the EffectSizeelation for each random iteration and check if it is greater than the true EffectSizeelation
			randLineElements = SNPMethylEffectSizesRandFileList[i].readline().strip().split("\t")
			randEffectSize = abs(float(randLineElements[4])) # Use absolute value
			if randEffectSize >= currentEffectSize:
				# The random EffectSizeelation is greater than or equal to the true EffectSizeelation
				numGreaterEqualEffectSize = numGreaterEqualEffectSize + 1
		pVal = float(numGreaterEqualEffectSize)/float(numIters)
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
	SNPMethylEffectSizesFileName = sys.argv[1] # Should NOT end with .gz
	SNPMethylEffectSizesRandFileNamePrefix = sys.argv[2]
	numIters = int(sys.argv[3])
	SNPMethylpValuesFileName = sys.argv[4] # Should NOT end with .gz

	getSNPMethylationpValues(SNPMethylEffectSizesFileName, SNPMethylEffectSizesRandFileNamePrefix, numIters, SNPMethylpValuesFileName)
