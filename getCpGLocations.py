def getCpGLocations(genomeFileName, CpGLocationsFileName):
	# Get the locations of all CpGs in the genome
	genomeFile = open(genomeFileName)
	CpGLocationsFile = open(CpGLocationsFileName, 'w+')
	
	for record in SeqIO.parse(genomeFile, "fasta"):
		# Iterate through the parts of the fasta file and count the number of CpGs in each
		# ASSUMES THAT THERE IS AN ENTRY FOR EACH CHROMOSOME
		chrom = record.id
		sequence = record.seq
		
		for i in range(0, len(sequence) - 1):
			# Iterate through the bases in the current fasta section and record those that are CpGs
			if string.upper(str(sequence[i:i+2])) == "CG":
				# At a CpG, so record the location
				CpGLocationsFile.write(chrom + "\t" + str(i + 1) + "\t" + str(i + 2) + "\n") # ADDING 1 BECAUSE SAM FILES ARE 1-INDEXED
				
	genomeFile.close()
	CpGLocationsFile.close()

if __name__=="__main__":
	import sys
	import string
	from Bio import SeqIO
	genomeFileName = sys.argv[1]
	CpGLocationsFileName = sys.argv[2]

	getCpGLocations(genomeFileName, CpGLocationsFileName)