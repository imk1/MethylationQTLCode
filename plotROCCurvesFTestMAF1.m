pooledFTest100Indivs1MAF40ReadsNegative = [numSigPooledNegBinFTestScaleCpGsPPNegativepVal5(2,1); numSigPooledNegBinFTestScaleCpGsPPNegativepVal1(2,1); numSigPooledNegBinFTestScaleCpGsPPNegativepVal05(2,1); numSigPooledNegBinFTestScaleCpGsPPNegativepVal01(2,1); numSigPooledNegBinFTestScaleCpGsPPNegativepVal005(2,1); numSigPooledNegBinFTestScaleCpGsPPNegativepVal001(2,1); numSigPooledNegBinFTestScaleCpGsPPNegativepVal0005(2,1); numSigPooledNegBinFTestScaleCpGsPPNegativepVal0001(2,1); numSigPooledNegBinFTestScaleCpGsPPNegativepVal00005(2,1); numSigPooledNegBinFTestScaleCpGsPPNegativepVal00001(2,1)];
save pooledFTest100Indivs1MAF40ReadsNegative pooledFTest100Indivs1MAF40ReadsNegative
genotypeFTest100Indivs1MAF40ReadsNegative = [numSigIndivsGenotypeNegBinFTestScaleCpGsPPNegativepVal5(2,1); numSigIndivsGenotypeNegBinFTestScaleCpGsPPNegativepVal1(2,1); numSigIndivsGenotypeNegBinFTestScaleCpGsPPNegativepVal05(2,1); numSigIndivsGenotypeNegBinFTestScaleCpGsPPNegativepVal01(2,1); numSigIndivsGenotypeNegBinFTestScaleCpGsPPNegativepVal005(2,1); numSigIndivsGenotypeNegBinFTestScaleCpGsPPNegativepVal001(2,1); numSigIndivsGenotypeNegBinFTestScaleCpGsPPNegativepVal0005(2,1); numSigIndivsGenotypeNegBinFTestScaleCpGsPPNegativepVal0001(2,1); numSigIndivsGenotypeNegBinFTestScaleCpGsPPNegativepVal00005(2,1); numSigIndivsGenotypeNegBinFTestScaleCpGsPPNegativepVal00001(2,1)];
save genotypeFTest100Indivs1MAF40ReadsNegative genotypeFTest100Indivs1MAF40ReadsNegative
genotypeFTest100Indivs1MAF40Reads1EffectSize = [numSigIndivsGenotypeNegBinFTestScaleCpGsPPpVal5(2,1,1); numSigIndivsGenotypeNegBinFTestScaleCpGsPPpVal1(2,1,1); numSigIndivsGenotypeNegBinFTestScaleCpGsPPpVal05(2,1,1); numSigIndivsGenotypeNegBinFTestScaleCpGsPPpVal01(2,1,1); numSigIndivsGenotypeNegBinFTestScaleCpGsPPpVal005(2,1,1); numSigIndivsGenotype100IndivsNegBinFTestScaleCpGsPP(1,1); numSigIndivsGenotypeNegBinFTestScaleCpGsPPpVal0005(2,1,1); numSigIndivsGenotypeNegBinFTestScaleCpGsPPpVal0001(2,1,1); numSigIndivsGenotypeNegBinFTestScaleCpGsPPpVal00005(2,1,1); numSigIndivsGenotypeNegBinFTestScaleCpGsPPpVal00001(2,1,1)];
save genotypeFTest100Indivs1MAF40Reads1EffectSize genotypeFTest100Indivs1MAF40Reads1EffectSize
pooledFTest100Indivs1MAF40Reads1EffectSize = [numSigPooledNegBinFTestScaleCpGsPPpVal5(2,1,1); numSigPooledNegBinFTestScaleCpGsPPpVal1(2,1,1); numSigPooledNegBinFTestScaleCpGsPPpVal05(2,1,1); numSigPooledNegBinFTestScaleCpGsPPpVal01(2,1,1); numSigPooledNegBinFTestScaleCpGsPPpVal005(2,1,1); numSigPooled100IndivsNegBinFTestScaleCpGsPP(1,1); numSigPooledNegBinFTestScaleCpGsPPpVal0005(2,1,1); numSigPooledNegBinFTestScaleCpGsPPpVal0001(2,1,1); numSigPooledNegBinFTestScaleCpGsPPpVal00005(2,1,1); numSigPooledNegBinFTestScaleCpGsPPpVal00001(2,1,1)];
save pooledFTest100Indivs1MAF40Reads1EffectSize pooledFTest100Indivs1MAF40Reads1EffectSize
plot(pooledFTest100Indivs1MAF40ReadsNegative/10000, pooledFTest100Indivs1MAF40Reads1EffectSize/10000, 'r--.', 'LineWidth', 4, 'MarkerSize', 25);
hold on
plot(genotypeFTest100Indivs1MAF40ReadsNegative/10000, genotypeFTest100Indivs1MAF40Reads1EffectSize/10000, 'b--.', 'LineWidth', 4, 'MarkerSize', 25);
xlim([-0.02, 1.02])
ylim([-0.02, 1.02])
set(gca, 'XTick', [0, 0.2, 0.4, 0.6, 0.8, 1.0]);
set(gca, 'YTick', [0, 0.2, 0.4, 0.6, 0.8, 1.0]);
set(gca, 'XTickLabel', {})
set(gca, 'yTickLabel', {})
set(gca, 'LineWidth', 3.0)
hold off
genotypeFTest100Indivs1MAF40Reads05EffectSize = [numSigIndivsGenotypeNegBinFTestScaleCpGsPPpVal5(2,10,1); numSigIndivsGenotypeNegBinFTestScaleCpGsPPpVal1(2,10,1); numSigIndivsGenotypeNegBinFTestScaleCpGsPPpVal05(2,10,1); numSigIndivsGenotypeNegBinFTestScaleCpGsPPpVal01(2,10,1); numSigIndivsGenotypeNegBinFTestScaleCpGsPPpVal005(2,10,1); numSigIndivsGenotype100IndivsNegBinFTestScaleCpGsPP(1,10); numSigIndivsGenotypeNegBinFTestScaleCpGsPPpVal0005(2,10,1); numSigIndivsGenotypeNegBinFTestScaleCpGsPPpVal0001(2,10,1); numSigIndivsGenotypeNegBinFTestScaleCpGsPPpVal00005(2,10,1); numSigIndivsGenotypeNegBinFTestScaleCpGsPPpVal00001(2,10,1)];
save genotypeFTest100Indivs1MAF40Reads05EffectSize genotypeFTest100Indivs1MAF40Reads05EffectSize
pooledFTest100Indivs1MAF40Reads05EffectSize = [numSigPooledNegBinFTestScaleCpGsPPpVal5(2,10,1); numSigPooledNegBinFTestScaleCpGsPPpVal1(2,10,1); numSigPooledNegBinFTestScaleCpGsPPpVal05(2,10,1); numSigPooledNegBinFTestScaleCpGsPPpVal01(2,10,1); numSigPooledNegBinFTestScaleCpGsPPpVal005(2,10,1); numSigPooled100IndivsNegBinFTestScaleCpGsPP(1,10); numSigPooledNegBinFTestScaleCpGsPPpVal0005(2,10,1); numSigPooledNegBinFTestScaleCpGsPPpVal0001(2,10,1); numSigPooledNegBinFTestScaleCpGsPPpVal00005(2,10,1); numSigPooledNegBinFTestScaleCpGsPPpVal00001(2,10,1)];
save pooledFTest100Indivs1MAF40Reads05EffectSize pooledFTest100Indivs1MAF40Reads05EffectSize
plot(pooledFTest100Indivs1MAF40ReadsNegative/10000, pooledFTest100Indivs1MAF40Reads05EffectSize/10000, 'r--.', 'LineWidth', 4, 'MarkerSize', 25);
hold on
plot(genotypeFTest100Indivs1MAF40ReadsNegative/10000, genotypeFTest100Indivs1MAF40Reads05EffectSize/10000, 'b--.', 'LineWidth', 4, 'MarkerSize', 25);
xlim([-0.02, 1.02])
ylim([-0.02, 1.02])
set(gca, 'XTick', [0, 0.2, 0.4, 0.6, 0.8, 1.0]);
set(gca, 'YTick', [0, 0.2, 0.4, 0.6, 0.8, 1.0]);
set(gca, 'XTickLabel', {})
set(gca, 'yTickLabel', {})
set(gca, 'LineWidth', 3.0)
hold off

