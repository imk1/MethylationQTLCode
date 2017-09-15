def getSNPMethylLocations(line):
	# Get the chromosome, SNP location, and methylation location from a file
	allFileRead = False
	if line == "":
		# At the end of the file
		allFileRead = True
		return [("", 0, 0), allFileRead]
	
	lineElements = line.strip().split()
	lineSNPMethylLocations = (lineElements[0], int(lineElements[1]), int(lineElements[3]))
	return [lineSNPMethylLocations, allFileRead]


def getSNPMethylOverlap(SNPMethylFileNameOne, SNPMethylFileNameTwo, outputFileName):
	# Get SNP, CpG pairs that are in two files
	# ASSUMES THAT BOTH FILES ARE SORTED BY METHYLATION CHROMOSOME, METHYLATION LOCATION, SNP CHROMOSOME, SNP LOCATION
	# THE FIRST FILE'S p-VALUE WILL BE IN THE OUTPUT FILE
	SNPMethylFileOne = open(SNPMethylFileNameOne)
	SNPMethylFileTwo = open(SNPMethylFileNameTwo)
	[lineTwoSNPMethylLocations, allFileTwoRead] = getSNPMethylLocations(SNPMethylFileTwo.readline())
	outputFile = open(outputFileName, 'w+')
	
	for line in SNPMethylFileOne:
		# Iterate through the lines of the first SNP, methylation file and find those with locations that are also in the second
		[lineOneSNPMethylLocations, allFileOneRead] = getSNPMethylLocations(line)
		while lineTwoSNPMethylLocations[0] < lineOneSNPMethylLocations[0]:
			# Go through the second file until a SNP, CpG pair on the proper chromosome is reached
			[lineTwoSNPMethylLocations, allFileTwoRead] = getSNPMethylLocations(SNPMethylFileTwo.readline())
			if allFileTwoRead == True:
				# At the end of the second file
				break
		if allFileTwoRead == True:
				# At the end of the second file, so stop
				break
		
		while (lineTwoSNPMethylLocations[2] < lineOneSNPMethylLocations[2]) and (lineTwoSNPMethylLocations[0] == lineOneSNPMethylLocations[0]):
			# Go through the second file until a SNP, CpG pair on the proper chromosome with the same CpG as in the first file is reached
			[lineTwoSNPMethylLocations, allFileTwoRead] = getSNPMethylLocations(SNPMethylFileTwo.readline())
			if allFileTwoRead == True:
				# At the end of the second file
				break
		if allFileTwoRead == True:
				# At the end of the second file, so stop
				break
		
		while (lineTwoSNPMethylLocations[1] < lineOneSNPMethylLocations[1]) and ((lineTwoSNPMethylLocations[0] == lineOneSNPMethylLocations[0]) and (lineTwoSNPMethylLocations[2] == lineOneSNPMethylLocations[2])):
			# Go through the second file until a SNP, CpG pair on the proper chromosome with the same CpG and SNP as in the first file is reached
			[lineTwoSNPMethylLocations, allFileTwoRead] = getSNPMethylLocations(SNPMethylFileTwo.readline())
			if allFileTwoRead == True:
				# At the end of the second file
				break
		if allFileTwoRead == True:
				# At the end of the second file, so stop
				break
		if (lineTwoSNPMethylLocations[1] == lineOneSNPMethylLocations[1]) and ((lineTwoSNPMethylLocations[0] == lineOneSNPMethylLocations[0]) and (lineTwoSNPMethylLocations[2] == lineOneSNPMethylLocations[2])):
			# The current SNP, CpG pair is in both files
			lineElements = line.strip().split("\t")
			outputFile.write(lineOneSNPMethylLocations[0] + "\t" + str(lineOneSNPMethylLocations[1]) + "\t" + lineOneSNPMethylLocations[0] + "\t" + str(lineOneSNPMethylLocations[2]) + "\t" + lineElements[4] + "\n")
	
	SNPMethylFileOne.close()
	SNPMethylFileTwo.close()
	outputFile.close()


if __name__=="__main__":
	import sys
	SNPMethylFileNameOne = sys.argv[1]
	SNPMethylFileNameTwo = sys.argv[2]
	outputFileName = sys.argv[3]
	
	getSNPMethylOverlap(SNPMethylFileNameOne, SNPMethylFileNameTwo, outputFileName)