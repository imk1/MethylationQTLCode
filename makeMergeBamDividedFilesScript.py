def makeMergeBamDividedFilesScript(bamFileListFileName, suffix, scriptFileName):
	# Make a script that will merge bam files
	bamFileListFile = open(bamFileListFileName)
	scriptFile = open(scriptFileName, 'w+')
	lastPrefix = ""
	bamFileNameList = []

	for line in bamFileListFile:
		# Iterate through the bam files and make a part of a line in the script for each
		# ASSUMES THAT bamFileListFile IS SORTED BY bam FILE PREFIX (all parts for each sequence, flowcell, lane, library consecutive)
		bamFileName = line.strip()
		bamFileNameElements = line.split("/")
		bamFileNameNonPathElements = bamFileNameElements[-1].split("_")
		bamFileNamePrefix = bamFileName[0:len(bamFileName)-len(bamFileNameElements[-1])] + "/"
		for i in range(9):
			# Iterate through the parts of the methylation data file name that are common to all parts for a sequence, flowcell, lane, library, and add them to the prefix
			bamFileNamePrefix = bamFileNamePrefix + bamFileNameNonPathElements[i] + "_"
		if (bamFileNamePrefix != lastPrefix) and (lastPrefix != ""):
			# At a new prefix, so record the end of the script for the last prefix and start the script for the new prefix
			bamFileNameEndElements = bamFileNameNonPathElements[-1].split(".")
			fileTypeLength = len(bamFileNameEndElements[-1])
			outputFileName = lastPrefix + suffix
			if len(bamFileNameList) > 1:
				# There are multiple bam files with the same prefix, so merge them
				scriptFile.write("samtools merge " + outputFileName)
				for bfn in bamFileNameList:
					# merge each bam file with the same prefix
					scriptFile.write(" " + bfn)
				scriptFile.write("\n")
			else:
				scriptFile.write("cp " + bamFileNameList[0] + " " + outputFileName + "\n")
			lastPrefix = bamFileNamePrefix
			bamFileNameList = []
			bamFileNameList.append(bamFileName.strip())
		elif lastPrefix == "":
			# At the beginning of the list, so start the script for the new prefix
			bamFileNameList.append(bamFileName.strip())
			lastPrefix = bamFileNamePrefix
		else:
			bamFileNameList.append(bamFileName.strip())
	
	outputFileName = lastPrefix + suffix
	if len(bamFileNameList) > 1:
		# There are multiple bam files with the same prefix, so merge them
		scriptFile.write("samtools merge " + outputFileName)
		for bfn in bamFileNameList:
			# merge each bam file with the same prefix
			scriptFile.write(" " + bfn)
		scriptFile.write("\n")
	else:
		scriptFile.write("cp " + bamFileNameList[0] + " " + outputFileName + "\n")

	bamFileListFile.close()
	scriptFile.close()


if __name__=="__main__":
	import sys
	bamFileListFileName = sys.argv[1]
	suffix = sys.argv[2] # Should end with .gz
	scriptFileName = sys.argv[3]

	makeMergeBamDividedFilesScript(bamFileListFileName, suffix, scriptFileName)
