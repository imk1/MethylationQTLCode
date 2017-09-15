def getSNPMethylationpValues(SNPMethylCorrsFileName, SNPMethylCorrsRandFileNamePrefix, numIters, SNPMethylpValuesFileName):
	# Get the correlation p-values for each SNP, C pair
	# ASSUMES THAT LINES IN TRUE CORRELATION FILE AND RANDOM CORRELATION FILES COME FROM THE SAME (SNP, C) PAIRS
	SNPMethylCorrsFile = gzip.open(SNPMethylCorrsFileName, 'rb')
	SNPMethylCorrsRandFileList = []
	for i in range(numIters):
		# Open the file from each random iteration
		SNPMethylCorrsRandFileList.append(gzip.open(SNPMethylCorrsRandFileNamePrefix + str(i) + ".gz", 'rb'))
	SNPMethylpValuesFile = open(SNPMethylpValuesFileName, 'w+')

	for line in SNPMethylCorrsFile:
		# Iterate through the correlations and compute the p-value for each
		lineElements = line.strip().split("\t")
		currentCorr = float(lineElements[4])
		numGreaterEqualCorr = 0
		for i in range(numIters):
			# Find the correlation for each random iteration and check if it is greater than the true correlation
			randLineElements = SNPMethylCorrsRandFileList[i].readline().strip().split("\t")
			randCorr = float(randLineElements[4])
			if randCorr >= currentCorr:
				# The random correlation is greater than or equal to the true correlation
				numGreaterEqualCorr = numGreaterEqualCorr + 1
		pVal = float(numGreaterEqualCorr)/float(numIters)
		for le in lineElements[0:4]:
			# Write the SNP and methylation location information to the output file
			SNPMethylpValuesFile.write(le + "\t")
		SNPMethylpValuesFile.write(str(pVal) + "\n")

	SNPMethylCorrsFile.close()
	for SNPMethylCorrsRandFile in SNPMethylCorrsRandFileList:
		# Close the file from each random iteration
		SNPMethylCorrsRandFile.close()
	SNPMethylpValuesFile.close()


if __name__=="__main__":
	import sys
	import gzip
	SNPMethylCorrsFileName = sys.argv[1] # Should end with .gz
	SNPMethylCorrsRandFileNamePrefix = sys.argv[2]
	numIters = int(sys.argv[3])
	SNPMethylpValuesFileName = sys.argv[4] # Should NOT end with .gz

	getSNPMethylationpValues(SNPMethylCorrsFileName, SNPMethylCorrsRandFileNamePrefix, numIters, SNPMethylpValuesFileName)
