def makeCorrelationSNPsMethylationpValScript(SNPMethylFileListFileName, suffix, minReadsCutoff, MAFCutoff, methylCutoff, pValSuffix, scriptFileName, codePath):
	# Make a script that will run correlateSNPsMethylationpVal.py on each file in a list
	SNPMethylFileListFile = open(SNPMethylFileListFileName)
	scriptFile = open(scriptFileName, 'w+')

	for line in SNPMethylFileListFile:
		# Iterate through the batch factor files and create a line in the script that will filter them
		SNPMethylFileName = line.strip()
		SNPMethylFileNameElements = SNPMethylFileName.split(".")
		fileTypeLength = len(SNPMethylFileNameElements[-1])
		outputFileName = SNPMethylFileName[0:len(SNPMethylFileName) - fileTypeLength - 1] + suffix
		pValOutputFileName = SNPMethylFileName[0:len(SNPMethylFileName) - fileTypeLength - 1] + pValSuffix
		cmd = "python " + codePath + "/" + "correlateSNPsMethylationpVal.py"
		scriptFile.write(cmd + " " + SNPMethylFileName + " " + outputFileName + " " + str(minReadsCutoff) + " " + str(MAFCutoff) + " " + str(methylCutoff) + " " + pValOutputFileName + "\n")

	SNPMethylFileListFile.close()
	scriptFile.close()


if __name__=="__main__":
	import sys
	import gzip
	SNPMethylFileListFileName = sys.argv[1]
	suffix = sys.argv[2]
	minReadsCutoff = int(sys.argv[3])
	MAFCutoff = float(sys.argv[4])
	methylCutoff = float(sys.argv[5])
	pValSuffix = sys.argv[6]
	scriptFileName = sys.argv[7]
	codePath = sys.argv[8] # Should not end with /

	makeCorrelationSNPsMethylationpValScript(SNPMethylFileListFileName, suffix, minReadsCutoff, MAFCutoff, methylCutoff, pValSuffix, scriptFileName, codePath)
