def getLocations(locationsFileName):
	# Get the locations from a file
	locationList = []
	locationsFile = open(locationsFileName)
	
	for line in locationsFile:
		# Iterate through the locations and add each to the list
		lineElements = line.split("\t")
		location = (lineElements[0], int(lineElements[1]))
		locationList.append(location)
		
	locationsFile.close()
	return locationList
	

def processLineMethyl(line, methylLetter, isTop, CGDist):
	# Get the informtion for a line from the methylation file
	if line == "":
		# At the end of the file
		return ["", "", 0, -1]

	lineElements = line.split("\t")
	read = lineElements[0][0:-2] # Removing the last 2 characters so that pairs are considered part of the same read
	chrom = lineElements[2]
	position = int(lineElements[3])
	if isTop == False:
		# On the bottom strand, so the CpG/CHG starts CGDist positions earlier
		position = position - CGDist
	call = lineElements[4].strip()
	state = 0
	if call == methylLetter:
		# The C is methylated
		state = 1
	return [read, chrom, position, state]


def processLineSNP(line):
	# Get the informtion for a line from the methylation file
	if line == "":
		# At the end of the file
		return ["", "", 0, -1]

	lineElements = line.split("\t")
	read = lineElements[0][0:-2] # Removing the last 2 characters so that pairs are considered part of the same read
	chrom = lineElements[2]
	position = int(lineElements[3])
	statePM = lineElements[1]
	state = 0
	if statePM == "-":
		# The SNP is the alternate allele, so make the state 1
		state = 1
	return [read, chrom, position, state]


def getSNPMethylReadsPlusPlus(bismarkSNPFileName, bismarkMethylationFileName, regionsWithSNPs, methylLetter, CGDist, sampleNum, outputFileName):
	# Find the reads with SNPs and Cs, while EXCLUDING CpGs THAT CONTAIN SNPs
	# ASSUMES THAT BOTH SNP AND METHYLATION FILES ARE SORTED BY READ NAME
	# ASSUMES THAT THE TOP STRAND FILE (with CpGs) HAS "OT" AT POSITIONS 4 AND 5 (0-indexed) AND THE BOTTOM STRAND FILE (with GpCs) HAS "OB"
	# Output file will have the following information for each (SNP, C in the same read):
	# 1.  Read Name
	# 2.  SNP chromosome
	# 3.  SNP position in chromosome
	# 4.  1 or 0 indicating allele of SNP
	# 5.  Methylation chromosome
	# 6.  Methylation position in chromosome
	# 7.  1 or 0 indicating whether C is methylated (1 means methylated)
	# 8.  Number indicating which file (replicate and strand) read came from
	bismarkSNPFile = open(bismarkSNPFileName)
	isTop = True
	bismarkMethylationFileNameElements = bismarkMethylationFileName.split("/") # Only considering last part in file name
	if bismarkMethylationFileNameElements[-1][4:6] == "OB":
		# On the bottom strand
		isTop = False
	print isTop
	bismarkMethylationFile = gzip.open(bismarkMethylationFileName, 'rb')
	outputFile = gzip.open(outputFileName, 'wb')
	[methylRead, methylChrom, methylPosition, methylState] = processLineMethyl(bismarkMethylationFile.readline(), methylLetter, isTop, CGDist)
	CInfo = []
	lastRead = ""
	SNPPositionsOnRead = []
	atEnd = False

	count = 0
	for line in bismarkSNPFile:
		# Iterate through the SNPs and find those that are on reads with C's
		count = count + 1
		if count % 500 == 0:
			print count
		[SNPRead, SNPChrom, SNPPosition, SNPState] = processLineSNP(line)	
		if SNPRead == lastRead:
			# The SNP is on the same read as the previous SNP
			if SNPPosition in SNPPositionsOnRead:
				# The SNP has been called twice (because it was picked up in both pair members), so skip it
				continue

 			for Ci in CInfo:
				# Iterate through the C information from the last SNP and output it for the current SNP (C*Gs with SNPs were not added to CInfo)
				outputFile.write(SNPRead + "\t" + SNPChrom + "\t" + str(SNPPosition) + "\t" + str(SNPState) + "\t" + Ci[0] + "\t" + str(Ci[1]) + "\t" + str(Ci[2]) + "\t" + str(sampleNum) + "\n")
			SNPPositionsOnRead.append(SNPPosition)
			continue

		if atEnd == True:
			# Reached the end of the methylation file on the last iteration and at a new read, so stop
			break

		SNPPositionsOnRead = []
		CInfo = []
		while methylRead < SNPRead:
			# Go through the methylation file until the reads match or the methylation read passes the SNP read
			[methylRead, methylChrom, methylPosition, methylState] = processLineMethyl(bismarkMethylationFile.readline(), methylLetter, isTop, CGDist)
			if methylRead == "":
				# At the end of the methylation file, so stop
				atEnd = True
				break
		if atEnd == True:
			# At the end of the methylation file, so stop
			break

		while methylRead == SNPRead:
			# Go through the methylation data that is on the same read as the SNP and output the information
			if (methylChrom, methylPosition) not in regionsWithSNPs:
				# The current C*G does not have a SNP
				outputFile.write(SNPRead + "\t" + SNPChrom + "\t" + str(SNPPosition) + "\t" + str(SNPState) + "\t" + methylChrom + "\t" + str(methylPosition) + "\t" + str(methylState) + "\t" + str(sampleNum) + "\n")
				CInfo.append([methylChrom, methylPosition, methylState])
			[methylRead, methylChrom, methylPosition, methylState] = processLineMethyl(bismarkMethylationFile.readline(), methylLetter, isTop, CGDist)
			if methylRead == "":
				# At the end of the methylation file, so stop
				atEnd = True
				break
		lastRead = SNPRead
		SNPPositionsOnRead.append(SNPPosition)

	bismarkSNPFile.close()
	bismarkMethylationFile.close()
	outputFile.close()


if __name__=="__main__":
	import sys
	import gzip
	bismarkSNPFileName = sys.argv[1]
	bismarkMethylationFileName = sys.argv[2] # Should end with .gz
	regionsWithSNPsFileName = sys.argv[3]
	methylLetter = sys.argv[4]
	CGDist = int(sys.argv[5]) # 1 for CpG, 2 for CHG, UNKNOWN FOR CHH
	sampleNum = sys.argv[6]
	outputFileName = sys.argv[7] # Should end with .gz

	regionsWithSNPs = getLocations(regionsWithSNPsFileName)
	getSNPMethylReadsPlusPlus(bismarkSNPFileName, bismarkMethylationFileName, regionsWithSNPs, methylLetter, CGDist, sampleNum, outputFileName)
