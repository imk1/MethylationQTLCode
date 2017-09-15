%numReadsDataCpGs = importdata('autosomes_numReadsNewVecAll_CpGsFilt');
%numReadsMeanCpGs = mean(numReadsDataCpGs);
%negBinParamsCpGs = nbinfit(numReadsDataCpGs);
%save negBinParamsCpGs negBinParamsCpGs

cd /scr/MethylationQTLProject/SimulationsHW/
numSigPooled100IndivsNegBinScaleCpGs = zeros(3, 10);
numSigIndivsGenotype100IndivsNegBinScaleCpGs = zeros(3, 10);
rankSumPooledLowerGenotype100IndivsNegBinScaleCpGs = ones(3, 10);

i = 2;
numReads = (2 ^ i) * 10
for j = 0:9
    % Iteraete through the effect sizes
    k = 0.1;
    [pValsPooled, pValsIndivsGenotype] = simulateRandomReadsNegBinWithParamsScaleHWPlus(200, round(j * k * 10), negBinParamsCpGs, numReadsMeanCpGs, numReads, 10000, k);
    numSigPooled100IndivsNegBinScaleCpGs(i/2, j+1) = length(find(pValsPooled < .001));
    numSigIndivsGenotype100IndivsNegBinScaleCpGs(i/2, j+1) = length(find(pValsIndivsGenotype < .001));
    rankSumPooledLowerGenotype100IndivsNegBinScaleCpGs(i/2, j+1) = ranksum(pValsPooled, pValsIndivsGenotype, 'tail', 'left');
end

i = 4;
numReads = (2 ^ i) * 10
for j = 0:9
    % Iteraete through the effect sizes
    k = 0.1;
    [pValsPooled, pValsIndivsGenotype] = simulateRandomReadsNegBinWithParamsScaleHWPlus(200, round(j * k * 10), negBinParamsCpGs, numReadsMeanCpGs, numReads, 10000, k);
    numSigPooled100IndivsNegBinScaleCpGs(i/2, j+1) = length(find(pValsPooled < .001));
    numSigIndivsGenotype100IndivsNegBinScaleCpGs(i/2, j+1) = length(find(pValsIndivsGenotype < .001));
    rankSumPooledLowerGenotype100IndivsNegBinScaleCpGs(i/2, j+1) = ranksum(pValsPooled, pValsIndivsGenotype, 'tail', 'left');
end

i = 6;
numReads = (2 ^ i) * 10
for j = 0:9
    % Iteraete through the effect sizes
    k = 0.1;
    [pValsPooled, pValsIndivsGenotype] = simulateRandomReadsNegBinWithParamsScaleHWPlus(200, round(j * k * 10), negBinParamsCpGs, numReadsMeanCpGs, numReads, 10000, k);
    numSigPooled100IndivsNegBinScaleCpGs(i/2, j+1) = length(find(pValsPooled < .001));
    numSigIndivsGenotype100IndivsNegBinScaleCpGs(i/2, j+1) = length(find(pValsIndivsGenotype < .001));
    rankSumPooledLowerGenotype100IndivsNegBinScaleCpGs(i/2, j+1) = ranksum(pValsPooled, pValsIndivsGenotype, 'tail', 'left');
end

save numSigPooled100IndivsNegBinScaleCpGs numSigPooled100IndivsNegBinScaleCpGs
save numSigIndivsGenotype100IndivsNegBinScaleCpGs numSigIndivsGenotype100IndivsNegBinScaleCpGs
save rankSumPooledLowerGenotype100IndivsNegBinScaleCpGs rankSumPooledLowerGenotype100IndivsNegBinScaleCpGs

numSigPooled100IndivsNegBinScaleCpGsPlus = zeros(7, 10, 5);
numSigIndivsGenotype100IndivsNegBinScaleCpGsPlus = zeros(7, 10, 5);
rankSumPooledLowerGenotype100IndivsNegBinScaleCpGsPlus = ones(7, 10, 5);

for i = 1:7
    % Iterate through numbers of reads
    numReads = (2 ^ i) * 10
    for j = 0:9
        % Iteraete through the effect sizes
        for k = .1:.1:.5
            % Iterate through the MAFs
            if (((i == 2) && (k == .1)) || ((i == 4) && (k == .1))) || ((i == 6) && (k == .1))
                % At a parameter setting that has already been computing
                numSigPooled100IndivsNegBinScaleCpGsPlus(i, j+1, round(10*k)) = numSigPooled100IndivsNegBinScaleCpGs(i/2, j+1);
                continue
            end
            [pValsPooled, pValsIndivsGenotype] = simulateRandomReadsNegBinWithParamsScaleHWPlus(200, round(j * k * 10), negBinParamsCpGs, numReadsMeanCpGs, numReads, 10000, k);
            numSigPooled100IndivsNegBinScaleCpGsPlus(i, j+1, round(10*k)) = length(find(pValsPooled < .001));
            numSigIndivsGenotype100IndivsNegBinScaleCpGsPlus(i, j+1, round(10*k)) = length(find(pValsIndivsGenotype < .001));
            rankSumPooledLowerGenotype100IndivsNegBinScaleCpGsPlus(i, j+1, round(10*k)) = ranksum(pValsPooled, pValsIndivsGenotype, 'tail', 'left');
        end
    end
end

save numSigPooled100IndivsNegBinScaleCpGsPlus numSigPooled100IndivsNegBinScaleCpGsPlus
save numSigIndivsGenotype100IndivsNegBinScaleCpGsPlus numSigIndivsGenotype100IndivsNegBinScaleCpGsPlus
save rankSumPooledLowerGenotype100IndivsNegBinScaleCpGsPlus rankSumPooledLowerGenotype100IndivsNegBinScaleCpGsPlus
