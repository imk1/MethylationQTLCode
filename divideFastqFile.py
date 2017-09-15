def divideFastqFile(fastqFileName, numLinesPerOutputFile):
	# Divide the fastq file into multiple files
	# ASSUMES THAT fastqFileName INCLUDES THE COMPLETE PATH AND NOT ../
	fastqFileNameElements = fastqFileName.split(".")
	outputFileCount = 1
	outputFileName = fastqFileNameElements[0][0:-1] + str(outputFileCount) + "_" + fastqFileNameElements[0][-1] + ".fq.gz" # Add output file number
	fastqFile = gzip.open(fastqFileName)
	outputFile = gzip.open(outputFileName, 'w+')
	line = fastqFile.readline()
	lineCount = 1
	while line != "":
		# Iterate through the fastq file, writing each line to it smaller output file
		for i in range(4):
			# Write the next 4 lines of the fastq file to the output file
			outputFile.write(line)
			line = fastqFile.readline()
		lineCount = lineCount + 4
		if lineCount > numLinesPerOutputFile:
			# The current output file has the maximum number of lines
			outputFile.close()
			outputFileCount = outputFileCount + 1
			outputFileName = fastqFileNameElements[0][0:-1] + str(outputFileCount) + "_" + fastqFileNameElements[0][-1] + ".fq.gz" # Add output file number
			outputFile = gzip.open(outputFileName, 'w+')
			lineCount = 1
	outputFile.close()
	fastqFile.close()
	
if __name__=="__main__":
   import sys
   import gzip
   fastqFileName = sys.argv[1] # Should end with .gz
   numLinesPerOutputFile = int(sys.argv[2])
   divideFastqFile(fastqFileName, numLinesPerOutputFile)
