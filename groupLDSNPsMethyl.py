def getNextPerfectLDSNPs(perfectLDSNPsLine):
	# Get the SNP locations and alleles for the next perfect LD SNPs
	if perfectLDSNPsLine == "":
		# At the end of the file
		SNPPairInfo = (0, 0, 0)
		return SNPPairInfo
	perfectLDSNPsLineElements = perfectLDSNPsLine.strip().split("\t")
	SNPOneLocation = int(perfectLDSNPsLineElements[1])
	SNPTwoLocation = int(perfectLDSNPsLineElements[5])
	LDInfo = float(perfectLDSNPsLineElements[8])
	SNPPairInfo = (SNPOneLocation, SNPTwoLocation, LDInfo)
	return SNPPairInfo
	
def updateSNPsToGroup(SNPPairInfo, firstSNPsToGroup, secondSNPsToGroup, LDInfoSNPsToGroup):
	# Update which SNPs should be grouped using a new pair of SNPs in perfect LD
	if SNPPairInfo[0] in secondSNPsToGroup:
		# The SNP at location SNPPairInfo[0] (call it SNP B) has already been grouped with some other SNP (call it SNP A).
		# Therefore, the SNP at location SNPPairInfo[1] (call it SNP C) must also be in perfect LD with SNP A.
		# Because SNP A is earlier on the chromosome than SNP B (since SNPPairInfoList is sorted), SNPs A and C must already be listed for grouping.
		# Thus, listing SNPs B and C for grouping is redundant, so continue.
		return [firstSNPsToGroup, secondSNPsToGroup, LDInfoSNPsToGroup]
	if SNPPairInfo[1] in secondSNPsToGroup:
		# The SNP at location SNPPairInfo[1] (call it SNP C) has already been grouped with some other SNP (call it SNP A).
		# Therefore, the SNP at location SNPPairInfo[0] (call it SNP B) must also be in perfect LD with SNP A.
		# Because SNP A is earlier on the chromosome than SNP B (since SNPPairInfoList is sorted), SNPs A and B must already be listed for grouping.
		# Thus, listing SNPs B and C for grouping is redundant, so continue.
		return [firstSNPsToGroup, secondSNPsToGroup, LDInfoSNPsToGroup]
	firstSNPsToGroup.append(SNPPairInfo[0])
	secondSNPsToGroup.append(SNPPairInfo[1])
	LDInfoSNPsToGroup.append(SNPPairInfo[2])
	return [firstSNPsToGroup, secondSNPsToGroup, LDInfoSNPsToGroup]
	
def createRevisedSNPVecs(SNPLocationVec, SNPVec, firstSNPsToGroup, secondSNPsToGroup, LDInfoSNPsToGroup):
	# Create the revised SNP vectors
	SNPLocationVecModified = []
	SNPVecModified = []
	for i in range(len(SNPLocationVec)):
		# Iterate through the SNP locations and modify those and the corresponding alleles that are in secondSNPsToGroup
		if SNPLocationVec[i] in secondSNPsToGroup:
			# The current SNP location is in secondSNPsToGroup
			SNPLocationIndex = secondSNPsToGroup.index(SNPLocationVec[i])
			SNPLocationVecModified.append(firstSNPsToGroup[SNPLocationIndex])
			if LDInfoSNPsToGroup[SNPLocationIndex] == 1:
				# The reference allele of the current SNP corresponds to the reference allele of the SNP that is in perfect LD
				SNPVecModified.append(SNPVec[i])
			elif SNPVec[i] == 0:
				# Change the allele to a 1 because the reference allele corresponds to the alternate allele of the other SNP
				SNPVecModified.append(1)
			else:
				# Change the allele to a 0 because the alternate allele corresponds to the reference allele of the other SNP
				SNPVecModified.append(0)
		else:
			SNPLocationVecModified.append(SNPLocationVec[i])
			SNPVecModified.append(SNPVec[i])
	return [SNPLocationVecModified, SNPVecModified]
	
