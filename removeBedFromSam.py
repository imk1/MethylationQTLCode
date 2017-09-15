def processBismarkSamLineShort(bismarkSamLine):
	# Get the chromosome, position on chromosome, and cigar from a line of a sam file
	# Direction = True means iterate through the sequence in the forwards direction (position is the first base)
	# Direction = False means iterate through the sequence in the backwards direction (position is the last base)
	bismarkSamLineElements = bismarkSamLine.split("\t")
	if (("_" in bismarkSamLineElements[2]) or ("chrM" in bismarkSamLineElements[2])) or (("chrX" in bismarkSamLineElements[2]) or ("chrY" in bismarkSamLineElements[2])):
		# The read maps to an unknown chromosome, mitochondrial DNA, or a sex chromosome
		# EXCLUDING SEX CHROMOSOMES, MITOCHONDRIAL DNA, AND UNKNOWN CHROMOSOMES
		return [0, int(bismarkSamLineElements[3]), bismarkSamLineElements[5]]

	bismarkChrom = int(bismarkSamLineElements[2][3:])
	return [bismarkChrom, int(bismarkSamLineElements[3]), bismarkSamLineElements[5]]


def getCigarList(bismarkCigar):
	# Get the list of the elements in the cigar
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
	return cigarList

	
def getBismarkEnd(cigarList, bismarkEnd):
	# Find the end of the read
	for cl in cigarList:
		# Iterate through the parts of the cigar and update the end appropriately
		if cl[1] == "M":
			# At a match, so add the number of matches to the end
			bismarkEnd = bismarkEnd + cl[0]
		
		elif cl[1] == "D":
			# At a deletion, so add the number of missing bases
			bismarkEnd = bismarkEnd + cl[0]
		
		elif cl[1] == "I":
			# At an insertion, so do not add anything
			continue
	return bismarkEnd

	
def removeBedFromSam(samFileName, bedFileName, outputFileName):
	# Remove reads from sam file that overlap regions in bed file
	# ASSUMES THAT SAM FILE AND BED FILE ARE SORTED IN KARYOTYPIC ORDER
	bismarkSamFile = open(samFileName)
	bedFile = open(bedFileName)
	bedLineElements = bedFile.readline().strip().split("\t")
	bedInfo = (int(bedLineElements[0][3:]), int(bedLineElements[1]), int(bedLineElements[2]))
	outputFile = open(outputFileName, 'w+')
	bismarkSamLine = bismarkSamFile.readline().strip()
	bedEnd = False
	
	while bismarkSamLine[0] == "@":
		# The line is part of the header, so go record it and to the next line
		outputFile.write(bismarkSamLine + "\n")
		bismarkSamLine = bismarkSamFile.readline().strip()
	
	while bismarkSamLine != "":
		# Iterate through the sam file and find the lines that do not overlap any regions in the bed file
		if bedEnd == True:
			# At the end of the bed file, so stop and record the line of the sam file
			outputFile.write(bismarkSamLine + "\n")
			bismarkSamLine = bismarkSamFile.readline().strip()
			continue
		[bismarkChrom, bismarkPosition, bismarkCigar] = processBismarkSamLineShort(bismarkSamLine)
		cigarList = getCigarList(bismarkCigar)
		bismarkEnd = getBismarkEnd(cigarList, bismarkPosition - 1)
		
		while bedInfo[0] < bismarkChrom:
			# Iterate through the bed file until the correct chromosome has been reached
			bedLine = bedFile.readline()
			if bedLine == "":
				# At the end of the bed file
				bedEnd = True
				break
			bedLineElements = bedLine.strip().split("\t")
			bedInfo = (int(bedLineElements[0][3:]), int(bedLineElements[1]), int(bedLineElements[2]))
		if bedEnd == True:
			# At the end of the bed file, so stop and record the line of the sam file
			outputFile.write(bismarkSamLine + "\n")
			bismarkSamLine = bismarkSamFile.readline().strip()
			continue
		
		while (bedInfo[0] == bismarkChrom) and (bedInfo[2] < bismarkPosition):
			# Iterate through the bed file until the position of the start of the read has been reached
			bedLine = bedFile.readline()
			if bedLine == "":
				# At the end of the bed file
				bedEnd = True
				break
			bedLineElements = bedLine.strip().split("\t")
			bedInfo = (int(bedLineElements[0][3:]), int(bedLineElements[1]), int(bedLineElements[2]))
			if bedInfo[0] > bismarkChrom:
				# At a new chromosome, so stop
				break
		if bedEnd == True:
			# At the end of the bed file, so stop and record the line of the sam file
			outputFile.write(bismarkSamLine + "\n")
			bismarkSamLine = bismarkSamFile.readline().strip()
			continue
		
		if (bedInfo[0] == bismarkChrom) and (bedInfo[1] <= bismarkEnd):
			# The current region overlaps the current read
			bismarkSamLine = bismarkSamFile.readline().strip()
			continue
		outputFile.write(bismarkSamLine + "\n")
		bismarkSamLine = bismarkSamFile.readline().strip()
		
	bismarkSamFile.close()
	bedFile.close()
	outputFile.close()

	
if __name__=="__main__":
	import sys
	samFileName = sys.argv[1]
	# Sam file has the following important columns:
	# 1.  Read name
	# 3.  Chromosome
	# 4.  Start of current read
	# 6.  Match/deletion/insertion information
	bedFileName = sys.argv[2]
	outputFileName = sys.argv[3]

	removeBedFromSam(samFileName, bedFileName, outputFileName)
		