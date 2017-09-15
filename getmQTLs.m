function mQTLs = getmQTLs(locationsBetasIndividualsMethylFileName, genotypesFiltFileName, distanceCutoff)
% Get mQTLs for array data using Pearson correlation

locationsBetasIndividualsMethyl = importdata(locationsBetasIndividualsMethylFileName);
genotypesFilt = importdata(genotypesFiltFileName);
mQTLs = sparse(size(genotypesFilt.data, 1), size(locationsBetasIndividualsMethyl.data, 1));
numIndividualsPlusOne = size(genotypesFilt.data, 2);

for i = 1:size(mQTLs, 1)
    % Iterate through the SNPs and get the correlations with each close CpG
    if mod(i,100000) == 1
        i
    end
    CpGsToCorr = intersect(find(strcmp(locationsBetasIndividualsMethyl.textdata, genotypesFilt.textdata{i}) == 1), find(abs(genotypesFilt.data(i,1) - locationsBetasIndividualsMethyl.data(:,1)) < distanceCutoff));
    mQTLs(i, CpGsToCorr) = corr(genotypesFilt.data(i,2:numIndividualsPlusOne)', locationsBetasIndividualsMethyl.data(CpGsToCorr, 2:numIndividualsPlusOne)');
end