maskgenome <- function(genome="UCSC",SNPs="dbsnp",gbuild=c("hg18","hg19"),genomestored=FALSE,SNPsstored=FALSE,genomeloc=NA,SNPsloc=NA,liblocation=NULL,masktech=c("N","nonseg"),numchrom=22) {

# Code written by Trevor Martin
# Modified by Irene Kaplow

# This code replaces SNPs in a genome with Ns or the other allele.
# This code requires Bioconductor (source) and will be faster if BiocGenerics, IRanges, Biostrings, GenomicRanges, and BSgenome are downloaded in advance
# Need to include all inputs

cat("Loading required packages..."); flush.console()
require(BiocGenerics,lib.loc=liblocation)
require(IRanges,lib.loc=liblocation)
require(Biostrings,lib.loc=liblocation)
require(GenomicRanges,lib.loc=liblocation)
require(BSgenome,lib.loc=liblocation)
cat("...done.\n"); flush.console()

if(numchrom <= 0) { # ADDED: Sanity check to make sure that at least 1 chromosome will be used
	cat("WARNING: YOUR INPUT FOR numchrom WILL GIVE YOU EMPTY OUTPUT; USE numchrom >= 1.\n")
}
if(genome=="UCSC") { # Sanity check and to allow for extended genome support
    if(genomestored==FALSE) {
        cat("Loading Genome from online respository..."); flush.console()
        if(gbuild=="hg19") {
            require("BSgenome.Hsapiens.UCSC.hg19",lib.loc=liblocation) # Loads the reference genome from Bioconductor
            # Reference genome is stored as the object "Hsapiens" can access chromosomes by
            # using for example Hsapiens$chr1
        }
        if(gbuild=="hg18") {
            require("BSgenome.Hsapiens.UCSC.hg18",lib.loc=liblocation)
        }
        cat("...finished.\n"); flush.console()
    }
    if(genomestored==TRUE) {
        cat("WARNING: THIS MODE ONLY SUPPORTED FOR UCSC GENOME VERSIONS\n")
        cat("Loading Genome from local file..."); flush.console()
        Hsapiens = read.DNAStringSet(genomeloc) # Load the reference genome from local file, must be FASTA format
        # If in proper format reference genome should be accessible as above
        cat("finished.\n"); flush.console()
        # ONLY SUPPORTED FOR MASKING IF UCSC GENOME VERSION
    }
}
if(SNPs=="dbsnp") { # Sanity check and to allow for extended polymorphism support
	# ADDED numchrom AS INPUT (default is 22)
    #numchrom = 22 # Only want the 22 autosomal chromosomes (changing this can be an added option later)
    if(SNPsstored==FALSE) {
        cat("Loading SNPs from online repository..."); flush.console()
        require("SNPlocs.Hsapiens.dbSNP.20101109",lib.loc=liblocation) # Loads the SNP locations from Bioconductor
        chromquer = paste("ch",1:22,sep="") # Correct querying format for the getSNPlocs() command
        HsapiensSNPs = vector("list",numchrom) # Stores the SNP locations and alleles
        cat("...annotating SNPs..."); flush.console()
        for(i in 1:numchrom) {
            HsapiensSNPs[[i]] = getSNPlocs(chromquer[i]) # Returns a data.frame with the columns in the following order: rs ID (no duplicates), alleles at each SNP, and loc (relative to first base
        # on 5' end of reference sequence)
        }
        cat("finished.\n"); flush.console()
    }
    if(SNPsstored==TRUE) {
        cat("WARNING: SNP DATA FILE MUST BE IN CORRECT FORMAT, TAB DELIMITED, AND USE CONSISTENT BUILD COORDINATES\n")
        cat("Correct format:\nOne row for each SNP, SNPs must be in same order as SNP columns of genotype file used in calculateprechipfreq().\n- Column 1: chr #\n- Column 2: SNP location on chr\n- Column 3: Major Allele\n- Column 4: Minor Allele\n")
        HsapiensSNPsh = read.table(file=SNPsloc,sep="\t",header=F,stringsAsFactors=FALSE) # Read in the stored SNP data
        # SNPs should be from build consistent with genome build
        # Stratify data by chromosome
        HsapiensSNPs = vector("list",numchrom) # Stores the SNP locations and alleles
        cat("...annotating SNPs"); flush.console()
        for(i in 1:numchrom) {
            HsapiensSNPstemp = HsapiensSNPsh[which(HsapiensSNPsh[,1]==i),-1] # Extracts all data for SNPs on this chromosome except the chromosome data
            # Rearrange columns to match dbSNP input so that later calculations can work correctly for either
            majminallelehold = paste(HsapiensSNPstemp[,2],HsapiensSNPstemp[,3],sep="") # Collapse major and minor allele into one string
            #iupacholdcodes = mergeIUPACLetters(majminallelehold) # Convert major minor allele combination to IUPAC code (not used now as very time consuming)
            iupacholdcodes = majminallelehold
            HsapiensSNPstemp2 = cbind(1:nrow(HsapiensSNPstemp),iupacholdcodes,as.numeric(HsapiensSNPstemp[,1])) # Then reorder columns and add dummy "rs ID" column
            nacheck = which(is.na(as.numeric(HsapiensSNPstemp[,1]))) # Some "SNPs" are labeled as indels and stuff, throw these out for now (this is where NA warnings come from)
            if(length(nacheck)>0) {
            HsapiensSNPstemp2 = HsapiensSNPstemp2[-nacheck,]
            }
            HsapiensSNPs[[i]] = HsapiensSNPstemp2 # Save result
        }
        cat("...finished.\n"); flush.console()
    }
}

cat("Masking genome...\n"); flush.console()

if(masktech=="N") {
    cat("Masking Technique: Replace with N.\n")
    # Each SNP will be masked by switching the base pair to a N, the ambiguous SNP character
    # Mask each SNP by replacing it with N
    Hsapiensmasked = NULL # Initialize for DNAStringSet object
    for(i in 1:numchrom) {
        holdchr = Hsapiens[[paste("chr",i,sep="")]] # Pulls out the current chromosome's sequence
        #holdchrum = Biostrings::unmasked(holdchr) # Unmasks the sequence so that letters can be replaced
        #holdreplaced = Biostrings::replaceLetterAt(holdchrum, at=as.numeric(HsapiensSNPs[[i]][,3]), letter=rep("N",length(HsapiensSNPs[[i]][,3]))) # Replaces each SNP with non-segregating allele
        holdreplaced = Biostrings::replaceLetterAt(holdchr, at=as.numeric(HsapiensSNPs[[i]][,3]), letter=rep("N",length(HsapiensSNPs[[i]][,3]))) # Replaces each SNP with non-segregating allele
		holdreplaced = DNAStringSet(holdreplaced) # Turn into string set object from string object
        Hsapiensmasked = append(Hsapiensmasked, holdreplaced) # Store everything in DNAStringSet object for output later
        names(Hsapiensmasked)[i] = paste("chr",i,sep="") # Store chromosome names
    }
}

if(masktech=="nonseg") {
    cat("Masking Technique: Replace with non-segregating allele.\n")
    # Each SNP will be masked by switching the base pair to a non-segregating allele
    # e.g. A/G -> T
    iupacinfo = IUPAC_CODE_MAP # From Biostrings package
    code = labels(iupacinfo) # IUPAC codes
    alleles = as.character(iupacinfo) # IUPAC alleles
    VariationChart = cbind(code, alleles)
    nonseg = c("N","N","N","N","T","T","G","T","G","C","T","G","C","A","N") # Non-segregatting allele analogs to IUPAC data
    VariationChart = cbind(VariationChart, nonseg)# Adding the appropriate non-segregating allele data, N for those that are not SNPs/not replaceable
    # Determine an appropriate non-segregating allele based on IUPAC ambiguity letter for each SNP
    nsalleles = vector("list",numchrom)
    for(i in 1:numchrom) {
        holdalleles = HsapiensSNPs[[i]][,2] # Pull out current chromosome's SNP alleles
        matchalleles = match(holdalleles,VariationChart[,1]) # Determines which code is present
        nsalleles[[i]] = VariationChart[,3][matchalleles] # Determines nonsegregating version
    }
    # Mask each SNP by replacing it with the given non-segregating allele
    Hsapiensmasked = NULL # Initialize for DNAStringSet object
    for(i in 1:numchrom) {
        holdchr = Hsapiens[[paste("chr",i,sep="")]] # Pulls out the current chromosome's sequence
        holdchrum = unmasked(holdchr) # Unmasks the sequence so that letters can be replaced
        holdreplaced = replaceLetterAt(holdchrum, at=HsapiensSNPs[[i]][,3], letter=nsalleles[[i]]) # Replaces each SNP with non-segregating allele
        holdreplaced = DNAStringSet(holdreplaced) # Turn into string set object from string object
        Hsapiensmasked = append(Hsapiensmasked, holdreplaced) # Store everything in DNAStringSet object for output later
        names(Hsapiensmasked)[i] = paste("chr",i,sep="") # Store chromosome names
        # Note: <1% of SNPs map incorrectly between UCSC and NCBI
    }
}

cat("Finished.\n"); flush.console()

maskeddata = list(Hsapiensmasked=Hsapiensmasked,Hsapiens=Hsapiens,HsapiensSNPs=HsapiensSNPs)
return(maskeddata)
}


