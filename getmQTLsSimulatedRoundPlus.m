function [mQTLsSimulated, mQTLsRandListSimulated] = getmQTLsSimulatedRoundPlus(locationsBetasIndividualsMethylFileName, genotypesFiltFileName, SNPMethylFileName, numPerms, numSimulatedReads)
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
    genotypesNew = round(.5*genotypesFilt.data(i,2:numIndividualsPlusOne));
    for j = 1:length(methylLocations)
        % Iterate through the CpGs for the current SNP and get the
        % correlation for each
         methylIndex = find(locationsBetasIndividualsMethyl.data(:,1) == methylLocations(j));
         
         if ~isempty(methylIndex)
             % The methylation site that was tested with the SNP near the
             % pooled data is in the array
            methylIndexesList{i} = vertcat(methylIndexesList{i}, methylIndex);
            methylValues = locationsBetasIndividualsMethyl.data(methylIndex, 2:numIndividualsPlusOne);
            nonNanIndexes = find(~isnan(methylValues));
            numIndividualsNan = length(find(isnan(methylValues)));
            methylNew = round(methylValues(nonNanIndexes));
            fracReadsMethylRef = length(intersect(find(genotypesNew(nonNanIndexes) == 1), find(methylNew == 1))) / (numIndividualsPlusOne - 1 - numIndividualsNan);
            fracReadsUnmethylRef = length(intersect(find(genotypesNew(nonNanIndexes) == 1), find(methylNew == 0))) / (numIndividualsPlusOne - 1 - numIndividualsNan);
            fracReadsMethylAlt = length(intersect(find(genotypesNew(nonNanIndexes) == 0), find(methylNew == 1))) / (numIndividualsPlusOne - 1 - numIndividualsNan);
            fracReadsUnmethylAlt = length(intersect(find(genotypesNew(nonNanIndexes) == 0), find(methylNew == 0))) / (numIndividualsPlusOne - 1 - numIndividualsNan);
            
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
            K = round(numSimulatedReads * (fracReadsMethylAlt + fracReadsUnmethylAlt));
            N = round(numSimulatedReads * (fracReadsMethylAlt + fracReadsMethylRef));
            M = numSimulatedReads;
            if a < N + K - numSimulatedReads
                % a is too small due to rounding, so add to the number of
                % simulated reads
                M = M + 1;
            end
            mQTLsSimulated(i, methylIndex) = fexact(a, M, K, N);
         end
    end
end

mQTLsRandListSimulated = {};
for k = 1:numPerms
    % Compute the Fisher's Exact Test p-value for each permutation
    if mod(k, 50) == 1
        k
    end
    permutation = randperm(numIndividualsPlusOne - 1);
    locationsBetasIndividualsMethylRand = locationsBetasIndividualsMethyl.data(:,permutation + 1);
    mQTLsRandListSimulated{k} = sparse(size(genotypesFilt.data, 1), size(locationsBetasIndividualsMethyl.data, 1));
    for i = 1:size(mQTLsSimulated, 1)
        % Iterate through the SNPs and get the correlations with each CpG that
        % is listed for it in the SNPMethyl file
        
        for j = 1:length(methylIndexesList{i})
            % Iterate through the CpGs for the current SNP and get the
            % correlation for each
            methylValues = locationsBetasIndividualsMethylRand(methylIndexesList{i}(j), :);
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
            K = round(numSimulatedReads * (fracReadsMethylAlt + fracReadsUnmethylAlt));
            N = round(numSimulatedReads * (fracReadsMethylAlt + fracReadsMethylRef));
            M = numSimulatedReads;
            if a < N + K - numSimulatedReads
                % a is too small due to rounding, so add to the number of
                % simulated reads
                M = M + 1;
            end
            mQTLsRandListSimulated{k}(i, methylIndexesList{i}(j)) = fexact(a, M, K, N);
        end
    end
end