def convertGenotypesFileToBed(genotypesFileName, chromName, positionCol, bedFileName):
	# Converts a file with genotypes to a bed file
	genotypesFile = gzip.open(genotypesFileName, 'rb')
	bedFile = open(bedFileName, 'w+')
	# NO HEADER
	for line in genotypesFile:
		# Iterate through the SNPs and create a bed file for each, where the 1st coordinate is the SNP
		lineElements = line.split(" ")
		bedFile.write(chromName + ":" + lineElements[positionCol] + "-" + lineElements[positionCol] + "\n")
	genotypesFile.close()
	bedFile.close()

if __name__=="__main__":
	import sys
	import gzip
	genotypesFileName = sys.argv[1]
	chromName = sys.argv[2]
	positionCol = int(sys.argv[3])
	bedFileName = sys.argv[4]
	convertGenotypesFileToBed(genotypesFileName, chromName, positionCol, bedFileName)
