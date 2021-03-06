def getStrandPairMethylation(methylationLocationsOneFileName, methylationLocationsTwoFileName, outputFileName):
	# Gets the locations of the methylated bases that are in both strands
	# Also determines the fraction of methylated bases in each strand that are methylated in the other strand
	# ASSUMES THAT LOCATIONS IN FILE TWO CORRESPOND TO LOCATIONS IN FILE ONE + 1 (usually: file one is OT, two is OB)
	# ASSUMES THAT BOTH FILES ARE SORTED BY CHROM, BASE AND HAVE NO REPEATS
	methylationLocationsOneFile = open(methylationLocationsOneFileName)
	methylationLocationsTwoFile = open(methylationLocationsTwoFileName)
	outputFile = open(outputFileName, 'w+')
	methylationOneCount = 0
	methylationOverlapCount = 0
	methylationTwoCount = 0
	lineTwo = methylationLocationsTwoFile.readline()
	lineTwoElements = lineTwo.split("\t")
	fileTwoDone = False
	for line in methylationLocationsOneFile:
		# Iterate through locations in the first file and find those that correspond to locations in the second file
		methylationOneCount = methylationOneCount + 1
		if fileTwoDone == True:
			# The second file has been read to completion, so continue
			continue
		lineElements = line.split("\t")
		while lineElements[0] > lineTwoElements[0]:
			# Iterate through lines from the second file until a line with the right chromosome is reached
			methylationTwoCount = methylationTwoCount + 1
			lineTwo = methylationLocationsTwoFile.readline()
			if lineTwo == "":
				# The second file has been read to completion, so stop
				fileTwoDone = True
				break
			lineTwoElements = lineTwo.split("\t")
		if fileTwoDone == True:
			# The second file has been read to completion, so continue
			continue
		while (lineElements[0] == lineTwoElements[0]) and (int(lineElements[1].strip()) >= int(lineTwoElements[1].strip())):
			# Iterate through the lines from the second file until a line with the right base is reached
			methylationTwoCount = methylationTwoCount + 1
			lineTwo = methylationLocationsTwoFile.readline()
			if lineTwo == "":
				# The second file has been read to completion, so stop
				fileTwoDone = True
				break
			lineTwoElements = lineTwo.split("\t")
		if fileTwoDone == True:
			# The second file has been read to completion, so continue
			continue
		if (lineElements[0] == lineTwoElements[0]) and (int(lineElements[1].strip()) + 1 == int(lineTwoElements[1].strip())):
			methylationOverlapCount = methylationOverlapCount + 1
			outputFile.write(lineElements[0] + "\t" + lineElements[1].strip() + "\n")
	if fileTwoDone == False:
		# Increment counts for the second file based on how many lines remain
		methylationTwoCount = methylationTwoCount + 1 # The latest line has not yet been counted
		methylationTwoLines = methylationLocationsTwoFile.readlines()
		methylationTwoCount = methylationTwoCount + len(methylationTwoLines)
	print float(methylationOverlapCount)/float(methylationOneCount)
	print float(methylationOverlapCount)/float(methylationTwoCount)
	methylationLocationsOneFile.close()
	methylationLocationsTwoFile.close()
	outputFile.close()

if __name__=="__main__":
	import sys
	methylationLocationsOneFileName = sys.argv[1]
	methylationLocationsTwoFileName = sys.argv[2]
	outputFileName = sys.argv[3]
	getStrandPairMethylation(methylationLocationsOneFileName, methylationLocationsTwoFileName, outputFileName)
