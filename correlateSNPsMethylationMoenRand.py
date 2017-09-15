def getInfo(line):
	# Get SNP or methylation information from a line of the file
	lineElements = line.strip().split("\t")
	location = (lineElements[0], int(lineElements[1]))
	
	vals = []
	for le in lineElements[2:]:
		# Iterate through the SNP or methylation values and add them to a vector
		vals.append(float(le))
	return [location, vals]
	

def getInfoRand(line):
	# Get SNP or methylation information from a line of the file
	lineElements = line.strip().split("\t")
	location = (lineElements[0], int(lineElements[1]))
	
	vals = []
	for le in lineElements[2:]:
		# Iterate through the SNP or methylation values and add them to a vector
		vals.append(float(le))
	random.shuffle(vals)
	return [location, vals]


def correlateSNPsMethylationMoen(methylFileName, SNPsFileName, distanceCutoff, outputFileName):
	# Correlate methylation statuses and SNPs for data from individual arrays
	methylFile = open(methylFileName)
	SNPsFile = open(SNPsFileName)
	outputFile = open(outputFileName, 'w+') # Will have SNP location, then methylation location, then correlation
	lastRelevantSNPsInfo = []
	currentSNPInfo = getInfo(SNPsFile.readline())
	atEnd = False
	
	for line in methylFile:
		# Iterate through the methylation file and find the correlation for each corresponding SNP
		methylInfo = getInfoRand(line)
		relevantSNPsInfo = []
		
		for SNPInfo in lastRelevantSNPsInfo:
			if (methylInfo[0][0] == SNPInfo[0][0]) and (abs(methylInfo[0][1] - SNPInfo[0][1]) <= distanceCutoff):
				# The current SNP close enough to the current methylation site, so include it
				relevantSNPsInfo.append(SNPInfo)
				[corr, pVal] = scipy.stats.pearsonr(SNPInfo[1], methylInfo[1])
				outputFile.write(SNPInfo[0][0] + "\t" + str(SNPInfo[0][1]) + "\t" + methylInfo[0][0] + "\t" + str(methylInfo[0][1]) + "\t" + str(corr) + "\n")
				
		if atEnd == False:
			# There are still more SNPs
			while methylInfo[0][0] > currentSNPInfo[0][0]:
				# The SNP chromosome is too early, so read the next SNP
				currentSNPInfo = getInfo(SNPsFile.readline())
			while methylInfo[0][1] - currentSNPInfo[0][1] > distanceCutoff:
				# The SNP is too early on the chromosome, so read the next SNP
				currentSNPInfo = getInfo(SNPsFile.readline())
			while (methylInfo[0][0] == currentSNPInfo[0][0]) and (abs(methylInfo[0][1] - currentSNPInfo[0][1]) <= distanceCutoff):
				# The current SNP close enough to the current methylation site, so include it
				relevantSNPsInfo.append(currentSNPInfo)
				[corr, pVal] = scipy.stats.pearsonr(currentSNPInfo[1], methylInfo[1])
				outputFile.write(currentSNPInfo[0][0] + "\t" + str(currentSNPInfo[0][1]) + "\t" + methylInfo[0][0] + "\t" + str(methylInfo[0][1]) + "\t" + str(corr) + "\n")
				SNPLine = SNPsFile.readline()
				if SNPLine != "":
					# There are still SNPs in the file, so see if the next SNP is close enough to the current SNP
					currentSNPInfo = getInfo(SNPLine)
				else:
					atEnd = True
					break
					
		lastRelevantSNPsInfo = relevantSNPsInfo
	methylFile.close()
	SNPsFile.close()
	outputFile.close()


if __name__=="__main__":
	import sys
	import scipy
	from scipy import stats
	import random
	methylFileName = sys.argv[1]
	SNPsFileName = sys.argv[2]
	distanceCutoff = int(sys.argv[3])
	outputFileName = sys.argv[4]

	correlateSNPsMethylationMoen(methylFileName, SNPsFileName, distanceCutoff, outputFileName)