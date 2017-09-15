def getCigarList(bismarkCigar):
	# Get the list of the elements in the cigar
	cigarList = []
	cigarNumStr = ""
	
	for bc in bismarkCigar:
		# Iterate through the characters in the Cigar string and divide the string into parts
		if (bc == "M") or ((bc == "D") or (bc == "I")):
			# At a breaking point between parts
			cigarList.append((int(cigarNumStr), bc))
			cigarNumStr = ""
		
		else:
			cigarNumStr = cigarNumStr + bc
	return cigarList
	

def getBismarkEnd(cigarList, position):
	# Find the end of the read
	bismarkEnd = position
	for cl in cigarList:
		# Iterate through the parts of the cigar and update the end appropriately
		if cl[1] == "M":
			# At a match, so add the number of matches to the end
			bismarkEnd = bismarkEnd + cl[0]
		
		elif cl[1] == "D":
			# At a deletion, so add the number of missing bases
			bismarkEnd = bismarkEnd + cl[0]
		
		elif cl[1] == "I":
			# At an insertion, so do not add anything
			continue
	return bismarkEnd


def getBaseQualityMethylStatus(bamFileName, methylLetter, unmethylLetter, outputFileName):
	# Get the base quality and methylation status for each cytosine
	bamFile = pysam.Samfile(bamFileName)
	usedReads = []
	outputFile = open(outputFileName, 'w+')
	
	for read in bamFile.fetch():
		# Iterate through the reads in a sam file and find the quality and methylation status of each base
		if read.qname in usedReads:
			# The read has already been processed when its mate was processed earlier
			usedReads.remove(read.qname)
			continue
		usedReads.append(read.qname)
		readQuals = read.qual
		readMethylCalls = read.tags[2][1]
		for i in range(len(readMethylCalls)):
			# Iterate through the bases on the first read and record the methylation statuses and corresponding qualities
			rmc = readMethylCalls[i]
			if rmc == methylLetter:
				# The current bases is a methylated cytosine, so record the quality and the methylation status
				outputFile.write(str(ord(readQuals[i]) - 33) + "\t1\n")
			elif rmc == unmethylLetter:
				# The current base is an unmethylated cytosine, so record the quality and the methylation status
				outputFile.write(str(ord(readQuals[i]) - 33) + "\t0\n")
		
		pointer = bamFile.tell()
		try: 
			mate = bamFile.mate(read)
			# The read has a mate, so record its methylation information
			mateMethylCalls = mate.tags[2][1]
			mateQuals = mate.qual
			cigarList = getCigarList(read.cigarstring)
			readEnd = getBismarkEnd(cigarList, read.pos)
			mateStartForMethyl = mate.pos
			if mateStartForMethyl < readEnd:
				# Move the mate start for methylation to the first base in the mate that does not overlap the read
				mateStartForMethyl = readEnd + 1
			for i in range(mateStartForMethyl - mate.pos, len(mateMethylCalls)):
				# Iterate through the bases in the mate and record the methylation statuses and the corrsponding qualities
				mmc = mateMethylCalls[i]
				if mmc == methylLetter:
					# The current bases is a methylated cytosine, so record the quality and the methylation status
					outputFile.write(str(ord(mateQuals[i]) - 33) + "\t1\n")
				elif mmc == unmethylLetter:
					# The current base is an unmethylated cytosine, so record the quality and the methylation status
					outputFile.write(str(ord(mateQuals[i]) - 33) + "\t0\n")
		except ValueError:
			# Invalid/No mate (maybe due to duplicate removal)
			print "No mate!"
			continue
		finally:
			bamFile.seek(pointer) # Return the BAM file to the position of the first read in the pair
	
	bamFile.close()
	outputFile.close()


if __name__=="__main__":
   import sys
   import pysam
   bamFileName = sys.argv[1]
   methylLetter = sys.argv[2]
   unmethylLetter = sys.argv[3]
   outputFileName = sys.argv[4]
   
   getBaseQualityMethylStatus(bamFileName, methylLetter, unmethylLetter, outputFileName)
	
