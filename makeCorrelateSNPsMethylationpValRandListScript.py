def makeCorrelateSNPsMethylationRandpValScriptPart(SNPMethylFileListFileName, suffix, minReadsCutoff, MAFCutoff, methylCutoff, pValSuffix, scriptFile, scriptFileNamePrefix, codePath, pythonPath, maxLinesPerScript, numLinesInScriptCount, scriptFileNum):
	# Make a script that will run correlateSNPsMethylationpValRand.py on each file in a list
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
		pValOutputFileName = SNPMethylFileName[0:len(SNPMethylFileName) - fileTypeLength - 1] + pValSuffix
		cmd = pythonPath + "/" + "python " + codePath + "/" + "correlateSNPsMethylationpValRand.py"
		
		scriptFile.write(cmd + " " + SNPMethylFileName + " " + outputFileName + " " + str(minReadsCutoff) + " " + str(MAFCutoff) + " " + str(methylCutoff) + " " + pValOutputFileName + "\n")
		numLinesInScriptCount = numLinesInScriptCount + 1
		
	SNPMethylFileListFile.close()
	return [scriptFile, numLinesInScriptCount, scriptFileNum]


def makeCorrelateSNPsMethylationpValRandListScript(SNPMethylFileListFileName, suffix, minReadsCutoff, MAFCutoff, methylCutoff, pValSuffix, scriptFileNamePrefix, codePath, pythonPath, listStart, listEnd, maxLinesPerScript):
		# Make a script that will run correlateSNPsMethylationpValRand.py on each file in a list listEnd - listStart + 1 times
		scriptFileNum = 1
		scriptFile = open(scriptFileNamePrefix + str(scriptFileNum) + ".sh", 'w+')
		numLinesInScriptCount = 0
		for i in range(listStart, listEnd + 1):
			# Make a part of the script for each random trial
			suffixFull = suffix + str(i)
			pValSuffixFull = pValSuffix + str(i)
			
			[scriptFile, numLinesInScriptCount, scriptFileNum]  = makeCorrelateSNPsMethylationRandpValScriptPart(SNPMethylFileListFileName, suffixFull, minReadsCutoff, MAFCutoff, methylCutoff, pValSuffixFull,  scriptFile, scriptFileNamePrefix, codePath, pythonPath, maxLinesPerScript, numLinesInScriptCount, scriptFileNum)
		scriptFile.close()	


if __name__=="__main__":
	import sys
	SNPMethylFileListFileName = sys.argv[1]
	suffix = sys.argv[2] # Should not start with _
	minReadsCutoff = int(sys.argv[3])
	MAFCutoff = float(sys.argv[4])
	methylCutoff = float(sys.argv[5])
	pValSuffix = sys.argv[6] # Should not start with _
	scriptFileNamePrefix = sys.argv[7]
	codePath = sys.argv[8] # Should not end with /
	pythonPath = sys.argv[9] # Should not end with /
	listStart = int(sys.argv[10])
	listEnd = int(sys.argv[11])
	maxLinesPerScript = int(sys.argv[12])

	makeCorrelateSNPsMethylationpValRandListScript(SNPMethylFileListFileName, suffix, minReadsCutoff, MAFCutoff, methylCutoff, pValSuffix, scriptFileNamePrefix, codePath, pythonPath, listStart, listEnd, maxLinesPerScript)
