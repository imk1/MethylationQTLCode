def makeSortSNPDataScript(SNPDataFileListFileName, suffix, scriptFileName):
	# Make a script that will remove the header from the methylation files and sort them by read name, chrom., position
	SNPDataFileListFile = open(SNPDataFileListFileName)
	scriptFile = open(scriptFileName, 'w+')

	for line in SNPDataFileListFile:
		# Iterate through the files from Bismark's methylation extractor and make a line in the script for each
		SNPDataFileName = line.strip()
		SNPDataFileNameElements = SNPDataFileName.split(".")
		fileTypeLength = len(SNPDataFileNameElements[-1])
		outputFileName = SNPDataFileName[0:len(SNPDataFileName) - fileTypeLength] + suffix
		scriptFile.write("sort -k1,1 -k3,3 -k4,4n " + SNPDataFileName + " > " + outputFileName + "\n")

	SNPDataFileListFile.close()
	scriptFile.close()


if __name__=="__main__":
	import sys
	SNPDataFileListFileName = sys.argv[1]
	suffix = sys.argv[2]
	scriptFileName = sys.argv[3]

	makeSortSNPDataScript(SNPDataFileListFileName, suffix, scriptFileName)
