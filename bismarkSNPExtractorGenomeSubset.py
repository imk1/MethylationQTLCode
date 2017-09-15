def inSNPMethyl(SNPRef, SNPAlt):
	# Check if the current SNP is a SNP that could be affected by bisulfite treatment
	if len(SNPRef) > 1:
		# At an indel, not a SNP
		return False
	if len(SNPAlt) > 1:
		# At an indel, not a SNP
		return False
	if ("C" in SNPRef) and ("T" in SNPAlt):#Y
		# In a C/T SNP
		return True
	if ("T" in SNPRef) and ("C" in SNPAlt):#Y
		# In a T/C SNP
		return True
	if ("G" in SNPRef) and ("A" in SNPAlt):#Y
		# In a G/A SNP
		return True
	if ("A" in SNPRef) and ("G" in SNPAlt):#Y
		# In an A/G SNP
		return True
	return False


def processSNPVcfStartLine(SNPVcfStartLine, SNPVcfStartFile):
	# Get the chromosome, position on the chromosome, reference allele, and alternate allele from a line of a vcf file
	if SNPVcfStartLine == "":
		# At the end of the vcf file, so stop
		return ["", 0, "", "", True]
	SNPVcfStartLineElements = SNPVcfStartLine.split("\t")
	SNPChrom = int(SNPVcfStartLineElements[0][3:])
	SNPRef = SNPVcfStartLineElements[3]
	SNPAlt = SNPVcfStartLineElements[4]
	atEnd = False

	while inSNPMethyl(SNPRef, SNPAlt):
		# Go to the next SNP until a SNP that may be miscalled due to bisulfite treatment is reached
		SNPVcfStartLine = SNPVcfStartFile.readline().strip()
		if SNPVcfStartLine == "":
			# At the end of the SNP file
			atEnd = True
			break
		SNPVcfStartLineElements = SNPVcfStartLine.split("\t")
		SNPChrom = int(SNPVcfStartLineElements[0][3:])
		SNPRef = SNPVcfStartLineElements[3]
		SNPAlt = SNPVcfStartLineElements[4]
	return [SNPChrom, int(SNPVcfStartLineElements[1]), SNPRef, SNPAlt, atEnd]


def processBismarkSamLineGenomeSubset(bismarkSamLine):
	# Get the chromosome, position on chromosome, direction in which to iterate, and sequence from a line of a sam file
	# Direction = True means iterate through the sequence in the forwards direction (position is the first base)
	# Direction = False means iterate through the sequence in the backwards direction (position is the last base)
	bismarkSamLineElements = bismarkSamLine.split("\t")
	if (("_" in bismarkSamLineElements[2]) or ("chrM" in bismarkSamLineElements[2])) or (("chrX" in bismarkSamLineElements[2]) or ("chrY" in bismarkSamLineElements[2])):
		# The read maps to an unknown chromosome, mitochondrial DNA, or a sex chromosome
		# EXCLUDING SEX CHROMOSOMES, MITOCHONDRIAL DNA, AND UNKNOWN CHROMOSOMES
		return [bismarkSamLineElements[0], 0, int(bismarkSamLineElements[3]), bismarkSamLineElements[5], bismarkSamLineElements[9]]

	# CHROMOSOME COLUMN HAS REGION
	bismarkChromElements = bismarkSamLineElements[2][3:].split(":")
	bismarkChrom = int(bismarkChromElements[0])
	bismarkRegionElements = bismarkChromElements[1].split("-")
	bismarkPosition = int(bismarkSamLineElements[3]) + int(bismarkRegionElements[0]) - 1
	return [bismarkSamLineElements[0], bismarkChrom, bismarkPosition, bismarkSamLineElements[5], bismarkSamLineElements[9]]


