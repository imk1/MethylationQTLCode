def getSNPInfo(SNPLine):
	# Get the location of a SNP
	if SNPLine == "":
		# At the end of the SNP file
		return ("", 0, "")
	SNPLineElements = SNPLine.strip().split("\t")
	return((SNPLineElements[0], int(SNPLineElements[1]), SNPLine))

def filterBothSNPFiles(SNPFileNameOne, SNPFileNameTwo, outputFileNameOne, outputFileNameTwo):
	# Filter two SNP files so that they have only the SNPs that are in both files
	# ASSUME THAT BOTH FILES ARE SORTED BY CHROMOSOME, POSITION
	# ASSUMES THAT SNPS ARE NOT REPEATED
	SNPFileOne = open(SNPFileNameOne)
	SNPFileTwo = open(SNPFileNameTwo)
	outputFileOne = open(outputFileNameOne, 'w+')
	outputFileTwo = open(outputFileNameTwo, 'w+')
	SNPTwoInfo = getSNPInfo(SNPFileTwo.readline())
	for line in SNPFileOne:
		# Iterate through the SNP files and record information for only the SNPs that are in both files
		SNPInfo = getSNPInfo(line)
		atEnd = False
		while (SNPInfo[0] > SNPTwoInfo[0]):
			# Go through the second SNP file until a SNP on the proper chromosome has been reached
			SNPTwoInfo = getSNPInfo(SNPFileTwo.readline())
			if SNPTwoInfo[0] == "":
				# At the end of the second SNP file, so stop
				atEnd = True
				break
		if atEnd == True:
			# At the end of the second SNP file, so stop
			break
		while (SNPInfo[0] == SNPTwoInfo[0]) and (SNPInfo[1] > SNPTwoInfo[1]):
			# Go through the second SNP file until a SNP at the proper location has been reached
			SNPTwoInfo = getSNPInfo(SNPFileTwo.readline())
			if SNPTwoInfo[0] == "":
				# At the end of the second SNP file, so stop
				atEnd = True
				break
		if atEnd == True:
			# At the end of the second SNP file, so stop
			break
		if (SNPInfo[0] == SNPTwoInfo[0]) and (SNPInfo[1] == SNPTwoInfo[1]):
			# The SNPs are at the same location, so record both
			outputFileOne.write(SNPInfo[2])
			outputFileTwo.write(SNPTwoInfo[2])
			SNPTwoInfo = getSNPInfo(SNPFileTwo.readline())
	SNPFileOne.close()
	SNPFileTwo.close()
	outputFileOne.close()
	outputFileTwo.close()

if __name__=="__main__":
   import sys
   SNPFileNameOne = sys.argv[1] 
   SNPFileNameTwo = sys.argv[2]
   outputFileNameOne = sys.argv[3]
   outputFileNameTwo = sys.argv[4]
   filterBothSNPFiles(SNPFileNameOne, SNPFileNameTwo, outputFileNameOne, outputFileNameTwo)