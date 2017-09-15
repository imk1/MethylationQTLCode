def makeUnmappedLocationsList(unmappedFileName):
	# Make a list of umapped locations
	unmappedFile = open(unmappedFileName)
	unmappedFileLines = unmappedFile.readlines()
	unmappedFile.close()
	unmappedLocations = []
	lineNum = 0
	while lineNum < len(unmappedFileLines):
		# Iterate through the unmapped locations and add each to the list
		if "Deleted" not in unmappedFileLines[lineNum]:
			print "Problem!"
			print unmappedFileLines[lineNum]
		unmappedLocationInfo = unmappedFileLines[lineNum + 1]
		unmappedLocationElements = unmappedLocationInfo.split(":")
		chrom = unmappedLocationElements[0]
		positionElements = unmappedLocationElements[1].split("-")
		start = int(positionElements[0])
		unmappedLocations.append((chrom, start))
		lineNum = lineNum + 2
	return unmappedLocations

def insertLiftedGenotypes(genotypesFileName, liftedFileName, unmappedFileName, genotypesLiftedFileName, chromName):
	# Inserts lifted over genotypes into a file and removes those that were not mapped
	unmappedLocations = makeUnmappedLocationsList(unmappedFileName)
	genotypesFile = gzip.open(genotypesFileName, 'rb')
	liftedFile = open(liftedFileName)
	genotypesLiftedFile = open(genotypesLiftedFileName, 'w+')
	# NO HEADER
	for line in genotypesFile:
		# Iterate through the SNPs and create a bed file for each, where the 1st coordinate is the SNP
		lineElements = line.split(" ")
		location = (chromName, int(lineElements[2]))
		if location not in unmappedLocations:
			# The location was mapped
			newLocationLine = liftedFile.readline()
			newLocationElements = newLocationLine.split(":")
			chrom = newLocationElements[0]
			positionElements = newLocationElements[1].split("-")
			start = int(positionElements[0])
			genotypesLiftedFile.write(lineElements[0] + " " + lineElements[1] + " ")
			genotypesLiftedFile.write(str(start) + " " + lineElements[3] + " " + lineElements[4])
			for le in lineElements[5:]:
				# Iterate through the information for the SNP and record it in the new file
				genotypesLiftedFile.write(" " + le.strip())
			genotypesLiftedFile.write("\n")
	genotypesFile.close()
	liftedFile.close()
	genotypesLiftedFile.close()

if __name__=="__main__":
	import sys
	import gzip
	genotypesFileName = sys.argv[1]
	liftedFileName = sys.argv[2]
	unmappedFileName = sys.argv[3]
	genotypesLiftedFileName = sys.argv[4]
	newAssembly = sys.argv[5]
	insertLiftedGenotypes(genotypesFileName, liftedFileName, unmappedFileName, genotypesLiftedFileName, newAssembly)
