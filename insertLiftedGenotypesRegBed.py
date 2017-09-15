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
		unmappedLocationElements = unmappedLocationInfo.split("\t")
		chrom = unmappedLocationElements[0]
		start = int(unmappedLocationElements[1])
		unmappedLocations.append((chrom, start))
		lineNum = lineNum + 2
	return unmappedLocations

def insertLiftedGenotypesRegBed(genotypesFileName, liftedFileName, unmappedFileName, genotypesLiftedFileName, newAssembly, chromCol, positionCol, assemblyCol):
	# Inserts lifted over genotypes into a file and removes those that were not mapped
	# ASSUMES THAT chromCol < positionCol < assemblyCol
	unmappedLocations = makeUnmappedLocationsList(unmappedFileName)
	genotypesFile = open(genotypesFileName)
	liftedFile = open(liftedFileName)
	genotypesLiftedFile = open(genotypesLiftedFileName, 'w+')
	genotypesLiftedFile.write(genotypesFile.readline()) # Record the header
	for line in genotypesFile:
		# Iterate through the SNPs and create a bed file for each, where the 1st coordinate is the SNP
		lineElements = line.strip().split()
		location = (lineElements[chromCol], int(lineElements[positionCol]))
		if location not in unmappedLocations:
			# The location was mapped
			newLocationLine = liftedFile.readline()
			newLocationElements = newLocationLine.split("\t")
			chrom = newLocationElements[0]
			start = int(newLocationElements[1])
			for i in range(chromCol):
				# Iterate through the locations before the chromosomes and record what is in each location to the output file
				genotypesLiftedFile.write(lineElements[i] + "\t")
			genotypesLiftedFile.write(chrom + "\t")
			for i in range(chromCol+1, positionCol):
				# Iterate through the locations between the chromosome and the position and record everything to the output file
				genotypesLiftedFile.write(lineElements[i] + "\t")
			genotypesLiftedFile.write(str(start) + "\t")
			for i in range(positionCol+1, assemblyCol):
				# Iterate through the locations between the position and the assembly and record everything to the output file
				genotypesLiftedFile.write(lineElements[i] + "\t")
			genotypesLiftedFile.write(newAssembly)
			for i in range(assemblyCol + 1, len(lineElements)):
				# Iterate through the locations between the assembly and the end and record everything to the output file
				genotypesLiftedFile.write("\t" + lineElements[i])
			genotypesLiftedFile.write("\n")
	genotypesFile.close()
	liftedFile.close()
	genotypesLiftedFile.close()

if __name__=="__main__":
	import sys
	genotypesFileName = sys.argv[1]
	liftedFileName = sys.argv[2]
	unmappedFileName = sys.argv[3]
	genotypesLiftedFileName = sys.argv[4]
	newAssembly = sys.argv[5]
	chromCol = int(sys.argv[6])
	positionCol = int(sys.argv[7])
	assemblyCol = int(sys.argv[8])
	insertLiftedGenotypesRegBed(genotypesFileName, liftedFileName, unmappedFileName, genotypesLiftedFileName, newAssembly, chromCol, positionCol, assemblyCol)
