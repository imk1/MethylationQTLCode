def divideBed (bedFileName, outputFileName):
	# Divide a bed file so that there is a separate line for each base
	bedFile = open(bedFileName)
	outputFile = open(outputFileName, 'w+')
	for line in bedFile:
		# Iterate through the lines in the bed file, and divide each line into a line for each base
		lineElements = line.split("\t")
		start = int(lineElements[1])
		end = int(lineElements[2])
		for i in range(start, end+1):
			# Iterate through the bases and write a line in the output file for each
			outputFile.write(lineElements[0] + "\t" + str(i) + "\t" + str(i) + "\n")
	bedFile.close()
	outputFile.close()

if __name__=="__main__":
   import sys
   bedFileName = sys.argv[1]
   outputFileName = sys.argv[2]
   divideBed (bedFileName, outputFileName)