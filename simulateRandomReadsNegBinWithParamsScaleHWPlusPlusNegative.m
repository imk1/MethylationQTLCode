function [pValsPooled, pValsIndivsGenotype] = simulateRandomReadsNegBinWithParamsScaleHWPlusPlusNegative(numAlleles, negBinParams, numReadsMean, numReads, numSimulations, MAF)
% In these simulations, assume that there is no relationship between the
% allele and the methylation status
% Simulate random reads and compute the number of mQTLs for pooled data
% and individuals data with associations between genotype and average 
% methylation, where numbers of reads are drawn from a negative binomial 
% distribution whose parameters have been inputted
% For traditional method, simulate the number of reads in the same way as
% for the pooled method and then randomly distribute the reads across the
% individuals

numIndivs = numAlleles/2;
indivsAlleles = zeros(numIndivs, 2);
numIndivsAltAlt = round(numIndivs * (MAF ^ 2));
numIndivsRefAlt = round(numIndivs * 2 * (1 - MAF)  * MAF);
indivsAlleles(1:numIndivsAltAlt, :) = 1;
indivsAlleles(numIndivsAltAlt + 1:numIndivsAltAlt + numIndivsRefAlt, 1) = 1;
alleles = vertcat(indivsAlleles(:,1), indivsAlleles(:,2));

methyls = zeros(size(alleles));
allelesZeroIndexes = find(alleles == 0);
allelesOneIndexes = find(alleles == 1);
%methyls(allelesOneIndexes(1:round(MAF*length(allelesOneIndexes)))) = 1;
%methyls(allelesZeroIndexes(1:round((1-MAF)*length(allelesOneIndexes)))) = 1;
for i = 1:length(allelesOneIndexes)
    % Iterate through the alternate allele locations and set MAF*length of
    % them to 0
    if (mod(i, round(length(allelesOneIndexes)/(MAF*length(allelesOneIndexes)))) == 0) && (length(find(methyls == 1)) < round(MAF*length(allelesOneIndexes)))
        % Set the current methylation status to 0
        % 2nd and makes sure that additional 1 methylation statuses are not
        % created due to rounding
        methyls(allelesOneIndexes(i)) = 1;
    end
end
for i = 1:length(allelesZeroIndexes)
    % Iterate through the reference allele locations and set (1-MAF)*length 
    % of them to 0
    if (mod(i, round(length(allelesZeroIndexes)/((1-MAF)*length(allelesOneIndexes)))) == 0) && (length(find(methyls == 1)) < length(allelesOneIndexes))
        % Set the current methylation status to 0
        % 2nd and makes sure that additional 1 methylation statuses are not
        % created due to rounding
        methyls(allelesZeroIndexes(i)) = 1;
    end
end

indivsMethyls = zeros(numIndivs, 2);
for j = 1:numIndivs
    % Iterate through the individuals and record the alleles for each
    indivsMethyls(j, 1) = methyls(j);
    indivsMethyls(j, 2) = methyls(numIndivs + j);
end

pValsPooled = ones(numSimulations, 1);
pValsIndivsGenotype = ones(numSimulations, 1);
numReadsPooled = round((numReads * nbinrnd(negBinParams(1), negBinParams(2), numSimulations, 1)) / numReadsMean);
numReadsIndivs = zeros(numSimulations, numIndivs);
for i = 1:numSimulations
    % Iterate through the simulations and randomly distribute the reads for
    % each across the inidviduals
    for j = 1:numReadsPooled(i)
        % Iterate through each read and randomly assign it to an individual
        indivForRead = randi(numIndivs);
        numReadsIndivs(i, indivForRead) = numReadsIndivs(i, indivForRead) + 1;
    end
end

for i = 1:numSimulations
    % Iterate through the simulations and compute whether the current
    % location has an mQTL for pooled data and for data from individuals   
    % Use the pooled method:
    if numReadsPooled(i) > 0
        % There is at least one read for the current simulation for the
        % pooled methold
        randIndexesPooled = randi(numAlleles, [numReadsPooled(i), 1]);
        randAllelesPooled = alleles(randIndexesPooled);
        randMethylsPooled = methyls(randIndexesPooled);
        randAllelesPooledOneIndexes = find(randAllelesPooled == 1);
        randMethylsPooledOneIndexes = find(randMethylsPooled == 1);
        % Table indicating values for Fisher's Exact Test (taken from fexact.m 
        % by Mike Boedigheimer).
        %       Methyl.  Unmethyl.
        % Alt.   a        c       K
        % Ref.   b        d       -
        % total  N        -       M
        % a,b,c,d are the numbers of alternative and reference alleles for the 
        % methylated and unmethylated CpGs. K, N, M are the row, column, and 
        % grand totals.
        a = length(intersect(randAllelesPooledOneIndexes, randMethylsPooledOneIndexes));
        K = length(randAllelesPooledOneIndexes);
        N = length(randMethylsPooledOneIndexes);
        M = numReadsPooled(i);
        pValsPooled(i) = fexact(a, M, K, N);
    end
    
    % Use the individuals separate genotypes method:
    if sum(numReadsIndivs(i,:)) > 0  
        % There is at least one read for the current simulation for the
        % individuals method
        % Table indicating values for Fisher's Exact Test (taken from
        % myfisher23.m by Giuseppe Cardillo)
        %               RR   RA  AA
        %           -------------------
        %Unmethyl.       a   b   c
        %           -------------------    
        %Methyl.         d   e   f
        %           -------------------
        % a, b, c, d, e, and f, are the numbers of unmethylated and
        % methylated CpGs for ref./ref., ref./alt., and alt./alt.
        % genotypes
        contingencyTable = zeros(2, 3);
        for j = 1:numIndivs
            % Iterate through the individuals and find the random alleles and
            % methylation information for each
            if numReadsIndivs(i,j) == 0
                % There are no reads for the current individual in the current
                % simulation
                continue
            end
            randIndexesIndivs = randi(2, [numReadsIndivs(i,j), 1]);
            currentMethylStatus = round(mean(indivsMethyls(j,randIndexesIndivs)));
            currentAllele = sum(indivsAlleles(j, :));
            contingencyTable(currentMethylStatus + 1, currentAllele + 1) = contingencyTable(currentMethylStatus + 1, currentAllele + 1) + 1;
        end
        pValsIndivsGenotype(i) = myfisher23(contingencyTable);
    end
end