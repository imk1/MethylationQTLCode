function [mQTLs, mQTLsRandList] = getmQTLsWithRandPlusPlus(locationsBetasIndividualsMethylFileName, genotypesFiltFileName, methylIndexesMatFileName, numPerms)
% Get mQTLs for array data and permuted array data using Pearson 
% correlation

locationsBetasIndividualsMethyl = importdata(locationsBetasIndividualsMethylFileName);
genotypesFilt = importdata(genotypesFiltFileName);
methylIndexesMat = importdata(methylIndexesMatFileName);
numIndividualsPlusOne = size(genotypesFilt.data, 2);

mQTLs = sparse(methylIndexesMat .* corr(genotypesFilt.data(:,2:numIndividualsPlusOne)', locationsBetasIndividualsMethyl.data(:, 2:numIndividualsPlusOne)', 'rows', 'complete'));

mQTLsRandList = {};
for k = 1:numPerms
    % Compute the correlation for each permutation
    k
    if mod(k, 100) == 1
        k
    end
    permutation = randperm(numIndividualsPlusOne - 1);
    locationsBetasIndividualsMethylRand = locationsBetasIndividualsMethyl.data(:,permutation + 1);
    mQTLsRandList{k} = sparse(methylIndexesMat .* corr(genotypesFilt.data(:,2:numIndividualsPlusOne)', locationsBetasIndividualsMethylRand', 'rows', 'complete'));
end