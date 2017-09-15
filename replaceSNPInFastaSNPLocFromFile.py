def goToNextFastaSequence(fastaFile, fastaHeader, fastaSequence, newFastaSequence, outputFile, currentSNPList, sequenceChange):
	# Record the current fasta sequence if it has changed and move to the next one
	if sequenceChange:
		# The fasta has changed, so record it
		outputFile.write(fastaHeader)
		outputFile.write(newFastaSequence + "\n")
	fastaHeader = fastaFile.readline()
	return [fastaHeader, currentSNPList]

def replaceSNPInFastaSNPLocFromFile(fastaFileName, SNPFileName, colToReplace, outputFileName):
	# Replace each location in the fasta file that has a SNP in SNPFile with the allele of SNP that is specified in colToReplace
	# ASSUMES THAT fastaFile and SNPFile ARE SORTED BY CHROMOSOME, START
	# Remove fasta entries that do not have variants
	fastaFile = open(fastaFileName)
	SNPFile = open(SNPFileName)
	outputFile = open(outputFileName, 'w+')
	fastaHeader = fastaFile.readline()
	SNPLine = SNPFile.readline().strip()
	SNPLineElements = SNPLine.split("\t")
	SNP = [SNPLineElements[0], int(SNPLineElements[1]), SNPLineElements[colToReplace]]
	lastSNPList = []
	while fastaHeader != "":
		# Iterate through the fasta file and replace the appropriate base in each sequence
		fastaHeaderElements = fastaHeader.strip().split(":")
		fastaChr = fastaHeaderElements[0][1:]
		fastaHeaderLocationElements = fastaHeaderElements[1].split("-")
		fastaSequence = fastaFile.readline().strip().upper()
		newFastaSequence = fastaSequence
		sequenceChange = False
		currentSNPList = []
		for lastSNP in lastSNPList:
			# Iterate through the SNPs from the previous fasta and replace the appropriate base in each sequence for those that overlap the current fasta
			if (lastSNP[0] == fastaChr) and ((lastSNP[1] >= int(fastaHeaderLocationElements[0])) and (lastSNP[1] < int(fastaHeaderLocationElements[1]))):
				# The current SNP is in the current fasta, so replace the appropriate base with the allele in colToReplace
				SNPLocation = lastSNP[1] - int(fastaHeaderLocationElements[0])
				newFastaSequence = newFastaSequence[0:SNPLocation - 1] + lastSNP[2] + newFastaSequence[SNPLocation:len(fastaSequence)]
				sequenceChange = True
				currentSNPList.append(lastSNP)
		if SNPLine == "":
			# At the end of the SNP file, so stop
			[fastaHeader, lastSNPList] = goToNextFastaSequence(fastaFile, fastaHeader, fastaSequence, newFastaSequence, outputFile, currentSNPList, sequenceChange)
			continue
		while SNP[0] < fastaChr:
			# Iterate through the SNP file until a SNP on the proper chromosome has been reached
			SNPLine = SNPFile.readline().strip()
			if SNPLine == "":
				# At the end of the SNP file, so stop
				break
			SNPLineElements = SNPLine.split("\t")
			SNP = [SNPLineElements[0], int(SNPLineElements[1]), SNPLineElements[colToReplace]]
		if SNPLine == "":
			# At the end of the SNP file, so stop
			[fastaHeader, lastSNPList] = goToNextFastaSequence(fastaFile, fastaHeader, fastaSequence, newFastaSequence, outputFile, currentSNPList, sequenceChange)
			continue
		while (SNP[1] < int(fastaHeaderLocationElements[0])) and (SNP[0] == fastaChr):
			# Iterate through the SNP file unitl a SNP at the proper location has been reached
			SNPLine = SNPFile.readline().strip()
			if SNPLine == "":
				# At the end of the SNP file, so stop
				break
			SNPLineElements = SNPLine.split("\t")
			SNP = [SNPLineElements[0], int(SNPLineElements[1]), SNPLineElements[colToReplace]]
		if SNPLine == "":
			# At the end of the SNP file, so stop
			[fastaHeader, lastSNPList] = goToNextFastaSequence(fastaFile, fastaHeader, fastaSequence, newFastaSequence, outputFile, currentSNPList, sequenceChange)
			continue
		while (SNP[0] == fastaChr) and ((SNP[1] >= int(fastaHeaderLocationElements[0])) and (SNP[1] < int(fastaHeaderLocationElements[1]))):
			# Iterate through the SNPs that are in the fasta sequence and replace them with the approriate alleles
			SNPLocation = SNP[1] - int(fastaHeaderLocationElements[0])
			newFastaSequence = newFastaSequence[0:SNPLocation - 1] + SNP[2] + newFastaSequence[SNPLocation:len(fastaSequence)]
			sequenceChange = True
			currentSNPList.append(SNP)
			SNPLine = SNPFile.readline().strip()
			if SNPLine == "":
				# At the end of the SNP file, so stop
				break
			SNPLineElements = SNPLine.split("\t")
			SNP = [SNPLineElements[0], int(SNPLineElements[1]), SNPLineElements[colToReplace]]
		[fastaHeader, lastSNPList] = goToNextFastaSequence(fastaFile, fastaHeader, fastaSequence, newFastaSequence, outputFile, currentSNPList, sequenceChange)
	fastaFile.close()
	SNPFile.close()
	outputFile.close()

if __name__=="__main__":
	import sys
	fastaFileName = sys.argv[1]
	SNPFileName = sys.argv[2]
	colToReplace = int(sys.argv[3])
	outputFileName = sys.argv[4]
	replaceSNPInFastaSNPLocFromFile(fastaFileName, SNPFileName, colToReplace, outputFileName)
			
