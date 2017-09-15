def makeSortMethylationDataScript(methylationDataFileListFileName, suffix, scriptFileName):
	# Make a script that will and sort methylation files by read name, chrom., position
	methylationDataFileListFile = open(methylationDataFileListFileName)
	scriptFile = open(scriptFileName, 'w+')

	for line in methylationDataFileListFile:
		# Iterate through the files from Bismark's methylation extractor and make a line in the script for each
		methylationDataFileName = line.strip()
		methylationDataFileNameElements = methylationDataFileName.split(".")
		fileTypeLength = len(methylationDataFileNameElements[-1])
		outputFileName = methylationDataFileName[0:len(methylationDataFileName) - fileTypeLength] + suffix
		scriptFile.write("zcat " + methylationDataFileName + " | sort -t ':' -k5,5n -k6,6n -k7,7n -T /tmp | gzip > " + outputFileName + "\n")

	methylationDataFileListFile.close()
	scriptFile.close()


if __name__=="__main__":
	import sys
	methylationDataFileListFileName = sys.argv[1]
	suffix = sys.argv[2] # Should end with .gz
	scriptFileName = sys.argv[3]

	makeSortMethylationDataScript(methylationDataFileListFileName, suffix, scriptFileName)
