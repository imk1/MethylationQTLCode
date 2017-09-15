function pValsIndivsGenotype = simulateRandomReadsNegBinGenotypeWithParams(numAlleles, numMinorAlleles, numDevFromPerfectCorr, negBinParamsIndivs, numSimulations)
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
    % MINOR GENOTYPE AND METHYLATION STATUS PAIR FREQUENCIES WILL BE 0
    indivsAlleles(j, 1) = alleles(j);
    indivsAlleles(j, 2) = alleles(numIndivs + j);
    indivsMethyls(j, 1) = methyls(j);
    indivsMethyls(j, 2) = methyls(numIndivs + j);
end

pValsIndivsGenotype = ones(numSimulations, 1);

numReadsIndivs = nbinrnd(negBinParamsIndivs(1), negBinParamsIndivs(2), numSimulations, numIndivs);

for i = 1:numSimulations
    % Iterate through the simulations and compute whether the current
    % location has an mQTL for data from individuals, treating each 
    % individual separetly with its genotype    
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