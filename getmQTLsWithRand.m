function [mQTLs, mQTLsRandList] = getmQTLsWithRand(locationsBetasIndividualsMethylFileName, genotypesFiltFileName, distanceCutoff, numPerms)
% Get mQTLs for array data and permuted array data using Pearson 
% correlation

locationsBetasIndividualsMethyl = importdata(locationsBetasIndividualsMethylFileName);
genotypesFilt = importdata(genotypesFiltFileName);
mQTLs = sparse(size(genotypesFilt.data, 1), size(locationsBetasIndividualsMethyl.data, 1));
numIndividualsPlusOne = size(genotypesFilt.data, 2);
methylIndexesList = {};

for i = 1:size(mQTLs, 1)
    % Iterate through the SNPs and get the correlations with each close CpG
    if mod(i,100000) == 1
        i
    end
    CpGsToCorr = intersect(find(strcmp(locationsBetasIndividualsMethyl.textdata, genotypesFilt.textdata{i}) == 1), find(abs(genotypesFilt.data(i,1) - locationsBetasIndividualsMethyl.data(:,1)) < distanceCutoff));
    methylIndexesList{i} = CpGsToCorr;
    mQTLs(i, CpGsToCorr) = corr(genotypesFilt.data(i,2:numIndividualsPlusOne)', locationsBetasIndividualsMethyl.data(CpGsToCorr, 2:numIndividualsPlusOne)', 'rows', 'complete');
end

mQTLsRandList = {};
for k = 1:numPerms
    % Compute the correlation for each permutation
    if mod(k, 100) == 1
        k
    end
    permutation = randperm(numIndividualsPlusOne - 1);
    locationsBetasIndividualsMethylRand = locationsBetasIndividualsMethyl.data(:,permutation + 1);
    mQTLsRandList{k} = sparse(size(genotypesFilt.data, 1), size(locationsBetasIndividualsMethyl.data, 1));
    for i = 1:size(mQTLs, 1)
        % Iterate through the SNPs and get the permuted correlations with each CpG that
        % is listed for it in the SNPMethyl file
        mQTLsRandList{k}(i, methylIndexesList{i}) = corr(genotypesFilt.data(i,2:numIndividualsPlusOne)', locationsBetasIndividualsMethylRand(methylIndexesList{i}, :)', 'rows', 'complete');
    end
end