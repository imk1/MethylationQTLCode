def getNextLDSNPsInfo(LDSNPsInfoLine):
	# Get the SNP locations and alleles for the next perfect LD SNPs
	if LDSNPsInfoLine == "":
		# At the end of the file
		SNPPairInfo = (0, 0, 0, 0, 0, 0, 0)
		return SNPPairInfo
	LDSNPsInfoLineElements = LDSNPsInfoLine.strip().split("\t")
	SNPOneLocation = int(LDSNPsInfoLineElements[1])
	SNPTwoLocation = int(LDSNPsInfoLineElements[5])
	LDInfo = [float(LDSNPsInfoLineElements[8]), float(LDSNPsInfoLineElements[9]), float(LDSNPsInfoLineElements[10])]
	# LDInfo[0] = r
	# LDInfo[1] = Probability first SNP is alternate allele given second SNP is alternate allele
	# LDInfo[2] = Probability first SNP is alternate allele given second SNP is reference allele
	SNPPairInfo = (SNPOneLocation, SNPTwoLocation, LDInfo)
	return SNPPairInfo
	
def updateSNPsToGroup(SNPPairInfo, firstSNPsToGroup, secondSNPsToGroup, LDInfoSNPsToGroup):
	# Update which SNPs should be grouped using a new pair of SNPs in possibly non-perfect LD
	if SNPPairInfo[0] in secondSNPsToGroup:#Y
		# The SNP at location SNPPairInfo[0] (call it SNP B) has already been grouped with some other SNP (call it SNP A).
		# Therefore, the SNP at location SNPPairInfo[1] (call it SNP C) is probably in possibly non-perfect LD with SNP A.
		# Because SNP A is earlier on the chromosome than SNP B (since SNPPairInfoList is sorted), SNPs A and C should already be listed for grouping.
		# Thus, listing SNPs B and C for grouping is probably redundant, so continue.
		# However, if the LD between SNPs C and A is not strong enough, then they will not have been listed together.
		# In this case, since SNP B has already been grouped with SNP A, SNP C should not be grouped with anything, so continue.
		return [firstSNPsToGroup, secondSNPsToGroup, LDInfoSNPsToGroup]
	if SNPPairInfo[1] in secondSNPsToGroup:#Y
		# The SNP at location SNPPairInfo[1] (call it SNP C) has already been grouped with some other SNP (call it SNP A).
		# Therefore, the SNP at location SNPPairInfo[0] (call it SNP B) is probably also in possibly non-perfect LD with SNP A.
		# Because SNP A is earlier on the chromosome than SNP B (since SNPPairInfoList is sorted), SNPs A and B should already be listed for grouping.
		# Thus, listing SNPs B and C for grouping is probably redundant, so continue.
		# However, if the LD between SNPs B and A is not strong enough, then they will not have been listed together (TRUE because of previous condition).
		# In this case, since SNP C has already been grouped with SNP A, SNP B should not be grouped with anything, so continue.
		return [firstSNPsToGroup, secondSNPsToGroup, LDInfoSNPsToGroup]
	firstSNPsToGroup.append(SNPPairInfo[0])
	secondSNPsToGroup.append(SNPPairInfo[1])
	LDInfoSNPsToGroup.append(SNPPairInfo[2])
	return [firstSNPsToGroup, secondSNPsToGroup, LDInfoSNPsToGroup]
	
def createRevisedSNPVecsNonPerfect(SNPLocationVec, SNPVec, firstSNPsToGroup, secondSNPsToGroup, LDInfoSNPsToGroup):
	# Create the revised SNP vectors
	SNPLocationVecModified = []
	SNPVecModified = []
	for i in range(len(SNPLocationVec)):
		# Iterate through the SNP locations and modify those and the corresponding alleles that are in secondSNPsToGroup
		if SNPLocationVec[i] in secondSNPsToGroup:#Y
			# The current SNP location is in secondSNPsToGroup
			SNPLocationIndex = secondSNPsToGroup.index(SNPLocationVec[i])
			SNPLocationVecModified.append(firstSNPsToGroup[SNPLocationIndex])
			if SNPVec[i] == 0:#Y
				# Append the probability that the SNP in the first group is at the alternate allele given the second SNP is the reference allele
				SNPVecModified.append(LDInfoSNPsToGroup[SNPLocationIndex][2])
			else:#Y
				# Append the probability that the SNP in the first group is at the alternate allele given the second SNP is the alternate allele
				SNPVecModified.append(LDInfoSNPsToGroup[SNPLocationIndex][1])
		else:#Y
			SNPLocationVecModified.append(SNPLocationVec[i])
			SNPVecModified.append(SNPVec[i])
	return [SNPLocationVecModified, SNPVecModified]
	
