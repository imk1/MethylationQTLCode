function [mQTLsSimulated, mQTLsRandListSimulated] = getmQTLsSimulatedPlus(locationsBetasIndividualsMethylFileName, genotypesFiltFileName, SNPMethylReadsFileName, numPerms)
% Get mQTLs for array data simulated as pooled reads data using Fisher's 
% Exact Test

locationsBetasIndividualsMethyl = importdata(locationsBetasIndividualsMethylFileName);
genotypesFilt = importdata(genotypesFiltFileName);
mQTLsSimulated = ones(size(genotypesFilt.data, 1), size(locationsBetasIndividualsMethyl.data, 1));
numIndividualsPlusOne = size(genotypesFilt.data, 2);
SNPMethylReads = importdata(SNPMethylReadsFileName);
methylIndexesList = {};
numSimulatedReadsList = {};
fracReadsRefArray = zeros(size(mQTLsSimulated, 1), 1);
fracReadsAltArray = zeros(size(mQTLsSimulated, 1), 1);
individualsRefArray = {};
individualsHetArray = {};
individualsAltArray = {};

for i = 1:size(mQTLsSimulated, 1)
    % Iterate through the SNPs and get the simulated Fisher's Exact Test 
    % p-value with each CpG that is listed for it in the SNPMethyl file
    if mod(i, 10000) == 1
        i
    end
    fracReadsRef = sum(genotypesFilt.data(i,2:numIndividualsPlusOne))/(2 * (numIndividualsPlusOne - 1));
    fracReadsRefArray(i) = fracReadsRef;
    fracReadsAlt = 1 - fracReadsRef;
    fracReadsAltArray(i) = fracReadsAlt;
    individualsRef = find(round(genotypesFilt.data(i,2:numIndividualsPlusOne)) == 2);
    individualsRefArray{i} = individualsRef;
    individualsHet = find(round(genotypesFilt.data(i,2:numIndividualsPlusOne)) == 1);
    individualsHetArray{i} = individualsHet;
    individualsAlt = find(round(genotypesFilt.data(i,2:numIndividualsPlusOne)) == 0);
    individualsAltArray{i} = individualsAlt;
    if ((length(individualsRef) == 0) && (length(individualsHet) == 0)) || ((length(individualsAlt) == 0) && (length(individualsHet) == 0))
        % There are no reads for one allele, so skip the current SNP
        continue
    end
    SNPIndexes = find(SNPMethylReads(:,1) == genotypesFilt.data(i,1));
    methylLocations = SNPMethylReads(SNPIndexes, 2);
    numSimulatedReadsList{i} = SNPMethylReads(SNPIndexes, 3);
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
            numIndividualsRefNan = length(find(isnan(methylValues(individualsRef))));
            numIndividualsHetNan = length(find(isnan(methylValues(individualsHet))));
            numIndividualsAltNan = length(find(isnan(methylValues(individualsAlt))));
            fracReadsMethylRef = fracReadsRef * ((nansum(methylValues(individualsRef)) + (.5 * nansum(methylValues(individualsHet))))/(length(individualsRef) - numIndividualsRefNan + (.5 * (length(individualsHet) - numIndividualsHetNan))));
            %fracReadsUnmethylRef = fracReadsRef * ((nansum(1 - methylValues(individualsRef)) + (.5 * nansum(1 - methylValues(individualsHet))))/(length(individualsRef) - numIndividualsRefNan + (.5 * (length(individualsHet) - numIndividualsHetNan))));
            fracReadsMethylAlt = fracReadsAlt * ((nansum(methylValues(individualsAlt)) + (.5 * nansum(methylValues(individualsHet))))/(length(individualsAlt) - numIndividualsAltNan + (.5 * (length(individualsHet) - numIndividualsHetNan))));
            fracReadsUnmethylAlt = fracReadsAlt * ((nansum(1 - methylValues(individualsAlt)) + (.5 * nansum(1 - methylValues(individualsHet))))/(length(individualsAlt) - numIndividualsAltNan + (.5 * (length(individualsHet) - numIndividualsHetNan))));
            
            % Table indicating values for Fisher's Exact Test (taken from 
            % fexact.m by Mike Boedigheimer).
            %       Methyl.  Unmethyl.
            % Alt.   a        c       K
            % Ref.   b        d       -
            % total  N        -       M
            % a,b,c,d are the numbers of alternative and reference alleles 
            % for the methylated and unmethylated CpGs. K, N, M are the 
            % row, column, and grand totals.  (M = numSimulatedReads.)
            a = round(numSimulatedReadsList{i}(j) * fracReadsMethylAlt);
            K = round(numSimulatedReadsList{i}(j) * (fracReadsMethylAlt + fracReadsUnmethylAlt));
            N = round(numSimulatedReadsList{i}(j) * (fracReadsMethylAlt + fracReadsMethylRef));
            M = numSimulatedReadsList{i}(j);
            if a < N + K - numSimulatedReadsList{i}(j)
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
    mQTLsRandListSimulated{k} = ones(size(genotypesFilt.data, 1), size(locationsBetasIndividualsMethyl.data, 1));
    for i = 1:size(mQTLsSimulated, 1)
        % Iterate through the SNPs and get the correlations with each CpG that
        % is listed for it in the SNPMethyl file
        
        for j = 1:length(methylIndexesList{i})
            % Iterate through the CpGs for the current SNP and get the
            % correlation for each
            methylValues = locationsBetasIndividualsMethylRand(methylIndexesList{i}(j), :);
            numIndividualsRefNan = length(find(isnan(methylValues(individualsRefArray{i}))));
            numIndividualsHetNan = length(find(isnan(methylValues(individualsHetArray{i}))));
            numIndividualsAltNan = length(find(isnan(methylValues(individualsAltArray{i}))));
            fracReadsMethylRef = fracReadsRef * ((nansum(methylValues(individualsRefArray{i})) + (.5 * nansum(methylValues(individualsHetArray{i}))))/(length(individualsRefArray{i}) - numIndividualsRefNan + (.5 * (length(individualsHetArray{i}) - numIndividualsHetNan))));
            %fracReadsUnmethylRef = fracReadsRef * ((nansum(1 - methylValues(individualsRefArray{i})) + (.5 * nansum(1 - methylValues(individualsHetArray{i}))))/(length(individualsRefArray{i}) - numIndividualsRefNan + (.5 * (length(individualsHetArray{i}) - numIndividualsHetNan))));
            fracReadsMethylAlt = fracReadsAlt * ((nansum(methylValues(individualsAltArray{i})) + (.5 * nansum(methylValues(individualsHetArray{i}))))/(length(individualsAltArray{i}) - numIndividualsAltNan + (.5 * (length(individualsHetArray{i}) - numIndividualsHetNan))));
            fracReadsUnmethylAlt = fracReadsAlt * ((nansum(1 - methylValues(individualsAltArray{i})) + (.5 * nansum(1 - methylValues(individualsHetArray{i}))))/(length(individualsAltArray{i}) - numIndividualsAltNan + (.5 * (length(individualsHetArray{i}) - numIndividualsHetNan))));
            
            % Table indicating values for Fisher's Exact Test (taken from 
            % fexact.m by Mike Boedigheimer).
            %       Methyl.  Unmethyl.
            % Alt.   a        c       K
            % Ref.   b        d       -
            % total  N        -       M
            % a,b,c,d are the numbers of alternative and reference alleles 
            % for the methylated and unmethylated CpGs. K, N, M are the 
            % row, column, and grand totals.  (M = numSimulatedReads.)
            a = round(numSimulatedReadsList{i}(j) * fracReadsMethylAlt);
            K = round(numSimulatedReadsList{i}(j) * (fracReadsMethylAlt + fracReadsUnmethylAlt));
            N = round(numSimulatedReadsList{i}(j) * (fracReadsMethylAlt + fracReadsMethylRef));
            M = numSimulatedReadsList{i}(j);
            if a < N + K - numSimulatedReadsList{i}(j)
                % a is too small due to rounding, so add to the number of
                % simulated reads
                M = M + 1;
            end
            mQTLsRandListSimulated{k}(i, methylIndexesList{i}(j)) = fexact(a, M, K, N);
        end
    end
end