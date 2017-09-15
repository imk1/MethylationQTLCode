numReadsDataCpGs = importdata('autosomes_numReadsNewVecAll_CpGsFilt');
numReadsMeanCpGs = mean(numReadsDataCpGs);
negBinParamsCpGs = nbinfit(numReadsDataCpGs);
save negBinParamsCpGs negBinParamsCpGs

cd /scr/MethylationQTLProject/SimulationsHW/
numSigPooled100IndivsNegBinScaleCpGsPP = zeros(3, 10);
numSigIndivsGenotype100IndivsNegBinScaleCpGsPP = zeros(3, 10);
rankSumPooledLowerGenotype100IndivsNegBinScaleCpGsPP = ones(3, 10);

i = 2;
numReads = (2 ^ i) * 10
for j = 0:9
    % Iteraete through the effect sizes
    k = 0.1;
    [pValsPooled, pValsIndivsGenotype] = simulateRandomReadsNegBinWithParamsScaleHWPlusPlus(200, round(j * k * 10), negBinParamsCpGs, numReadsMeanCpGs, numReads, 10000, k);
    numSigPooled100IndivsNegBinScaleCpGsPP(i/2, j+1) = length(find(pValsPooled < .001));
    numSigIndivsGenotype100IndivsNegBinScaleCpGsPP(i/2, j+1) = length(find(pValsIndivsGenotype < .001));
    rankSumPooledLowerGenotype100IndivsNegBinScaleCpGsPP(i/2, j+1) = ranksum(pValsPooled, pValsIndivsGenotype, 'tail', 'left');
end

i = 4;
numReads = (2 ^ i) * 10
for j = 0:9
    % Iteraete through the effect sizes
    k = 0.1;
    [pValsPooled, pValsIndivsGenotype] = simulateRandomReadsNegBinWithParamsScaleHWPlusPlus(200, round(j * k * 10), negBinParamsCpGs, numReadsMeanCpGs, numReads, 10000, k);
    numSigPooled100IndivsNegBinScaleCpGsPP(i/2, j+1) = length(find(pValsPooled < .001));
    numSigIndivsGenotype100IndivsNegBinScaleCpGsPP(i/2, j+1) = length(find(pValsIndivsGenotype < .001));
    rankSumPooledLowerGenotype100IndivsNegBinScaleCpGsPP(i/2, j+1) = ranksum(pValsPooled, pValsIndivsGenotype, 'tail', 'left');
end

i = 6;
numReads = (2 ^ i) * 10
for j = 0:9
    % Iteraete through the effect sizes
    k = 0.1;
    [pValsPooled, pValsIndivsGenotype] = simulateRandomReadsNegBinWithParamsScaleHWPlusPlus(200, round(j * k * 10), negBinParamsCpGs, numReadsMeanCpGs, numReads, 10000, k);
    numSigPooled100IndivsNegBinScaleCpGsPP(i/2, j+1) = length(find(pValsPooled < .001));
    numSigIndivsGenotype100IndivsNegBinScaleCpGsPP(i/2, j+1) = length(find(pValsIndivsGenotype < .001));
    rankSumPooledLowerGenotype100IndivsNegBinScaleCpGsPP(i/2, j+1) = ranksum(pValsPooled, pValsIndivsGenotype, 'tail', 'left');
end

save numSigPooled100IndivsNegBinScaleCpGsPP numSigPooled100IndivsNegBinScaleCpGsPP
save numSigIndivsGenotype100IndivsNegBinScaleCpGsPP numSigIndivsGenotype100IndivsNegBinScaleCpGsPP
save rankSumPooledLowerGenotype100IndivsNegBinScaleCpGsPP rankSumPooledLowerGenotype100IndivsNegBinScaleCpGsPP

numSigPooled100IndivsNegBinScaleCpGsPPPlus = zeros(7, 10, 5);
numSigIndivsGenotype100IndivsNegBinScaleCpGsPPPlus = zeros(7, 10, 5);
rankSumPooledLowerGenotype100IndivsNegBinScaleCpGsPPPlus = ones(7, 10, 5);

for i = 1:7
    % Iterate through numbers of reads
    numReads = (2 ^ i) * 10
    for j = 0:9
        % Iteraete through the effect sizes
        for k = .1:.1:.5
            % Iterate through the MAFs
            if (((i == 2) && (k == .1)) || ((i == 4) && (k == .1))) || ((i == 6) && (k == .1))
                % At a parameter setting that has already been computing
                numSigPooled100IndivsNegBinScaleCpGsPPPlus(i, j+1, round(10*k)) = numSigPooled100IndivsNegBinScaleCpGsPP(i/2, j+1);
                numSigIndivsGenotype100IndivsNegBinScaleCpGsPPPlus(i, j+1, round(10*k)) = numSigIndivsGenotype100IndivsNegBinScaleCpGsPP(i/2, j+1);
                rankSumPooledLowerGenotype100IndivsNegBinScaleCpGsPPPlus(i, j+1, round(10*k)) = rankSumPooledLowerGenotype100IndivsNegBinScaleCpGsPP(i/2, j+1);
                continue
            end
            [pValsPooled, pValsIndivsGenotype] = simulateRandomReadsNegBinWithParamsScaleHWPlusPlus(200, round(j * k * 10), negBinParamsCpGs, numReadsMeanCpGs, numReads, 10000, k);
            numSigPooled100IndivsNegBinScaleCpGsPPPlus(i, j+1, round(10*k)) = length(find(pValsPooled < .001));
            numSigIndivsGenotype100IndivsNegBinScaleCpGsPPPlus(i, j+1, round(10*k)) = length(find(pValsIndivsGenotype < .001));
            rankSumPooledLowerGenotype100IndivsNegBinScaleCpGsPPPlus(i, j+1, round(10*k)) = ranksum(pValsPooled, pValsIndivsGenotype, 'tail', 'left');
        end
    end
end

save numSigPooled100IndivsNegBinScaleCpGsPPPlus numSigPooled100IndivsNegBinScaleCpGsPPPlus
save numSigIndivsGenotype100IndivsNegBinScaleCpGsPPPlus numSigIndivsGenotype100IndivsNegBinScaleCpGsPPPlus
save rankSumPooledLowerGenotype100IndivsNegBinScaleCpGsPPPlus rankSumPooledLowerGenotype100IndivsNegBinScaleCpGsPPPlus
