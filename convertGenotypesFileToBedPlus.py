def convertGenotypesFileToBedPlus(genotypesFileName, chromCol, positionCol, bedFileName):
	# Converts a file with genotypes to a bed file
	genotypesFile = open(genotypesFileName)
	bedFile = open(bedFileName, 'w+')
	for line in genotypesFile:
		# Iterate through the SNPs and create a bed file for each, where the 1st coordinate is the SNP
		lineElements = line.strip().split("\t")
		bedFile.write(lineElements[chromCol] + ":" + lineElements[positionCol] + "-" + lineElements[positionCol] + "\n")
	genotypesFile.close()
	bedFile.close()

if __name__=="__main__":
	import sys
	genotypesFileName = sys.argv[1]
	chromCol = int(sys.argv[2])
	positionCol = int(sys.argv[3])
	bedFileName = sys.argv[4]
	convertGenotypesFileToBedPlus(genotypesFileName, chromCol, positionCol, bedFileName)
