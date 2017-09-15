def makeSortBamScript(bismarkBamFileListFileName, suffix, scriptFileName):
	# Make a script that will run bismarkSNPExtractor.py on a list of files
	bismarkBamFileListFile = open(bismarkBamFileListFileName)
	scriptFile = open(scriptFileName, 'w+')

	for line in bismarkBamFileListFile:
		# Iterate through the sam outputs from Bismark and make a line in the script for each
		bismarkBamFileName = line.strip()
		bismarkBamFileNameElements = bismarkBamFileName.split(".")
		fileTypeLength = len(bismarkBamFileNameElements[-1])
		outputFileName = bismarkBamFileName[0:len(bismarkBamFileName) - fileTypeLength] + suffix
		scriptFile.write("samtools sort " + bismarkBamFileName + " " + outputFileName + "\n")

	bismarkBamFileListFile.close()
	scriptFile.close()


if __name__=="__main__":
	import sys
	bismarkBamFileListFileName = sys.argv[1]
	suffix = sys.argv[2]
	scriptFileName = sys.argv[3]

	makeSortBamScript(bismarkBamFileListFileName, suffix, scriptFileName)
