def makeFilterLowReadCsScript(methylBatchFactorsListFileName, minReads, suffix, scriptFileName, codePath):
	# Make a script that will remove Cs with fewer than minReads
	methylBatchFactorsListFile = open(methylBatchFactorsListFileName)
	scriptFile = open(scriptFileName, 'w+')
	for line in methylBatchFactorsListFile:
		# Iterate through the batch factor files and create a line in the script that will filter them
		methylBatchFactorsFileName = line.strip()
		methylBatchFactorsFileNameElements = methylBatchFactorsFileName.split(".")
		fileTypeLength = len(methylBatchFactorsFileNameElements[-1])
		outputFileName = methylBatchFactorsFileName[0:len(methylBatchFactorsFileName) - fileTypeLength - 1] + suffix
		scriptFile.write(codePath + "/" + "filterLowReadCs.py " + methylBatchFactorsFileName + " " + str(minReads) + " " + outputFileName + "\n")
	methylBatchFactorsListFile.close()
	scriptFile.close()

if __name__=="__main__":
   import sys
   methylBatchFactorsListFileName = sys.argv[1]
   minReads = int(sys.argv[2])
   suffix = sys.argv[3] # Should end in .gz
   scriptFileName = sys.argv[4]
   codePath = sys.argv[5] # Should not end in /
   makeFilterLowReadCsScript(methylBatchFactorsListFileName, minReads, suffix, scriptFileName, codePath)
