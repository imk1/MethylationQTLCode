function [pValsPooled, pValsIndivsGenotype] = simulateRandomReadsNegBinWithParamsHWPlus(numAlleles, numDevFromPerfectCorr, negBinParamsPooled, negBinParamsIndivs, numSimulations, MAF)
% Simulate random reads and compute the number of mQTLs for pooled data
% and individuals data with associations between genotype and average 
% methylation, where numbers of reads are drawn from a negative binomial 
% distribution whose parameters have been inputted

numIndivs = numAlleles/2;
indivsAlleles = zeros(numIndivs, 2);
numIndivsAltAlt = round(numIndivs * (MAF ^ 2));
numIndivsRefAlt = round(numIndivs * 2 * (1 - MAF)  * MAF);
indivsAlleles(1:numIndivsAltAlt, :) = 1;
indivsAlleles(numIndivsAltAlt + 1:numIndivsAltAlt + numIndivsRefAlt, 1) = 1;
alleles = vertcat(indivsAlleles(:,1), indivsAlleles(:,2));

methyls = alleles;
allelesZeroIndexes = find(alleles == 0);
allelesOneIndexes = find(alleles == 1);
methyls(allelesOneIndexes(length(allelesOneIndexes) - numDevFromPerfectCorr + 1:length(allelesOneIndexes))) = 0;
methyls(allelesZeroIndexes(1:numDevFromPerfectCorr)) = 1;

indivsMethyls = zeros(numIndivs, 2);
for j = 1:numIndivs
    % Iterate through the individuals and record the alleles for each
    indivsMethyls(j, 1) = methyls(j);
    indivsMethyls(j, 2) = methyls(numIndivs + j);
end

pValsPooled = ones(numSimulations, 1);
pValsIndivsGenotype = ones(numSimulations, 1);
numReadsPooled = nbinrnd(negBinParamsPooled(1), negBinParamsPooled(2), numSimulations, 1);
numReadsIndivs = nbinrnd(negBinParamsIndivs(1), negBinParamsIndivs(2), numSimulations, numIndivs);

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