def reviseSNPVecsNonPerfect(SNPLocationVec, SNPVec, SNPPairInfoList, perfectLDSNPsFile, distanceCutoff, atLDInfoFileEnd, rCutoff):
	# Modify the vectors of SNP locations and SNP alleles to group SNPs that share a CpG
	firstSNP = min(SNPLocationVec)
	lastSNP = max(SNPLocationVec)
	SNPsTooLate = False
	firstSNPsToGroup = []
	secondSNPsToGroup = []
	LDInfoSNPsToGroup = []
	for SNPPairInfo in SNPPairInfoList:
		# Iterate through the SNPs in perfect LD and find those that are associated with the current CpG
		if SNPPairInfo[0] < firstSNP - distanceCutoff:
			# The current pair of SNPs is too early on the chromosome, so remove it
			SNPPairInfoList.remove(SNPPairInfo)
			continue
		if SNPPairInfo[0] > lastSNP:
			# The current pair of SNPs is too late on the chromosome, so stop
			SNPsTooLate = True
			break
		if (SNPPairInfo[0] in SNPLocationVec) and (SNPPairInfo[1] in SNPLocationVec):#Y
			# The current pair of SNPs should be grouped
			[firstSNPsToGroup, secondSNPsToGroup, LDInfoSNPsToGroup] = updateSNPsToGroup(SNPPairInfo, firstSNPsToGroup, secondSNPsToGroup, LDInfoSNPsToGroup)
	while (SNPsTooLate == False) and (atLDInfoFileEnd == False):
		# Add more SNP pairs to the list until the SNP is past the last SNP that is associated with the current CpG
		SNPPairInfo = getNextLDSNPsInfo(perfectLDSNPsFile.readline())
		if SNPPairInfo[0] == 0:
			# At the end of the LD file, so stop
			atLDInfoFileEnd = True
			print SNPLocationVec[0]
			break
		if abs(SNPPairInfo[2][0]) >= rCutoff:#Y
				# The correlation between the SNPs is sufficiently strong that the SNPs should be grouped
				SNPPairInfoList.append(SNPPairInfo)
				if (SNPPairInfo[0] in SNPLocationVec) and (SNPPairInfo[1] in SNPLocationVec):#Y
					# The current pair of SNPs should be grouped (allowed only if the correlation between the genotypes is sufficiently high)
					[firstSNPsToGroup, secondSNPsToGroup, LDInfoSNPsToGroup] = updateSNPsToGroup(SNPPairInfo, firstSNPsToGroup, secondSNPsToGroup, LDInfoSNPsToGroup)
		if SNPPairInfo[0] > lastSNP:
			# The current pair of SNPs is too late on the chromosome, so stop
			SNPsTooLate = True
	# There should be no SNP locations in both firstSNPsToGroup and secondSNPsToGroup, and each SNP location in secondSNPsToGroup should be listed only once
	# SNP locations in secondSNPsToGroup will be changed along with their alleles to match the SNP with the location in the same place in firstSNPsToGroup
	[SNPLocationVecModified, SNPVecModified] = createRevisedSNPVecsNonPerfect(SNPLocationVec, SNPVec, firstSNPsToGroup, secondSNPsToGroup, LDInfoSNPsToGroup)
	return [SNPLocationVecModified, SNPVecModified, SNPPairInfoList, atLDInfoFileEnd]
	
def recordRevisedSNPMethyl(readNameVec, chromName, SNPLocationVec, SNPVec, methylLocationVec, methylVec, outputFile):
	# Record the modified SNP, methylation information for the current CpG to the output file
	for i in range(len(readNameVec)):
		# Iterate through all of the reads for the current CpG and record all of the SNP, methylation information
		# If there is more than 1 SNP on a read that is in perfect LD, record the information for only the 1st SNP so as not to double-count
		readName = readNameVec[i]
		SNPLocation = SNPLocationVec[i]
		previousReadIndexes = [readIndex for readIndex,rn in enumerate(readNameVec[0:i]) if rn == readName]
		readSNPMethylRecorded = False
		for pri in previousReadIndexes:
			# Iterate through the occurrences of this read and determine whether the SNP location post-LD-grouping for an occurrences is the same
			if SNPLocationVec[pri] == SNPLocation:#Y
				# The read, SNP, methylation combination has already been recorded
				readSNPMethylRecorded = True
				break
		if readSNPMethylRecorded == False:#Y
			# The current read, SNP, methylation combination has not yet been recorded, so record it
			outputFile.write(readName + "\t" + chromName + "\t" + str(SNPLocation) + "\t" + str(SNPVec[i]) + "\t" + chromName + "\t" + str(methylLocationVec[i]) + "\t" + str(methylVec[i]) + "\n") # No longer recording sample information

