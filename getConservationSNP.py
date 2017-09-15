def getConservationSNP(SNPFileName, PhastconsFileName, conservationFileName):
	# Gets the average conservation score of each SNP
	SNPFile = open(SNPFileName)
	PhastconsFile = open(PhastconsFileName)
	conservationFile = open(conservationFileName, 'w+')
	PhastconsIndex = 0
	PhastconsChrom = "chr0"
	PhastconsScore = -1
	PhastconsLine = ""
	lastChrom = "chr0"
	for line in SNPFile:
		# Iterate through SNPs and find the conservation score for each
		lineElements = line.split("\t")
		chrom = lineElements[0]
		if chrom != lastChrom:
			print chrom
			lastChrom = chrom
		location = int(lineElements[1])
		stopReached = False
		while chrom > PhastconsChrom:
			# At a new chromosome, so read through Phastcons file until the next chromosome is reached
			newChromReached = False
			while newChromReached == False:
				# Have not reached a new chromosome, so keep reading the Phastcons file
				PhastconsLine = PhastconsFile.readline()
				PhastconsLineElements = PhastconsLine.split(" ")
				if len(PhastconsLine) == 0:
					# There is no more conservation information, so do not record any conservation information for the region
					conservationFile.write(str(-1))
					conservationFile.write("\n")
					stopReached = True
					break
				if len(PhastconsLineElements) > 1:
					# A new chromosome has been reached
					newChromReached = True
					PhastconsChromInfo = PhastconsLineElements[1].split("=")
					PhastconsChrom = PhastconsChromInfo[1]
					PhastconsStartInfo = PhastconsLineElements[2].split("=")
					PhastconsIndex = int(PhastconsStartInfo[1])
					PhastconsLine = PhastconsFile.readline()
					PhastconsLineElements = PhastconsLine.split(" ")
				else:
					PhastconsIndex = PhastconsIndex + 1
			if stopReached == True:
				# The conservation information for this region cannot be obtained, so continue
				break
		if stopReached == True:
			# The conservation information for this region cannot be obtained, so continue
			continue
		if PhastconsChrom > chrom:
			# DNase conservation information is not in Phastcons file because a new chromosome has been reached in the Phastcons file
			conservationFile.write(str(-1))
			conservationFile.write("\n")
			continue
		while PhastconsIndex < location:
			# Go through bases until the location is reached
			PhastconsLine = PhastconsFile.readline()
			PhastconsLineElements = PhastconsLine.split(" ")
			if len(PhastconsLine) == 0:
				# There is no more conservation information, so do not record any conservation information for the region
				conservationFile.write(str(-1))
				conservationFile.write("\n")
				stopReached = True
				break
			if len(PhastconsLineElements) > 1:
				# At a new starting index for conservation scores
				PhastconsChromInfo = PhastconsLineElements[1].split("=")
				PhastconsChrom = PhastconsChromInfo[1]
				PhastconsStartInfo = PhastconsLineElements[2].split("=")
				if PhastconsChrom != chrom:
					# There is no more conservation information for the rest of the region, so do not compute its conservation
					conservationFile.write(str(-1))
					conservationFile.write("\n")
					PhastconsIndex = int(PhastconsStartInfo[1])
					stopReached = True
					break
				if int(PhastconsStartInfo[1]) != PhastconsIndex:
					# Modify PhastconsIndex appropriately
					PhastconsIndex = int(PhastconsStartInfo[1])
				# ASSUMES THAT THERE IS AT LEAST 1 CONSERVATION SCORE PER HEADING
				PhastconsLine = PhastconsFile.readline()
				PhastconsLineElements = PhastconsLine.split(" ")
			else:
				# Increment PhastconsIndex only when not at a new segment because the base in the header for a segment is the base of the segment's 1st score
				PhastconsIndex = PhastconsIndex + 1
		if stopReached == True:
			# The conservation information for this region cannot be obtained, so continue
			continue
		if (PhastconsChrom == chrom) and (PhastconsIndex == location):
			# There is a Phastcons score for the current location
			PhastconsScore = float(PhastconsLineElements[0])
		conservationFile.write(str(PhastconsScore))
		conservationFile.write("\n")
	SNPFile.close()
	PhastconsFile.close()
	conservationFile.close()

if __name__=="__main__":
    import sys
    SNPFileName = sys.argv[1]
    PhastconsFileName = sys.argv[2]
    conservationFileName = sys.argv[3]
    getConservationSNP(SNPFileName, PhastconsFileName, conservationFileName)