pooledFTest100Indivs1MAF160ReadsNegative = [numSigPooledNegBinFTestScaleCpGsPPNegativepVal5(4,1); numSigPooledNegBinFTestScaleCpGsPPNegativepVal1(4,1); numSigPooledNegBinFTestScaleCpGsPPNegativepVal05(4,1); numSigPooledNegBinFTestScaleCpGsPPNegativepVal01(4,1); numSigPooledNegBinFTestScaleCpGsPPNegativepVal005(4,1); numSigPooledNegBinFTestScaleCpGsPPNegativepVal001(4,1); numSigPooledNegBinFTestScaleCpGsPPNegativepVal0005(4,1); numSigPooledNegBinFTestScaleCpGsPPNegativepVal0001(4,1); numSigPooledNegBinFTestScaleCpGsPPNegativepVal00005(4,1); numSigPooledNegBinFTestScaleCpGsPPNegativepVal00001(4,1)];
save pooledFTest100Indivs1MAF160ReadsNegative pooledFTest100Indivs1MAF160ReadsNegative
genotypeFTest100Indivs1MAF160ReadsNegative = [numSigIndivsGenotypeNegBinFTestScaleCpGsPPNegativepVal5(4,1); numSigIndivsGenotypeNegBinFTestScaleCpGsPPNegativepVal1(4,1); numSigIndivsGenotypeNegBinFTestScaleCpGsPPNegativepVal05(4,1); numSigIndivsGenotypeNegBinFTestScaleCpGsPPNegativepVal01(4,1); numSigIndivsGenotypeNegBinFTestScaleCpGsPPNegativepVal005(4,1); numSigIndivsGenotypeNegBinFTestScaleCpGsPPNegativepVal001(4,1); numSigIndivsGenotypeNegBinFTestScaleCpGsPPNegativepVal0005(4,1); numSigIndivsGenotypeNegBinFTestScaleCpGsPPNegativepVal0001(4,1); numSigIndivsGenotypeNegBinFTestScaleCpGsPPNegativepVal00005(4,1); numSigIndivsGenotypeNegBinFTestScaleCpGsPPNegativepVal00001(4,1)];
save genotypeFTest100Indivs1MAF160ReadsNegative genotypeFTest100Indivs1MAF160ReadsNegative
genotypeFTest100Indivs1MAF160Reads1EffectSize = [numSigIndivsGenotypeNegBinFTestScaleCpGsPPpVal5(4,1,1); numSigIndivsGenotypeNegBinFTestScaleCpGsPPpVal1(4,1,1); numSigIndivsGenotypeNegBinFTestScaleCpGsPPpVal05(4,1,1); numSigIndivsGenotypeNegBinFTestScaleCpGsPPpVal01(4,1,1); numSigIndivsGenotypeNegBinFTestScaleCpGsPPpVal005(4,1,1); numSigIndivsGenotype100IndivsNegBinFTestScaleCpGsPP(2,1); numSigIndivsGenotypeNegBinFTestScaleCpGsPPpVal0005(4,1,1); numSigIndivsGenotypeNegBinFTestScaleCpGsPPpVal0001(4,1,1); numSigIndivsGenotypeNegBinFTestScaleCpGsPPpVal00005(4,1,1); numSigIndivsGenotypeNegBinFTestScaleCpGsPPpVal00001(4,1,1)];
save genotypeFTest100Indivs1MAF160Reads1EffectSize genotypeFTest100Indivs1MAF160Reads1EffectSize
pooledFTest100Indivs1MAF160Reads1EffectSize = [numSigPooledNegBinFTestScaleCpGsPPpVal5(4,1,1); numSigPooledNegBinFTestScaleCpGsPPpVal1(4,1,1); numSigPooledNegBinFTestScaleCpGsPPpVal05(4,1,1); numSigPooledNegBinFTestScaleCpGsPPpVal01(4,1,1); numSigPooledNegBinFTestScaleCpGsPPpVal005(4,1,1); numSigPooled100IndivsNegBinFTestScaleCpGsPP(2,1); numSigPooledNegBinFTestScaleCpGsPPpVal0005(4,1,1); numSigPooledNegBinFTestScaleCpGsPPpVal0001(4,1,1); numSigPooledNegBinFTestScaleCpGsPPpVal00005(4,1,1); numSigPooledNegBinFTestScaleCpGsPPpVal00001(4,1,1)];
save pooledFTest100Indivs1MAF160Reads1EffectSize pooledFTest100Indivs1MAF160Reads1EffectSize
plot(pooledFTest100Indivs1MAF160ReadsNegative/10000, pooledFTest100Indivs1MAF160Reads1EffectSize/10000, 'r--.', 'LineWidth', 4, 'MarkerSize', 25);
hold on
plot(genotypeFTest100Indivs1MAF160ReadsNegative/10000, genotypeFTest100Indivs1MAF160Reads1EffectSize/10000, 'b--.', 'LineWidth', 4, 'MarkerSize', 25);
xlim([-0.02, 1.02])
ylim([-0.02, 1.02])
set(gca, 'XTick', [0, 0.2, 0.4, 0.6, 0.8, 1.0]);
set(gca, 'YTick', [0, 0.2, 0.4, 0.6, 0.8, 1.0]);
set(gca, 'XTickLabel', {})
set(gca, 'yTickLabel', {})
set(gca, 'LineWidth', 3.0)
hold off
genotypeFTest100Indivs1MAF160Reads05EffectSize = [numSigIndivsGenotypeNegBinFTestScaleCpGsPPpVal5(4,10,1); numSigIndivsGenotypeNegBinFTestScaleCpGsPPpVal1(4,10,1); numSigIndivsGenotypeNegBinFTestScaleCpGsPPpVal05(4,10,1); numSigIndivsGenotypeNegBinFTestScaleCpGsPPpVal01(4,10,1); numSigIndivsGenotypeNegBinFTestScaleCpGsPPpVal005(4,10,1); numSigIndivsGenotype100IndivsNegBinFTestScaleCpGsPP(2,10); numSigIndivsGenotypeNegBinFTestScaleCpGsPPpVal0005(4,10,1); numSigIndivsGenotypeNegBinFTestScaleCpGsPPpVal0001(4,10,1); numSigIndivsGenotypeNegBinFTestScaleCpGsPPpVal00005(4,10,1); numSigIndivsGenotypeNegBinFTestScaleCpGsPPpVal00001(4,10,1)];
save genotypeFTest100Indivs1MAF160Reads05EffectSize genotypeFTest100Indivs1MAF160Reads05EffectSize
pooledFTest100Indivs1MAF160Reads05EffectSize = [numSigPooledNegBinFTestScaleCpGsPPpVal5(4,10,1); numSigPooledNegBinFTestScaleCpGsPPpVal1(4,10,1); numSigPooledNegBinFTestScaleCpGsPPpVal05(4,10,1); numSigPooledNegBinFTestScaleCpGsPPpVal01(4,10,1); numSigPooledNegBinFTestScaleCpGsPPpVal005(4,10,1); numSigPooled100IndivsNegBinFTestScaleCpGsPP(2,10); numSigPooledNegBinFTestScaleCpGsPPpVal0005(4,10,1); numSigPooledNegBinFTestScaleCpGsPPpVal0001(4,10,1); numSigPooledNegBinFTestScaleCpGsPPpVal00005(4,10,1); numSigPooledNegBinFTestScaleCpGsPPpVal00001(4,10,1)];
save pooledFTest100Indivs1MAF160Reads05EffectSize pooledFTest100Indivs1MAF160Reads05EffectSize
plot(pooledFTest100Indivs1MAF160ReadsNegative/10000, pooledFTest100Indivs1MAF160Reads05EffectSize/10000, 'r--.', 'LineWidth', 4, 'MarkerSize', 25);
hold on
plot(genotypeFTest100Indivs1MAF160ReadsNegative/10000, genotypeFTest100Indivs1MAF160Reads05EffectSize/10000, 'b--.', 'LineWidth', 4, 'MarkerSize', 25);
xlim([-0.02, 1.02])
ylim([-0.02, 1.02])
set(gca, 'XTick', [0, 0.2, 0.4, 0.6, 0.8, 1.0]);
set(gca, 'YTick', [0, 0.2, 0.4, 0.6, 0.8, 1.0]);
set(gca, 'XTickLabel', {})
set(gca, 'yTickLabel', {})
set(gca, 'LineWidth', 3.0)
hold off

