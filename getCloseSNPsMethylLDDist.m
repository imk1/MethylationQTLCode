function [closeSNPsMethylLDDist, closeSNPsMethylLDDistRand] = getCloseSNPsMethylLDDist(pValsFileName, mQTLIndexesFileName, pValsRandFileNamePrefix, LDNPsInfoFileName, rCutoff, distanceCutoff, numRand)
% Get SNP, CpG pairs that are in tight LD mQTLs

closeSNPsMethylLDDist = [];

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
    CpGLDChromIndexes = find(strcmp(LDSNPsInfo.textdata, CpGChrom) == 1);
    CpGLDIndexes = union(intersect(CpGLDChromIndexes, LDSNPsInfo.data(:,1)), intersect(CpGLDChromIndexes, LDSNPsInfo.data(:,2)));
    CpGCloseLDIndexes = intersect(CpGLDIndexes, find(LDSNPsInfo.data(:,3) >= rCutoff));
    CpGCloseLDIndexespVals = setdiff(find(ismember(pValsSNPs, CpGCloseLDIndexes)), mQTLIndexes); % Find the rows of the p-value matrix w/SNPs in LD with the current SNP
    CpGCloseLDIndexespValsNew = CpGCloseLDIndexespVals;
    if ~isempty(closeSNPsMethylLDDist)
        % There is at least 1 SNP, CpG pair already added, so do not add it
        CpGCloseLDIndexespValsNew = setdiff(CpGCloseLDIndexespVals, closeSNPsMethylLDDist(:,1));
    end
    
    CpGLocation = pVals.data(mQTLIndexes(i), 1);
    CpGChromIndexes = find(strcmp(pVals.textdata(:,3), CpGChrom) == 1);
    CpGCloseIndexes = intersect(CpGChromIndexes, setdiff(find(abs(pVals.data(:,1) - CpGLocation) < distanceCutoff), mQTLIndexes));
    CpGCloseIndexesNew = CpGCloseIndexes;
    if ~isempty(closeSNPsMethylLDDist)
        % There is at least 1 SNP, CpG pair already added, so do not add it
        CpGCloseIndexesNew = setdiff(CpGCloseIndexes, closeSNPsMethylLDDist(:,1));
    end
    
    CpGCloseLDDistIndexes = intersect(CpGCloseLDIndexespValsNew, CpGCloseIndexesNew);
    
    CpGCloseLDDistpVals = pVals.data(CpGCloseLDDistIndexes, 2);
    CpGCloseIndexespVals = horzcat(CpGCloseLDDistIndexes, CpGCloseLDDistpVals);
    closeSNPsMethylLDDist = vertcat(closeSNPsMethylLDDist, CpGCloseIndexespVals);
end

closeSNPsMethylLDDistRand = zeros(size(closeSNPsMethylLDDist, 1), numRand);
for i = 1:numRand
    % Iterate through the random files and get the SNP, CpG pairs near the
    % mQTLs
    if mod(i, 10) == 1
        i
    end
    pValsRand = importdata(horzcat(pValsRandFileNamePrefix, num2str(i)));
    closeSNPsMethylLDDistRand(:,i) = pValsRand.data(closeSNPsMethylLDDist(:,1), 2);
end