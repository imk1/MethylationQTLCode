def makeFisherExactSNPsMethylationScript(SNPMethylFileListFileName, suffix, readsToMinMinorReadsFileName, scriptFileName, codePath, pythonPath):
	# Make a script that will run correlateSNPsMethylation.py on each file in a list
	SNPMethylFileListFile = open(SNPMethylFileListFileName)
	scriptFile = open(scriptFileName, 'w+')

	for line in SNPMethylFileListFile:
		# Iterate through the batch factor files and create a line in the script that will filter them
		SNPMethylFileName = line.strip()
		SNPMethylFileNameElements = SNPMethylFileName.split(".")
		fileTypeLength = len(SNPMethylFileNameElements[-1])
		outputFileName = SNPMethylFileName[0:len(SNPMethylFileName) - fileTypeLength - 1] + "_" + suffix
		cmd = pythonPath + "/" + "python " + codePath + "/" + "fisherExactSNPsMethylationPlusPlusRandBoth.py"
		scriptFile.write(cmd + " " + SNPMethylFileName + " " + outputFileName + " " + readsToMinMinorReadsFileName + "\n")

	SNPMethylFileListFile.close()
	scriptFile.close()


if __name__=="__main__":
	import sys
	SNPMethylFileListFileName = sys.argv[1]
	suffix = sys.argv[2] # Should not start with _
	readsToMinMinorReadsFileName = sys.argv[3]
	scriptFileName = sys.argv[4]
	codePath = sys.argv[5] # Should not end with /
	pythonPath = sys.argv[6] # Should not end with /

	makeFisherExactSNPsMethylationScript(SNPMethylFileListFileName, suffix, readsToMinMinorReadsFileName, scriptFileName, codePath, pythonPath)
