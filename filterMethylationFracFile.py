def filterMethylationFracFile(methylationFracFileName, minReads, methylFracCutoff, outputFileName):
	# Filter a methylation file to include only Cs with at least minReads reads and more than methylFracCutoff of reads methylated
	methylationFracFile = open(methylationFracFileName)
	outputFile = open(outputFileName, 'w+')
	for line in methylationFracFile:
		# Iterate through the methylation information and record the lines that satisfy the cutoffs
		lineElements = line.split("\t")
		if int(lineElements[3]) >= minReads:
			# The read cutoff is satisfied
			if float(lineElements[4]) > methylFracCutoff:
				# The methylation cutoff is satisfied
				outputFile.write(line)
	methylationFracFile.close()
	outputFile.close()

if __name__=="__main__":
   import sys
   methylationFracFileName = sys.argv[1] 
   minReads = int(sys.argv[2])
   methylFracCutoff = float(sys.argv[3])
   outputFileName = sys.argv[4]
   filterMethylationFracFile(methylationFracFileName, minReads, methylFracCutoff, outputFileName)