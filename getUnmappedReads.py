def getUnmappedReads(samFileName, fastqFileName, fastqTwoFileName, unmappedReadsFileName, unmappedReadsTwoFileName):
	# Get the reads from the fastq file that have not been mapped in the sam file
	# ASSUMES THAT THE READS IN THE SAM FILE AND FASTQ FILE ARE IN THE SAME ORDER
	# ASSUMES THAT THERE ARE 2 LINES PER READ IN THE SAM FILE (paired-end)
	# ASSUMES THAT THERE ARE 4 LINES PER READ IN THE FASTQ FILE, WHERE EACH NEW READ STARTS WITH @ AND CONTAINS A SPACE INSTEAD OF AN _
	samFile = open(samFileName)
	fastqFile = gzip.open(fastqFileName)
	fastqTwoFile = gzip.open(fastqTwoFileName)
	unmappedReadsFile = gzip.open(unmappedReadsFileName, 'w+')
	unmappedReadsTwoFile = gzip.open(unmappedReadsTwoFileName, 'w+')
	currentSamLine = samFile.readline().strip()
	while(currentSamLine[0] == "@"):
		# The current line is a header, so skip it
		currentSamLine = samFile.readline().strip()
	currentSamLineElements = currentSamLine.split("\t")
	currentSamRead = currentSamLineElements[0][:-2] # Removing the pair information
	currentFastqLine = fastqFile.readline()
	currentFastqTwoLine = fastqTwoFile.readline()
	
	while currentFastqLine != "":
		# Iterate through the lines of the fastq file and write those from reads that are not in the sam file to the unmapped file
		currentFastqLineElements = currentFastqLine.strip().split(" ")
		currentFastqRead = currentFastqLineElements[0][1:] + "_" + currentFastqLineElements[1]
		
		while currentFastqRead != currentSamRead:
			# Record all of the reads that are not in the sam file in the unmapped file
			unmappedReadsFile.write(currentFastqLine)
			unmappedReadsTwoFile.write(currentFastqTwoLine)
			for i in range(3):
				currentFastqLine = fastqFile.readline()
				currentFastqTwoLine = fastqTwoFile.readline()
				unmappedReadsFile.write(currentFastqLine)
				unmappedReadsTwoFile.write(currentFastqTwoLine)
			currentFastqLine = fastqFile.readline()
			currentFastqTwoLine = fastqTwoFile.readline()
			if currentFastqLine == "":
				# At the end of the fastq file, so stop
				break
			currentFastqLineElements = currentFastqLine.strip().split(" ")
			currentFastqRead = currentFastqLineElements[0][1:] + "_" + currentFastqLineElements[1]
		
		samFile.readline() # Ignore the read from the other end of the pair
		currentSamLine = samFile.readline().strip()
		currentSamLineElements = currentSamLine.split("\t")
		currentSamRead = currentSamLineElements[0][:-2] # Removing the pair information
		for i in range(3):
			# Read the rest of the fastq lines that correspond to the current line in the same file
			fastqFile.readline()
			fastqTwoFile.readline()
		currentFastqLine = fastqFile.readline() # Repeat the loop to check if this new line's read is the same as the read in the sam file
		currentFastqTwoLine = fastqTwoFile.readline()
		
	samFile.close()
	fastqFile.close()
	fastqTwoFile.close()
	unmappedReadsFile.close()
	unmappedReadsTwoFile.close()


if __name__=="__main__":
	import sys
	import gzip
	samFileName = sys.argv[1]
	fastqFileName = sys.argv[2] # Should end with .gz
	fastqFileTwoName = sys.argv[3] # Should end with .gz
	unmappedReadsFileName = sys.argv[4] # Should end with .gz
	unmappedReadsTwoFileName = sys.argv[5] # Should end with .gz

	getUnmappedReads(samFileName, fastqFileName, fastqFileTwoName, unmappedReadsFileName, unmappedReadsTwoFileName)