function getmQTLsWithRandPlus(locationsBetasIndividualsMethylFileName, genotypesFiltFileName, distanceCutoff, numPerms, outputFileName)
% Get mQTLs for array data and permuted array data using Pearson 
% correlation

locationsBetasIndividualsMethyl = importdata(locationsBetasIndividualsMethylFileName);
genotypesFilt = importdata(genotypesFiltFileName);
numIndividualsPlusOne = size(genotypesFilt.data, 2);

methylIndexesMat = sparse(size(genotypesFilt.data, 1), size(locationsBetasIndividualsMethyl.data, 1));
for i = 1:size(methylIndexesMat, 1)
    % Iterate through the mQTLs and find those that are close enough for
    % consideration
    if mod(i,10000) == 1
        i
    end
    CpGsToCorr = intersect(find(strcmp(locationsBetasIndividualsMethyl.textdata, genotypesFilt.textdata{i}) == 1), find(abs(genotypesFilt.data(i,1) - locationsBetasIndividualsMethyl.data(:,1)) < distanceCutoff));
    methylIndexesMat(i,CpGsToCorr') = 1;
end

mQTLs = methylIndexesMat .* sparse(corr(genotypesFilt.data(:,2:numIndividualsPlusOne)', locationsBetasIndividualsMethyl.data(:, 2:numIndividualsPlusOne)', 'rows', 'complete'));
saveExpr = horzcat('save ', outputFileName, ' mQTLs');
eval(saveExpr);
clear mQTLs

for k = 1:numPerms
    % Compute the correlation for each permutation
    k
    if mod(k, 100) == 1
        k
    end
    permutation = randperm(numIndividualsPlusOne - 1);
    locationsBetasIndividualsMethylRand = locationsBetasIndividualsMethyl.data(:,permutation + 1);
    mQTLsRand = methylIndexesMat .* sparse(corr(genotypesFilt.data(:,2:numIndividualsPlusOne)', locationsBetasIndividualsMethylRand', 'rows', 'complete'));
    outputFileNameRand = horzcat(outputFileName, 'Rand', num2str(k));
    saveExpr = horzcat('save ', outputFileNameRand, ' mQTLsRand');
    eval(saveExpr);
    clear mQTLsRand
end