def recordSNPNoIndels(readName, bismarkChrom, bismarkStart, bismarkSequence, SNPPosition, SNPRef, SNPAlt, outputFile):
	# Determine which allele the SNP has and record the SNP's information for the read
	# RECORDS THE TRUE ALLELES, NOT THE BISULFITE-TREATED ALLELES
	SNPLocationInRead = SNPPosition - bismarkStart
	if (len(SNPRef) == 1) and (len(SNPAlt) == 1):
		# SNP, not an indel
		SNP = bismarkSequence[SNPLocationInRead]
		if SNP == SNPRef:#Y
			# The SNP matches the reference allele
			outputFile.write(readName + "\t" + "+" + "\t" + "chr" + str(bismarkChrom) + "\t" + str(SNPPosition) + "\t" + SNPRef + "\n")
		elif SNP == SNPAlt:#Y
			# The SNP matches the alternate allele
			outputFile.write(readName + "\t" + "-" + "\t" + "chr" + str(bismarkChrom) + "\t" + str(SNPPosition) + "\t" + SNPAlt + "\n")

		elif SNP == "T":
			# The SNP is a T in the bisulfite-treated DNA, so it probably is a C in the true DNA sequence
			if SNPRef == "C":#Y
				# The SNP matches the reference allele
				outputFile.write(readName + "\t" + "+" + "\t" + "chr" + str(bismarkChrom) + "\t" + str(SNPPosition) + "\t" + SNPRef + "\n")
			elif SNPAlt == "C":
				# The SNP matches the alternate allele
				outputFile.write(readName + "\t" + "-" + "\t" + "chr" + str(bismarkChrom) + "\t" + str(SNPPosition) + "\t" + SNPAlt + "\n")
		elif SNP == "A":
			# The SNP is an A in the bisulfite-treated DNA, so it probably is a G in the true DNA sequence
			if SNPRef == "G":#Y
				# The SNP matches the reference allele
				outputFile.write(readName + "\t" + "+" + "\t" + "chr" + str(bismarkChrom) + "\t" + str(SNPPosition) + "\t" + SNPRef + "\n")
			elif SNPAlt == "G":#Y
				# The SNP matches the alternate allele
				outputFile.write(readName + "\t" + "-" + "\t" + "chr" + str(bismarkChrom) + "\t" + str(SNPPosition) + "\t" + SNPAlt + "\n")

	else:#Y
		# There are no insertions or deletions, so ASSUME REFERENCE ALLELE
		outputFile.write(readName + "\t" + "+" + "\t" + "chr" + str(bismarkChrom) + "\t" + str(SNPPosition) + "\t" + SNPRef + "\n")


