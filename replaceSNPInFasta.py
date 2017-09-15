def replaceSNPInFasta(fastaFileName, SNPLocationDist, vcfFileName, outputFileName):
	# Replace each location in the fasta file that is SNPLocationDist away from the start of the sequence with the other allele for the SNP
	# ASSUMES THAT EVERY SNP IS IN vcfFile
	# ASSUMES THAT fastaFile and vcfFile ARE SORTED BY CHROMOSOME, START
	fastaFile = open(fastaFileName)
	vcfFile = open(vcfFileName)
	outputFile = open(outputFileName, 'w+')
	fastaHeader = fastaFile.readline()
	vcfLineElements = vcfFile.readline().strip().split("\t")
	SNP = [vcfLineElements[0], int(vcfLineElements[1]), vcfLineElements[3], vcfLineElements[4]]
	while fastaHeader != "":
		# Iterate through the fasta file and replace the appropriate base in each sequence
		fastaHeaderElements = fastaHeader.strip().split(":")
		fastaChr = fastaHeaderElements[0][1:]
		fastaHeaderLocationElements = fastaHeaderElements[1].split("-")
		SNPLocation = int(fastaHeaderLocationElements[0]) + SNPLocationDist
		fastaSequence = fastaFile.readline().strip().upper()
		while SNP[0] < fastaChr:
			# Iterate through the vcf file until a SNP on the proper chromosome has been reached
			vcfLineElements = vcfFile.readline().strip().split("\t")
			SNP = [vcfLineElements[0], int(vcfLineElements[1]), vcfLineElements[3], vcfLineElements[4]]
		while SNP[1] < SNPLocation:
			# Iterate through the vcf file unitl a SNP at the proper location has been reached
			vcfLineElements = vcfFile.readline().strip().split("\t")
			SNP = [vcfLineElements[0], int(vcfLineElements[1]), vcfLineElements[3], vcfLineElements[4]]
		if fastaSequence[SNPLocationDist-1:SNPLocationDist-1+len(SNP[2])] != SNP[2]:
			print "Problem!"
			print fastaSequence[SNPLocationDist-1:SNPLocationDist-1+len(SNP[2])]
			print SNP
			print fastaHeader
		newFastaSequence = fastaSequence[0:SNPLocationDist-1] + SNP[3] + fastaSequence[SNPLocationDist-1+len(SNP[2]):len(fastaSequence)]
		outputFile.write(fastaHeader)
		outputFile.write(newFastaSequence + "\n")
		fastaHeader = fastaFile.readline()
	fastaFile.close()
	vcfFile.close()
	outputFile.close()

if __name__=="__main__":
	import sys
	fastaFileName = sys.argv[1]
	SNPLocationDist = int(sys.argv[2])
	vcfFileName = sys.argv[3]
	outputFileName = sys.argv[4]
	replaceSNPInFasta(fastaFileName, SNPLocationDist, vcfFileName, outputFileName)
			