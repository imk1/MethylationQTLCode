def makeGetMethylBatchFactorsScript(methylationFileNameListFileName, poolInfoFileName, barCodesFileName, methylLetter, outputFileNamePath, outputFileNameSuffix, scriptFileName, codePath):
	# Make a script that will run getMethylBatchFactors.py on a list of files
	methylationFileNameListFile = open(methylationFileNameListFileName)
	scriptFile = open(scriptFileName, 'w+')

	for line in methylationFileNameListFile:
		# Iterate through the methylation files and make a line in the script for each
		methylationFileName = line.strip()
		methylationFileNameElements = methylationFileName.split("/")
		methylationFileNameSpecificElements = methylationFileNameElements[-1].split("_1_")
		outputFileName = outputFileNamePath + "/" + methylationFileNameSpecificElements[0] + "_" + outputFileNameSuffix
		scriptFile.write("python " + codePath + "/" + "getMethylBatchFactors.py " + methylationFileName + " " + poolInfoFileName + " " + " " + barCodesFileName + " " + methylLetter + " " + outputFileName + "\n")

	methylationFileNameListFile.close()
	scriptFile.close()


if __name__=="__main__":
	import sys
	methylationFileNameListFileName = sys.argv[1]
	poolInfoFileName = sys.argv[2]
	barCodesFileName = sys.argv[3]
	methylLetter = sys.argv[4]
	outputFileNamePath = sys.argv[5] # Should not end with /
	outputFileNameSuffix = sys.argv[6] # Should end with .gz
	scriptFileName = sys.argv[7]
	codePath = sys.argv[8] # Should not end with /

	makeGetMethylBatchFactorsScript(methylationFileNameListFileName, poolInfoFileName, barCodesFileName, methylLetter, outputFileNamePath, outputFileNameSuffix, scriptFileName, codePath)
