def convertMartLikeToMaskgenome(martLikeFileName, outputFileName):
	# Convert a file from Ensembl MART with Chromosome,Position,Minor allele (ALL),Variant Alleles to maskgenome format
	martLikeFile = open(martLikeFileName)
	outputFile = open(outputFileName, 'w+')
	martLikeFile.readline() # Remove the header
	for line in martLikeFile:
		# Iterate through the lines of the MART-like (alleles, chromosome, position; separated by space) file and convert each line to the format for maskgenome
		lineElements = line.strip().split(" ")
		alleles = lineElements[0].strip().split("/")
		minorAllele = alleles[1] # Might not be the minor allele
		majorAllele = alleles[0]
		outputFile.write(lineElements[1] + "\t" + lineElements[2] + "\t" + majorAllele + "\t" + minorAllele + "\n")
	martLikeFile.close()
	outputFile.close()

if __name__=="__main__":
	import sys
	martLikeFileName = sys.argv[1]
	outputFileName = sys.argv[2]
	convertMartLikeToMaskgenome(martLikeFileName, outputFileName)
