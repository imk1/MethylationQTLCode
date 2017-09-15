function [pValsPooled, pValsIndivsGenotype] = simulateRandomReadsCorrHWPlusPlus(numAlleles, numDevFromPerfectCorr, numReads, numSimulations, MAF)
% Simulate random reads and compute the number of mQTLs for pooled and
% individuals data as well as individuals data with each individual's
% association computed separately
% For traditional method, simulate the number of reads in the same way as
% for the pooled method and then randomly distribute the reads across the
% individuals
% Compute p-values using the asymptotic p-value from the Pearson
% correlation

numIndivs = numAlleles/2;
indivsAlleles = zeros(numIndivs, 2);
numIndivsAltAlt = round(numIndivs * (MAF ^ 2));
numIndivsRefAlt = round(numIndivs * 2 * (1 - MAF)  * MAF);
indivsAlleles(1:numIndivsAltAlt, :) = 1;
indivsAlleles(numIndivsAltAlt + 1:numIndivsAltAlt + numIndivsRefAlt, 1) = 1;
indivsAllelesSum = sum(indivsAlleles, 2)/2;
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
numReadsPooled = poissrnd(numReads, numSimulations, 1);
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
        % There is at least one read for the current simulation
        % Pooled method
        randIndexesPooled = randi(numAlleles, [numReadsPooled(i), 1]);
        randAllelesPooled = alleles(randIndexesPooled);
        randMethylsPooled = methyls(randIndexesPooled);
        % Compute the p-value using the Pearson correlation
        [~, pValsPooled(i)] = corr(randAllelesPooled, randMethylsPooled);

        % Individuals method
        % Compute the p-value using the Pearson correlation
        currentIndivsMethyls = zeros(numIndivs, 1);
        for j = 1:numIndivs
            % Iterate through the individuals and find the random alleles and
            % methylation information for each
            if numReadsIndivs(i,j) == 0
                % There are no reads for the current individual in the current
                % simulation
                continue
            end
            randIndexesIndivs = randi(2, [numReadsIndivs(i,j), 1]);
            currentIndivsMethyls(j) = mean(indivsMethyls(j,randIndexesIndivs));
        end
        [~, pValsIndivsGenotype(i)] = corr(indivsAllelesSum, currentIndivsMethyls);
    end
end