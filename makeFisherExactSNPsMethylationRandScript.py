def makeFisherExactSNPsMethylationRandScript(SNPMethylFileListFileName, suffix, minReadsCutoff, MAFCutoff, methylCutoff, scriptFileName, codePath, pythonPath):
	# Make a script that will run correlateSNPsMethylation.py on each file in a list
	SNPMethylFileListFile = open(SNPMethylFileListFileName)
	scriptFile = open(scriptFileName, 'w+')

	for line in SNPMethylFileListFile:
		# Iterate through the batch factor files and create a line in the script that will filter them
		SNPMethylFileName = line.strip()
		SNPMethylFileNameElements = SNPMethylFileName.split(".")
		fileTypeLength = len(SNPMethylFileNameElements[-1])
		outputFileName = SNPMethylFileName[0:len(SNPMethylFileName) - fileTypeLength - 1] + "_" + suffix
		cmd =pythonPath + "/" + "python " + codePath + "/" + "fisherExactSNPsMethylationRand.py"
		scriptFile.write(cmd + " " + SNPMethylFileName + " " + outputFileName + " " + str(minReadsCutoff) + " " + str(MAFCutoff) + " " + str(methylCutoff) + "\n")

	SNPMethylFileListFile.close()
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

	makeFisherExactSNPsMethylationRandScript(SNPMethylFileListFileName, suffix, minReadsCutoff, MAFCutoff, methylCutoff, scriptFileName, codePath, pythonPath)
