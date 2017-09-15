function [pValsPooled, pValsIndivsGenotype] = simulateRandomReadsNegBinFTestRegressNegative(numAlleles, negBinParams, numReadsMean, numReads, numSimulations, MAF)
% In these simulations, assume that there is no relationship between the
% allele and the methylation status
% Simulate random reads and compute the number of mQTLs for pooled data
% and individuals data with associations between genotype and average 
% methylation, where numbers of reads are drawn from a negative binomial 
% distribution whose parameters have been inputted
% For traditional method, simulate the number of reads in the same way as
% for the pooled method and then randomly distribute the reads across the
% individuals
% Compute p-values using the one-way ANOVA F-test to compare variance
% within each allele/genotype to variance between alleles/genotypes

numIndivs = numAlleles/2;
indivsAlleles = zeros(numIndivs, 2);
numIndivsAltAlt = round(numIndivs * (MAF ^ 2));
numIndivsRefAlt = round(numIndivs * 2 * (1 - MAF)  * MAF);
indivsAlleles(1:numIndivsAltAlt, :) = 1;
indivsAlleles(numIndivsAltAlt + 1:numIndivsAltAlt + numIndivsRefAlt, 1) = 1;
indivsAllelesSum = sum(indivsAlleles, 2)/2;
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
        % There is at least one read for the current simulation
        % Pooled method
        randIndexesPooled = randi(numAlleles, [numReadsPooled(i), 1]);
        randAllelesPooled = alleles(randIndexesPooled);
        randMethylsPooled = methyls(randIndexesPooled);
        % Compute the p-value using the F-statistic of the regression
        mdl = LinearModel.fit(randAllelesPooled, randMethylsPooled);
        MSM = sum((mdl.Fitted - mean(randMethylsPooled)).^2); % = SSM because DFM = 1
        F = MSM/mdl.MSE;
        pValsPooled(i) = 1 - fcdf(F, 1, numReadsPooled(i) - 2) + fpdf(F, 1, numReadsPooled(i) - 2); % p = 2 (b/c intercept), n = numReadsPooled(i)
        
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
        mdlIndivs = LinearModel.fit(indivsAllelesSum, currentIndivsMethyls);
        MSMIndivs = sum((mdlIndivs.Fitted - mean(currentIndivsMethyls)).^2); % = SSM because DFM = 1
        FIndivs = MSMIndivs/mdlIndivs.MSE;
        pValsIndivsGenotype(i) = 1 - fcdf(FIndivs, 1, numIndivs - 2) + fpdf(FIndivs, 1, numIndivs - 2); % p = 2, n = numIndivs
    end
end
