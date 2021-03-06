def makeBismarkSNPExtractorGenomeSubsetScript(bismarkSamFileListFileName, SNPVcfStartFileName, suffix, scriptFileName, codePath):
	# Make a script that will run bismarkSNPExtractor.py on a list of files
	bismarkSamFileListFile = open(bismarkSamFileListFileName)
	scriptFile = open(scriptFileName, 'w+')

	for line in bismarkSamFileListFile:
		# Iterate through the sam outputs from Bismark and make a line in the script for each
		bismarkSamFileName = line.strip()
		bismarkSamFileNameElements = bismarkSamFileName.split(".")
		fileTypeLength = len(bismarkSamFileNameElements[-1])
		outputFileName = bismarkSamFileName[0:len(bismarkSamFileName) - fileTypeLength] + suffix
		scriptFile.write("python " + codePath + "/" + "bismarkSNPExtractorGenomeSubset.py " + bismarkSamFileName + " " + SNPVcfStartFileName + " " + outputFileName + "\n")

	bismarkSamFileListFile.close()
	scriptFile.close()


if __name__=="__main__":
	import sys
	bismarkSamFileListFileName = sys.argv[1]
	SNPVcfStartFileName = sys.argv[2]
	suffix = sys.argv[3]
	scriptFileName = sys.argv[4]
	codePath = sys.argv[5] # Should not have a / at the end

	makeBismarkSNPExtractorGenomeSubsetScript(bismarkSamFileListFileName, SNPVcfStartFileName, suffix, scriptFileName, codePath)
