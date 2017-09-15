function [pValsPooled, pValsIndivs] = simulateRandomReadsNegBinWithParams(numAlleles, numMinorAlleles, numDevFromPerfectCorr, negBinParamsPooled, negBinParamsIndivs, numSimulations)
% Simulate random reads and compute the number of mQTLs for pooled and
% individuals data

alleles = zeros(numAlleles, 1);
methyls = zeros(numAlleles, 1);
alleles(1:numMinorAlleles) = 1;
methyls(1:numMinorAlleles - numDevFromPerfectCorr) = 1;
methyls(numMinorAlleles + 1:numMinorAlleles + numDevFromPerfectCorr) = 1;

numIndivs = numAlleles/2;
indivsAlleles = zeros(numIndivs, 2);
indivsMethyls = zeros(numIndivs, 2);
for j = 1:numIndivs
    % Iterate through the individuals and record the alleles for each
    indivsAlleles(j, :) = alleles((2*j) - 1:(2*j));
    indivsMethyls(j, :) = methyls((2*j) - 1:(2*j));
end

pValsPooled = ones(numSimulations, 1);
pValsIndivs = ones(numSimulations, 1);
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
    
    % Use the individuals method:
    if sum(numReadsIndivs(i,:)) > 0
        % There is at least one read for the current simulation for the
        % individuals method
        randAllelesIndivs = zeros(sum(numReadsIndivs(i,:)));
        randMethylsIndivs = zeros(sum(numReadsIndivs(i,:)));
        randCountIndivs = 0;
        for j = 1:numIndivs
            % Iterate through the individuals and find the random alleles and
            % methylation information for each
            if numReadsIndivs(i,j) == 0
                % There are no reads for the current individual in the current
                % simulation
                continue
            end
            randIndexesIndivs = randi(2, [numReadsIndivs(i,j), 1]);
            randAllelesIndivs(randCountIndivs + 1:randCountIndivs + numReadsIndivs(i,j)) = indivsAlleles(j,randIndexesIndivs);
            randMethylsIndivs(randCountIndivs + 1:randCountIndivs + numReadsIndivs(i,j)) = indivsMethyls(j,randIndexesIndivs);
            randCountIndivs = randCountIndivs + numReadsIndivs(i,j);
        end
        randAllelesIndivsOneIndexes = find(randAllelesIndivs == 1);
        randMethylsIndivsOneIndexes = find(randMethylsIndivs == 1);
        % Table indicating values for Fisher's Exact Test (taken from fexact.m 
        % by Mike Boedigheimer).
        %       Methyl.  Unmethyl.
        % Alt.   a        c       K
        % Ref.   b        d       -
        % total  N        -       M
        % a,b,c,d are the numbers of alternative and reference alleles for the 
        % methylated and unmethylated CpGs. K, N, M are the row, column, and 
        % grand totals.
        aI = length(intersect(randAllelesIndivsOneIndexes, randMethylsIndivsOneIndexes));
        KI = length(randAllelesIndivsOneIndexes);
        NI = length(randMethylsIndivsOneIndexes);
        MI = sum(numReadsIndivs(i,:));
        pValsIndivs(i) = fexact(aI, MI, KI, NI);
    end
end