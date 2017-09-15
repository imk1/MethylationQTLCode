function [mQTLsSimulated, mQTLsRandListSimulated] = getmQTLsSimulatedSampleWithReplacement(locationsBetasIndividualsMethylFileName, genotypesFiltFileName, SNPMethylFileName, numPerms, numSimulatedReads)
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
            numReadsMethylAlt = 0;
            numReadsUnmethylAlt = 0;
            numReadsMethylRef = 0;
            numReadsUnmethylRef = 0;
            sampledIndividuals = randsample(numIndividualsPlusOne - 1, numSimulatedReads, 1);
            for k = 1:numSimulatedReads
                currentIndividual = sampledIndividuals(k);
                while isnan(methylValues(currentIndividual))
                    % Choose a different individual until an individual
                    % with no missing data has been found
                    currentIndividual = randsample(numIndividualsPlusOne - 1, 1, 1);
                end
                SNP = genotypesFilt.data(i,currentIndividual + 1)/2;
                methyl = methylValues(currentIndividual);
                randSNP = rand(1);
                randMethyl = rand(1);
                if (randSNP < SNP) && (randMethyl < methyl)
                    % Choose the alterate allele and unmethylated
                    numReadsUnmethylAlt = numReadsUnmethylAlt + 1;
                elseif (randSNP < SNP) && (randMethyl >= methyl)
                    % Choose the alterate allele and methylated
                    numReadsMethylAlt = numReadsMethylAlt + 1;
                elseif (randSNP >= SNP) && (randMethyl < methyl)
                    % Choose the reference allele and unmethylated
                    numReadsUnmethylRef = numReadsUnmethylRef + 1;
                else
                    % Choose the refrence allele and methylated
                    numReadsMethylRef = numReadsMethylRef + 1;
                end
            end
                        
            % Table indicating values for Fisher's Exact Test (taken from 
            % fexact.m by Mike Boedigheimer).
            %       Methyl.  Unmethyl.
            % Alt.   a        c       K
            % Ref.   b        d       -
            % total  N        -       M
            % a,b,c,d are the numbers of alternative and reference alleles 
            % for the methylated and unmethylated CpGs. K, N, M are the 
            % row, column, and grand totals.  (M = numSimulatedReads.)
            a = numReadsMethylAlt;
            K = numReadsMethylAlt + numReadsUnmethylAlt;
            N = numReadsMethylAlt + numReadsMethylRef;
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
for l = 1:numPerms
    % Compute the Fisher's Exact Test p-value for each permutation
    if mod(l, 50) == 1
        l
    end
    permutation = randperm(numIndividualsPlusOne - 1);
    locationsBetasIndividualsMethylRand = locationsBetasIndividualsMethyl.data(:,permutation + 1);
    mQTLsRandListSimulated{l} = sparse(size(genotypesFilt.data, 1), size(locationsBetasIndividualsMethyl.data, 1));
    for i = 1:size(mQTLsSimulated, 1)
        % Iterate through the SNPs and get the correlations with each CpG that
        % is listed for it in the SNPMethyl file
        
        for j = 1:length(methylIndexesList{i})
            % Iterate through the CpGs for the current SNP and get the
            % correlation for each
            methylValues = locationsBetasIndividualsMethylRand(methylIndexesList{i}(j), :);
            numReadsMethylAlt = 0;
            numReadsUnmethylAlt = 0;
            numReadsMethylRef = 0;
            numReadsUnmethylRef = 0;
            sampledIndividuals = randsample(numIndividualsPlusOne - 1, numSimulatedReads, 1);
            for k = 1:numSimulatedReads
                currentIndividual = sampledIndividuals(k);
                while isnan(methylValues(currentIndividual))
                    % Choose a different individual until an individual
                    % with no missing data has been found
                    currentIndividual = randsample(numIndividualsPlusOne - 1, 1, 1);
                end
                SNP = genotypesFilt.data(i,currentIndividual + 1)/2;
                methyl = methylValues(currentIndividual);
                randSNP = rand(1);
                randMethyl = rand(1);
                if (randSNP < SNP) && (randMethyl < methyl)
                    % Choose the alterate allele and unmethylated
                    numReadsUnmethylAlt = numReadsUnmethylAlt + 1;
                elseif (randSNP < SNP) && (randMethyl >= methyl)
                    % Choose the alterate allele and methylated
                    numReadsMethylAlt = numReadsMethylAlt + 1;
                elseif (randSNP >= SNP) && (randMethyl < methyl)
                    % Choose the reference allele and unmethylated
                    numReadsUnmethylRef = numReadsUnmethylRef + 1;
                else
                    % Choose the refrence allele and methylated
                    numReadsMethylRef = numReadsMethylRef + 1;
                end
            end
                        
            % Table indicating values for Fisher's Exact Test (taken from 
            % fexact.m by Mike Boedigheimer).
            %       Methyl.  Unmethyl.
            % Alt.   a        c       K
            % Ref.   b        d       -
            % total  N        -       M
            % a,b,c,d are the numbers of alternative and reference alleles 
            % for the methylated and unmethylated CpGs. K, N, M are the 
            % row, column, and grand totals.  (M = numSimulatedReads.)
            a = numReadsMethylAlt;
            K = numReadsMethylAlt + numReadsUnmethylAlt;
            N = numReadsMethylAlt + numReadsMethylRef;
            M = numSimulatedReads;
            if a < N + K - numSimulatedReads
                % a is too small due to rounding, so add to the number of
                % simulated reads
                M = M + 1;
            end
            mQTLsRandListSimulated{l}(i, methylIndexesList{i}(j)) = fexact(a, M, K, N);
        end
    end
end