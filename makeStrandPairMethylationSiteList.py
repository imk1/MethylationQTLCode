def makeStrandPairMethylationSiteList(methylationLocationsOneFileName, methylationLocationsTwoFileName, outputOneFileName, outputTwoFileName):
	# Makes a list of sites with CpGs across both strands for each strand (includes methylated and non-methylated sites)
	# ASSUMES THAT LOCATIONS IN FILE TWO CORRESPOND TO LOCATIONS IN FILE ONE + 1 (usually: file one is OT, two is OB)
	# ASSUMES THAT BOTH FILES ARE SORTED BY CHROM, BASE AND HAVE NO REPEATS
	methylationLocationsOneFile = open(methylationLocationsOneFileName)
	methylationLocationsTwoFile = open(methylationLocationsTwoFileName)
	outputOneFile = open(outputOneFileName, 'w+')
	outputTwoFile = open(outputTwoFileName, 'w+')
	lineTwo = methylationLocationsTwoFile.readline()
	lineTwoElements = lineTwo.split("\t")
	fileTwoDone = False
	for line in methylationLocationsOneFile:
		# Iterate through locations in the first file and write those to the output files
		lineElements = line.split("\t")
		if fileTwoDone == True:
			# The second file has been read to completion, so write the line from the first file and continue
			outputOneFile.write(line)
			outputTwoFile.write(lineElements[0] + "\t" + str(int(lineElements[1].strip()) + 1) + "\n")
			continue
		while lineElements[0] > lineTwoElements[0]:
			# Iterate through lines from the second file until a line with the right chromosome is reached
			# Write each line of the second file to the output files
			outputOneFile.write(lineTwoElements[0] + "\t" + str(int(lineTwoElements[1].strip()) - 1) + "\n")
			outputTwoFile.write(lineTwo)
			lineTwo = methylationLocationsTwoFile.readline()
			if lineTwo == "":
				# The second file has been read to completion, so stop
				fileTwoDone = True
				break
			lineTwoElements = lineTwo.split("\t")
		if fileTwoDone == True:
			# The second file has been read to completion, so write the line from the first file and continue
			outputOneFile.write(line)
			outputTwoFile.write(lineElements[0] + "\t" + str(int(lineElements[1].strip()) + 1) + "\n")
			continue
		while (lineElements[0] == lineTwoElements[0]) and (int(lineElements[1].strip()) >= int(lineTwoElements[1].strip())):
			# Iterate through the lines from the second file until a line with the right base is reached
			# Write each line of the second file to the output files
			outputOneFile.write(lineTwoElements[0] + "\t" + str(int(lineTwoElements[1].strip()) - 1) + "\n")
			outputTwoFile.write(lineTwo)
			lineTwo = methylationLocationsTwoFile.readline()
			if lineTwo == "":
				# The second file has been read to completion, so stop
				fileTwoDone = True
				break
			lineTwoElements = lineTwo.split("\t")
		if fileTwoDone == True:
			# The second file has been read to completion, so write the line from the first file and continue
			outputOneFile.write(line)
			outputTwoFile.write(lineElements[0] + "\t" + str(int(lineElements[1].strip()) + 1) + "\n")
			continue
		if (lineElements[0] == lineTwoElements[0]) and (int(lineElements[1].strip()) + 1 == int(lineTwoElements[1].strip())):
			# The methylation sites in the files overlap
			outputOneFile.write(lineElements[0] + "\t" + lineElements[1].strip() + "\n")
			outputTwoFile.write(lineTwoElements[0] + "\t" + lineTwoElements[1].strip() + "\n")
			lineTwo = methylationLocationsTwoFile.readline()
			if lineTwo == "":
				# The second file has been read to completion
				fileTwoDone = True
			lineTwoElements = lineTwo.split("\t")
		else:
			# The methylation site in the first file is earler than the one in the second file
			outputOneFile.write(line)
			outputTwoFile.write(lineElements[0] + "\t" + str(int(lineElements[1].strip()) + 1) + "\n")
	if fileTwoDone == False:
		# Record the remaining lines in the second file to the output files
		outputOneFile.write(lineTwoElements[0] + "\t" + str(int(lineTwoElements[1].strip()) - 1) + "\n")
		outputTwoFile.write(lineTwo)
		for lineTwo in methylationLocationsTwoFile:
			# Iterate through the remaining lines of the second file and write each to the output files
			lineTwoElements = lineTwo.split("\t")
			outputOneFile.write(lineTwoElements[0] + "\t" + str(int(lineTwoElements[1].strip()) - 1) + "\n")
			outputTwoFile.write(lineTwo)
	methylationLocationsOneFile.close()
	methylationLocationsTwoFile.close()
	outputOneFile.close()
	outputTwoFile.close()

if __name__=="__main__":
	import sys
	import numpy
	methylationLocationsOneFileName = sys.argv[1]
	methylationLocationsTwoFileName = sys.argv[2]
	outputOneFileName = sys.argv[3]
	outputTwoFileName = sys.argv[4]
	makeStrandPairMethylationSiteList(methylationLocationsOneFileName, methylationLocationsTwoFileName, outputOneFileName, outputTwoFileName)
