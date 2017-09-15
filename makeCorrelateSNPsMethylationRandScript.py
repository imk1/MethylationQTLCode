def makeCorrelationSNPsMethylationScript(SNPMethylCorrsPrefixFileName, SNPVecFileListFileName, methylVecFileListFileName, numIters, scriptFileName, codePath):
	# Make a script that will run correlateSNPsMethylationRand.py on each file in a list for each iteration
	# ASSUMES THAT SNPMethylCorrsPrefixFile, SNPVecFileListFile, AND methylVecFileListFile CORRESPOND TO EACH OTHER
	SNPMethylCorrsPrefixFile = open(SNPMethylCorrsPrefixFileName)
	SNPVecFileListFile = open(SNPVecFileListFileName)
	methylVecFileListFile = open(methylVecFileListFileName)
	scriptFile = open(scriptFileName, 'w+')

	for line in SNPMethylCorrsPrefixFile:
		# Iterate through the SNP methyl. files and create a line that will find their random correlations
		SNPMethylCorrsPrefix = line.strip()
		SNPVecFileName = SNPVecFileListFile.readline().strip()
		methylVecFileName = methylVecFileListFile.readline().strip()
		cmd = "python " + codePath + "/" + "correlateSNPsMethylationRand.py"
		for i in range(numIters):
			# Make a line in the script for each iteration
			scriptFile.write(cmd + " " + SNPMethylCorrsPrefix + " " + SNPVecFileName + " " + methylVecFileName + " " + str(i) + "\n")

	SNPMethylCorrsPrefixFile.close()
	SNPVecFileListFile.close()
	methylVecFileListFile.close()
	scriptFile.close()


if __name__=="__main__":
	import sys
	SNPMethylCorrsPrefixFileName = sys.argv[1]
	SNPVecFileListFileName = sys.argv[2]
	methylVecFileListFileName = sys.argv[3]
	numIters = int(sys.argv[4])
	scriptFileName = sys.argv[5]
	codePath = sys.argv[6] # Should not end with /

	makeCorrelationSNPsMethylationScript(SNPMethylCorrsPrefixFileName, SNPVecFileListFileName, methylVecFileListFileName, numIters, scriptFileName, codePath)