def reviseSNPVecs(SNPLocationVec, SNPVec, SNPPairInfoList, perfectLDSNPsFile, distanceCutoff, atPerfectLDFileEnd):
	# Modify the vectors of SNP locations and SNP alleles to group SNPs that are in perfect LD
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
		if (SNPPairInfo[0] in SNPLocationVec) and (SNPPairInfo[1] in SNPLocationVec):
			# The current pair of SNPs should be grouped
			[firstSNPsToGroup, secondSNPsToGroup, LDInfoSNPsToGroup] = updateSNPsToGroup(SNPPairInfo, firstSNPsToGroup, secondSNPsToGroup, LDInfoSNPsToGroup)
	while (SNPsTooLate == False) and (atPerfectLDFileEnd == False):
		# Add more SNP pairs to the list until the SNP is past the last SNP that is associated with the current CpG
		SNPPairInfo = getNextPerfectLDSNPs(perfectLDSNPsFile.readline())
		if SNPPairInfo[0] == 0:
			# At the end of the perfect LD file, so stop
			atPerfectLDFileEnd = True
			break
		SNPPairInfoList.append(SNPPairInfo)
		if SNPPairInfo[0] > lastSNP:
			# The current pair of SNPs is too late on the chromosome, so stop
			SNPsTooLate = True
		elif (SNPPairInfo[0] in SNPLocationVec) and (SNPPairInfo[1] in SNPLocationVec):
			# The current pair of SNPs should be grouped
			[firstSNPsToGroup, secondSNPsToGroup, LDInfoSNPsToGroup] = updateSNPsToGroup(SNPPairInfo, firstSNPsToGroup, secondSNPsToGroup, LDInfoSNPsToGroup)
	# There should be no SNP locations in both firstSNPsToGroup and secondSNPsToGroup, and each SNP location in secondSNPsToGroup should be listed only once
	# SNP locations in secondSNPsToGroup will be changed along with their alleles to match the SNP with the location in the same place in firstSNPsToGroup
	[SNPLocationVecModified, SNPVecModified] = createRevisedSNPVecs(SNPLocationVec, SNPVec, firstSNPsToGroup, secondSNPsToGroup, LDInfoSNPsToGroup)
	return [SNPLocationVecModified, SNPVecModified, SNPPairInfoList, atPerfectLDFileEnd]
	
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
			if SNPLocationVec[pri] == SNPLocation:
				# The read, SNP, methylation combination has already been recorded
				readSNPMethylRecorded = True
				break
		if readSNPMethylRecorded == False:
			# The current read, SNP, methylation combination has not yet been recorded, so record it
			outputFile.write(readName + "\t" + chromName + "\t" + str(SNPLocation) + "\t" + str(SNPVec[i]) + "\t" + chromName + "\t" + str(methylLocationVec[i]) + "\t" + str(methylVec[i]) + "\n") # No longer recording sample information

def groupLDSNPsMethyl(SNPMethylFileName, perfectLDSNPsFileName, chromName, outputFileName, distanceCutoff):
	# For each C, consider all SNPs that are associated with that C.
	# Group all SNPs that are in perfect LD by converting the SNP location to the 1st SNP's location and the allele to the corresponding allele for the 1st SNP.
	# ASSUMES THAT SNPMethylFile IS SORTED BY METH. CHR., METH. POS., SNP CHR., SNP POS. AND perfectLDSNPsFile IS SORTED BY SNP 1 POS., SNP 2 POS.
	# ASSUMES THAT THE FIRST ALLELE FOR SNP 1 POSITION IS THE REFERENCE ALLELE AND SNP 1 POS. < SNP 2 POS.
	# ASSUMES THAT ALL SNPs IN SNPMethylFile ARE ON THE SAME CHROMOSOME chromName, WHICH IS THE CHROMOSOME FOR perfectLDSNPsFile
	perfectLDSNPsFile = open(perfectLDSNPsFileName)
	SNPPairInfoList = [] # Will be sorted by SNP 1 position, SNP 2 position
	SNPPairInfo = getNextPerfectLDSNPs(perfectLDSNPsFile.readline())
	SNPPairInfoList.append(SNPPairInfo)
	SNPMethylFile = gzip.open(SNPMethylFileName, 'rb')
	outputFile = gzip.open(outputFileName, 'w+')
	lastMethylLocation = 0
	readNameVec = []
	SNPLocationVec = []
	SNPVec = []
	methylLocationVec = []
	methylVec = []
	atPerfectLDFileEnd = False
	for line in SNPMethylFile:
		# Iterate through the lines of the SNP methylation file and, for each C, group the SNPs that are in perfect LD
		lineElements = line.strip().split("\t")
		readName = lineElements[0]
		currentSNPLocation = int(lineElements[2])
		currentMethylLocation = int(lineElements[5])
		if (currentMethylLocation != lastMethylLocation) and (lastMethylLocation != 0):
			# At a new methylation location, so find the group the SNPs in LD for the previous one (also not at the beginning of the file)
			[SNPLocationVecModified, SNPVecModified, SNPPairInfoList, atPerfectLDFileEnd] = reviseSNPVecs(SNPLocationVec, SNPVec, SNPPairInfoList, perfectLDSNPsFile, distanceCutoff, atPerfectLDFileEnd)
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
	[SNPLocationVecModified, SNPVecModified, SNPPairInfoList, atPerfectLDFileEnd] = reviseSNPVecs(SNPLocationVec, SNPVec, SNPPairInfoList, perfectLDSNPsFile, distanceCutoff, atPerfectLDFileEnd)
	recordRevisedSNPMethyl(readNameVec, chromName, SNPLocationVecModified, SNPVecModified, methylLocationVec, methylVec, outputFile)
	perfectLDSNPsFile.close()
	SNPMethylFile.close()
	outputFile.close()
	
if __name__=="__main__":
	import sys
	import gzip
	SNPMethylFileName = sys.argv[1] # Should end with .gz
	perfectLDSNPsFileName = sys.argv[2]
	chromName = sys.argv[3]
	outputFileName = sys.argv[4] # Should end with .gz
	distanceCutoff = int(sys.argv[5])
	groupLDSNPsMethyl(SNPMethylFileName, perfectLDSNPsFileName, chromName, outputFileName, distanceCutoff)