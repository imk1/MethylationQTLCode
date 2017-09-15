%numReadsDataCpGs = importdata('autosomes_numReadsNewVecAll_CpGsFilt');
%numReadsMeanCpGs = mean(numReadsDataCpGs);
%negBinParamsCpGs = nbinfit(numReadsDataCpGs);
%save negBinParamsCpGs negBinParamsCpGs

cd /scr/MethylationQTLProject/SimulationsHW/
numSigPooled100IndivsNegBinFTestScaleCpGsPP = zeros(3, 10);
numSigIndivsGenotype100IndivsNegBinFTestScaleCpGsPP = zeros(3, 10);
rankSumPooledLowerGenotype100IndivsNegBinFTestScaleCpGsPP = ones(3, 10);

i = 2;
numReads = (2 ^ i) * 10
for j = 0:9
    % Iteraete through the effect sizes
    k = 0.1;
    [pValsPooled, pValsIndivsGenotype] = simulateRandomReadsNegBinFTestWithParamsScaleHWPlusPlus(200, round(j * k * 10), negBinParamsCpGs, numReadsMeanCpGs, numReads, 10000, k);
    numSigPooled100IndivsNegBinFTestScaleCpGsPP(i/2, j+1) = length(find(pValsPooled < .001));
    numSigIndivsGenotype100IndivsNegBinFTestScaleCpGsPP(i/2, j+1) = length(find(pValsIndivsGenotype < .001));
    rankSumPooledLowerGenotype100IndivsNegBinFTestScaleCpGsPP(i/2, j+1) = ranksum(pValsPooled, pValsIndivsGenotype, 'tail', 'left');
end

i = 4;
numReads = (2 ^ i) * 10
for j = 0:9
    % Iteraete through the effect sizes
    k = 0.1;
    [pValsPooled, pValsIndivsGenotype] = simulateRandomReadsNegBinFTestWithParamsScaleHWPlusPlus(200, round(j * k * 10), negBinParamsCpGs, numReadsMeanCpGs, numReads, 10000, k);
    numSigPooled100IndivsNegBinFTestScaleCpGsPP(i/2, j+1) = length(find(pValsPooled < .001));
    numSigIndivsGenotype100IndivsNegBinFTestScaleCpGsPP(i/2, j+1) = length(find(pValsIndivsGenotype < .001));
    rankSumPooledLowerGenotype100IndivsNegBinFTestScaleCpGsPP(i/2, j+1) = ranksum(pValsPooled, pValsIndivsGenotype, 'tail', 'left');
end

i = 6;
numReads = (2 ^ i) * 10
for j = 0:9
    % Iteraete through the effect sizes
    k = 0.1;
    [pValsPooled, pValsIndivsGenotype] = simulateRandomReadsNegBinFTestWithParamsScaleHWPlusPlus(200, round(j * k * 10), negBinParamsCpGs, numReadsMeanCpGs, numReads, 10000, k);
    numSigPooled100IndivsNegBinFTestScaleCpGsPP(i/2, j+1) = length(find(pValsPooled < .001));
    numSigIndivsGenotype100IndivsNegBinFTestScaleCpGsPP(i/2, j+1) = length(find(pValsIndivsGenotype < .001));
    rankSumPooledLowerGenotype100IndivsNegBinFTestScaleCpGsPP(i/2, j+1) = ranksum(pValsPooled, pValsIndivsGenotype, 'tail', 'left');
end

save numSigPooled100IndivsNegBinFTestScaleCpGsPP numSigPooled100IndivsNegBinFTestScaleCpGsPP
save numSigIndivsGenotype100IndivsNegBinFTestScaleCpGsPP numSigIndivsGenotype100IndivsNegBinFTestScaleCpGsPP
save rankSumPooledLowerGenotype100IndivsNegBinFTestScaleCpGsPP rankSumPooledLowerGenotype100IndivsNegBinFTestScaleCpGsPP

numSigPooled100IndivsNegBinFTestScaleCpGsPPPlus = zeros(7, 10, 5);
numSigIndivsGenotype100IndivsNegBinFTestScaleCpGsPPPlus = zeros(7, 10, 5);
rankSumPooledLowerGenotype100IndivsNegBinFTestScaleCpGsPPPlus = ones(7, 10, 5);

% for i = 1:7
%     % Iterate through numbers of reads
%     numReads = (2 ^ i) * 10
%     for j = 0:9
%         % Iteraete through the effect sizes
%         for k = .1:.1:.5
%             % Iterate through the MAFs
%             if (((i == 2) && (k == .1)) || ((i == 4) && (k == .1))) || ((i == 6) && (k == .1))
%                 % At a parameter setting that has already been computing
%                 numSigPooled100IndivsNegBinFTestScaleCpGsPPPlus(i, j+1, round(10*k)) = numSigPooled100IndivsNegBinFTestScaleCpGsPP(i/2, j+1);
%                 numSigIndivsGenotype100IndivsNegBinFTestScaleCpGsPPPlus(i, j+1, round(10*k)) = numSigIndivsGenotype100IndivsNegBinFTestScaleCpGsPP(i/2, j+1);
%                 rankSumPooledLowerGenotype100IndivsNegBinFTestScaleCpGsPPPlus(i, j+1, round(10*k)) = rankSumPooledLowerGenotype100IndivsNegBinFTestScaleCpGsPP(i/2, j+1);
%                 continue
%             end
%             [pValsPooled, pValsIndivsGenotype] = simulateRandomReadsNegBinFTestWithParamsScaleHWPlusPlus(200, round(j * k * 10), negBinParamsCpGs, numReadsMeanCpGs, numReads, 10000, k);
%             numSigPooled100IndivsNegBinFTestScaleCpGsPPPlus(i, j+1, round(10*k)) = length(find(pValsPooled < .001));
%             numSigIndivsGenotype100IndivsNegBinFTestScaleCpGsPPPlus(i, j+1, round(10*k)) = length(find(pValsIndivsGenotype < .001));
%             rankSumPooledLowerGenotype100IndivsNegBinFTestScaleCpGsPPPlus(i, j+1, round(10*k)) = ranksum(pValsPooled, pValsIndivsGenotype, 'tail', 'left');
%         end
%     end
% end
% 
% save numSigPooled100IndivsNegBinFTestScaleCpGsPPPlus numSigPooled100IndivsNegBinFTestScaleCpGsPPPlus
% save numSigIndivsGenotype100IndivsNegBinFTestScaleCpGsPPPlus numSigIndivsGenotype100IndivsNegBinFTestScaleCpGsPPPlus
% save rankSumPooledLowerGenotype100IndivsNegBinFTestScaleCpGsPPPlus rankSumPooledLowerGenotype100IndivsNegBinFTestScaleCpGsPPPlus
