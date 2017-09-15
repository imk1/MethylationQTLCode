def makeGetSNPEffectSizesRandScript(SNPMethylPlusListFileName, outputFilePath, suffix, minReadsCutoff, MAFCutoff, methylCutoff, CVal, numIters, scriptFileName, codePath, pythonPath):
	# Make a script that will run correlateSNPsMethylation.py on each file in a list
	SNPMethylPlusListFile = open(SNPMethylPlusListFileName)
	scriptFile = open(scriptFileName, 'w+')

	for line in SNPMethylPlusListFile:
		# Iterate through the batch factor files and create a line in the script that will filter them
		SNPMethylFileName = line.strip()
		SNPMethylFilePathElements = SNPMethylFileName.split("/")
		SNPMethylFileNameElements = SNPMethylFilePathElements[-1].split(".")
		fileTypeLength = len(SNPMethylFileNameElements[-1])
		outputFileNamePrefix = outputFilePath + "/" + SNPMethylFilePathElements[-1][0:len(SNPMethylFilePathElements[-1]) - fileTypeLength - 1] + suffix
		cmd = pythonPath + "/" + "python " + codePath + "/" + "getSNPEffectSizesRand.py"
		for i in range(numIters):
			# Write a line in the script for each iteration
			scriptFile.write(cmd + " " + SNPMethylFileName + " " + outputFileNamePrefix + " " + str(minReadsCutoff) + " " + str(MAFCutoff) + " " + str(methylCutoff) + " " + str(CVal) + " " + str(i) + "\n")

	SNPMethylPlusListFile.close()
	scriptFile.close()


if __name__=="__main__":
	import sys
	SNPMethylPlusListFileName = sys.argv[1]
	outputFilePath = sys.argv[2] # Should not end with /
	suffix = sys.argv[3]
	minReadsCutoff = int(sys.argv[4])
	MAFCutoff = float(sys.argv[5])
	methylCutoff = float(sys.argv[6])
	CVal = float(sys.argv[7]) # For minimal regularization, use approximately 1000000000
	numIters = int(sys.argv[8])
	scriptFileName = sys.argv[9]
	codePath = sys.argv[10] # Should not end with /
	pythonPath = sys.argv[11] # Should not end with /

	makeGetSNPEffectSizesRandScript(SNPMethylPlusListFileName, outputFilePath, suffix, minReadsCutoff, MAFCutoff, methylCutoff, CVal, numIters, scriptFileName, codePath, pythonPath)
