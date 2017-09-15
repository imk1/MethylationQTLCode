function [mQTLspVals, mQTLspValsRand] = getmQTLspVals(locationsBetasIndividualsMethylFileName, genotypesFiltFileName, mQTLs, mQTLsRandList, numRand)
% Get the p-value for mQTLs and random mQTLs for array data

locationsBetasIndividualsMethyl = importdata(locationsBetasIndividualsMethylFileName);
genotypesFilt = importdata(genotypesFiltFileName);
mQTLspVals = [];
mQTLspValsRand = {};
for l = 1:numRand
    % Initialize mQTL p-value lists for the permuted data
    mQTLspValsRand{l} = [];
end

for i = 1:size(mQTLs, 1)
    % Iterate through the SNP, methylation pairs and record the p-value for
    % each
    if mod(i, 100) == 1
        i
    end
    CpGIndexes = find(abs(mQTLs(i,:)) > 0);
    SNPLocation = genotypesFilt.data(i,1);
    methylLocations = locationsBetasIndividualsMethyl.data(CpGIndexes,1);
    currentCorrs = abs(mQTLs(i,CpGIndexes));
    numGreaterCorrs = zeros(length(CpGIndexes), 1);
    currentCorrsRand = zeros(length(CpGIndexes), numRand);
    for k = 1:length(mQTLsRandList)
        % Iterate through the random list and determine how many
        % permutations have |correlations| greater than the |current
        % correlation|
        numGreaterCorrs = numGreaterCorrs + (abs(mQTLsRandList{k}(i,CpGIndexes(j))) >= currentCorr)';
        if abs(mQTLsRandList{k}(i,CpGIndexes(j))) >= currentCorr
            % The correlation in the permuted list is greater than the
            % real correlation
            numGreaterCorr = numGreaterCorr + 1;
        end
        if k <= numRand
            % Store the random correlation
            currentCorrRand(k) = abs(mQTLsRandList{k}(i,CpGIndexes(j)));
        end
    end
    
    for j = 1:length(CpGIndexes)
        % Iterate through the methylation sites that were in the pooled
        % data for the current SNP and compute the mQTL p-value for each
        methylLocation = locationsBetasIndividualsMethyl.data(CpGIndexes(j),1);
        currentCorr = abs(mQTLs(i,CpGIndexes(j)));
        numGreaterCorr = 0;
        currentCorrRand = zeros(numRand, 1);
        
        for k = 1:length(mQTLsRandList)
            % Iterate through the random list and determine how many
            % permutations have |correlations| greater than the |current
            % correlation|
            if abs(mQTLsRandList{k}(i,CpGIndexes(j))) >= currentCorr
                % The correlation in the permuted list is greater than the
                % real correlation
                numGreaterCorr = numGreaterCorr + 1;
            end
            if k <= numRand
                % Store the random correlation
                currentCorrRand(k) = abs(mQTLsRandList{k}(i,CpGIndexes(j)));
            end
        end
        
        numGreaterCorrRand = zeros(numRand, 1);
        for k = 1:length(mQTLsRandList)
            % Iterate through the random list and determine how many
            % permutations have |correlations| greater than the |current
            % random correlation|
            for l = 1:numRand
                % Iterate through the random list for determining the FDR
                % and compute the number of other random |correlations|
                % that are greater than the current one
                if l == k
                    % At the current permutation, so do not check it
                    continue
                end
                if abs(mQTLsRandList{k}(i,CpGIndexes(j))) >= currentCorrRand(l)
                    % The correlation in the permuted list is greater than the
                    % real correlation
                    numGreaterCorrRand(l) = numGreaterCorrRand(l) + 1;
                end
            end
        end
        
        pVal = numGreaterCorr/length(mQTLsRandList);
        mQTLspVals = vertcat(mQTLspVals, [SNPLocation, methylLocation, pVal]);
        for l = 1:numRand
            % Compute the p-value for each permuted data-set that will be
            % used to compute an FDR
            pValRand = numGreaterCorrRand(l)/(length(mQTLsRandList) - 1);
            mQTLspValsRand{l} = vertcat(mQTLspValsRand{l}, [SNPLocation, methylLocation, pValRand]);
        end
    end
end