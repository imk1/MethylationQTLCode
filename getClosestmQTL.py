def getClosestmQTL(SNPLocationFileName, CpGLocationFileName, closestmQTLFileName):
	# For each CpG with an mQTL, finds the closest mQTL
	# closestmQTLFile includes:
	# 1.  SNP chromosome
	# 2.  SNP position
	# 3.  CpG chromosome
	# 4.  CpG position
	# 5.  Distance between SNP and CpG
	SNPLocationFile = open(SNPLocationFileName)
	CpGLocationFile = open(CpGLocationFileName)
	closestmQTLFile = open(closestmQTLFileName, 'w+')
	# ASSUMES THAT CpGLocationFile is sorted by chromosome, position
	lastCpG = ("", 0)
	closestSNPForCpG = ("", 0)
	closestDistance = float("inf")
	for line in CpGLocationFile:
		# Iterate through the mQTLs and record the closest mQTL for each CpG with an mQTL
		lineElements = line.strip().split("\t")
		currentCpG = (lineElements[0], int(lineElements[1]))
		SNPLineElements = SNPLocationFile.readline().strip().split("\t")
		currentSNP = (SNPLineElements[0], int(SNPLineElements[1]))
		if currentCpG != lastCpG:
			# At a new CpG, so record the information from the last CpG
			if lastCpG[0] != "":
				# Not at the beginning of the file
				closestmQTLFile.write(closestSNPForCpG[0] + "\t" + str(closestSNPForCpG[1]) + "\t" + lastCpG[0] + "\t" + str(lastCpG[1]) + "\t" + str(closestDistance) + "\n")
			lastCpG = currentCpG
			closestSNPForCpG = currentSNP
			closestDistance = abs(currentSNP[1] - currentCpG[1])
		else:
			distance = abs(currentSNP[1] - currentCpG[1])
			# ASSUMES THAT ALL mQTLs ARE ON THE SAME CHROMOSOME AS THEIR CpG
			if distance < closestDistance:
				# CHOOSES THE FIRST LISTED SNP WHEN THERE ARE TIES
				closestSNPForCpG = currentSNP
				closestDistance = distance
	closestmQTLFile.write(closestSNPForCpG[0] + "\t" + str(closestSNPForCpG[1]) + "\t" + lastCpG[0] + "\t" + str(lastCpG[1]) + "\t" + str(closestDistance))
	SNPLocationFile.close()
	CpGLocationFile.close()
	closestmQTLFile.close()
	
if __name__=="__main__":
	import sys
	SNPLocationFileName = sys.argv[1]
	CpGLocationFileName = sys.argv[2]
	closestmQTLFileName = sys.argv[3]
	getClosestmQTL(SNPLocationFileName, CpGLocationFileName, closestmQTLFileName)
				