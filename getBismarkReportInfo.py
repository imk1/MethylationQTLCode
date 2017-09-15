def makePairDict(pairDictFileName):
	# Make a dictionary that maps (column 1, column 2) to column 3
	pairDict = {}
	pairDictFile = open(pairDictFileName)

	for line in pairDictFile:
		# Iterate through the lines of the file and make an entry for each in the dictionary
		lineElements = line.strip().split("\t")
		pairDict[(lineElements[0], lineElements[1])] = int(lineElements[2])

	pairDictFile.close()
	return pairDict


def makeIntList(intFileName):
	# Make a list of integers from a file
	intFile = open(intFileName)
	intList = []

	for line in intFile:
		# Iterate through the lines of the file and add the int in each to the list
		intList.append(int(line.strip()))

	intFile.close()
	return intList


def getBismarkReportInfo(bismarkReportFileListFileName, poolInfoFileName, reportInfoLinesFileName, outputFileName):
	# Get the methylation information from each report
	# For each Bismark report, output the following:
	# 1.  Bar code
	# 2.  Pool
	# 3.  Flowcell
	# 4.  Lane
	# 5.  Number of paired-end alignments with a unique best hit
	# 6.  Mapping efficiency
	# 7.  Number of C's measured
	# 8.  Percentage of C's methylated in CpG context
	# 9.  Percentage of C's methylated in CHG context
	# 10.  Percentage of C's methylated in CHH context
	poolInfoDict = makePairDict(poolInfoFileName)
	reportInfoLines = makeIntList(reportInfoLinesFileName)
	bismarkReportFileListFile = open(bismarkReportFileListFileName)
	outputFile = open(outputFileName, 'w+')

	for line in bismarkReportFileListFile:
		# Iterate through the Bismark reports and find the information for each
		lineElements = line.strip().split("/")
		bismarkReportFileName = lineElements[-1].split("_")
		flowcell = bismarkReportFileName[3]
		lane = bismarkReportFileName[4]
		pool = poolInfoDict[(flowcell, lane)]
		barCode = bismarkReportFileName[5]
		outputFile.write(barCode + "\t" + str(pool) + "\t" + flowcell + "\t" + lane)

		bismarkReportFile = open(line.strip())
		bismarkReportFileLines = bismarkReportFile.readlines()
		bismarkReportFile.close()
		for ril in reportInfoLines:
			# Iterate through the lines of interest and record each in the ouput file
			rilElements = bismarkReportFileLines[ril].strip().split()
			info = rilElements[-1]
			outputFile.write("\t" + info)
		outputFile.write("\n")

	bismarkReportFileListFile.close()
	outputFile.close()


if __name__=="__main__":
	import sys
	bismarkReportFileListFileName = sys.argv[1]
	poolInfoFileName = sys.argv[2]
	reportInfoLinesFileName = sys.argv[3]
	outputFileName = sys.argv[4]

	getBismarkReportInfo(bismarkReportFileListFileName, poolInfoFileName, reportInfoLinesFileName, outputFileName)
