def makeChromFilesDict(chromListFileName, outputFilePath, outputFileNameSuffix):
	# Make an output file for each chromosome
	chromListFile = open(chromListFileName)
	chromFilesDict = {}
	for line in chromListFile:
		# Iterate through the chromosomes and open a separate output file for each
		chromFileName = outputFilePath + "/" + line.strip() + "_" + outputFileNameSuffix
		cf = gzip.open(chromFileName, 'w+')
		chromFilesDict[line.strip()] = cf
	return chromFilesDict

def catSeparateChroms(fileNameListFileName, chromListFileName, outputFilePath, outputFileNameSuffix, chromCol):
	# Combine all files into a separate file for each chromosome
	# ASSUMES THAT THE CHROMOSOME IS IN THE 2ND COLUMN AND IS THE SAME FOR SNPS AND C'S
	chromFilesDict = makeChromFilesDict(chromListFileName, outputFilePath, outputFileNameSuffix)
	fileNameListFile = open(fileNameListFileName)
	for fileName in fileNameListFile:
		# Itereate through the files and combine the lines from each chromosome
		print fileName.strip()
		inputFile = gzip.open(fileName.strip())
		for line in inputFile:
			# Iterate through the lines of the file and put them into the output file for their chromosomes
			lineElements =line.strip().split("\t")
			
			# ADDED MAY 2014 FOR WHEN SAM IS FROM A SUBSET OF THE GENOME
			chromElements = lineElements[chromCol].split(":")
			chrom = chromElements[0]
			#chrom = lineElements[chromCol]
			
			chromFilesDict[chrom].write(line)
		inputFile.close()
	fileNameListFile.close()
	chromNames = chromFilesDict.keys()
	for chrom in chromNames:
		# Close all of the output files
		chromFilesDict[chrom].close()

if __name__=="__main__":
   import sys
   import gzip
   fileNameListFileName = sys.argv[1] 
   chromListFileName = sys.argv[2]
   outputFilePath = sys.argv[3] # Should not end in /
   outputFileNameSuffix = sys.argv[4] # Should end in .gz, should not start with _
   chromCol = int(sys.argv[5]) # 0-indexed; 1 for SNPMethyl, 2 for methylation
   catSeparateChroms(fileNameListFileName, chromListFileName, outputFilePath, outputFileNameSuffix, chromCol)