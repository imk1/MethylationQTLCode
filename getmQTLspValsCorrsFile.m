function [mQTLsCorrspVals, mQTLsCorrspValsRand] = getmQTLspValsCorrsFile(corrsFileName, corrsRandFileNamePrefix, numPermutations, numRandForFDR)
% Get the p-value for mQTLs and random mQTLs for array data from files with
% correlations on real and permuted data, where the file format is SNP
% chromosome, SNP position, methylation chromosome, methylation position,
% correlation
% ASSUMES THAT THE SNP, CpG PAIRS IN THE PERMUTATION FILES ARE IN THE SAME
% ORDER AS THOSE IN THE REAL FILES

corrsData = importdata(corrsFileName);
corrsDataRandMat = zeros(size(corrsData.data, 1), numPermutations);
numGreaterCorrs = zeros(size(corrsData.data, 1), 1);
corrsRandForFDR = zeros(size(corrsData.data, 1), numRandForFDR);
for i = 1:numPermutations
    % Iterate through the permutations and import the data for each
    %if mod(i, 100) == 1
    %    i
    %end
    corrsDataRand = importdata(horzcat(corrsRandFileNamePrefix, num2str(i)));
    corrsDataRandMat(:,i) = corrsDataRand.data(:,2);
    if isempty(find(corrsDataRandMat(:,i) < 0))
        i
    end
    numGreaterCorrs = numGreaterCorrs + (abs(corrsDataRandMat(:,i)) >= abs(corrsData.data(:,2)));
    if i <= numRandForFDR
        % Put the correation for the current permutation into the random
        % correlation matrix
        corrsRandForFDR(:,i) = abs(corrsDataRandMat(:,i));
    end
end
mQTLsCorrspVals = numGreaterCorrs/numPermutations;

numGreaterCorrsRand = zeros(size(corrsData.data, 1), numRandForFDR);
for i = 1:numPermutations
    % Iterate through the permutations and compare them to the perumutated
    % data
    %if mod(i, 100) == 1
    %    i
    %end
    permutedRepMat = repmat(abs(corrsDataRandMat(:,i)), 1, numRandForFDR);
    numGreaterCorrsRand = numGreaterCorrsRand + (permutedRepMat >= corrsRandForFDR);
    if i <= numRandForFDR
        % Subtract 1 for the current permutation, which is being treated as
        % real
        numGreaterCorrsRand(:,i) = numGreaterCorrsRand(:,i) - 1;
    end
end
mQTLsCorrspValsRand = numGreaterCorrsRand / (numPermutations - 1);