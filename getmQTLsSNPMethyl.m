function [mQTLs, mQTLsRandList] = getmQTLsSNPMethyl(locationsBetasIndividualsMethylFileName, genotypesFiltFileName, SNPMethylFileName, numPerms)
% Get mQTLs for array data using Pearson correlation

locationsBetasIndividualsMethyl = importdata(locationsBetasIndividualsMethylFileName);
genotypesFilt = importdata(genotypesFiltFileName);
mQTLs = sparse(size(genotypesFilt.data, 1), size(locationsBetasIndividualsMethyl.data, 1));
numIndividualsPlusOne = size(genotypesFilt.data, 2);
SNPMethyl = importdata(SNPMethylFileName);
methylIndexesList = {};

for i = 1:size(mQTLs, 1)
    % Iterate through the SNPs and get the correlations with each CpG that
    % is listed for it in the SNPMethyl file
    SNPIndexes = find(SNPMethyl(:,1) == genotypesFilt.data(i,1));
    methylLocations = SNPMethyl(SNPIndexes, 2);
    methylIndexesList{i} = [];
    for j = 1:length(methylLocations)
        % Iterate through the CpGs for the current SNP and get the
        % correlation for each
         methylIndex = find(locationsBetasIndividualsMethyl.data(:,1) == methylLocations(j));
         if ~isempty(methylIndex)
             % The methylation site that was tested with the SNP near the
             % pooled data is in the array
            methylIndexesList{i} = vertcat(methylIndexesList{i}, methylIndex);
            mQTLs(i, methylIndex) = corr(genotypesFilt.data(i,2:numIndividualsPlusOne)', locationsBetasIndividualsMethyl.data(methylIndex, 2:numIndividualsPlusOne)', 'rows', 'complete');
         end
    end
end

mQTLsRandList = {};
for k = 1:numPerms
    % Compute the correlation for each permutation
    if mod(k, 1000) == 1
        k
    end
    permutation = randperm(numIndividualsPlusOne - 1);
    locationsBetasIndividualsMethylRand = locationsBetasIndividualsMethyl.data(:,permutation + 1);
    mQTLsRandList{k} = sparse(size(genotypesFilt.data, 1), size(locationsBetasIndividualsMethyl.data, 1));
    for i = 1:size(mQTLs, 1)
        % Iterate through the SNPs and get the correlations with each CpG that
        % is listed for it in the SNPMethyl file
        for j = 1:length(methylIndexesList{i})
            % Iterate through the CpGs for the current SNP and get the
            % correlation for each
            mQTLsRandList{k}(i, methylIndexesList{i}(j)) = corr(genotypesFilt.data(i,2:numIndividualsPlusOne)', locationsBetasIndividualsMethylRand(methylIndexesList{i}(j), :)', 'rows', 'complete');
        end
    end
end