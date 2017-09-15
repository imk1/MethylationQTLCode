def makeCorrelateSNPsMethylationScript(SNPMethylFileListFileName, suffix, readsToMinMinorReadsFileName, pValSuffix, scriptFileName, codePath, pythonPath):
	# Make a script that will run correlateSNPsMethylation.py on each file in a list
	SNPMethylFileListFile = open(SNPMethylFileListFileName)
	scriptFile = open(scriptFileName, 'w+')

	for line in SNPMethylFileListFile:
		# Iterate through the batch factor files and create a line in the script that will filter them
		SNPMethylFileName = line.strip()
		SNPMethylFileNameElements = SNPMethylFileName.split(".")
		fileTypeLength = len(SNPMethylFileNameElements[-1])
		outputFileName = SNPMethylFileName[0:len(SNPMethylFileName) - fileTypeLength - 1] + "_" + suffix
		pValOutputFileName = SNPMethylFileName[0:len(SNPMethylFileName) - fileTypeLength - 1] + pValSuffix
		cmd = pythonPath + "/" + "python " + codePath + "/" + "correlateSNPsMethylationpValPlusPlus.py"
		scriptFile.write(cmd + " " + SNPMethylFileName + " " + outputFileName + " " + readsToMinMinorReadsFileName + " " + pValOutputFileName + "\n")

	SNPMethylFileListFile.close()
	scriptFile.close()


if __name__=="__main__":
	import sys
	SNPMethylFileListFileName = sys.argv[1]
	suffix = sys.argv[2] # Should not start with _
	readsToMinMinorReadsFileName = sys.argv[3]
	pValSuffix = sys.argv[4]
	scriptFileName = sys.argv[5]
	codePath = sys.argv[6] # Should not end with /
	pythonPath = sys.argv[7] # Should not end with /

	makeCorrelateSNPsMethylationScript(SNPMethylFileListFileName, suffix, readsToMinMinorReadsFileName, pValSuffix, scriptFileName, codePath, pythonPath)
