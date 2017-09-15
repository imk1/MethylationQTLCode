function [numSigPooledNegBinScaleCpGsPPpVal, numSigIndivsGenotypeNegBinScaleCpGsPPpVal] = simulateNegBinHWPlusPlusScaleNegativeROCScript(numAlleles, negBinParamsCpGs, numReadsMeanCpGs, numReadsExpList, numSimulations, MAFList, pVal)
% Runs simulations and gets numbers of true positives detected with p-value
% < pVal using Fisher's Exact Test

% Parameters used in simulations:
% numAlleles = 200;
% numReadsExpList = 1:7
% numSimulations = 10000
% MAFList = .1:.1:.5

numSigPooledNegBinScaleCpGsPPpVal = zeros(length(numReadsExpList), length(MAFList));
numSigIndivsGenotypeNegBinScaleCpGsPPpVal = zeros(length(numReadsExpList), length(MAFList));

for iIndex = 1:length(numReadsExpList)
    % Iterate through numbers of reads
    i = numReadsExpList(iIndex);
    numReads = (2 ^ i) * 10
    for kIndex = 1:length(MAFList)
        % Iterate through the MAFs
        k = MAFList(kIndex);
        [pValsPooled, pValsIndivsGenotype] = simulateRandomReadsNegBinWithParamsScaleHWPlusPlusNegative(numAlleles, negBinParamsCpGs, numReadsMeanCpGs, numReads, numSimulations, k);
        numSigPooledNegBinScaleCpGsPPpVal(iIndex, round(10*k)) = length(find(pValsPooled < pVal));
        numSigIndivsGenotypeNegBinScaleCpGsPPpVal(iIndex, round(10*k)) = length(find(pValsIndivsGenotype < pVal));
    end
end