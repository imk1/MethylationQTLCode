def makeSortMethylationDataDividedFilesScript(methylationDataFileListFileName, suffix, tempFileName, scriptFileName):
	# Make a script that will and sort methylation files by read name, chrom., position
	methylationDataFileListFile = open(methylationDataFileListFileName)
	scriptFile = open(scriptFileName, 'w+')
	lastPrefix = ""

	for line in methylationDataFileListFile:
		# Iterate through the files from Bismark's methylation extractor and make a line in the script for each
		# ASSUMES THAT methylationDataFileListFile IS SORTED BY METHYLATION FILE PREFIX (all parts for each sequence, flowcell, lane, library consecutive)
		methylationDataFileName = line.strip()
		methylationDataFileNameElements = line.split("/")
		methylationDataFileNameNonPathElements = methylationDataFileNameElements[-1].split("_")
		methylationDataFileNamePrefix = methylationDataFileName[0:len(methylationDataFileName)-len(methylationDataFileNameElements[-1])] + "/"
		for i in range(11):
			# Iterate through the parts of the methylation data file name that are common to all parts for a sequence, flowcell, lane, library, and add them to the prefix
			methylationDataFileNamePrefix = methylationDataFileNamePrefix + methylationDataFileNameNonPathElements[i] + "_"
		if (methylationDataFileNamePrefix != lastPrefix) and (lastPrefix != ""):
			# At a new prefix, so record the end of the script for the last prefix and start the script for the new prefix
			methylationDataFileNameEndElements = methylationDataFileNameNonPathElements[-1].split(".")
			fileTypeLength = len(methylationDataFileNameEndElements[-1])
			outputFileName = lastPrefix + suffix
			scriptFile.write( " | grep -v Bismark | sort -t ':' -k5,5n -k6,6n -k7,7n -T " + tempFileName + " | gzip > " + outputFileName + "\n")
			scriptFile.write("zcat " + methylationDataFileName.strip())
			lastPrefix = methylationDataFileNamePrefix
		elif lastPrefix == "":
			# At the beginning of the list, so start the script for the new prefix
			scriptFile.write("zcat " + methylationDataFileName.strip())
			lastPrefix = methylationDataFileNamePrefix
		else:
			scriptFile.write (" " + methylationDataFileName.strip())
			
	methylationDataFileNameEndElements = methylationDataFileNameNonPathElements[-1].split(".")
	fileTypeLength = len(methylationDataFileNameEndElements[-1])
	outputFileName = lastPrefix + suffix
	scriptFile.write( " | grep -v Bismark | sort -t ':' -k5,5n -k6,6n -k7,7n -T " + tempFileName + " | gzip > " + outputFileName + "\n")

	methylationDataFileListFile.close()
	scriptFile.close()


if __name__=="__main__":
	import sys
	methylationDataFileListFileName = sys.argv[1]
	suffix = sys.argv[2] # Should end with .gz
	tempFileName = sys.argv[3]
	scriptFileName = sys.argv[4]

	makeSortMethylationDataDividedFilesScript(methylationDataFileListFileName, suffix, tempFileName, scriptFileName)
