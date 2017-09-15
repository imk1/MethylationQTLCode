%numReadsDataCpGs = importdata('autosomes_numReadsNewVecAll_CpGsFilt');
%numReadsMeanCpGs = mean(numReadsDataCpGs);
%negBinParamsCpGs = nbinfit(numReadsDataCpGs);
%save negBinParamsCpGs negBinParamsCpGs

cd /scr/MethylationQTLProject/SimulationsHW/
numSigPooled100IndivsNegBinCorrScaleCpGsPP = zeros(3, 10);
numSigIndivsGenotype100IndivsNegBinCorrScaleCpGsPP = zeros(3, 10);
rankSumPooledLowerGenotype100IndivsNegBinCorrScaleCpGsPP = ones(3, 10);

i = 2;
numReads = (2 ^ i) * 10
for j = 0:9
    % Iteraete through the effect sizes
    k = 0.1;
    [pValsPooled, pValsIndivsGenotype] = simulateRandomReadsNegBinCorrWithParamsScaleHWPlusPlus(200, round(j * k * 10), negBinParamsCpGs, numReadsMeanCpGs, numReads, 10000, k);
    numSigPooled100IndivsNegBinCorrScaleCpGsPP(i/2, j+1) = length(find(pValsPooled < .001));
    numSigIndivsGenotype100IndivsNegBinCorrScaleCpGsPP(i/2, j+1) = length(find(pValsIndivsGenotype < .001));
    rankSumPooledLowerGenotype100IndivsNegBinCorrScaleCpGsPP(i/2, j+1) = ranksum(pValsPooled, pValsIndivsGenotype, 'tail', 'left');
end

i = 4;
numReads = (2 ^ i) * 10
for j = 0:9
    % Iteraete through the effect sizes
    k = 0.1;
    [pValsPooled, pValsIndivsGenotype] = simulateRandomReadsNegBinCorrWithParamsScaleHWPlusPlus(200, round(j * k * 10), negBinParamsCpGs, numReadsMeanCpGs, numReads, 10000, k);
    numSigPooled100IndivsNegBinCorrScaleCpGsPP(i/2, j+1) = length(find(pValsPooled < .001));
    numSigIndivsGenotype100IndivsNegBinCorrScaleCpGsPP(i/2, j+1) = length(find(pValsIndivsGenotype < .001));
    rankSumPooledLowerGenotype100IndivsNegBinCorrScaleCpGsPP(i/2, j+1) = ranksum(pValsPooled, pValsIndivsGenotype, 'tail', 'left');
end

i = 6;
numReads = (2 ^ i) * 10
for j = 0:9
    % Iteraete through the effect sizes
    k = 0.1;
    [pValsPooled, pValsIndivsGenotype] = simulateRandomReadsNegBinCorrWithParamsScaleHWPlusPlus(200, round(j * k * 10), negBinParamsCpGs, numReadsMeanCpGs, numReads, 10000, k);
    numSigPooled100IndivsNegBinCorrScaleCpGsPP(i/2, j+1) = length(find(pValsPooled < .001));
    numSigIndivsGenotype100IndivsNegBinCorrScaleCpGsPP(i/2, j+1) = length(find(pValsIndivsGenotype < .001));
    rankSumPooledLowerGenotype100IndivsNegBinCorrScaleCpGsPP(i/2, j+1) = ranksum(pValsPooled, pValsIndivsGenotype, 'tail', 'left');
end

save numSigPooled100IndivsNegBinCorrScaleCpGsPP numSigPooled100IndivsNegBinCorrScaleCpGsPP
save numSigIndivsGenotype100IndivsNegBinCorrScaleCpGsPP numSigIndivsGenotype100IndivsNegBinCorrScaleCpGsPP
save rankSumPooledLowerGenotype100IndivsNegBinCorrScaleCpGsPP rankSumPooledLowerGenotype100IndivsNegBinCorrScaleCpGsPP

numSigPooled100IndivsNegBinCorrScaleCpGsPPPlus = zeros(7, 10, 5);
numSigIndivsGenotype100IndivsNegBinCorrScaleCpGsPPPlus = zeros(7, 10, 5);
rankSumPooledLowerGenotype100IndivsNegBinCorrScaleCpGsPPPlus = ones(7, 10, 5);

for i = 1:7
    % Iterate through numbers of reads
    numReads = (2 ^ i) * 10
    for j = 0:9
        % Iteraete through the effect sizes
        for k = .1:.1:.5
            % Iterate through the MAFs
            if (((i == 2) && (k == .1)) || ((i == 4) && (k == .1))) || ((i == 6) && (k == .1))
                % At a parameter setting that has already been computing
                numSigPooled100IndivsNegBinCorrScaleCpGsPPPlus(i, j+1, round(10*k)) = numSigPooled100IndivsNegBinCorrScaleCpGsPP(i/2, j+1);
                numSigIndivsGenotype100IndivsNegBinCorrScaleCpGsPPPlus(i, j+1, round(10*k)) = numSigIndivsGenotype100IndivsNegBinCorrScaleCpGsPP(i/2, j+1);
                rankSumPooledLowerGenotype100IndivsNegBinCorrScaleCpGsPPPlus(i, j+1, round(10*k)) = rankSumPooledLowerGenotype100IndivsNegBinCorrScaleCpGsPP(i/2, j+1);
                continue
            end
            [pValsPooled, pValsIndivsGenotype] = simulateRandomReadsNegBinCorrWithParamsScaleHWPlusPlus(200, round(j * k * 10), negBinParamsCpGs, numReadsMeanCpGs, numReads, 10000, k);
            numSigPooled100IndivsNegBinCorrScaleCpGsPPPlus(i, j+1, round(10*k)) = length(find(pValsPooled < .001));
            numSigIndivsGenotype100IndivsNegBinCorrScaleCpGsPPPlus(i, j+1, round(10*k)) = length(find(pValsIndivsGenotype < .001));
            rankSumPooledLowerGenotype100IndivsNegBinCorrScaleCpGsPPPlus(i, j+1, round(10*k)) = ranksum(pValsPooled, pValsIndivsGenotype, 'tail', 'left');
        end
    end
end

save numSigPooled100IndivsNegBinCorrScaleCpGsPPPlus numSigPooled100IndivsNegBinCorrScaleCpGsPPPlus
save numSigIndivsGenotype100IndivsNegBinCorrScaleCpGsPPPlus numSigIndivsGenotype100IndivsNegBinCorrScaleCpGsPPPlus
save rankSumPooledLowerGenotype100IndivsNegBinCorrScaleCpGsPPPlus rankSumPooledLowerGenotype100IndivsNegBinCorrScaleCpGsPPPlus
