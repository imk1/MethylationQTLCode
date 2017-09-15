def getSNPs(SNPFileName):
	# Make a list of SNP tuples, which are SNP, location, from the file of SNPs
	SNPs = []
	SNPFile = open(SNPFileName)
	
	for line in SNPFile:
		# Iterate through the SNPs in the file and add each to the list
		lineElements = line.strip().split("\t")
		SNPs.append((lineElements[0], int(math.floor(float(lineElements[1])))))
	
	SNPFile.close()
	return SNPs
		
		
def getSNPOverlap(mQTLSNPs, otherQTLsFileName, outputFileName):
	# Get the mQTLs that are also some other kind of QTL
	otherQTLsFile = open(otherQTLsFileName)
	outputFile = open(outputFileName, 'w+')
	
	for line in otherQTLsFile:
		# Iterate through the other QTLs and record those that overlap with the mQTLs
		lineElements = line.strip().split("\t")
		SNP = (lineElements[0],  int(math.floor(float(lineElements[1]))))
		if SNP in mQTLSNPs:
			# The other QTL is an mQTL, so record it
			outputFile.write(SNP[0] + "\t" + str(SNP[1]) + "\n")
			
	otherQTLsFile.close()
	outputFile.close()
	
	
if __name__=="__main__":
	import sys
	import math
	mQTLSNPsFileName = sys.argv[1]
	otherQTLsFileName = sys.argv[2]
	outputFileName = sys.argv[3]
	
	mQTLSNPs = getSNPs(mQTLSNPsFileName)
	getSNPOverlap(mQTLSNPs, otherQTLsFileName, outputFileName)