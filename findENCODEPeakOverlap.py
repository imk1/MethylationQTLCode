def getSNP(SNPLine):
	# Gets the SNP from a line with SNP information
	if SNPLine == "":
		return [("", 0), True]
	
	SNPLineElements = SNPLine.strip().split("\t")
	SNPPosition = (SNPLineElements[0], int(SNPLineElements[1]))
	return [SNPPosition, False]


def findENCODEPeakOverlap(ENCODEFileName, SNPFileName, outputFileName):
	# Determine which SNPs are in peaks in an ENCODE file
	# ASSUMES THAT ENCODEFile IS SORTED BY CHROMOSOME, START, END AND THAT SNPFile IS SORTED BY CHROMOSOME, POSITION
	ENCODEFile = gzip.open(ENCODEFileName)
	SNPFile = open(SNPFileName)
	outputFile = open(outputFileName, 'w+')
	
	[SNP, endOfSNPFile] = getSNP(SNPFile.readline())
	for line in ENCODEFile:
		# Iterate through the file with the ENCODE peaks and, for each SNP, record whether it is in a peak
		lineElements = line.strip().split("\t")
		while SNP[0] < lineElements[0]:
			# Go through the SNP file until a SNP on the proper chromosome is reached
			outputFile.write(SNP[0] + "\t" + str(SNP[1]) + "\t" + "0" + "\n")
			[SNP, endOfSNPFile] = getSNP(SNPFile.readline())
			if endOfSNPFile == True:
				# At the end of the file with SNPs, so stop
				break
		if endOfSNPFile == True:
			# At the end of the file with SNPs, so stop
			break
		
		while (SNP[0] == lineElements[0]) and (SNP[1] < int(lineElements[1])):
			# Go through the SNP file until a SNP that is not earlier in the chromosome than the peak is reached
			outputFile.write(SNP[0] + "\t" + str(SNP[1]) + "\t" + "0" + "\n")
			[SNP, endOfSNPFile] = getSNP(SNPFile.readline())
			if endOfSNPFile == True:
				# At the end of the file with SNPs, so stop
				break
		if endOfSNPFile == True:
			# At the end of the file with SNPs, so stop
			break
		
		while (SNP[0] == lineElements[0]) and ((SNP[1] >= int(lineElements[1])) and (SNP[1] <= int(lineElements[2]))):
			# Go through the SNP file until a SNP that is not earlier in the chromosome than the peak is reached
			outputFile.write(SNP[0] + "\t" + str(SNP[1]) + "\t" + "1" + "\n")
			[SNP, endOfSNPFile] = getSNP(SNPFile.readline())
			if endOfSNPFile == True:
				# At the end of the file with SNPs, so stop
				break
		if endOfSNPFile == True:
			# At the end of the file with SNPs, so stop
			break
	
	while endOfSNPFile == False:
		# Not at the end of the SNP file, so record 0 for each remaining SNP
		# ADDED MAY 2014 BUT NOT DEBUGGED
		outputFile.write(SNP[0] + "\t" + str(SNP[1]) + "\t" + "1" + "\n")
		[SNP, endOfSNPFile] = getSNP(SNPFile.readline())
	
	SNPFile.close()
	ENCODEFile.close()
	outputFile.close()

	
if __name__=="__main__":
	import sys
	import gzip
	ENCODEFileName = sys.argv[1]
	SNPFileName = sys.argv[2]
	outputFileName = sys.argv[3]
                        
	findENCODEPeakOverlap(ENCODEFileName, SNPFileName, outputFileName)