def getOverlapInfo(line):
	# Make a list of overlap information tuples, which are chromosome, position, from the file for overlap
	endOfFile = False
	if line == "":
		# At the end of the file
		endOfFile = True
		return [("", 0), endOfFile]
	
	lineElements = line.strip().split("\t")
	overlapInfo = (lineElements[0], int(lineElements[1]))
	return [overlapInfo, endOfFile]
		
		
def getSNPOverlapPlusPlusgzip(mQTLSNPsFileName, otherQTLsFileName, outputFileName, overlapColOne, overlapColTwo, headerPresent):
	# Get the mQTLs that are also some other kind of QTL
	# ASSUMES THAT BOTH FILES ARE SORTED BY CHROMOSOME, POSITION
	# RECORD INFORMATION IN THE SECOND FILE
	mQTLSNPsFile = open(mQTLSNPsFileName)
	[mQTLSNP, endOfmQTLFile] = getOverlapInfo(mQTLSNPsFile.readline())
	otherQTLsFile = gzip.open(otherQTLsFileName)
	outputFile = gzip.open(outputFileName, 'w+')
	if headerPresent == 1:
		# otherQTLsFile has a header, so remove it
		otherQTLsFile.readline()
	
	for line in otherQTLsFile:
		# Iterate through the other QTLs and record those that overlap with the mQTLs
		lineElements = line.strip().split()
		SNP = (lineElements[overlapColOne],  int(lineElements[overlapColTwo]))
		while mQTLSNP[0] < SNP[0]:
			# Go through the mQTL SNPs until one on the proper chromosome has been reached
			[mQTLSNP, endOfmQTLFile] = getOverlapInfo(mQTLSNPsFile.readline())
			if endOfmQTLFile == True:
				# At the end of the mQTL file, so stop
				break
		if endOfmQTLFile == True:
			# At the end of the mQTL file, so stop
			break
		
		while (mQTLSNP[1] < SNP[1]) and (mQTLSNP[0] == SNP[0]):
			# Go through the mQTL SNPs until one on the proper chromosome has been reached
			[mQTLSNP, endOfmQTLFile] = getOverlapInfo(mQTLSNPsFile.readline())
			if endOfmQTLFile == True:
				# At the end of the mQTL file, so stop
				break
		if endOfmQTLFile == True:
			# At the end of the mQTL file, so stop
			break
		
		if (mQTLSNP[1] == SNP[1]) and (mQTLSNP[0] == SNP[0]):
			# The other QTL (or genotype or other SNP info.) is an mQTL (or included in the first file), so record it and the other information in the same line
			outputFile.write(line)
	
	mQTLSNPsFile.close()
	otherQTLsFile.close()
	outputFile.close()
	
	
if __name__=="__main__":
	import sys
	import math
	import gzip
	mQTLSNPsFileName = sys.argv[1]
	otherQTLsFileName = sys.argv[2] # Should end with .gz
	outputFileName = sys.argv[3] # Should end with .gz
	overlapColOne = int(sys.argv[4]) # 0-INDEXED
	overlapColTwo = int(sys.argv[5])# 0-INDEXED
	headerPresent = int(sys.argv[6]) # 1 means header is present in otherQTLsFile
	
	getSNPOverlapPlusPlusgzip(mQTLSNPsFileName, otherQTLsFileName, outputFileName, overlapColOne, overlapColTwo, headerPresent)