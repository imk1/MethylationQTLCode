def getCHHLocations(genomeFileName, CHHLocationsFileName):
	# Get the locations of all CHHs in the genome
	genomeFile = open(genomeFileName)
	CHHLocationsFile = open(CHHLocationsFileName, 'w+')
	
	for record in SeqIO.parse(genomeFile, "fasta"):
		# Iterate through the parts of the fasta file and record the locations of the CHHs in each
		# ASSUMES THAT THERE IS AN ENTRY FOR EACH CHROMOSOME
		chrom = record.id
		print chrom
		sequence = record.seq
		
		for i in range(0, len(sequence) - 2):
			# Iterate through the bases in the current fasta section and record those that are CHHs
			if (string.upper(str(sequence[i])) == "C") and ("G" not in string.upper(str(sequence[i+1:i+3]))):
				# At a CHH, so record the location
				CHHLocationsFile.write(chrom + "\t" + str(i + 1) + "\t" + str(i + 3) + "\n") # ADDING 1 BECAUSE SAM FILES ARE 1-INDEXED
				
	genomeFile.close()
	CHHLocationsFile.close()

if __name__=="__main__":
	import sys
	import string
	from Bio import SeqIO
	genomeFileName = sys.argv[1]
	CHHLocationsFileName = sys.argv[2]

	getCHHLocations(genomeFileName, CHHLocationsFileName)