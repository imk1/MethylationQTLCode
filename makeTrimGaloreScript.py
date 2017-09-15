def makeTrimGaloreScript(fastqFileListFileName, stringency, outputFilePath, scriptFileName):
	# Make a script that runs trim_galore on the fastq files in a list
	# ASSUMES THAT, IN THE FILE WITH NAME fastqFileListFileName, ALL PAIRS ARE LISTED TOGETHER, WITH THE LEFT READS FIRST
	fastqFileListFile = open(fastqFileListFileName)
	scriptFile = open(scriptFileName, 'w+')
	fastqFileList = fastqFileListFile.readlines()
	fastqFileListFile.close()
	fastqFileIndex = 0
	while fastqFileIndex < len(fastqFileList):
		# Iterate through the pairs of fastq files and make a call to TopHat for each pair
		fastqFileLeft = fastqFileList[fastqFileIndex].strip()
		fastqFileRight = fastqFileList[fastqFileIndex + 1].strip()
		fastqFileElements = fastqFileLeft.split("/")
		scriptFile.write("trim_galore --stringency " + str(stringency) + " -o " + outputFilePath + " --paired " + fastqFileLeft + " " + fastqFileRight + "\n")
		fastqFileIndex = fastqFileIndex + 2
	scriptFile.close()

if __name__=="__main__":
	import sys
	fastqFileListFileName = sys.argv[1]
	stringency = int(sys.argv[2])
	outputFilePath = sys.argv[3]
	scriptFileName = sys.argv[4]
	makeTrimGaloreScript(fastqFileListFileName, stringency, outputFilePath, scriptFileName)
