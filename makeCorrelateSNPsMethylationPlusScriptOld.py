def makeCorrelationSNPsMethylationPlusScript(SNPMethylFileListFileName, suffix, SNPVecSuffix, methylVecSuffix, minReadsCutoff, MAFCutoff, methylCutoff, scriptFileName, codePath):
	# Make a script that will run correlateSNPsMethylation.py on each file in a list
	SNPMethylFileListFile = open(SNPMethylFileListFileName)
	scriptFile = open(scriptFileName, 'w+')

	for line in SNPMethylFileListFile:
		# Iterate through the batch factor files and create a line in the script that will filter them
		SNPMethylFileName = line.strip()
		SNPMethylFileNameElements = SNPMethylFileName.split(".")
		fileTypeLength = len(SNPMethylFileNameElements[-1])
		outputFileName = SNPMethylFileName[0:len(SNPMethylFileName) - fileTypeLength - 1] + suffix
		SNPVecFileName = SNPMethylFileName[0:len(SNPMethylFileName) - fileTypeLength - 1] + SNPVecSuffix
		methylVecFileName = SNPMethylFileName[0:len(SNPMethylFileName) - fileTypeLength - 1] + methylVecSuffix
		cmd = "python " + codePath + "/" + "correlateSNPsMethylation.py"
		scriptFile.write(cmd + " " + SNPMethylFileName + " " + outputFileName + " " + SNPVecFileName + " " + methylVecFileName + " " + str(minReadsCutoff) + " " + str(MAFCutoff) + " " + str(methylCutoff) + "\n")

	SNPMethylFileListFile.close()
	scriptFile.close()


if __name__=="__main__":
	import sys
	import scipy
	from scipy import stats
	import gzip
	SNPMethylFileListFileName = sys.argv[1]
	suffix = sys.argv[2] # Should end with .gz
	SNPVecSuffix = sys.argv[3] # Should end with .gz
	methylVecSuffix = sys.argv[4] # Should end with .gz
	minReadsCutoff = int(sys.argv[5])
	MAFCutoff = float(sys.argv[6])
	methylCutoff = float(sys.argv[7])
	scriptFileName = sys.argv[8]
	codePath = sys.argv[9] # Should not end with /

	makeCorrelationSNPsMethylationPlusScript(SNPMethylFileListFileName, suffix, SNPVecSuffix, methylVecSuffix, minReadsCutoff, MAFCutoff, methylCutoff, scriptFileName, codePath)
