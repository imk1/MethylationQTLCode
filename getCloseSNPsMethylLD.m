function [closeSNPsMethylLD, closeSNPsMethylLDRand] = getCloseSNPsMethylLD(pValsFileName, mQTLIndexesFileName, pValsRandFileNamePrefix, LDNPsInfoFileName, rCutoff, numRand)
% Get SNP, CpG pairs that are in tight LD mQTLs

closeSNPsMethylLD = [];

pVals = importdata(pValsFileName);
pValsSNPs = zeros(size(pVals.textdata, 1), 1);
for i = 1:size(pVals.textdata, 1)
    % Iterate through the SNPs and put each in the array
    pValsSNPs(i) = str2num(pVals.textdata{i,2});
end

mQTLIndexes = importdata(mQTLIndexesFileName);
LDSNPsInfo = importdata(LDNPsInfoFileName);

for i = 1:length(mQTLIndexes)
    % Iterate through the mQTLs and find the SNP, CpG pairs near each
    if mod(i,100) == 1
        i
    end
    CpGChrom = pVals.textdata(mQTLIndexes(i), 3);
    CpGChromIndexes = find(strcmp(LDSNPsInfo.textdata, CpGChrom) == 1);
    CpGLDIndexes = union(intersect(CpGChromIndexes, LDSNPsInfo.data(:,1)), intersect(CpGChromIndexes, LDSNPsInfo.data(:,2)));
    CpGCloseLDIndexes = intersect(CpGLDIndexes, find(LDSNPsInfo.data(:,3) >= rCutoff));
    CpGCloseLDIndexespVals = setdiff(find(ismember(pValsSNPs, CpGCloseLDIndexes)), mQTLIndexes); % Find the rows of the p-value matrix w/SNPs in LD with the current SNP
    CpGCloseLDIndexespValsNew = CpGCloseLDIndexespVals;
    if ~isempty(closeSNPsMethylLD)
        % There is at least 1 SNP, CpG pair already added, so do not add it
        CpGCloseLDIndexespValsNew = setdiff(CpGCloseLDIndexespVals, closeSNPsMethylLD(:,1));
    end
    CpGCloseLDpVals = pVals.data(CpGCloseLDIndexespValsNew, 2);
    CpGCloseIndexespVals = horzcat(CpGCloseLDIndexespValsNew, CpGCloseLDpVals);
    closeSNPsMethylLD = vertcat(closeSNPsMethylLD, CpGCloseIndexespVals);
end

closeSNPsMethylLDRand = zeros(size(closeSNPsMethylLD, 1), numRand);
for i = 1:numRand
    % Iterate through the random files and get the SNP, CpG pairs near the
    % mQTLs
    if mod(i, 10) == 1
        i
    end
    pValsRand = importdata(horzcat(pValsRandFileNamePrefix, num2str(i)));
    closeSNPsMethylLDRand(:,i) = pValsRand.data(closeSNPsMethylLD(:,1), 2);
end