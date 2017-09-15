def getRandomPositionSeconds(firstPositionsFileName, chromName, chromLength, mean, std, outputFileName):
	# Get a list of random position pairs that have approximately the same length distribution as the true position pairs, with one position already specified
	firstPositionsFile = open(firstPositionsFileName)
	outputFile = open(outputFileName, 'w+')
	random.seed()
	
	for line in firstPositionsFile:
		# Iterate through the distances and get the appropriate number of random pairs for each distance
		firstPosition = int(line.strip())
		secondPosition = int(round(firstPosition + random.gauss(mean, std)))
		if secondPosition >= chromLength:
			# The second position is too large, so make it the length of the chromosome
			secondPosition = chromLength - 1
		elif secondPosition < 0:
			# The second position is too small, so make it 0
			secondPosition = 0
		if firstPosition <= secondPosition:
			# The first position is earlier, so record it first
			outputFile.write(chromName + "\t" + str(firstPosition) + "\t" + str(secondPosition) + "\n")
		else:
			outputFile.write(chromName + "\t" + str(secondPosition) + "\t" + str(firstPosition) + "\n")
	
	firstPositionsFile.close()
	outputFile.close()

	
if __name__=="__main__":
	import sys
	import random
	firstPositionsFileName = sys.argv[1]
	chromName = sys.argv[2]
	chromLength = int(sys.argv[3])
	mean = float(sys.argv[4]) # Using 0
	std = float(sys.argv[5]) # Using 68
	outputFileName = sys.argv[6]

	getRandomPositionSeconds(firstPositionsFileName, chromName, chromLength, mean, std, outputFileName)