def recordSNP(readName, bismarkChrom, bismarkStart, bismarkCigar, bismarkSequence, SNPPosition, SNPRef, SNPAlt, outputFile):
	# Determine which allele the SNP has and record the SNP's information for the read
	# RECORDS THE TRUE ALLELES, NOT THE BISULFITE-TREATED ALLELES
	if ("D" not in bismarkCigar) and ("I" not in bismarkCigar):
		# The read has no insertions or deletions
		recordSNPNoIndels(readName, bismarkChrom, bismarkStart, bismarkSequence, SNPPosition, SNPRef, SNPAlt, outputFile)

	else:
		cigarList = []
		cigarNumStr = ""
		for bc in bismarkCigar:
			# Iterate through the characters in the Cigar string and divide the string into parts
			if (bc == "M") or ((bc == "D") or (bc == "I")):
				# At a breaking point between parts
				cigarList.append((int(cigarNumStr), bc))
				cigarNumStr = ""
			else:
				cigarNumStr = cigarNumStr + bc

		currentStart = bismarkStart # Genome coordinate
		currentLocation = 0 # Location within Bismark sequence
		for cl in cigarList:
			# Iterate through the parts of the read and record the SNPs appropriately
			if cl[1] == "M":
				# The current part has no insertions and deletions
				currentEnd = currentStart + cl[0] - 1#Y
				nextLocation = currentLocation + cl[0]#Y
				if (SNPPosition >= currentStart) and (SNPPosition < currentEnd):#Y
					# Record the current SNP information as if there are no insertions and deletions
					recordSNPNoIndels(readName, bismarkChrom, currentStart, bismarkSequence[currentLocation:nextLocation], SNPPosition, SNPRef, SNPAlt, outputFile)
				if ((SNPPosition >= currentStart) and (SNPPosition == currentEnd)) and ((len(SNPRef) == 1) and (len(SNPAlt) == 1)):
					# Record the current SNP information as if there are no insertions and deletions
					recordSNPNoIndels(readName, bismarkChrom, currentStart, bismarkSequence[currentLocation:nextLocation], SNPPosition, SNPRef, SNPAlt, outputFile)
				currentStart = currentEnd + 1#Y
				currentLocation = nextLocation#Y

			elif cl[1] == "D":#Y
				# The current part is a deletion
				if SNPPosition == currentStart - 1:#Y
					# The current SNP is a deletion
					if len(SNPRef) - 1 == cl[0]:#Y
						# The deletion is the right length, so ASSUME ALTERNATE ALLELE
						outputFile.write(readName + "\t" + "-" + "\t" + "chr" + str(bismarkChrom) + "\t" + str(SNPPosition) + "\t" + SNPAlt + "\n")
				currentStart = currentStart + cl[0]#Y

			else:
				# The current part is an insertion
				if SNPPosition == currentStart - 1:
					# The SNP is an insertion
					if len(SNPAlt) - 1 == cl[0]:
						# The insertion is the right length
						insertionMatches = True#Y
						for i in range(cl[0]):
							# Iterate through the locations and check if the insertion matches
							if bismarkSequence[currentLocation + i] != SNPAlt[i + 1]:
								# The sequence does not match the insertion, check bisulfite
								if (bismarkSequence[currentLocation + i] == "T") and (SNPAlt[i + 1] == "C"):
									# Difference probably due to bisulfite treatment
									continue
								if (bismarkSequence[currentLocation + i] == "A") and (SNPAlt[i + 1] == "G"):
									# Difference probably due to bisulfite treatment
									continue
								insertionMatches = False
								break
						if insertionMatches == True:#Y
							# The insertion matches the alternate allele, so record it
							outputFile.write(readName + "\t" + "-" + "\t" + "chr" + str(bismarkChrom) + "\t" + str(SNPPosition) + "\t" + SNPAlt + "\n")
				currentLocation = currentLocation + cl[0]


