def getBase(fileLine):
	# Get the current base
	if fileLine == "":
		# The file is finished
		return ("", 0)
	
	fileLineElements = fileLine.strip().split("\t")
	readFull = fileLineElements[0]
	readElements = readFull.split(":")
	read = (int(readElements[4]), int(readElements[5]), int(readElements[6][0:-2])) # Convert to ints
	return (read, fileLineElements[2], int(fileLineElements[3]), fileLineElements[4])


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


def compareMethylationCalls(trimmedFileName, untrimmedFileName):
	# Compare methylation calls of files with trimmed and untrimmed reads
	# ASSUMES THAT trimmedFile AND untrimmedFile are sorted by chrom., pos.
	# ASSUMES THAT EVERY BASE IN trimmedFile IS IN untrimmedFile
	# ASSUMES THAT untrimmedFile HAS AT LEAST 1 BASE
	trimmedFile = gzip.open(trimmedFileName)
	untrimmedFile = gzip.open(untrimmedFileName)
	(untrimmedRead, untrimmedChrom, untrimmedPos, untrimmedMethyl) = getBase(untrimmedFile.readline())
	numDisagree = 0
	untrimmedFileEnd = False
	
	for line in trimmedFile:
		# Iterate through the trimmed file and compare each methyl. call
		(trimmedRead, trimmedChrom, trimmedPos, trimmedMethyl) = getBase(line)
		while untrimmedChrom < trimmedChrom:
			# Iterate through the untrimmed file until correct chrom. is reached
			(untrimmedRead, untrimmedChrom, untrimmedPos, untrimmedMethyl) = getBase(untrimmedFile.readline())
			if untrimmedChrom == "":
				# At the end of the untrimmed file, so stop
				untrimmedFileEnd = True
				break
		if untrimmedFileEnd == True:
			# At the end of the untrimmed file, so stop
			break
		while (untrimmedChrom == trimmedChrom) and (untrimmedPos < trimmedPos):
			# Iterate through the untrimmed file until the correct pos. is reached
			(untrimmedRead, untrimmedChrom, untrimmedPos, untrimmedMethyl) = getBase(untrimmedFile.readline())
			if untrimmedChrom == "":
				# At the end of the untrimmed file, so stop
				untrimmedFileEnd = True
				break
		if untrimmedFileEnd == True:
			# At the end of the untrimmed file, so stop
			break
		while ((untrimmedChrom == trimmedChrom) and (untrimmedPos == trimmedPos)) and (compareMethylSNPReads(untrimmedRead, trimmedRead) == -1):
			# Iterate through the untrimmed file until the correct read is reached
			(untrimmedRead, untrimmedChrom, untrimmedPos, untrimmedMethyl) = getBase(untrimmedFile.readline())
			if untrimmedChrom == "":
				# At the end of the untrimmed file, so stop
				untrimmedFileEnd = True
				break
		if untrimmedFileEnd == True:
			# At the end of the untrimmed file, so stop
			break
		
		if ((untrimmedChrom == trimmedChrom) and (untrimmedPos == trimmedPos)) and (compareMethylSNPReads(untrimmedRead, trimmedRead) == 0):
			# The trimmed and untrimmed files are at the same location on the same read
			if trimmedMethyl != untrimmedMethyl:
				# The trimmed file and untrimmed file disagree with each other
				print (trimmedRead, trimmedChrom, trimmedPos, trimmedMethyl)
				print (untrimmedRead, untrimmedChrom, untrimmedPos, untrimmedMethyl)
				print "Trimmed file is " + trimmedMethyl + "; untrimmed file is " + untrimmedMethyl
				numDisagree = numDisagree + 1
	
	trimmedFile.close()
	untrimmedFile.close()
	
	
if __name__=="__main__":
	import sys
	import gzip
	trimmedFileName = sys.argv[1] # Should end with .gz
	untrimmedFileName = sys.argv[2] # Should end with .gz
	compareMethylationCalls(trimmedFileName, untrimmedFileName)
