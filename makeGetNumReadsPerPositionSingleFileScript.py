def makeGetNumReadsPerPositionSingleFileScript(readsFileNameListFileName, pairsFileNameListFileName, outputFilePath, outputFileNameSuffix, scriptFileName, codePath):
	# Write a script that will run getSNPMethylReads.py on each pair of methylation, SNP files
	readsFileNameListFile = open(readsFileNameListFileName)
	pairsFileNameListFile = open(pairsFileNameListFileName)
	pairsFileNameList = pairsFileNameListFile.readlines()
	pairsFileNameListFile.close()
	scriptFile = open(scriptFileName, 'w+')
	count = 0

	for line in readsFileNameListFile:
		# Iterate through the reads files and make a line in the script for each and all position files
		readsFileName = line.strip()
		for pairsFileName in pairsFileNameList:
			# Iterate through the pairs files and write a line in the script for each
			pairsFileNameElements = pairsFileName.strip().split("/")
			outputFileName = outputFilePath + "/" + pairsFileNameElements[-1] + "_" + str(count) + "_" + outputFileNameSuffix
			scriptFile.write("python " + codePath + "/" + "getNumReadsPerPositionPairSingleFile.py " + readsFileName + " " + pairsFileName.strip() + " " + outputFileName + "\n")
		count = count + 1

	readsFileNameListFile.close()
	scriptFile.close()

	
if __name__=="__main__":
	import sys
	readsFileNameListFileName = sys.argv[1]
	pairsFileNameListFileName = sys.argv[2]
	outputFilePath = sys.argv[3]
	outputFileNameSuffix = sys.argv[4]
	scriptFileName = sys.argv[5]
	codePath = sys.argv[6] # Should not end with /

	makeGetNumReadsPerPositionSingleFileScript(readsFileNameListFileName, pairsFileNameListFileName, outputFilePath, outputFileNameSuffix, scriptFileName, codePath)
