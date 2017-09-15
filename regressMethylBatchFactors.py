def processMethylBatchFactorsLine(methylBatchFactorsLine):
	# Process a line of the methylation batch factors file
	lineElements = methylBatchFactorsLine.strip().split("\t")
	read = lineElements[0]
	location = (lineElements[1], int(lineElements[2]))
	label = int(lineElements[3])

	featureElements = lineElements[4:]
	return [read, location, label, featureElements]


def updateInfo(read, label, featureElements, currentReads, currentLabels, currentFeatures, numFeatures):
	# Update the read, label, and feature information
	currentReads.append(read)
	currentLabels.append(label)

	for i in range(numFeatures):
		# Iterate through the features for the current read and add each to its feature list
		currentFeatures[i].append(int(featureElements[i]))
	return [currentReads, currentLabels, currentFeatures]


def computeRegression(currentLabels, currentFeatures):
	# Find the residuals for the current features
	featureArray = np.vstack(currentFeatures).T
	enc = OneHotEncoder()
	featureArrayDummyVariables = enc.fit_transform(featureArray).toarray()

	regr = linear_model.LinearRegression()
	regr.fit(featureArrayDummyVariables, currentLabels)
	residuals = currentLabels - regr.predict(featureArrayDummyVariables)
	return residuals


def outputResiduals(currentReads, location, residuals, residualsFile):
	# Output the reads, location, and methylation residuals
	for i in range(len(currentReads)):
		# Iterate through the current reads and output each read's information
		residualsFile.write(currentReads[i] + "\t" + location[0] + "\t" + str(location[1]) + "\t" + str(residuals[i]) + "\n")

def regressMethylBatchFactors(methylBatchFactorsFileName, numFeatures, residualsFileName):
	# Compute the residual for the methylation for each C in each read
	# ASSUMES THAT THE FILE IS SORTED BY CHROMOSOME, THEN POSITION ON CHROMOSOME
	methylBatchFactorsFile = gzip.open(methylBatchFactorsFileName)
	residualsFile = gzip.open(residualsFileName, 'w+')
	# residualsFile will have the following information for each C on each read:
	# 1.  Read name (without base pair)
	# 2.  Chromosome
	# 3.  Position on chromosome
	# 4.  Methylation residual
	currentReads = []
	currentLabels = []
	currentFeatures = []
	for i in range(numFeatures):
		# Initialize all of the current feature lists (need separate list for each feature, NOT each read)
		currentFeatures.append([])
	[read, lastLocation, label, featureElements] = processMethylBatchFactorsLine(methylBatchFactorsFile.readline())
	[currentReads, currentLabels, currentFeatures] = updateInfo(read, label, featureElements, currentReads, currentLabels, currentFeatures, numFeatures)

	for line in methylBatchFactorsFile:
		# Iterate through the reads and, when reaching a C at a new location, find the residuals for the previous C
		[read, location, label, featureElements] = processMethylBatchFactorsLine(line)
		if location == lastLocation:
			# The location has not changed, so add reads, labels, and features to the current information
			[currentReads, currentLabels, currentFeatures] = updateInfo(read, label, featureElements, currentReads, currentLabels, currentFeatures, numFeatures)

		else:
			residuals = computeRegression(currentLabels, currentFeatures)
			outputResiduals(currentReads, lastLocation, residuals, residualsFile)
			currentReads = []
			currentLabels = []
			currentFeatures = []
			for i in range(numFeatures):
				# Initialize all of the current feature lists (need separate list for each feature, NOT each read)
				currentFeatures.append([])
			[currentReads, currentLabels, currentFeatures] = updateInfo(read, label, featureElements, currentReads, currentLabels, currentFeatures, numFeatures)
			lastLocation = location
	outputResiduals(currentReads, location, residuals, residualsFile)

	methylBatchFactorsFile.close()
	residualsFile.close()


if __name__=="__main__":
	import sys
	import gzip
	import numpy as np
	from sklearn.preprocessing import OneHotEncoder
	from sklearn import linear_model
	methylBatchFactorsFileName = sys.argv[1] # Should end with .gz
	numFeatures = int(sys.argv[2])
	residualsFileName = sys.argv[3] # Should end with .gz

	regressMethylBatchFactors(methylBatchFactorsFileName, numFeatures, residualsFileName)
