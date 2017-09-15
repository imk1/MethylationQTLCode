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

def catSeparateChromsIndivFile(fileName, chromListFileName, outputFilePath, chromCol):
	# Create a separate file for each chromosome
	# ASSUMES THAT THE CHROMOSOME IS THE SAME FOR SNPS AND C'S
	fileNameElements = fileName.strip().split("/")
	outputFileNameSuffix = fileNameElements[-1]
	chromFilesDict = makeChromFilesDict(chromListFileName, outputFilePath, outputFileNameSuffix)
	inputFile = gzip.open(fileName)
	for line in inputFile:
		# Iterate through the lines of the file and put them into the output file for their chromosomes
		lineElements =line.strip().split("\t")
		chrom = lineElements[chromCol]
		chromFilesDict[chrom].write(line)
	inputFile.close()
	chromNames = chromFilesDict.keys()
	for chrom in chromNames:
		# Close all of the output files
		chromFilesDict[chrom].close()

if __name__=="__main__":
   import sys
   import gzip
   fileName = sys.argv[1] 
   chromListFileName = sys.argv[2]
   outputFilePath = sys.argv[3] # Should not end in /
   chromCol = int(sys.argv[4]) # 0-indexed; 1 for SNPMethyl, 2 for methylation
   catSeparateChromsIndivFile(fileName, chromListFileName, outputFilePath, chromCol)