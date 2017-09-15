def getMBias(methylationFileName, methylLetter, readLength):
	# Get the percentage of methylated cytosines at each position in the read
	methylationFile = gzip.open(methylationFileName)
	methylationFile.readline() # Remove the header
	readPositionTotalCounts = []
	readPositionMethylCounts = []
	for i in range(readLength):
		# Initialize all of the counts to 0
		readPositionTotalCounts.append(0)
		readPositionMethylCounts.append(0)
	for line in methylationFile:
		# Iterate through the lines of the methylation file and increment the appropriate counts
		lineElements = line.strip().split("\t")
		readPosition = int(lineElements[5]) - 1
		readPositionTotalCounts[readPosition] = readPositionTotalCounts[readPosition] + 1
		methylStatus = lineElements[4]
		if methylStatus == methylLetter:
			# The current base is methylated, so increment the appropriate methyl. count
			readPositionMethylCounts[readPosition] = readPositionMethylCounts[readPosition] + 1
	methylationFile.close()
	return [readPositionTotalCounts, readPositionMethylCounts]

def outputMBias(readPositionTotalCounts, readPositionMethylCounts, MBiasFileName):
	# Record the percentage of methylated cytosines at each position
	MBiasFile = open(MBiasFileName, 'w+')
	for i in range(len(readPositionMethylCounts)):
		# Iterate through the positions and compute the percentage of methylated cytosines at each position
		MBias = float(readPositionMethylCounts[i])/float(readPositionTotalCounts[i])
		MBiasFile.write(str(i + 1) + '\t' + str(readPositionMethylCounts[i]) + '\t' + str(readPositionTotalCounts[i]) + '\t' + str(MBias) + '\n')
	MBiasFile.close()

if __name__=="__main__":
	import sys
	import gzip
	methylationFileName = sys.argv[1] # Should end with .gz
	methylLetter = sys.argv[2]
	readLength = int(sys.argv[3])
	MBiasFileName = sys.argv[4] # Should not end with .gz
	[readPositionTotalCounts, readPositionMethylCounts] = getMBias(methylationFileName, methylLetter, readLength)
	outputMBias(readPositionTotalCounts, readPositionMethylCounts, MBiasFileName)