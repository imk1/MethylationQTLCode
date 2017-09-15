def makeGetSNPMethylationpValuesScript(SNPMethylEffectSizesFileNameSuffix, SNPMethylEffectSizesRandFileNameMiddle, numIters, SNPMethylpValuesFileNameSuffix, chromListFileName, filePath, randStr, numRandIters, scriptFileName, codePath):
	# Make a script that will get the methylation p-values for each chromosome in the real data and numRandIters random data-sets
	chromListFile = open(chromListFileName)
	scriptFile = open(scriptFileName, 'w+')
	for line in chromListFile:
		# Write commands for each chromosome
		chrom = line.strip()
		SNPMethylEffectSizesFileName = filePath + "/" + chrom + "_" + SNPMethylEffectSizesFileNameSuffix
		SNPMethylEffectSizesRandFileNamePrefix = filePath + "/" + chrom + "_" + SNPMethylEffectSizesRandFileNameMiddle
		SNPMethylpValuesFileName = filePath + "/" + chrom + "_" + SNPMethylpValuesFileNameSuffix
		scriptFile.write("python "  + codePath + "/" + "getSNPMethylationpValues.py " + SNPMethylEffectSizesFileName + " " + SNPMethylEffectSizesRandFileNamePrefix + " " + str(numIters) + " " + SNPMethylpValuesFileName + "\n")
		for i in range(1, numRandIters + 1):
			# Make a line in the script for each random iteration, which can be used to compute an FDR
			SNPMethylpValuesFileNameRand = SNPMethylpValuesFileName + randStr + str(i)
			scriptFile.write("python "  + codePath + "/" + "getSNPMethylationRandpValues.py " + SNPMethylEffectSizesRandFileNamePrefix + " " + str(i) + " " + str(numIters) + " " + SNPMethylpValuesFileNameRand + "\n")
	chromListFile.close()
	scriptFile.close()

if __name__=="__main__":
	import sys
	import gzip
	SNPMethylEffectSizesFileNameSuffix = sys.argv[1] # Should not start with _
	SNPMethylEffectSizesRandFileNameMiddle = sys.argv[2] # Should not start with _
	numIters = int(sys.argv[3])
	SNPMethylpValuesFileNameSuffix = sys.argv[4] # Should start with _
	chromListFileName = sys.argv[5]
	filePath = sys.argv[6] # Should not end with /
	randStr = sys.argv[7]
	numRandIters = int(sys.argv[8])
	scriptFileName = sys.argv[9]
	codePath = sys.argv[10] # Should not end with /
	makeGetSNPMethylationpValuesScript(SNPMethylEffectSizesFileNameSuffix, SNPMethylEffectSizesRandFileNameMiddle, numIters, SNPMethylpValuesFileNameSuffix, chromListFileName, filePath, randStr, numRandIters, scriptFileName, codePath)