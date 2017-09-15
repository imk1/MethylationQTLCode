function [numSigPooled100IndivsNegBinCorrScaleCpGsPPpVal, numSigIndivsGenotype100IndivsNegBinCorrScaleCpGsPPpVal] = simulateNegBinCorrHWPlusPlusScaleROC(numAlleles, numDevFromPerfectCorrList, negBinParamsCpGs, numReadsMeanCpGs, numReadsExpList, numSimulations, MAFList, pVal)
% Runs simulations and gets numbers of true positives detected with p-value
% < pVal

% Parameters used in simulations:
% numAlleles = 200;
% numDevFromPerfectCorrList = 0:9
% numReadsExpList = 1:7
% numSimulations = 10000
% MAFList = .1:.1:.5

numSigPooled100IndivsNegBinCorrScaleCpGsPPpVal = zeros(length(numReadsExpList), length(numDevFromPerfectCorrList), length(MAFList));
numSigIndivsGenotype100IndivsNegBinCorrScaleCpGsPPpVal = zeros(length(numReadsExpList), length(numDevFromPerfectCorrList), length(MAFList));

for iIndex = 1:length(numReadsExpList)
    % Iterate through numbers of reads
    i = numReadsExpList(i);
    numReads = (2 ^ i) * 10
    for jIndex = 1:length(numDevFromPerfectCorrList)
        % Iteraete through the effect sizes
        j = numDevFromPerfectCorrList(jIndex);
        for kIndex = 1:length(MAFList)
            % Iterate through the MAFs
            k = MAFList(kIndex);
            [pValsPooled, pValsIndivsGenotype] = simulateRandomReadsNegBinCorrWithParamsScaleHWPlusPlus(numAlleles, round(j * k * 10), negBinParamsCpGs, numReadsMeanCpGs, numReads, numSimulations, k);
            numSigPooled100IndivsNegBinCorrScaleCpGsPPpVal(i, j+1, round(10*k)) = length(find(pValsPooled < pVal));
            numSigIndivsGenotype100IndivsNegBinCorrScaleCpGsPPpVal(i, j+1, round(10*k)) = length(find(pValsIndivsGenotype < pVal));
        end
    end
end
