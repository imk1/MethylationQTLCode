%numReadsDataCpGs = importdata('autosomes_numReadsNewVecAll_CpGsFilt');
%numReadsMeanCpGs = mean(numReadsDataCpGs);
%negBinParamsCpGs = nbinfit(numReadsDataCpGs);
%save negBinParamsCpGs negBinParamsCpGs

cd /scr/MethylationQTLProject/SimulationsHW/
numSigPooled100IndivsNegBinFTestRegressScaleCpGsPP = zeros(3, 10);
numSigIndivsGenotype100IndivsNegBinFTestRegressScaleCpGsPP = zeros(3, 10);
rankSumPooledLowerGenotype100IndivsNegBinFTestRegress = ones(3, 10);

i = 2;
numReads = (2 ^ i) * 10
for j = 0:9
    % Iteraete through the effect sizes
    k = 0.1;
    [pValsPooled, pValsIndivsGenotype] = simulateRandomReadsNegBinFTestRegressWithParamsScaleHWPlusPlus(200, round(j * k * 10), negBinParamsCpGs, numReadsMeanCpGs, numReads, 10000, k);
    numSigPooled100IndivsNegBinFTestRegressScaleCpGsPP(i/2, j+1) = length(find(pValsPooled < .001));
    numSigIndivsGenotype100IndivsNegBinFTestRegressScaleCpGsPP(i/2, j+1) = length(find(pValsIndivsGenotype < .001));
    rankSumPooledLowerGenotype100IndivsNegBinFTestRegress(i/2, j+1) = ranksum(pValsPooled, pValsIndivsGenotype, 'tail', 'left');
end

i = 4;
numReads = (2 ^ i) * 10
for j = 0:9
    % Iteraete through the effect sizes
    k = 0.1;
    [pValsPooled, pValsIndivsGenotype] = simulateRandomReadsNegBinFTestRegressWithParamsScaleHWPlusPlus(200, round(j * k * 10), negBinParamsCpGs, numReadsMeanCpGs, numReads, 10000, k);
    numSigPooled100IndivsNegBinFTestRegressScaleCpGsPP(i/2, j+1) = length(find(pValsPooled < .001));
    numSigIndivsGenotype100IndivsNegBinFTestRegressScaleCpGsPP(i/2, j+1) = length(find(pValsIndivsGenotype < .001));
    rankSumPooledLowerGenotype100IndivsNegBinFTestRegress(i/2, j+1) = ranksum(pValsPooled, pValsIndivsGenotype, 'tail', 'left');
end

i = 6;
numReads = (2 ^ i) * 10
for j = 0:9
    % Iteraete through the effect sizes
    k = 0.1;
    [pValsPooled, pValsIndivsGenotype] = simulateRandomReadsNegBinFTestRegressWithParamsScaleHWPlusPlus(200, round(j * k * 10), negBinParamsCpGs, numReadsMeanCpGs, numReads, 10000, k);
    numSigPooled100IndivsNegBinFTestRegressScaleCpGsPP(i/2, j+1) = length(find(pValsPooled < .001));
    numSigIndivsGenotype100IndivsNegBinFTestRegressScaleCpGsPP(i/2, j+1) = length(find(pValsIndivsGenotype < .001));
    rankSumPooledLowerGenotype100IndivsNegBinFTestRegress(i/2, j+1) = ranksum(pValsPooled, pValsIndivsGenotype, 'tail', 'left');
end

save numSigPooled100IndivsNegBinFTestRegressScaleCpGsPP numSigPooled100IndivsNegBinFTestRegressScaleCpGsPP
save numSigIndivsGenotype100IndivsNegBinFTestRegressScaleCpGsPP numSigIndivsGenotype100IndivsNegBinFTestRegressScaleCpGsPP
save rankSumPooledLowerGenotype100IndivsNegBinFTestRegress rankSumPooledLowerGenotype100IndivsNegBinFTestRegress

numSigPooled100IndivsNegBinFTestRegressScaleCpGsPPPlus = zeros(7, 10, 5);
numSigIndivsGenotype100IndivsNegBinFTestRegressScaleCpGsPPPlus = zeros(7, 10, 5);
rankSumPooledLowerGenotype100IndivsNegBinFTestRegressPlus = ones(7, 10, 5);

% for i = 1:7
%     % Iterate through numbers of reads
%     numReads = (2 ^ i) * 10
%     for j = 0:9
%         % Iteraete through the effect sizes
%         for k = .1:.1:.5
%             % Iterate through the MAFs
%             if (((i == 2) && (k == .1)) || ((i == 4) && (k == .1))) || ((i == 6) && (k == .1))
%                 % At a parameter setting that has already been computing
%                 numSigPooled100IndivsNegBinFTestRegressScaleCpGsPPPlus(i, j+1, round(10*k)) = numSigPooled100IndivsNegBinFTestRegressScaleCpGsPP(i/2, j+1);
%                 numSigIndivsGenotype100IndivsNegBinFTestRegressScaleCpGsPPPlus(i, j+1, round(10*k)) = numSigIndivsGenotype100IndivsNegBinFTestRegressScaleCpGsPP(i/2, j+1);
%                 rankSumPooledLowerGenotype100IndivsNegBinFTestRegressPlus(i, j+1, round(10*k)) = rankSumPooledLowerGenotype100IndivsNegBinFTestRegressPlus(i/2, j+1);
%                 continue
%             end
%             [pValsPooled, pValsIndivsGenotype] = simulateRandomReadsNegBinFTestRegressWithParamsScaleHWPlusPlus(200, round(j * k * 10), negBinParamsCpGs, numReadsMeanCpGs, numReads, 10000, k);
%             numSigPooled100IndivsNegBinFTestRegressScaleCpGsPPPlus(i, j+1, round(10*k)) = length(find(pValsPooled < .001));
%             numSigIndivsGenotype100IndivsNegBinFTestRegressScaleCpGsPPPlus(i, j+1, round(10*k)) = length(find(pValsIndivsGenotype < .001));
%             rankSumPooledLowerGenotype100IndivsNegBinFTestRegressPlus(i, j+1, round(10*k)) = ranksum(pValsPooled, pValsIndivsGenotype, 'tail', 'left');
%         end
%     end
% end
% 
% save numSigPooled100IndivsNegBinFTestRegressScaleCpGsPPPlus numSigPooled100IndivsNegBinFTestRegressScaleCpGsPPPlus
% save numSigIndivsGenotype100IndivsNegBinFTestRegressScaleCpGsPPPlus numSigIndivsGenotype100IndivsNegBinFTestRegressScaleCpGsPPPlus
% save rankSumPooledLowerGenotype100IndivsNegBinFTestRegressPlus rankSumPooledLowerGenotype100IndivsNegBinFTestRegressPlus
