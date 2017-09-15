def makeSortChromRangeScript(chromRangeFileNameListFileName, suffix, scriptFileName):
	# Make a script that will remove the header from the methylation files and sort them by chrom., position
	chromRangeFileNameListFile = open(chromRangeFileNameListFileName)
	scriptFile = open(scriptFileName, 'w+')

	for line in chromRangeFileNameListFile:
		# Iterate through the files from Bismark's methylation extractor and make a line in the script for each
		chromRangeFileName = line.strip()
		chromRangeFileNameElements = chromRangeFileName.split(".")
		fileTypeLength = len(chromRangeFileNameElements[-1]) + len(chromRangeFileNameElements[-2]) + 1
		outputFileName = chromRangeFileName[0:len(chromRangeFileName) - fileTypeLength] + suffix
		scriptFile.write("zcat " + chromRangeFileName + " | sort -k1,1 -k2,2n -k3,3n -T /tmp | gzip > " + outputFileName + "\n")

	chromRangeFileNameListFile.close()
	scriptFile.close()


if __name__=="__main__":
	import sys
	chromRangeFileNameListFileName = sys.argv[1]
	suffix = sys.argv[2] # Should end with .gz
	scriptFileName = sys.argv[3]

	makeSortChromRangeScript(chromRangeFileNameListFileName, suffix, scriptFileName)