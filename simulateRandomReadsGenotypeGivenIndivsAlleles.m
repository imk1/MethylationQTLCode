function pValsIndivsGenotype = simulateRandomReadsGenotypeGivenIndivsAlleles(numDevFromPerfectCorr, numReads, numSimulations, indivsAlleles)
% Simulate random reads and compute the number of mQTLs for individuals 
% data with each individual's association computed separately, where the
% alleles of the individuals are given


alleles = vertcat(indivsAlleles(:,1), indivsAlleles(:,2));
methyls = alleles;
allelesZeroIndexes = find(alleles == 0);
allelesOneIndexes = find(alleles == 1);
methyls(allelesOneIndexes(length(allelesOneIndexes) - numDevFromPerfectCorr + 1:length(allelesOneIndexes))) = 0;
methyls(allelesZeroIndexes(1:numDevFromPerfectCorr)) = 1;

numIndivs = size(indivsAlleles, 1);
indivsMethyls = zeros(numIndivs, 2);
for j = 1:numIndivs
    % Iterate through the individuals and record the alleles for each
    indivsMethyls(j, 1) = methyls(j);
    indivsMethyls(j, 2) = methyls(numIndivs + j);
end

numReadsPerIndiv = numReads/numIndivs;
pValsIndivsGenotype = ones(numSimulations, 1);
numReadsIndivs = poissrnd(numReadsPerIndiv, numSimulations, numIndivs);

for i = 1:numSimulations
    % Iterate through the simulations and compute whether the current
    % location has an mQTL for pooled data and for data from individuals    
    if sum(numReadsIndivs(i,:)) > 0
        % There is at least one read for the current simulation for the
        % individuals method    
        % Use the individuals separate genotypes method:
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