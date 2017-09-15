cd /scr/MethylationQTLProject/SimulationsHW/
numSigPooled100IndivsNegBinCpGs = zeros(3, 10);
numSigIndivsGenotype100IndivsNegBinCpGs = zeros(3, 10);
rankSumPooledLowerGenotype100IndivsNegBinCpGs = ones(3, 10);
i = 2;
numReads = (2 ^ i) * 10
j = 0;
k = 0.1;
[pValsPooled, pValsIndivsGenotype, negBinCpGsParamsPooled40Reads, negBinCpGsParamsIndivs40Reads] = simulateRandomReadsNegBinHWPlus(200, round(j * k * 10), numReads, 10000, k, numReadsDataCpGs);
numSigPooled100IndivsNegBinCpGs(i/2, j+1) = length(find(pValsPooled < .001));
numSigIndivsGenotype100IndivsNegBinCpGs(i/2, j+1) = length(find(pValsIndivsGenotype < .001));
rankSumPooledLowerGenotype100IndivsNegBinCpGs(i/2, j+1) = ranksum(pValsPooled, pValsIndivsGenotype, 'tail', 'left');
save ../HiseqDataProcessed/NumReadsPerPositionDataNew/negBinCpGsParamsPooled40Reads negBinCpGsParamsPooled40Reads
save ../HiseqDataProcessed/NumReadsPerPositionDataNew/negBinCpGsParamsIndivs40Reads negBinCpGsParamsIndivs40Reads

i = 4;
numReads = (2 ^ i) * 10
j = 0;
k = 0.1;
[pValsPooled, pValsIndivsGenotype, negBinCpGsParamsPooled160Reads, negBinCpGsParamsIndivs160Reads] = simulateRandomReadsNegBinHWPlus(200, round(j * k * 10), numReads, 10000, k, numReadsDataCpGs);
numSigPooled100IndivsNegBinCpGs(i/2, j+1) = length(find(pValsPooled < .001));
numSigIndivsGenotype100IndivsNegBinCpGs(i/2, j+1) = length(find(pValsIndivsGenotype < .001));
rankSumPooledLowerGenotype100IndivsNegBinCpGs(i/2, j+1) = ranksum(pValsPooled, pValsIndivsGenotype, 'tail', 'left');
save ../HiseqDataProcessed/NumReadsPerPositionDataNew/negBinCpGsParamsPooled160Reads negBinCpGsParamsPooled160Reads
save ../HiseqDataProcessed/NumReadsPerPositionDataNew/negBinCpGsParamsIndivs160Reads negBinCpGsParamsIndivs160Reads

i = 6;
numReads = (2 ^ i) * 10
j = 0;
k = 0.1;
[pValsPooled, pValsIndivsGenotype, negBinCpGsParamsPooled640Reads, negBinCpGsParamsIndivs640Reads] = simulateRandomReadsNegBinHWPlus(200, round(j * k * 10), numReads, 10000, k, numReadsDataCpGs);
numSigPooled100IndivsNegBinCpGs(i/2, j+1) = length(find(pValsPooled < .001));
numSigIndivsGenotype100IndivsNegBinCpGs(i/2, j+1) = length(find(pValsIndivsGenotype < .001));
rankSumPooledLowerGenotype100IndivsNegBinCpGs(i/2, j+1) = ranksum(pValsPooled, pValsIndivsGenotype, 'tail', 'left');
save ../HiseqDataProcessed/NumReadsPerPositionDataNew/negBinCpGsParamsPooled640Reads negBinCpGsParamsPooled640Reads
save ../HiseqDataProcessed/NumReadsPerPositionDataNew/negBinCpGsParamsIndivs640Reads negBinCpGsParamsIndivs640Reads

clear numReadsDataCpGs

i = 2
for j = 1:9
    % Iteraete through the effect sizes
    k = 0.1;
    [pValsPooled, pValsIndivsGenotype] = simulateRandomReadsNegBinWithParamsHWPlus(200, round(j * k * 10), negBinCpGsParamsPooled40Reads, negBinCpGsParamsIndivs40Reads, 10000, k);
    numSigPooled100IndivsNegBinCpGs(i/2, j+1) = length(find(pValsPooled < .001));
    numSigIndivsGenotype100IndivsNegBinCpGs(i/2, j+1) = length(find(pValsIndivsGenotype < .001));
    rankSumPooledLowerGenotype100IndivsNegBinCpGs(i/2, j+1) = ranksum(pValsPooled, pValsIndivsGenotype, 'tail', 'left');
end

i = 4
for j = 1:9
    % Iteraete through the effect sizes
    k = 0.1;
    [pValsPooled, pValsIndivsGenotype] = simulateRandomReadsNegBinWithParamsHWPlus(200, round(j * k * 10), negBinCpGsParamsPooled160Reads, negBinCpGsParamsIndivs160Reads, 10000, k);
    numSigPooled100IndivsNegBinCpGs(i/2, j+1) = length(find(pValsPooled < .001));
    numSigIndivsGenotype100IndivsNegBinCpGs(i/2, j+1) = length(find(pValsIndivsGenotype < .001));
    rankSumPooledLowerGenotype100IndivsNegBinCpGs(i/2, j+1) = ranksum(pValsPooled, pValsIndivsGenotype, 'tail', 'left');
