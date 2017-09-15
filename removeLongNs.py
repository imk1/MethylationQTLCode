def removeLongNs(genomeFileName, genomeNsRemovedFileName, numNsToRemove):
	# Remove long stretches of Ns in the genome
	# ASSUMES THAT EACH ENTRY IN genomeFile IS FOR ITS OWN CHROMOSOME
	genomeFile = open(genomeFileName)
	NStr = ""
	for i in range(len(numNsToRemove)):
		# Add an N to the NStr to make a String of Ns that is numNsToRemove long
		NStr = NStr + "N"
	genomeNsRemovedFile = open(genomeNsRemovedFileName, 'w+')
	for record in SeqIO.parse(genomeFile, "fasta"):
		# Iterate through the chromosomes and record the parts of each that do not contain long stretches of Ns
		currentStart = 0 # 0-INDEXING BECAUSE SAM FILES ARE 1-INDEXED (true index will be currentStart + sam index)
		sequence = record.seq
		NsToRemoveLocations = sequence.find(NStr)
		for i in range(len(NsToRemoveLocations)):
			# Iterate through the locations of Ns that are too long and create a new line of the fasta file for each region between them
			sequencePart = sequence[currentStart:i]
			#FINISH!!!!!!!!!!
