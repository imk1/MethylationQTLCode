function [mQTLspVals, mQTLspValsRand] = getmQTLspValsPlus(locationsBetasIndividualsMethylFileName, genotypesFiltFileName, mQTLs, mQTLsRandList, numRand)
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
    if isempty(CpGIndexes)
        % There are no CpGs for the current SNP
        continue
    end
    SNPLocation = genotypesFilt.data(i,1);
    methylLocations = locationsBetasIndividualsMethyl.data(CpGIndexes,1);
    currentCorrs = abs(mQTLs(i,CpGIndexes));
    numGreaterCorrs = zeros(length(CpGIndexes), 1);
    currentCorrsRand = zeros(numRand, length(CpGIndexes));
    for k = 1:length(mQTLsRandList)
        % Iterate through the random list and determine how many
        % permutations have |correlations| greater than the |current
        % correlation|
        numGreaterCorrs = numGreaterCorrs + (abs(mQTLsRandList{k}(i,CpGIndexes)) >= currentCorrs)'; % Adds 1 if the corr. in the perm. list is >=
        if k <= numRand
            % Store the random correlation
            currentCorrsRand(k, :) = abs(mQTLsRandList{k}(i,CpGIndexes));
        end
    end
    
    numGreaterCorrsRand = zeros(numRand, length(CpGIndexes));
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
            numGreaterCorrsRand(l, :) = numGreaterCorrsRand(l, :) + (abs(mQTLsRandList{k}(i,CpGIndexes)) >= currentCorrsRand(l, :));
        end
    end
    
    pVals = numGreaterCorrs/length(mQTLsRandList);
    SNPLocationRep = repmat(SNPLocation, length(CpGIndexes), 1);
    mQTLspVals = vertcat(mQTLspVals, [SNPLocationRep, methylLocations, pVals]);
    for l = 1:numRand
        % Compute the p-value for each permuted data-set that will be
        % used to compute an FDR
        pValsRand = numGreaterCorrsRand(l, :)'/(length(mQTLsRandList) - 1);
        mQTLspValsRand{l} = vertcat(mQTLspValsRand{l}, [SNPLocationRep, methylLocations, pValsRand]);
    end
end