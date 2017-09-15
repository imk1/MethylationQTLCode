def makeFisherExactSNPsMethylationRandPlusPlusScriptPart(SNPMethylFileListFileName, suffix, readsToMinMinorReadsFileName, scriptFile, scriptFileNamePrefix, codePath, pythonPath, maxLinesPerScript, numLinesInScriptCount, scriptFileNum):
	# Make a script that will run correlateSNPsMethylation.py on each file in a list
	SNPMethylFileListFile = open(SNPMethylFileListFileName)
	for line in SNPMethylFileListFile:
		# Iterate through the batch factor files and create a line in the script that will filter them
		if numLinesInScriptCount >= maxLinesPerScript:
			# The current script has the maximum number of lines, so close its file and start a new script file
			scriptFile.close()
			scriptFileNum = scriptFileNum + 1
			scriptFile = open(scriptFileNamePrefix + str(scriptFileNum) + ".sh", 'w+')
			numLinesInScriptCount = 0
		
		SNPMethylFileName = line.strip()
		SNPMethylFileNameElements = SNPMethylFileName.split(".")
		fileTypeLength = len(SNPMethylFileNameElements[-1])
		outputFileName = SNPMethylFileName[0:len(SNPMethylFileName) - fileTypeLength - 1] + "_" + suffix
		cmd = pythonPath + "/" + "python " + codePath + "/" + "fisherExactSNPsMethylationPlusPlusRandGen.py"
		
		scriptFile.write(cmd + " " + SNPMethylFileName + " " + outputFileName + " " + readsToMinMinorReadsFileName + "\n")
		numLinesInScriptCount = numLinesInScriptCount + 1
		
	SNPMethylFileListFile.close()
	return [scriptFile, numLinesInScriptCount, scriptFileNum]


def makeFisherExactSNPsMethylationPlusPlusRandListScript(SNPMethylFileListFileName, suffix, readsToMinMinorReadsFileName, scriptFileNamePrefix, codePath, pythonPath, listStart, listEnd, maxLinesPerScript):
		# Make a script that will run fisherExactSNPsMethylationPlusPlusRand.py on each file in a list listEnd - listStart + 1 times
		scriptFileNum = 1
		scriptFile = open(scriptFileNamePrefix + str(scriptFileNum) + ".sh", 'w+')
		numLinesInScriptCount = 0
		for i in range(listStart, listEnd + 1):
			# Make a part of the script for each random trial
			suffixFull = suffix + str(i)
			
			[scriptFile, numLinesInScriptCount, scriptFileNum]  = makeFisherExactSNPsMethylationRandPlusPlusScriptPart(SNPMethylFileListFileName, suffixFull, readsToMinMinorReadsFileName, scriptFile, scriptFileNamePrefix, codePath, pythonPath, maxLinesPerScript, numLinesInScriptCount, scriptFileNum)
		scriptFile.close()	


if __name__=="__main__":
	import sys
	SNPMethylFileListFileName = sys.argv[1]
	suffix = sys.argv[2] # Should not start with _
	readsToMinMinorReadsFileName = sys.argv[3]
	scriptFileNamePrefix = sys.argv[4]
	codePath = sys.argv[5] # Should not end with /
	pythonPath = sys.argv[6] # Should not end with /
	listStart = int(sys.argv[7])
	listEnd = int(sys.argv[8])
	maxLinesPerScript = int(sys.argv[9])

	makeFisherExactSNPsMethylationPlusPlusRandListScript(SNPMethylFileListFileName, suffix, readsToMinMinorReadsFileName, scriptFileNamePrefix, codePath, pythonPath, listStart, listEnd, maxLinesPerScript)
