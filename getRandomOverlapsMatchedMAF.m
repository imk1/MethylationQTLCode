function randomOverlapLengths = getRandomOverlapsMatchedMAF(allMAFs, QTLMAFs, mQTLSNPsIndexes, numRandomizations, MAFDiffCutoff)
% Get random overlaps of QTLs and SNP lists of the same length, where the
% SNP lists' MAFs are close to the QTLs' MAFs
% Used to test for enrichment of GWAS hits in mQTLs

% allMAFs: MAFs for SNPs in all SNP, CpG pairs tested for mQTLs
% QTLMAFs: MAFs for mQTLs in SNP, CpG pairs
% mQTLSNPIndexes: Indexes of GWAS SNPs in tested SNP, CpG pairs
% numRandomizations: Number of random SNP lists generated (use 10,000)
% MAFDiffCutoff: Cutoff for how close MAF needs to be to mQTL's MAF (use
%   0.001)

QTLMAFsCloseIndexes = {};
for j = 1:length(QTLMAFs)
    QTLMAFsCloseIndexes{j} = find(abs(allMAFs - QTLMAFs(j)) < MAFDiffCutoff);
end

randomOverlapLengths = zeros(numRandomizations, 1);
for i = 1:numRandomizations
    % For each randomization, permute the list of all MAFs, find the 1st
    % MAFs that are close to the QTL MAFs, and find the number of indexes
    % of those MAFs that are also mQTL SNP indexes
    if mod(i, 100) == 1
        i
    end
    QTLRandIndexes = zeros(length(QTLMAFs), 1);
    for j = 1:length(QTLMAFs)
        % Iterate through the MAFs for the QTLs and find MAFs in the
        % permuted list that are close to those
        randIndexes = randperm(length(QTLMAFsCloseIndexes{j}));
        k = 1;
        while find(ismember(QTLRandIndexes, QTLMAFsCloseIndexes{j}(randIndexes(k)))) == 1
            % Iterete through SNPs with close MAFs until one that has not
            % been selected is found
            k = k + 1;
        end
        QTLRandIndexes(j) = QTLMAFsCloseIndexes{j}(randIndexes(k));
    end
    randomOverlapLengths(i) = length(intersect(QTLRandIndexes, mQTLSNPsIndexes));
end