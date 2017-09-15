function mQTLspValsSimulated = getmQTLsFisherExactpValsOnlyReal(locationsBetasIndividualsMethylFileName, genotypesFiltFileName, SNPMethylFileName, mQTLsSimulated, mQTLsRandSimulated)
% Get mQTLs for array data simulated as pooled reads data using Fisher's 
% Exact Test

locationsBetasIndividualsMethyl = importdata(locationsBetasIndividualsMethylFileName);
genotypesFilt = importdata(genotypesFiltFileName);
mQTLspValsSimulated = [];
SNPMethyl = importdata(SNPMethylFileName);

for i = 1:size(genotypesFilt.data, 1)
    % Iterate through the SNPs and get the simulated Fisher's Exact Test 
    % p-value with each CpG that is listed for it in the SNPMethyl file
    SNPIndexes = find(SNPMethyl(:,1) == genotypesFilt.data(i,1));
    SNPLocation = genotypesFilt.data(i,1);
    methylLocations = SNPMethyl(SNPIndexes, 2);
    for j = 1:length(methylLocations)
        % Iterate through the CpGs for the current SNP and get the
        % p-value for each
         methylIndex = find(locationsBetasIndividualsMethyl.data(:,1) == methylLocations(j));
         if ~isempty(methylIndex)
             % The methylation site that was tested with the SNP near the
             % pooled data is in the array
             mQTLspValsSimulated = vertcat(mQTLspValsSimulated, [SNPLocation, methylLocations(j), mQTLsSimulated(i, methylIndex)]);
         else
             SNPLocation
             methylLocations(j)
         end
    end
end