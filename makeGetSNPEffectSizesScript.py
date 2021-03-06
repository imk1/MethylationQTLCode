def makeGetSNPEffectSizesScript(SNPMethylPlusListFileName, suffix, minReadsCutoff, MAFCutoff, methylCutoff, CVal, scriptFileName, codePath):
	# Make a script that will run correlateSNPsMethylation.py on each file in a list
	SNPMethylPlusListFile = open(SNPMethylPlusListFileName)
	scriptFile = open(scriptFileName, 'w+')

	for line in SNPMethylPlusListFile:
		# Iterate through the batch factor files and create a line in the script that will filter them
		SNPMethylFileName = line.strip()
		SNPMethylFileNameElements = SNPMethylFileName.split(".")
		fileTypeLength = len(SNPMethylFileNameElements[-1])
		outputFileName = SNPMethylFileName[0:len(SNPMethylFileName) - fileTypeLength - 1] + suffix
		cmd = "python " + codePath + "/" + "getSNPEffectSizes.py"
		scriptFile.write(cmd + " " + SNPMethylFileName + " " + outputFileName + " " + str(minReadsCutoff) + " " + str(MAFCutoff) + " " + str(methylCutoff) + " " + str(CVal) + "\n")

	SNPMethylPlusListFile.close()
	scriptFile.close()


if __name__=="__main__":
	import sys
	SNPMethylPlusListFileName = sys.argv[1]
	suffix = sys.argv[2]
	minReadsCutoff = int(sys.argv[3])
	MAFCutoff = float(sys.argv[4])
	methylCutoff = float(sys.argv[5])
	CVal = float(sys.argv[6]) # For minimal regularization, use approximately 1000000000
	scriptFileName = sys.argv[7]
	codePath = sys.argv[8] # Should not end with /

	makeGetSNPEffectSizesScript(SNPMethylPlusListFileName, suffix, minReadsCutoff, MAFCutoff, methylCutoff, CVal, scriptFileName, codePath)