pooledFTest100Indivs1MAF640ReadsNegative = [numSigPooledNegBinFTestScaleCpGsPPNegativepVal5(6,1); numSigPooledNegBinFTestScaleCpGsPPNegativepVal1(6,1); numSigPooledNegBinFTestScaleCpGsPPNegativepVal05(6,1); numSigPooledNegBinFTestScaleCpGsPPNegativepVal01(6,1); numSigPooledNegBinFTestScaleCpGsPPNegativepVal005(6,1); numSigPooledNegBinFTestScaleCpGsPPNegativepVal001(6,1); numSigPooledNegBinFTestScaleCpGsPPNegativepVal0005(6,1); numSigPooledNegBinFTestScaleCpGsPPNegativepVal0001(6,1); numSigPooledNegBinFTestScaleCpGsPPNegativepVal00005(6,1); numSigPooledNegBinFTestScaleCpGsPPNegativepVal00001(6,1)];
save pooledFTest100Indivs1MAF640ReadsNegative pooledFTest100Indivs1MAF640ReadsNegative
genotypeFTest100Indivs1MAF640ReadsNegative = [numSigIndivsGenotypeNegBinFTestScaleCpGsPPNegativepVal5(6,1); numSigIndivsGenotypeNegBinFTestScaleCpGsPPNegativepVal1(6,1); numSigIndivsGenotypeNegBinFTestScaleCpGsPPNegativepVal05(6,1); numSigIndivsGenotypeNegBinFTestScaleCpGsPPNegativepVal01(6,1); numSigIndivsGenotypeNegBinFTestScaleCpGsPPNegativepVal005(6,1); numSigIndivsGenotypeNegBinFTestScaleCpGsPPNegativepVal001(6,1); numSigIndivsGenotypeNegBinFTestScaleCpGsPPNegativepVal0005(6,1); numSigIndivsGenotypeNegBinFTestScaleCpGsPPNegativepVal0001(6,1); numSigIndivsGenotypeNegBinFTestScaleCpGsPPNegativepVal00005(6,1); numSigIndivsGenotypeNegBinFTestScaleCpGsPPNegativepVal00001(6,1)];
save genotypeFTest100Indivs1MAF640ReadsNegative genotypeFTest100Indivs1MAF640ReadsNegative
genotypeFTest100Indivs1MAF640Reads1EffectSize = [numSigIndivsGenotypeNegBinFTestScaleCpGsPPpVal5(6,1,1); numSigIndivsGenotypeNegBinFTestScaleCpGsPPpVal1(6,1,1); numSigIndivsGenotypeNegBinFTestScaleCpGsPPpVal05(6,1,1); numSigIndivsGenotypeNegBinFTestScaleCpGsPPpVal01(6,1,1); numSigIndivsGenotypeNegBinFTestScaleCpGsPPpVal005(6,1,1); numSigIndivsGenotype100IndivsNegBinFTestScaleCpGsPP(3,1); numSigIndivsGenotypeNegBinFTestScaleCpGsPPpVal0005(6,1,1); numSigIndivsGenotypeNegBinFTestScaleCpGsPPpVal0001(6,1,1); numSigIndivsGenotypeNegBinFTestScaleCpGsPPpVal00005(6,1,1); numSigIndivsGenotypeNegBinFTestScaleCpGsPPpVal00001(6,1,1)];
save genotypeFTest100Indivs1MAF640Reads1EffectSize genotypeFTest100Indivs1MAF640Reads1EffectSize
pooledFTest100Indivs1MAF640Reads1EffectSize = [numSigPooledNegBinFTestScaleCpGsPPpVal5(6,1,1); numSigPooledNegBinFTestScaleCpGsPPpVal1(6,1,1); numSigPooledNegBinFTestScaleCpGsPPpVal05(6,1,1); numSigPooledNegBinFTestScaleCpGsPPpVal01(6,1,1); numSigPooledNegBinFTestScaleCpGsPPpVal005(6,1,1); numSigPooled100IndivsNegBinFTestScaleCpGsPP(3,1); numSigPooledNegBinFTestScaleCpGsPPpVal0005(6,1,1); numSigPooledNegBinFTestScaleCpGsPPpVal0001(6,1,1); numSigPooledNegBinFTestScaleCpGsPPpVal00005(6,1,1); numSigPooledNegBinFTestScaleCpGsPPpVal00001(6,1,1)];
save pooledFTest100Indivs1MAF640Reads1EffectSize pooledFTest100Indivs1MAF640Reads1EffectSize
plot(pooledFTest100Indivs1MAF640ReadsNegative/10000, pooledFTest100Indivs1MAF640Reads1EffectSize/10000, 'r--.', 'LineWidth', 4, 'MarkerSize', 25);
hold on
plot(genotypeFTest100Indivs1MAF640ReadsNegative/10000, genotypeFTest100Indivs1MAF640Reads1EffectSize/10000, 'b--.', 'LineWidth', 4, 'MarkerSize', 25);
xlim([-0.02, 1.02])
ylim([-0.02, 1.02])
set(gca, 'XTick', [0, 0.2, 0.4, 0.6, 0.8, 1.0]);
set(gca, 'YTick', [0, 0.2, 0.4, 0.6, 0.8, 1.0]);
set(gca, 'XTickLabel', {})
set(gca, 'yTickLabel', {})
set(gca, 'LineWidth', 3.0)
hold off
genotypeFTest100Indivs1MAF640Reads05EffectSize = [numSigIndivsGenotypeNegBinFTestScaleCpGsPPpVal5(6,10,1); numSigIndivsGenotypeNegBinFTestScaleCpGsPPpVal1(6,10,1); numSigIndivsGenotypeNegBinFTestScaleCpGsPPpVal05(6,10,1); numSigIndivsGenotypeNegBinFTestScaleCpGsPPpVal01(6,10,1); numSigIndivsGenotypeNegBinFTestScaleCpGsPPpVal005(6,10,1); numSigIndivsGenotype100IndivsNegBinFTestScaleCpGsPP(3,10); numSigIndivsGenotypeNegBinFTestScaleCpGsPPpVal0005(6,10,1); numSigIndivsGenotypeNegBinFTestScaleCpGsPPpVal0001(6,10,1); numSigIndivsGenotypeNegBinFTestScaleCpGsPPpVal00005(6,10,1); numSigIndivsGenotypeNegBinFTestScaleCpGsPPpVal00001(6,10,1)];
save genotypeFTest100Indivs1MAF640Reads05EffectSize genotypeFTest100Indivs1MAF640Reads05EffectSize
pooledFTest100Indivs1MAF640Reads05EffectSize = [numSigPooledNegBinFTestScaleCpGsPPpVal5(6,10,1); numSigPooledNegBinFTestScaleCpGsPPpVal1(6,10,1); numSigPooledNegBinFTestScaleCpGsPPpVal05(6,10,1); numSigPooledNegBinFTestScaleCpGsPPpVal01(6,10,1); numSigPooledNegBinFTestScaleCpGsPPpVal005(6,10,1); numSigPooled100IndivsNegBinFTestScaleCpGsPP(3,10); numSigPooledNegBinFTestScaleCpGsPPpVal0005(6,10,1); numSigPooledNegBinFTestScaleCpGsPPpVal0001(6,10,1); numSigPooledNegBinFTestScaleCpGsPPpVal00005(6,10,1); numSigPooledNegBinFTestScaleCpGsPPpVal00001(6,10,1)];
save pooledFTest100Indivs1MAF640Reads05EffectSize pooledFTest100Indivs1MAF640Reads05EffectSize
plot(pooledFTest100Indivs1MAF640ReadsNegative/10000, pooledFTest100Indivs1MAF640Reads05EffectSize/10000, 'r--.', 'LineWidth', 4, 'MarkerSize', 25);
hold on
plot(genotypeFTest100Indivs1MAF640ReadsNegative/10000, genotypeFTest100Indivs1MAF640Reads05EffectSize/10000, 'b--.', 'LineWidth', 4, 'MarkerSize', 25);
xlim([-0.02, 1.02])
ylim([-0.02, 1.02])
set(gca, 'XTick', [0, 0.2, 0.4, 0.6, 0.8, 1.0]);
set(gca, 'YTick', [0, 0.2, 0.4, 0.6, 0.8, 1.0]);
set(gca, 'XTickLabel', {})
set(gca, 'yTickLabel', {})
set(gca, 'LineWidth', 3.0)
hold off