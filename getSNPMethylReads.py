def processLine(line):
	# Get the informtion for a line from the methylation file
	if line == "":
		# At the end of the file
		return ["", "", 0, "", ""]

	lineElements = line.split("\t")
	read = lineElements[0][0:-2] # Removing the last 2 characters so that pairs are considered part of the same read
	chrom = lineElements[2]
	position = int(lineElements[3])
	state = lineElements[1]
	call = lineElements[4].strip()
	return [read, chrom, position, state, call]


def getSNPMethylReads(bismarkSNPFileName, bismarkMethylationFileName, outputFileName):
	# Find the reads with SNPs and Cs
	# Output file will have the following information for each (SNP, C in the same read):
	# 1.  Read name
	# 2.  SNP chromosome
	# 3.  SNP position on chromosome
	# 4.  + if SNP is the reference allele, - if SNP is the alternate allele
	# 5.  SNP genotype
	# 6.  C chromosome
	# 7.  C position on chromosome
	# 8.  + if C is methylated, - if C is not methylated
	# 9.  Methylation call
	bismarkSNPFile = open(bismarkSNPFileName)
	bismarkMethylationFile = gzip.open(bismarkMethylationFileName, 'rb')
	outputFile = gzip.open(outputFileName, 'wb')
	[methylRead, methylChrom, methylPosition, methylState, methylCall] = processLine(bismarkMethylationFile.readline())
	CInfo = []
	lastRead = ""
	lastSNPPosition = 0
	atEnd = False

	for line in bismarkSNPFile:
		# Iterate through the SNPs and find those that are on reads with C's
		[SNPRead, SNPChrom, SNPPosition, SNPState, SNPCall] = processLine(line)	
		if SNPRead == lastRead:
			# The SNP is on the same read as the previous SNP
			if SNPPosition == lastSNPPosition:
				# The SNP has been called twice (because it was picked up in both pair members), so skip it
				continue

 			for Ci in CInfo:
				# Iterate through the C information from the last SNP and output it for the current SNP
				outputFile.write(SNPRead + "\t" + SNPChrom + "\t" + str(SNPPosition) + "\t" + SNPState + "\t" + SNPCall + "\t" + Ci[0] + "\t" + str(Ci[1]) + "\t" + Ci[2] + "\t" + Ci[3] + "\n")
			lastSNPPosition = SNPPosition
			continue

		if atEnd == True:
			# Reached the end of the methylation file on the last iteration	and at a new read, so stop
			break

		CInfo = []
		while methylRead < SNPRead:
			# Go through the methylation file until the reads match or the methylation read passes the SNP read
			[methylRead, methylChrom, methylPosition, methylState, methylCall] = processLine(bismarkMethylationFile.readline())
			if methylRead == "":
				# At the end of the methylation file, so stop
				atEnd = True
				break
		if atEnd == True:
			# At the end of the methylation file, so stop
			break

		while methylRead == SNPRead:
			# Go through the methylation data that is on the same read as the SNP and output the information
			outputFile.write(SNPRead + "\t" + SNPChrom + "\t" + str(SNPPosition) + "\t" + SNPState + "\t" + SNPCall + "\t" + methylChrom + "\t" + str(methylPosition) + "\t" + methylState + "\t" + methylCall + "\n")
			CInfo.append([methylChrom, methylPosition, methylState, methylCall])
			[methylRead, methylChrom, methylPosition, methylState, methylCall] = processLine(bismarkMethylationFile.readline())
			if methylRead == "":
				# At the endof the methylation file, so stop
				atEnd = True
				break
		lastRead = SNPRead
		lastSNPPosition = SNPPosition

	bismarkSNPFile.close()
	bismarkMethylationFile.close()
	outputFile.close()


if __name__=="__main__":
	import sys
	import gzip
	bismarkSNPFileName = sys.argv[1]
	bismarkMethylationFileName = sys.argv[2] # Should end with .gz
	outputFileName = sys.argv[3] # Should end with .gz

	getSNPMethylReads(bismarkSNPFileName, bismarkMethylationFileName, outputFileName)