def bismarkSNPExtractorGenomeSubset(bismarkSamFileName, SNPVcfStartFileName, outputFileName):
	# Find the version of each SNP in each read
	# ASSUMES THAT POSITIONS IN bismarkSamFileName AND SNPVcfStartFileName ARE SORTED BY CHROM., THEN START, THEN END
	# ASSUMES THAT CHROMOSOMES ARE IN KARYOTYPIC ORDER (1, 2, 3, etc.)
	# EXCLUDES ALL C/T AND G/A SNPS
	# Output file consists of 5 columns:
	# 1.  Read name (example: MISEQ:77:000000000-A49C4:1:1101:17229:1509_1:N:0:CGATG/1)
	# 2.  + if matches reference allele, - if matches alternate allele
	# 3.  Chromosome
	# 4.  Position in chromosome
	# 5.  Genotype
	#Y means condition seems to work properly
	SNPVcfStartFile = open(SNPVcfStartFileName)
	SNPVcfStartLine = SNPVcfStartFile.readline().strip()
	outputFile = open(outputFileName, 'w+')
	while SNPVcfStartLine[0] == "#":
		# The line is part of the header, so go to the next line
		SNPVcfStartLine = SNPVcfStartFile.readline().strip()
	[SNPChrom, SNPPosition, SNPRef, SNPAlt, atEnd] = processSNPVcfStartLine(SNPVcfStartLine, SNPVcfStartFile)
	if atEnd == True:
		# At the end of the SNP file, so stop
		outputFile.close()
		return

	bismarkSamFile = open(bismarkSamFileName)
	bismarkSamLine = bismarkSamFile.readline().strip()
	while bismarkSamLine[0] == "@":
		# The line is part of the header, so go to the next line
		bismarkSamLine = bismarkSamFile.readline().strip()
	lastSNPInfo = []
	currentSNPInfo = []

	while bismarkSamLine != "":
		# Iterate through the sam file and find the SNPs in each line
		[readName, bismarkChrom, bismarkPosition, bismarkCigar, bismarkSequence] = processBismarkSamLineGenomeSubset(bismarkSamLine)
		if bismarkChrom == 0:
			# The read maps to an unknown chromosome, mitochondrial DNA, or a sex chromosome
			bismarkSamLine = bismarkSamFile.readline()
			lastSNPInfo = currentSNPInfo
			continue
		bismarkStart = bismarkPosition
		bismarkEnd = bismarkStart + len(bismarkSequence) - 1

		currentSNPInfo = []
		for SNPInfo in lastSNPInfo:
			# Iterate through the SNPs from the last read and find those that overlap the current read
			if (bismarkChrom == SNPInfo[0]) and ((bismarkStart <= SNPInfo[1]) and ((bismarkEnd >= SNPInfo[1] + len(SNPInfo[2]) - 1) and (bismarkEnd >= SNPInfo[1] + len(SNPInfo[3]) - 1))):#Y
				# This SNP overlaps the current read
				currentSNPInfo.append(SNPInfo)
				recordSNP(readName, bismarkChrom, bismarkStart, bismarkCigar, bismarkSequence, SNPInfo[1], SNPInfo[2], SNPInfo[3], outputFile)

		while (bismarkChrom > SNPChrom) and (atEnd == False):
			# Iterate through the SNPs until a SNP on the proper chromosome has been reached
			SNPVcfStartLine = SNPVcfStartFile.readline().strip()
			[SNPChrom, SNPPosition, SNPRef, SNPAlt, atEnd] = processSNPVcfStartLine(SNPVcfStartLine, SNPVcfStartFile)
		if atEnd == True:
				# At the end of the SNP file, so stop
				bismarkSamLine = bismarkSamFile.readline()
				lastSNPInfo = currentSNPInfo
				continue
		while (SNPChrom == bismarkChrom) and ((bismarkStart > SNPPosition) and (atEnd == False)):#Y
			# Iterate through the SNPs until a SNP at the proper location has been reached
			SNPVcfStartLine = SNPVcfStartFile.readline().strip()
			[SNPChrom, SNPPosition, SNPRef, SNPAlt, atEnd] = processSNPVcfStartLine(SNPVcfStartLine, SNPVcfStartFile)
		if atEnd == True:
				# At the end of the SNP file, so stop
				bismarkSamLine = bismarkSamFile.readline()
				lastSNPInfo = currentSNPInfo
				continue

		while (bismarkChrom == SNPChrom) and ((bismarkStart <= SNPPosition) and (bismarkEnd >= SNPPosition)):#Y
			# Record the SNP information for all SNPs in the current read
			if (bismarkEnd >= SNPPosition + len(SNPRef) - 1) and (bismarkEnd >= SNPPosition + len(SNPAlt) - 1):
			# The current SNP/Indel is in the current read
				recordSNP(readName, bismarkChrom, bismarkStart, bismarkCigar, bismarkSequence, SNPPosition, SNPRef, SNPAlt, outputFile)
			currentSNPInfo.append([SNPChrom, SNPPosition, SNPRef, SNPAlt])
			if atEnd == False:
				# Go to the next SNP
				SNPVcfStartLine = SNPVcfStartFile.readline().strip()
				[SNPChrom, SNPPosition, SNPRef, SNPAlt, atEnd] = processSNPVcfStartLine(SNPVcfStartLine, SNPVcfStartFile)
				if atEnd == True:
					# At the end of the SNP file, so stop
					break			

		bismarkSamLine = bismarkSamFile.readline()
		lastSNPInfo = currentSNPInfo

	SNPVcfStartFile.close()
	bismarkSamFile.close()
	outputFile.close()


if __name__=="__main__":
	import sys
	bismarkSamFileName = sys.argv[1]
	# Sam file has the following important columns:
	# 1.  Read name
	# 3.  Chromosome
	# 4.  Start of current read
	# 6.  Match/deletion/insertion information
	# 8.  Start of other read in pair
	# 10.  Sequence
	SNPVcfStartFileName = sys.argv[2]
	outputFileName = sys.argv[3]

	bismarkSNPExtractorGenomeSubset(bismarkSamFileName, SNPVcfStartFileName, outputFileName)
