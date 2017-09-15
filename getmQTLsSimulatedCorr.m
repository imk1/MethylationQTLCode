function mQTLsSimulated = getmQTLsSimulatedCorr(locationsBetasIndividualsMethylFileName, genotypesFiltFileName, SNPMethylFileName, numPerms, numSimulatedReads)
% Get mQTLs for array data simulated as pooled reads data using Fisher's 
% Exact Test

locationsBetasIndividualsMethyl = importdata(locationsBetasIndividualsMethylFileName);
genotypesFilt = importdata(genotypesFiltFileName);
mQTLsSimulated = ones(size(genotypesFilt.data, 1), size(locationsBetasIndividualsMethyl.data, 1));
numIndividualsPlusOne = size(genotypesFilt.data, 2);
SNPMethyl = importdata(SNPMethylFileName);
methylIndexesList = {};

for i = 1:size(mQTLsSimulated, 1)
    % Iterate through the SNPs and get the simulated Fisher's Exact Test 
    % p-value with each CpG that is listed for it in the SNPMethyl file
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
            methylValues = locationsBetasIndividualsMethyl.data(methylIndex, 2:numIndividualsPlusOne);
            numIndividualsNan = length(find(isnan(methylValues)));
            fracReadsMethylRef = nansum((genotypesFilt.data(i,2:numIndividualsPlusOne) .* methylValues) * .5) / (numIndividualsPlusOne - 1 - numIndividualsNan);
            fracReadsUnmethylRef = nansum((genotypesFilt.data(i,2:numIndividualsPlusOne) .* (1 - methylValues)) * .5) / (numIndividualsPlusOne - 1 - numIndividualsNan);
            fracReadsMethylAlt = nansum(((2 - genotypesFilt.data(i,2:numIndividualsPlusOne)) .* methylValues) * .5) / (numIndividualsPlusOne - 1 - numIndividualsNan);
            fracReadsUnmethylAlt = nansum(((2 - genotypesFilt.data(i,2:numIndividualsPlusOne)) .* (1 - methylValues)) * .5) / (numIndividualsPlusOne - 1 - numIndividualsNan);
            
            % Table indicating values for Fisher's Exact Test (taken from 
            % fexact.m by Mike Boedigheimer).
            %       Methyl.  Unmethyl.
            % Alt.   a        c       K
            % Ref.   b        d       -
            % total  N        -       M
            % a,b,c,d are the numbers of alternative and reference alleles 
            % for the methylated and unmethylated CpGs. K, N, M are the 
            % row, column, and grand totals.  (M = numSimulatedReads.)
            a = round(numSimulatedReads * fracReadsMethylAlt);
            b = round(numSimulatedReads * fracReadsMethylRef);
            c = round(numSimulatedReads * fracReadsUnmethylAlt);
            d = round(numSimulatedReads * fracReadsUnmethylRef);
            genotypesNew = vertcat(ones(a, 1), zeros(b,1), ones(c,1), zeros(d, 1));
            methylNew = vertcat(ones(a, 1), ones(b,1), zeros(c,1), zeros(d, 1));
            [c, p] = corr(genotypesNew, methylNew);
            mQTLsSimulated(i, methylIndex) = p;
         end
    end
end