end

i = 6
for j = 1:9
    % Iteraete through the effect sizes
    k = 0.1;
    [pValsPooled, pValsIndivsGenotype] = simulateRandomReadsNegBinWithParamsHWPlus(200, round(j * k * 10), negBinCpGsParamsPooled640Reads, negBinCpGsParamsIndivs640Reads, 10000, k);
    numSigPooled100IndivsNegBinCpGs(i/2, j+1) = length(find(pValsPooled < .001));
    numSigIndivsGenotype100IndivsNegBinCpGs(i/2, j+1) = length(find(pValsIndivsGenotype < .001));
    rankSumPooledLowerGenotype100IndivsNegBinCpGs(i/2, j+1) = ranksum(pValsPooled, pValsIndivsGenotype, 'tail', 'left');
end

save numSigPooled100IndivsNegBinCpGs numSigPooled100IndivsNegBinCpGs
save numSigIndivsGenotype100IndivsNegBinCpGs numSigIndivsGenotype100IndivsNegBinCpGs
save rankSumPooledLowerGenotype100IndivsNegBinCpGs rankSumPooledLowerGenotype100IndivsNegBinCpGs

numSigPooled100IndivsNegBinCpGsPlus = zeros(3, 10, 4);
numSigIndivsGenotype100IndivsNegBinCpGsPlus = zeros(3, 10, 4);
rankSumPooledLowerGenotype100IndivsNegBinCpGsPlus = ones(3, 10, 4);

i = 2
for j = 1:9
    % Iteraete through the effect sizes
    for k = .2:.1:.5
        % Iterate through the MAFs
        [pValsPooled, pValsIndivsGenotype] = simulateRandomReadsNegBinWithParamsHWPlus(200, round(j * k * 10), negBinCpGsParamsPooled40Reads, negBinCpGsParamsIndivs40Reads, 10000, k);
        numSigPooled100IndivsNegBinCpGsPlus(i/2, j+1, round(10*k) -1) = length(find(pValsPooled < .001));
        numSigIndivsGenotype100IndivsNegBinCpGsPlus(i/2, j+1, round(10*k) -1) = length(find(pValsIndivsGenotype < .001));
        rankSumPooledLowerGenotype100IndivsNegBinCpGsPlus(i/2, j+1, round(10*k) -1) = ranksum(pValsPooled, pValsIndivsGenotype, 'tail', 'left');
    end
end

i = 4
for j = 1:9
    % Iteraete through the effect sizes
    for k = .2:.1:.5
        % Iterate through the MAFs
        [pValsPooled, pValsIndivsGenotype] = simulateRandomReadsNegBinWithParamsHWPlus(200, round(j * k * 10), negBinCpGsParamsPooled160Reads, negBinCpGsParamsIndivs160Reads, 10000, k);
        numSigPooled100IndivsNegBinCpGsPlus(i/2, j+1, round(10*k) -1) = length(find(pValsPooled < .001));
        numSigIndivsGenotype100IndivsNegBinCpGsPlus(i/2, j+1, round(10*k) -1) = length(find(pValsIndivsGenotype < .001));
        rankSumPooledLowerGenotype100IndivsNegBinCpGsPlus(i/2, j+1, round(10*k) -1) = ranksum(pValsPooled, pValsIndivsGenotype, 'tail', 'left');
    end
end

i = 6
for j = 1:9
    % Iteraete through the effect sizes
    for k = .2:.1:.5
        % Iterate through the MAFs
        [pValsPooled, pValsIndivsGenotype] = simulateRandomReadsNegBinWithParamsHWPlus(200, round(j * k * 10), negBinCpGsParamsPooled640Reads, negBinCpGsParamsIndivs640Reads, 10000, k);
        numSigPooled100IndivsNegBinCpGsPlus(i/2, j+1, round(10*k) -1) = length(find(pValsPooled < .001));
        numSigIndivsGenotype100IndivsNegBinCpGsPlus(i/2, j+1, round(10*k) -1) = length(find(pValsIndivsGenotype < .001));
        rankSumPooledLowerGenotype100IndivsNegBinCpGsPlus(i/2, j+1, round(10*k) -1) = ranksum(pValsPooled, pValsIndivsGenotype, 'tail', 'left');
    end
end

save numSigPooled100IndivsNegBinCpGsPlus numSigPooled100IndivsNegBinCpGsPlus
save numSigIndivsGenotype100IndivsNegBinCpGsPlus numSigIndivsGenotype100IndivsNegBinCpGsPlus
save rankSumPooledLowerGenotype100IndivsNegBinCpGsPlus rankSumPooledLowerGenotype100IndivsNegBinCpGsPlus
