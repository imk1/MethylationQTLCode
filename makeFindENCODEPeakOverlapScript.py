def makeFindENCODEPeakOverlapScript(chromRangeFileNameListFileName, SNPFileName, outputFilePath, suffix, scriptFileName):
	# Make a script that will remove the header from the methylation files and sort them by chrom., position
	chromRangeFileNameListFile = open(chromRangeFileNameListFileName)
	scriptFile = open(scriptFileName, 'w+')

	for line in chromRangeFileNameListFile:
		# Iterate through the files from Bismark's methylation extractor and make a line in the script for each
		chromRangeFileName = line.strip()
		chromRangeFilePathElements = chromRangeFileName.split("/")
		chromRangeFileNameElements = chromRangeFilePathElements[-1].split(".")
		fileTypeLength = len(chromRangeFileNameElements[-1]) + len(chromRangeFileNameElements[-2]) + 1
		outputFileName = outputFilePath + "/" + chromRangeFilePathElements[-1][0:len(chromRangeFilePathElements[-1]) - fileTypeLength] + suffix
		scriptFile.write("python /science/irene/MethylationQTLProject/src/findENCODEPeakOverlap.py " + chromRangeFileName + " " + SNPFileName + " " + outputFileName + "\n")

	chromRangeFileNameListFile.close()
	scriptFile.close()


if __name__=="__main__":
	import sys
	chromRangeFileNameListFileName = sys.argv[1]
	SNPFileName = sys.argv[2]
	outputFilePath = sys.argv[3] # Should not end with /
	suffix = sys.argv[4] # Should not end with .gz
	scriptFileName = sys.argv[5]

	makeFindENCODEPeakOverlapScript(chromRangeFileNameListFileName, SNPFileName, outputFilePath, suffix, scriptFileName)