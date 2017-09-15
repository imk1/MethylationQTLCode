python getMethylationBetas.py ../Moen2013Data/GSE39672_matrix_processed.txt ../Moen2013Data/CpG_list.txt ../HapmapIndividualsMethylSorted ../Moen2013Data/betasIndividualsMethylPlus

python convertCpGsToLocations.py ../Moen2013Data/GSE39672_RAW.tar_FILES/IlluminaIDTohg19Position ../Moen2013Data/betasIndividualsMethylPlus ../Moen2013Data/locationsBetasIndividualsMethylPlus

sort -k1,1 -k2,2n ../Moen2013Data/locationsBetasIndividualsMethylPlus > ../Moen2013Data/locationsBetasIndividualsMethylPlusSorted

grep -P 'chr1\t' ../Moen2013Data/locationsBetasIndividualsMethylPlusSorted | sort -k1,1 -k2,2n > ../Moen2013Data/chr1_locationsBetasIndividualsMethylPlusSorted

cut -f1,2 ../Moen2013Data/locationsBetasIndividualsMethylPlusSorted > ../Moen2013Data/CpGSiteshg19SortedPlus

python getSNPOverlapPlusPlus.py ../Moen2013Data/CpGSiteshg19SortedPlus ../HiseqDataProcessed/HiseqDataSNPsMethyl/chrAll_CpG_fisherExact0005Reads ../HiseqDataProcessed/HiseqDataSNPsMethyl/chrAll_CpG_fisherExact0005Reads_MoenOverlapMoenCpGsPlus 2 3

python getSNPOverlapPlusPlus.py ../Moen2013Data/CpGSiteshg19SortedPlus ../HiseqDataProcessed/HiseqDataSNPsMethyl/chrAll_CpG_fisherExactRand0005Reads1 ../HiseqDataProcessed/HiseqDataSNPsMethyl/chrAll_CpG_fisherExactRand0005Reads1_MoenOverlapMoenCpGsPlus 2 3

cut -f2,4 ../HiseqDataProcessed/HiseqDataSNPsMethyl/chr1_CpG_All_SNPsMethyl_LDGrouped_sorted_fisherExact0005Reads > ../HiseqDataProcessed/HiseqDataSNPsMethyl/chr1_CpG_All_SNPsMethyl_LDGrouped_sorted_fisherExact0005Reads_positions


python getSNPMethylOverlap.py ../HiseqDataProcessed/mQTLData/chrAll_CpG_fisherExact0005MoenpVal001_mQTLs ../Moen2013Data/chrAll_mQTLs003 ../HiseqDataProcessed/mQTLData/mQTLMoenPlus001003Overlap

python getSNPMethylOverlap.py ../Moen2013Data/chrAll_mQTLs003 ../HiseqDataProcessed/mQTLData/chrAll_CpG_fisherExact0005MoenpVal001_mQTLs ../Moen2013Data/chrAll_mQTLs003_Pooled001Overlap

cut -f3,4 ../HiseqDataProcessed/mQTLData/chrAll_CpG_fisherExact0005MoenpVal001_mQTLs | sort -u -k1,1 -k2,2n > ../HiseqDataProcessed/mQTLData/chrAll_CpG_fisherExact0005MoenpVal001_mQTLCpGs

cut -f3,4 ../Moen2013Data/chrAll_mQTLs003 | sort -u -k1,1 -k2,2n > ../Moen2013Data/chrAll_mQTLs003_CpGs

python getSNPOverlap.py ../HiseqDataProcessed/mQTLData/chrAll_CpG_fisherExact0005MoenpVal001_mQTLCpGs ../Moen2013Data/chrAll_mQTLs003_CpGs ../HiseqDataProcessed/mQTLData/mQTLCpGMoenPlus001Overlap