def groupNonPerfectLDSNPsMethyl(SNPMethylFileName, LDInfoSNPsFileName, chromName, outputFileName, distanceCutoff, rCutoff):
	# For each C, group all SNPs that are associated with that C using LD, where the SNP that is kept is the SNP with the most reads.
	# ASSUMES THAT SNPMethylFile IS SORTED BY METH. CHR., METH. POS., SNP CHR., SNP POS. AND LDInfoSNPsFile IS SORTED BY SNP 1 POS., SNP 2 POS.
	# ASSUMES THAT THE FIRST ALLELE FOR SNP 1 POSITION IS THE REFERENCE ALLELE AND SNP 1 POS. < SNP 2 POS.
	# ASSUMES THAT ALL SNPs IN SNPMethylFile ARE ON THE SAME CHROMOSOME chromName, WHICH IS THE CHROMOSOME FOR LDInfoSNPsFile
	LDInfoSNPsFile = open(LDInfoSNPsFileName)
	SNPPairInfoList = [] # Will be sorted by SNP 1 position, SNP 2 position
	SNPPairInfo = getNextLDSNPsInfo(LDInfoSNPsFile.readline())
	while abs(SNPPairInfo[2][0]) < rCutoff:
		# Iterate through the SNP pairs until a pair with sufficiently tight LD has been found
		SNPPairInfo = getNextLDSNPsInfo(LDInfoSNPsFile.readline())
	SNPPairInfoList.append(SNPPairInfo)
	SNPMethylFile = gzip.open(SNPMethylFileName, 'rb')
	outputFile = gzip.open(outputFileName, 'w+')
	lastMethylLocation = 0
	readNameVec = []
	SNPLocationVec = []
	SNPVec = []
	methylLocationVec = []
	methylVec = []
	atLDInfoFileEnd = False
	for line in SNPMethylFile:
		# Iterate through the lines of the SNP methylation file and, for each C, group the SNPs that are in perfect LD
		lineElements = line.strip().split("\t")
		readName = lineElements[0]
		currentSNPLocation = int(lineElements[2])
		currentMethylLocation = int(lineElements[5])
		if (currentMethylLocation != lastMethylLocation) and (lastMethylLocation != 0):#Y
			# At a new methylation location, so group the SNPs for the previous one using LD information (also not at the beginning of the file)
			[SNPLocationVecModified, SNPVecModified, SNPPairInfoList, atLDInfoFileEnd] = reviseSNPVecsNonPerfect(SNPLocationVec, SNPVec, SNPPairInfoList, LDInfoSNPsFile, distanceCutoff, atLDInfoFileEnd, rCutoff)
			recordRevisedSNPMethyl(readNameVec, chromName, SNPLocationVecModified, SNPVecModified, methylLocationVec, methylVec, outputFile)
			readNameVec = []
			SNPLocationVec = []
			SNPVec = []
			methylLocationVec = []
			methylVec = []
			lastMethylLocation = currentMethylLocation
		elif lastMethylLocation == 0:
			# At the beginning of the file, so update the methylation location
			lastMethylLocation = currentMethylLocation
		readNameVec.append(readName)
		SNPLocationVec.append(currentSNPLocation)
		SNPVec.append(int(lineElements[3]))
		methylLocationVec.append(currentMethylLocation)
		methylVec.append(int(lineElements[6]))
	[SNPLocationVecModified, SNPVecModified, SNPPairInfoList, atLDInfoFileEnd] = reviseSNPVecsNonPerfect(SNPLocationVec, SNPVec, SNPPairInfoList, LDInfoSNPsFile, distanceCutoff, atLDInfoFileEnd, rCutoff)
	recordRevisedSNPMethyl(readNameVec, chromName, SNPLocationVecModified, SNPVecModified, methylLocationVec, methylVec, outputFile)
	LDInfoSNPsFile.close()
	SNPMethylFile.close()
	outputFile.close()
	
if __name__=="__main__":
	import sys
	import gzip
	SNPMethylFileName = sys.argv[1] # Should end with .gz
	LDInfoSNPsFileName = sys.argv[2]
	chromName = sys.argv[3]
	outputFileName = sys.argv[4] # Should end with .gz
	distanceCutoff = int(sys.argv[5])
	rCutoff = float(sys.argv[6])
	groupNonPerfectLDSNPsMethyl(SNPMethylFileName, LDInfoSNPsFileName, chromName, outputFileName, distanceCutoff, rCutoff)