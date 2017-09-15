def getMethylFracs(methylCallsFileName, CGMethylFracsFileName, CHMethylFracsFileName, CGMostMethylFracsFileName, CHMostMethylFracsFileName, minReadsCutoff, mostCutoff):
	# Get the fraction of methylated C's for CGs and CHs from the bascall.txt.gz file
	methylCallsFile = gzip.open(methylCallsFileName)
	CGMethylFracsFile = gzip.open(CGMethylFracsFileName, 'w+')
	CHMethylFracsFile = gzip.open(CHMethylFracsFileName, 'w+')
	CGMostMethylFracsFile = open(CGMostMethylFracsFileName, 'w+')
	CHMostMethylFracsFile = open(CHMostMethylFracsFileName, 'w+')
	
	for line in methylCallsFile:
		# Iterate through the methylation calls and compute the fraction of methylated Cs
		lineElements = line.strip().split("\t")
		numMethyl = int(lineElements[4])
		numUnmethyl = int(lineElements[3])
		fracMethyl = float(numMethyl)/float(numMethyl + numUnmethyl)
		totalReads = numMethyl + numUnmethyl
		
		if lineElements[2] == "CG":
			# At a CG, so record information in the CG output files
			CGMethylFracsFile.write(lineElements[0] + "\t" + lineElements[1] + "\t" + str(numMethyl) + "\t" + str(totalReads)  + "\t" + str(fracMethyl) + "\n")
			if (totalReads >= minReadsCutoff) and (fracMethyl >= mostCutoff):
				# There are enough reads and enough methylated CGs to record the information in the most output file
				CGMostMethylFracsFile.write(lineElements[0] + "\t" + lineElements[1] + "\t" + str(numMethyl) + "\t" + str(totalReads)  + "\t" + str(fracMethyl) + "\n")
		
		else:
			CHMethylFracsFile.write(lineElements[0] + "\t" + lineElements[1] + "\t" + str(numMethyl) + "\t" + str(totalReads)  + "\t" + str(fracMethyl) + "\n")
			if (totalReads >= minReadsCutoff) and (fracMethyl >= mostCutoff):
				# There are enough reads and enough methylated CHs to record the information in the most output file
				CHMostMethylFracsFile.write(lineElements[0] + "\t" + lineElements[1] + "\t" + str(numMethyl) + "\t" + str(totalReads)  + "\t" + str(fracMethyl) + "\n")
	
	methylCallsFile.close()
	CGMethylFracsFile.close()
	CHMethylFracsFile.close()
	CGMostMethylFracsFile.close()
	CHMostMethylFracsFile.close()


if __name__=="__main__":
	import sys
	import gzip
	methylCallsFileName = sys.argv[1]
	CGMethylFracsFileName = sys.argv[2]
	CHMethylFracsFileName = sys.argv[3]
	CGMostMethylFracsFileName = sys.argv[4]
	CHMostMethylFracsFileName = sys.argv[5]
	minReadsCutoff = int(sys.argv[6])
	mostCutoff = float(sys.argv[7])

	getMethylFracs(methylCallsFileName, CGMethylFracsFileName, CHMethylFracsFileName, CGMostMethylFracsFileName, CHMostMethylFracsFileName, minReadsCutoff, mostCutoff)