def processBismarkSamLineShort(bismarkSamLine):
	# Get the chromosome, position on chromosome, direction in which to iterate, and sequence from a line of a sam file
	# Direction = True means iterate through the sequence in the fowards direction (position is the first base)
	# Direction = False means iterate through the sequence in the backwards direction (position is the last base)
	bismarkSamLineElements = bismarkSamLine.split("\t")
	if ("_" in bismarkSamLineElements[2]) or ("chrM" in bismarkSamLineElements[2]):
		# The read maps to an unknown chromosome or mitochondrial DNA
		return ["", int(bismarkSamLineElements[3]), len(bismarkSamLineElements[9])]

	bismarkChrom = bismarkSamLineElements[2]
	return [bismarkChrom, int(bismarkSamLineElements[3]), len(bismarkSamLineElements[9])]


def getReadsForPositionPair(readsFileNameListFileName, positionChrom, positionStart, positionEnd, outputFileName):
	# Get the number of reads at a position
	# ASSUMES THAT READS HAVE NO INDELS
	# ASSUMES THAT THE FIRST ELEMENT IN THE PAIR IS SMALLER
	pp = (positionChrom, positionStart, positionEnd)
	readsFileNameListFile = open(readsFileNameListFileName)
	outputFile = open(outputFileName, 'w+')
	
	for readsFileName in readsFileNameListFile:
		# Iterate through the files with the reads and increment the positions for each read in each file
		print readsFileName.strip()
		readsFile = open(readsFileName.strip())
		
		for line in readsFile:
			# Iterate through the reads and increment every position for every read
			if line[0] == "@":
				# The line is a header, so continue
				continue
			
			[bismarkChrom, bismarkPosition, bismarkSequenceLength] = processBismarkSamLineShort(line.strip())
			if (bismarkChrom == "") or (bismarkChrom != pp[0]):
				# The current read maps to mitochondrial DNA or an unknown region or a chromosome that is not the chromosome for the current position
				continue
				
			if (pp[1] >= bismarkPosition) and (pp[2] < bismarkPosition + bismarkSequenceLength):
				# The current position is in the current read
				outputFile.write(line)
			
		readsFile.close()
	readsFileNameListFile.close()
	outputFile.close()


if __name__=="__main__":
	import sys
if __name__=="__main__":
	import sys
	readsFileNameListFileName = sys.argv[1]
	# Each Sam in readsFileNameListFile file has the following important columns:
	# 3.  Chromosome
	# 4.  Start of current read
	# 10.  Sequence
	positionChrom = int(sys.argv[2])
	positionStart = int(sys.argv[3])
	positionEnd = int(sys.argv[4])
	outputFileName = sys.argv[5]

	getReadsForPositionPair(readsFileNameListFileName, positionChrom, positionStart, positionEnd, outputFileName)