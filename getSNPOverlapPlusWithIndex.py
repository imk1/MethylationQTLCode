def getSNP(line):
	# Make a list of SNP tuples, which are SNP, location, from the file of SNPs
	endOfFile = False
	if line == "":
		# At the end of the file
		endOfFile = True
		return [("", 0), endOfFile]
	
	lineElements = line.strip().split()
	SNP = (lineElements[0], int(math.floor(float(lineElements[1]))))
	return [SNP, endOfFile]
		
		
def getSNPOverlapPlusWithIndex(mQTLSNPsFileName, otherQTLsFileName, outputFileName):
	# Get the mQTLs that are also some other kind of QTL and those mQTLs indexes in the mQTL file
	# INDEXES ARE 1-INDEXED
	# ASSUMES THAT BOTH FILES ARE SORTED BY CHROMOSOME, POSITION
	mQTLSNPsFile = open(mQTLSNPsFileName)
	[mQTLSNP, endOfmQTLFile] = getSNP(mQTLSNPsFile.readline())
	index = 1
	otherQTLsFile = open(otherQTLsFileName)
	outputFile = open(outputFileName, 'w+')
	
	for line in otherQTLsFile:
		# Iterate through the other QTLs and record those that overlap with the mQTLs
		lineElements = line.strip().split()
		SNP = (lineElements[0],  int(math.floor(float(lineElements[1]))))
		while mQTLSNP[0] < SNP[0]:
			# Go through the mQTL SNPs until one on the proper chromosome has been reached
			[mQTLSNP, endOfmQTLFile] = getSNP(mQTLSNPsFile.readline())
			index = index + 1
			if endOfmQTLFile == True:
				# At the end of the mQTL file, so stop
				break
		if endOfmQTLFile == True:
			# At the end of the mQTL file, so stop
			break
		
		while (mQTLSNP[1] < SNP[1]) and (mQTLSNP[0] == SNP[0]):
			# Go through the mQTL SNPs until one on the proper chromosome has been reached
			[mQTLSNP, endOfmQTLFile] = getSNP(mQTLSNPsFile.readline())
			index = index + 1
			if endOfmQTLFile == True:
				# At the end of the mQTL file, so stop
				break
		if endOfmQTLFile == True:
			# At the end of the mQTL file, so stop
			break
		
		if (mQTLSNP[1] == SNP[1]) and (mQTLSNP[0] == SNP[0]):
			# The other QTL is an mQTL, so record it
			outputFile.write(SNP[0] + "\t" + str(SNP[1]) + "\t" + str(index) + "\n")
	
	mQTLSNPsFile.close()
	otherQTLsFile.close()
	outputFile.close()
	
	
if __name__=="__main__":
	import sys
	import math
	mQTLSNPsFileName = sys.argv[1] # INDEXES FOR THIS FILE WILL BE RECORDED
	otherQTLsFileName = sys.argv[2]
	outputFileName = sys.argv[3]
	
	getSNPOverlapPlusWithIndex(mQTLSNPsFileName, otherQTLsFileName, outputFileName)
