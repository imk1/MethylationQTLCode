def makeFisherExactSNPsMethylationRandBothScriptPart(SNPMethylFileListFileName, suffix, minReadsCutoff, MAFCutoff, methylCutoff, scriptFile, codePath, pythonPath):
	# Make a script that will run fisherExactSNPsMethylationRandBoth.py on each file in a list
	SNPMethylFileListFile = open(SNPMethylFileListFileName)
	for line in SNPMethylFileListFile:
		# Iterate through the batch factor files and create a line in the script that will filter them
		SNPMethylFileName = line.strip()
		SNPMethylFileNameElements = SNPMethylFileName.split(".")
		fileTypeLength = len(SNPMethylFileNameElements[-1])
		outputFileName = SNPMethylFileName[0:len(SNPMethylFileName) - fileTypeLength - 1] + "_" + suffix
		cmd =pythonPath + "/" + "python " + codePath + "/" + "fisherExactSNPsMethylationRandBoth.py"
		
		scriptFile.write(cmd + " " + SNPMethylFileName + " " + outputFileName + " " + str(minReadsCutoff) + " " + str(MAFCutoff) + " " + str(methylCutoff) + "\n")
	SNPMethylFileListFile.close()
	
	
def makeFisherExactSNPsMethylationRandBothListScript(SNPMethylFileListFileName, suffix, minReadsCutoff, MAFCutoff, methylCutoff, scriptFileName, codePath, pythonPath, listStart, listEnd):
		# Make a script that will run fisherExactSNPsMethylationRandBoth.py on each file in a list listEnd - listStart + 1 times
		scriptFile = open(scriptFileName, 'w+')
		for i in range(listStart, listEnd + 1):
			# Make a part of the script for each random trial
			suffixFull = suffix + str(i)
			
			makeFisherExactSNPsMethylationRandBothScriptPart(SNPMethylFileListFileName, suffixFull, minReadsCutoff, MAFCutoff, methylCutoff, scriptFile, codePath, pythonPath)
		scriptFile.close()


if __name__=="__main__":
	import sys
	SNPMethylFileListFileName = sys.argv[1]
	suffix = sys.argv[2] # Should not start with _
	minReadsCutoff = int(sys.argv[3])
	MAFCutoff = float(sys.argv[4])
	methylCutoff = float(sys.argv[5])
	scriptFileName = sys.argv[6]
	codePath = sys.argv[7] # Should not end with /
	pythonPath = sys.argv[8] # Should not end with /
	listStart = int(sys.argv[9])
	listEnd = int(sys.argv[10])

	makeFisherExactSNPsMethylationRandBothListScript(SNPMethylFileListFileName, suffix, minReadsCutoff, MAFCutoff, methylCutoff, scriptFileName, codePath, pythonPath, listStart, listEnd)
