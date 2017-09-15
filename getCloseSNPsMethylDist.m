function [closeSNPsMethylDist, closeSNPsMethylDistRand] = getCloseSNPsMethylDist(pValsFileName, mQTLIndexesFileName, pValsRandFileNamePrefix, distanceCutoff, numRand)
% Get SNP, CpG pairs that are close to mQTLs

closeSNPsMethylDist = [];
pVals = importdata(pValsFileName);
mQTLIndexes = importdata(mQTLIndexesFileName);

for i = 1:length(mQTLIndexes)
    % Iterate through the mQTLs and find the SNP, CpG pairs near each
    CpGChrom = pVals.textdata(mQTLIndexes(i), 3);
    CpGLocation = pVals.data(mQTLIndexes(i), 1);
    CpGChromIndexes = find(strcmp(pVals.textdata(:,3), CpGChrom) == 1);
    CpGCloseIndexes = intersect(CpGChromIndexes, setdiff(find(abs(pVals.data(:,1) - CpGLocation) < distanceCutoff), mQTLIndexes));
    CpGCloseIndexesNew = CpGCloseIndexes;
    if ~isempty(closeSNPsMethylDist)
        % There is at least 1 SNP, CpG pair already added, so do not add it
        CpGCloseIndexesNew = setdiff(CpGCloseIndexes, closeSNPsMethylDist(:,1));
    end
    CpGClosepVals = pVals.data(CpGCloseIndexesNew, 2);
    CpGCloseIndexespVals = horzcat(CpGCloseIndexesNew, CpGClosepVals);
    closeSNPsMethylDist = vertcat(closeSNPsMethylDist, CpGCloseIndexespVals);
end

closeSNPsMethylDistRand = zeros(size(closeSNPsMethylDist, 1), numRand);
for i = 1:numRand
    % Iterate through the random files and get the SNP, CpG pairs near the
    % mQTLs
    if mod(i, 10) == 1
        i
    end
    pValsRand = importdata(horzcat(pValsRandFileNamePrefix, num2str(i)));
    closeSNPsMethylDistRand(:,i) = pValsRand.data(closeSNPsMethylDist(:,1), 2);
end