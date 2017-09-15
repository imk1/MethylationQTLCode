def getOverlapInfo(line):
	# Make a list of overlap information tuples, which are chromosome, position, from the file for overlap
	endOfFile = False
	if line == "":
		# At the end of the file
		endOfFile = True
		return [("", 0), endOfFile]
	
	lineElements = line.strip().split("\t")
	overlapInfo = (lineElements[0], round(float(lineElements[1]))) # SNP THAT IS AT n.5 IS APPROXIMATED TO BE AT n+1
	return [overlapInfo, endOfFile]
		
		
def getSNPOverlapPlusPlus(mQTLSNPsFileName, otherQTLsFileName, outputFileName, overlapColOne, overlapColTwo, overlapIndexFileName):
	# Get the mQTLs that are also some other kind of QTL
	# ASSUMES THAT BOTH FILES ARE SORTED BY CHROMOSOME, POSITION
	# RECORD INFORMATION IN THE SECOND FILE
	mQTLSNPsFile = open(mQTLSNPsFileName)
	[mQTLSNP, endOfmQTLFile] = getOverlapInfo(mQTLSNPsFile.readline())
	mQTLIndex = 0
	otherQTLsFile = open(otherQTLsFileName)
	outputFile = open(outputFileName, 'w+')
	overlapIndexFile = None
	if overlapIndexFileName != None:
		# Create a non-overlapping index file
		overlapIndexFile = open(overlapIndexFileName, 'w+')
	
	for line in otherQTLsFile:
		# Iterate through the other QTLs and record those that overlap with the mQTLs
		lineElements = line.strip().split()
		SNP = (lineElements[overlapColOne],  round(float(lineElements[overlapColTwo])))
		while mQTLSNP[0] < SNP[0]:
			# Go through the mQTL SNPs until one on the proper chromosome has been reached
			[mQTLSNP, endOfmQTLFile] = getOverlapInfo(mQTLSNPsFile.readline())
			mQTLIndex = mQTLIndex + 1
			if endOfmQTLFile == True:
				# At the end of the mQTL file, so stop
				break
		if endOfmQTLFile == True:
			# At the end of the mQTL file, so stop
			break
		
		while (mQTLSNP[1] < SNP[1]) and (mQTLSNP[0] == SNP[0]):
			# Go through the mQTL SNPs until one on the proper chromosome has been reached
			[mQTLSNP, endOfmQTLFile] = getOverlapInfo(mQTLSNPsFile.readline())
			mQTLIndex = mQTLIndex + 1
			if endOfmQTLFile == True:
				# At the end of the mQTL file, so stop
				break
		if endOfmQTLFile == True:
			# At the end of the mQTL file, so stop
			break
		
		if (mQTLSNP[1] == SNP[1]) and (mQTLSNP[0] == SNP[0]):
			# The other QTL (or genotype or other SNP info.) is an mQTL (or included in the first file), so record it and the other information in the same line
			outputFile.write(line)
			if overlapIndexFileName != None:
				# Record the mQTL index
				overlapIndexFile.write(str(mQTLIndex) + "\n")
	
	mQTLSNPsFile.close()
	otherQTLsFile.close()
	outputFile.close()
	if overlapIndexFileName != None:
		overlapIndexFile.close()
	
	
if __name__=="__main__":
	import sys
	import math
	mQTLSNPsFileName = sys.argv[1]
	otherQTLsFileName = sys.argv[2]
	outputFileName = sys.argv[3]
	overlapColOne = int(sys.argv[4]) # 0-INDEXED
	overlapColTwo = int(sys.argv[5])# 0-INDEXED
	overlapIndexFileName = None
	if len(sys.argv) > 6:
		# Include a non-overlapping index file name
		overlapIndexFileName = sys.argv[6]
	
	getSNPOverlapPlusPlus(mQTLSNPsFileName, otherQTLsFileName, outputFileName, overlapColOne, overlapColTwo, overlapIndexFileName)
