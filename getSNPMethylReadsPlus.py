def processLineMethyl(line, methylLetter, isTop, CGDist):
	# Get the informtion for a line from the methylation file
	if line == "":
		# At the end of the file
		return ["", "", 0, -1]

	lineElements = line.split("\t")
	readFull = lineElements[0][0:-2] # Removing the last 2 characters so that pairs are considered part of the same read
	readElements = readFull.split(":")
	read = (int(readElements[4]), int(readElements[5]), int(readElements[6][0:-2])) # Convert to ints
	chrom = lineElements[2]
	position = int(lineElements[3])
	if isTop == False:#Y
		# On the bottom strand, so the CpG/CHG starts CGDist positions earlier
		position = position - CGDist
	call = lineElements[4].strip()
	state = 0
	if call == methylLetter:#Y
		# The C is methylated
		state = 1
	return [read, chrom, position, state]


def processLineSNP(line):
	# Get the informtion for a line from the methylation file
	if line == "":
		# At the end of the file
		return ["", "", 0, -1]

	lineElements = line.split("\t")
	readFull = lineElements[0][0:-2] # Removing the last 2 characters so that pairs are considered part of the same read
	readElements = readFull.split(":")
	read = (int(readElements[4]), int(readElements[5]), int(readElements[6][0:-2])) # Convert to ints
	chrom = lineElements[2]
	position = int(lineElements[3])
	statePM = lineElements[1]
	state = 0
	if statePM == "-":#Y
		# The SNP is the alternate allele, so make the state 1
		state = 1
	return [read, chrom, position, state, readFull]
	
	
def compareMethylSNPReads(methylRead, SNPRead):
	# Compare whether the methylation read is earlier in the alphabet than the SNP read
	# Output: -1 if methylation read is earlier, 0 if reads are equal, 1 if methylation read is later
	if methylRead[0] < SNPRead[0]:#Y
		# The methylation read is earlier in the alphabet
		return -1
	elif methylRead[0] > SNPRead[0]:#Y
		# The methylation read is later in the alphabet
		return 1
	elif methylRead [1] < SNPRead[1]:#Y
		# The methylation read is earlier in the alphabet
		return -1
	elif methylRead[1] > SNPRead[1]:#Y
		# The methylation read is later in the alphabet
		return 1
	elif methylRead[2] < SNPRead[2]:#Y
		# The methylation read is earlier in the alphabet
		return -1
	elif methylRead[2] > SNPRead[2]:#Y
		# The methylation read is later in the alphabet
		return 1
	else:#Y
		# The methylation and SNP reads are the same
		return 0


def getSNPMethylReadsPlus(bismarkSNPFileName, bismarkMethylationFileName, methylLetter, CGDist, sampleNum, outputFileName):
	# Find the reads with SNPs and Cs
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
	if bismarkMethylationFileNameElements[-1][4:6] == "OB":#Y
		# On the bottom strand
		isTop = False
	bismarkMethylationFile = gzip.open(bismarkMethylationFileName, 'rb')
	outputFile = gzip.open(outputFileName, 'wb')
	[methylRead, methylChrom, methylPosition, methylState] = processLineMethyl(bismarkMethylationFile.readline(), methylLetter, isTop, CGDist)
	if methylRead == "":
		# There are no reads the methylation file, so stop
		bismarkMethylationFile.close()
		bismarkSNPFile.close()
		outputFile.close()
		return
	CInfo = []
	lastRead = ""
	SNPPositionsOnRead = []
	atEnd = False

	for line in bismarkSNPFile:
		# Iterate through the SNPs and find those that are on reads with C's
		if line == "":
			# The file is empty, so stop
			break
		[SNPRead, SNPChrom, SNPPosition, SNPState, SNPReadFull] = processLineSNP(line)	
		if SNPRead == lastRead:#Y
			# The SNP is on the same read as the previous SNP
			if SNPPosition in SNPPositionsOnRead:#Y
				# The SNP has been called twice (because it was picked up in both pair members), so skip it
				continue

 			for Ci in CInfo:
				# Iterate through the C information from the last SNP and output it for the current SNP
				outputFile.write(SNPReadFull + "\t" + SNPChrom + "\t" + str(SNPPosition) + "\t" + str(SNPState) + "\t" + Ci[0] + "\t" + str(Ci[1]) + "\t" + str(Ci[2]) + "\t" + str(sampleNum) + "\n")
			SNPPositionsOnRead.append(SNPPosition)
			continue

		if atEnd == True:
			# Reached the end of the methylation file on the last iteration and at a new read, so stop
			break

		SNPPositionsOnRead = []
		CInfo = []
		while compareMethylSNPReads(methylRead, SNPRead) == -1:
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
			outputFile.write(SNPReadFull + "\t" + SNPChrom + "\t" + str(SNPPosition) + "\t" + str(SNPState) + "\t" + methylChrom + "\t" + str(methylPosition) + "\t" + str(methylState) + "\t" + str(sampleNum) + "\n")
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
	methylLetter = sys.argv[3]
	CGDist = int(sys.argv[4]) # 1 for CpG, 2 for CHG, UNKNOWN FOR CHH
	sampleNum = sys.argv[5]
	outputFileName = sys.argv[6] # Should end with .gz

	getSNPMethylReadsPlus(bismarkSNPFileName, bismarkMethylationFileName, methylLetter, CGDist, sampleNum, outputFileName)
