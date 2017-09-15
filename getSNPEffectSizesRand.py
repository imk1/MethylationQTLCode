def computeLogisticRegression(currentSNPs, currentMethyls, currentSamples, CVal):
	# Compute the logistic regression for the current SNP, methylation pair to determine the allele effect size
	samplesArray = np.vstack(currentSamples) # NOT .T
	enc = OneHotEncoder()
	samplesArrayDummyVariables = enc.fit_transform(samplesArray).toarray()

	SNPArray = np.vstack(currentSNPs)
	SNPSamplesArray = np.ma.concatenate((SNPArray[0], samplesArrayDummyVariables[0]), axis=0)
	for i in range(1, len(SNPArray)):
		# Add each SNP and dummy variable to SNPSamplesArray
		SNPSamplesArray = np.column_stack((SNPSamplesArray, np.ma.concatenate((SNPArray[i], samplesArrayDummyVariables[i]), axis=0)))
	methylsArray = np.hstack(currentMethyls)

	logRegr = linear_model.LogisticRegression(penalty='l2', dual=False, C=CVal, fit_intercept=True, intercept_scaling=1)
	logRegr.fit(SNPSamplesArray.T, methylsArray) # .T is necessary
	return logRegr


def outputEffectSizeRand(lastSNP, lastMethyl, currentSNPs, currentMethyls, currentSamples, minReadsCutoff, MAFCutoff, methylCutoff, effectSizesFile, CVal):
# Compute and output the effect size if the reads and MAF cutoffs are satisfied
	vecLen = len(currentMethyls)
	if vecLen >= minReadsCutoff:
		# The minimum reads cutoff is satisfied
		numRefAlleles = currentSNPs.count(0)
		numAltAlleles = currentSNPs.count(1)
		if (float(numRefAlleles)/float(vecLen) > MAFCutoff) and (float(numAltAlleles)/float(vecLen) > MAFCutoff):
			# Both alleles have sufficiently high frequencies
			numMethyl = currentMethyls.count(1)
			numUnmethyl = currentMethyls.count(0)
			if  (float(numMethyl)/float(vecLen) > methylCutoff) and (float(numUnmethyl)/float(vecLen) > methylCutoff):

				# The frequency of methylated and unmethylated reads is sufficient
				random.shuffle(currentMethyls) # Randomize the methylation states
				logRegr = computeLogisticRegression(currentSNPs, currentMethyls, currentSamples, CVal)
				effectSizesFile.write(lastSNP[0] + "\t" + str(lastSNP[1]) + "\t" + lastMethyl[0] + "\t" + str(lastMethyl[1]) + "\t" + str(logRegr.coef_[0][0]) + "\t" + str(logRegr.intercept_[0]))
				for i in range(1, len(logRegr.coef_[0])):
					# Output the effect size for each sample
					effectSizesFile.write("\t" + str(logRegr.coef_[0][i]))
				effectSizesFile.write("\n")
				

def getSNPEffectSizesRand(SNPMethylPlusFileName, effectSizesFileNamePrefix, minReadsCutoff, MAFCutoff, methylCutoff, CVal, iterNumber):
	# Compute the effect size for each SNP, C, but shuffle the methylation data first
	# ASSUMES THAT SNPMethylPlusFile IS SORTED BY METHYLATION CHROM., METHYLATION POSITION, SNP CHROM., SNP POSITION
	SNPMethylPlusFile = gzip.open(SNPMethylPlusFileName, 'rt')
	# Columns of SNPMethylPlusFile:
	# 1.  Read Name
	# 2.  SNP chromosome
	# 3.  SNP position in chromosome
	# 4.  1 or 0 indicating allele of SNP
	# 5.  Methylation chromosome
	# 6.  Methylation position in chromosome
	# 7.  1 or 0 indicating whether C is methylated (1 means methylated)
	# 8.  Number indicating which file (replicate and strand) read came from
	effectSizesFile = open(effectSizesFileNamePrefix + str(iterNumber), 'w+')
	# effectSizesFile will have the following information for each C, SNP pair that meets the cutoffs:
	# 1.  SNP chromosome
	# 2.  SNP position in chromosome
	# 3.  Methylation chromosome
	# 4.  Methylation position in chromosome
	# 5.  Effect size of SNP
	# 6.  Intercept term
	# 7+. Error terms for each replicate/strand
	lastSNP = ("", 0)
	lastMethyl = ("", 0)
	currentSNPs = []
	currentMethyls = []
	currentSamples = []
	random.seed()

	for line in SNPMethylPlusFile:
		# Iterate through the lines of the SNP methylation file and compute the correlation for each SNP, C pair
		lineElements = line.strip().split()
		currentSNP = (lineElements[1], int(lineElements[2]))
		currentMethyl = (lineElements[4], int(lineElements[5]))
		if (currentSNP != lastSNP) or (currentMethyl != lastMethyl):
			# At a new SNP or methylation location, so find the effect size for the previous one
			outputEffectSizeRand(lastSNP, lastMethyl, currentSNPs, currentMethyls, currentSamples, minReadsCutoff, MAFCutoff, methylCutoff, effectSizesFile, CVal)
			lastSNP = currentSNP
			lastMethyl = currentMethyl
			currentSNPs = []
			currentMethyls = []
			currentSamples = []
		currentSNPs.append(int(lineElements[3]))
		currentMethyls.append(int(lineElements[6]))
		currentSamples.append(int(lineElements[7]))

	outputEffectSizeRand(lastSNP, lastMethyl, currentSNPs, currentMethyls, currentSamples, minReadsCutoff, MAFCutoff, methylCutoff, effectSizesFile, CVal)
	SNPMethylPlusFile.close()
	effectSizesFile.close()


if __name__=="__main__":
	import sys
	import gzip
	import numpy as np
	from sklearn.preprocessing import OneHotEncoder
	from sklearn import linear_model
	import random
	SNPMethylPlusFileName = sys.argv[1] # Should end with .gz
	effectSizesFileNamePrefix = sys.argv[2]
	minReadsCutoff = int(sys.argv[3])
	MAFCutoff = float(sys.argv[4])
	methylCutoff = float(sys.argv[5])
	CVal = float(sys.argv[6]) # For minimal regularization, use approximately 1000000000
	iterNumber = int(sys.argv[7])

	getSNPEffectSizesRand(SNPMethylPlusFileName, effectSizesFileNamePrefix, minReadsCutoff, MAFCutoff, methylCutoff, CVal, iterNumber)
