def makermdupScript(bismarkSortedBamFileListFileName, suffix, scriptFileName):
	# Make a script that will run bismarkSNPExtractor.py on a list of files
	bismarkSortedBamFileListFile = open(bismarkSortedBamFileListFileName)
	scriptFile = open(scriptFileName, 'w+')

	for line in bismarkSortedBamFileListFile:
		# Iterate through the sam outputs from Bismark and make a line in the script for each
		bismarkSortedBamFileName = line.strip()
		bismarkSortedBamFileNameElements = bismarkSortedBamFileName.split(".")
		fileTypeLength = len(bismarkSortedBamFileNameElements[-1])
		outputFileName = bismarkSortedBamFileName[0:len(bismarkSortedBamFileName) - fileTypeLength] + suffix
		scriptFile.write("samtools rmdup " + bismarkSortedBamFileName + " " + outputFileName + "\n")

	bismarkSortedBamFileListFile.close()
	scriptFile.close()


if __name__=="__main__":
	import sys
	bismarkSortedBamFileListFileName = sys.argv[1]
	suffix = sys.argv[2]
	scriptFileName = sys.argv[3]

	makermdupScript(bismarkSortedBamFileListFileName, suffix, scriptFileName)
