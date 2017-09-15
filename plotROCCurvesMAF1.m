pooled100Indivs1MAF40ReadsNegative = [numSigPooledNegBinScaleCpGsPPNegativepVal5(2,1); numSigPooledNegBinScaleCpGsPPNegativepVal1(2,1); numSigPooledNegBinScaleCpGsPPNegativepVal05(2,1); numSigPooledNegBinScaleCpGsPPNegativepVal01(2,1); numSigPooledNegBinScaleCpGsPPNegativepVal005(2,1); numSigPooledNegBinScaleCpGsPPNegativepVal001(2,1); numSigPooledNegBinScaleCpGsPPNegativepVal0005(2,1); numSigPooledNegBinScaleCpGsPPNegativepVal0001(2,1); numSigPooledNegBinScaleCpGsPPNegativepVal00005(2,1); numSigPooledNegBinScaleCpGsPPNegativepVal00001(2,1)];
save pooled100Indivs1MAF40ReadsNegative pooled100Indivs1MAF40ReadsNegative
genotype100Indivs1MAF40ReadsNegative = [numSigIndivsGenotypeNegBinScaleCpGsPPNegativepVal5(2,1); numSigIndivsGenotypeNegBinScaleCpGsPPNegativepVal1(2,1); numSigIndivsGenotypeNegBinScaleCpGsPPNegativepVal05(2,1); numSigIndivsGenotypeNegBinScaleCpGsPPNegativepVal01(2,1); numSigIndivsGenotypeNegBinScaleCpGsPPNegativepVal005(2,1); numSigIndivsGenotypeNegBinScaleCpGsPPNegativepVal001(2,1); numSigIndivsGenotypeNegBinScaleCpGsPPNegativepVal0005(2,1); numSigIndivsGenotypeNegBinScaleCpGsPPNegativepVal0001(2,1); numSigIndivsGenotypeNegBinScaleCpGsPPNegativepVal00005(2,1); numSigIndivsGenotypeNegBinScaleCpGsPPNegativepVal00001(2,1)];
save genotype100Indivs1MAF40ReadsNegative genotype100Indivs1MAF40ReadsNegative
genotype100Indivs1MAF40Reads1EffectSize = [numSigIndivsGenotypeNegBinScaleCpGsPPpVal5(2,1,1); numSigIndivsGenotypeNegBinScaleCpGsPPpVal1(2,1,1); numSigIndivsGenotypeNegBinScaleCpGsPPpVal05(2,1,1); numSigIndivsGenotypeNegBinScaleCpGsPPpVal01(2,1,1); numSigIndivsGenotypeNegBinScaleCpGsPPpVal005(2,1,1); numSigIndivsGenotype100IndivsNegBinScaleCpGsPP(1,1); numSigIndivsGenotypeNegBinScaleCpGsPPpVal0005(2,1,1); numSigIndivsGenotypeNegBinScaleCpGsPPpVal0001(2,1,1); numSigIndivsGenotypeNegBinScaleCpGsPPpVal00005(2,1,1); numSigIndivsGenotypeNegBinScaleCpGsPPpVal00001(2,1,1)];
save genotype100Indivs1MAF40Reads1EffectSize genotype100Indivs1MAF40Reads1EffectSize
pooled100Indivs1MAF40Reads1EffectSize = [numSigPooledNegBinScaleCpGsPPpVal5(2,1,1); numSigPooledNegBinScaleCpGsPPpVal1(2,1,1); numSigPooledNegBinScaleCpGsPPpVal05(2,1,1); numSigPooledNegBinScaleCpGsPPpVal01(2,1,1); numSigPooledNegBinScaleCpGsPPpVal005(2,1,1); numSigPooled100IndivsNegBinScaleCpGsPP(1,1); numSigPooledNegBinScaleCpGsPPpVal0005(2,1,1); numSigPooledNegBinScaleCpGsPPpVal0001(2,1,1); numSigPooledNegBinScaleCpGsPPpVal00005(2,1,1); numSigPooledNegBinScaleCpGsPPpVal00001(2,1,1)];
save pooled100Indivs1MAF40Reads1EffectSize pooled100Indivs1MAF40Reads1EffectSize
plot(pooled100Indivs1MAF40ReadsNegative/10000, pooled100Indivs1MAF40Reads1EffectSize/10000, 'r--.', 'LineWidth', 4, 'MarkerSize', 25);
hold on
plot(genotype100Indivs1MAF40ReadsNegative/10000, genotype100Indivs1MAF40Reads1EffectSize/10000, 'b--.', 'LineWidth', 4, 'MarkerSize', 25);
xlim([-0.02, 1.02])
ylim([-0.02, 1.02])
set(gca, 'XTick', [0, 0.2, 0.4, 0.6, 0.8, 1.0]);
set(gca, 'YTick', [0, 0.2, 0.4, 0.6, 0.8, 1.0]);
set(gca, 'XTickLabel', {})
set(gca, 'yTickLabel', {})
set(gca, 'LineWidth', 3.0)
hold off
genotype100Indivs1MAF40Reads05EffectSize = [numSigIndivsGenotypeNegBinScaleCpGsPPpVal5(2,10,1); numSigIndivsGenotypeNegBinScaleCpGsPPpVal1(2,10,1); numSigIndivsGenotypeNegBinScaleCpGsPPpVal05(2,10,1); numSigIndivsGenotypeNegBinScaleCpGsPPpVal01(2,10,1); numSigIndivsGenotypeNegBinScaleCpGsPPpVal005(2,10,1); numSigIndivsGenotype100IndivsNegBinScaleCpGsPP(1,10); numSigIndivsGenotypeNegBinScaleCpGsPPpVal0005(2,10,1); numSigIndivsGenotypeNegBinScaleCpGsPPpVal0001(2,10,1); numSigIndivsGenotypeNegBinScaleCpGsPPpVal00005(2,10,1); numSigIndivsGenotypeNegBinScaleCpGsPPpVal00001(2,10,1)];
save genotype100Indivs1MAF40Reads05EffectSize genotype100Indivs1MAF40Reads05EffectSize
pooled100Indivs1MAF40Reads05EffectSize = [numSigPooledNegBinScaleCpGsPPpVal5(2,10,1); numSigPooledNegBinScaleCpGsPPpVal1(2,10,1); numSigPooledNegBinScaleCpGsPPpVal05(2,10,1); numSigPooledNegBinScaleCpGsPPpVal01(2,10,1); numSigPooledNegBinScaleCpGsPPpVal005(2,10,1); numSigPooled100IndivsNegBinScaleCpGsPP(1,10); numSigPooledNegBinScaleCpGsPPpVal0005(2,10,1); numSigPooledNegBinScaleCpGsPPpVal0001(2,10,1); numSigPooledNegBinScaleCpGsPPpVal00005(2,10,1); numSigPooledNegBinScaleCpGsPPpVal00001(2,10,1)];
save pooled100Indivs1MAF40Reads05EffectSize pooled100Indivs1MAF40Reads05EffectSize
plot(pooled100Indivs1MAF40ReadsNegative/10000, pooled100Indivs1MAF40Reads05EffectSize/10000, 'r--.', 'LineWidth', 4, 'MarkerSize', 25);
hold on
plot(genotype100Indivs1MAF40ReadsNegative/10000, genotype100Indivs1MAF40Reads05EffectSize/10000, 'b--.', 'LineWidth', 4, 'MarkerSize', 25);
xlim([-0.02, 1.02])
ylim([-0.02, 1.02])
set(gca, 'XTick', [0, 0.2, 0.4, 0.6, 0.8, 1.0]);
set(gca, 'YTick', [0, 0.2, 0.4, 0.6, 0.8, 1.0]);
set(gca, 'XTickLabel', {})
set(gca, 'yTickLabel', {})
set(gca, 'LineWidth', 3.0)
hold off

pooled100Indivs1MAF160ReadsNegative = [numSigPooledNegBinScaleCpGsPPNegativepVal5(4,1); numSigPooledNegBinScaleCpGsPPNegativepVal1(4,1); numSigPooledNegBinScaleCpGsPPNegativepVal05(4,1); numSigPooledNegBinScaleCpGsPPNegativepVal01(4,1); numSigPooledNegBinScaleCpGsPPNegativepVal005(4,1); numSigPooledNegBinScaleCpGsPPNegativepVal001(4,1); numSigPooledNegBinScaleCpGsPPNegativepVal0005(4,1); numSigPooledNegBinScaleCpGsPPNegativepVal0001(4,1); numSigPooledNegBinScaleCpGsPPNegativepVal00005(4,1); numSigPooledNegBinScaleCpGsPPNegativepVal00001(4,1)];
save pooled100Indivs1MAF160ReadsNegative pooled100Indivs1MAF160ReadsNegative
genotype100Indivs1MAF160ReadsNegative = [numSigIndivsGenotypeNegBinScaleCpGsPPNegativepVal5(4,1); numSigIndivsGenotypeNegBinScaleCpGsPPNegativepVal1(4,1); numSigIndivsGenotypeNegBinScaleCpGsPPNegativepVal05(4,1); numSigIndivsGenotypeNegBinScaleCpGsPPNegativepVal01(4,1); numSigIndivsGenotypeNegBinScaleCpGsPPNegativepVal005(4,1); numSigIndivsGenotypeNegBinScaleCpGsPPNegativepVal001(4,1); numSigIndivsGenotypeNegBinScaleCpGsPPNegativepVal0005(4,1); numSigIndivsGenotypeNegBinScaleCpGsPPNegativepVal0001(4,1); numSigIndivsGenotypeNegBinScaleCpGsPPNegativepVal00005(4,1); numSigIndivsGenotypeNegBinScaleCpGsPPNegativepVal00001(4,1)];
save genotype100Indivs1MAF160ReadsNegative genotype100Indivs1MAF160ReadsNegative
genotype100Indivs1MAF160Reads1EffectSize = [numSigIndivsGenotypeNegBinScaleCpGsPPpVal5(4,1,1); numSigIndivsGenotypeNegBinScaleCpGsPPpVal1(4,1,1); numSigIndivsGenotypeNegBinScaleCpGsPPpVal05(4,1,1); numSigIndivsGenotypeNegBinScaleCpGsPPpVal01(4,1,1); numSigIndivsGenotypeNegBinScaleCpGsPPpVal005(4,1,1); numSigIndivsGenotype100IndivsNegBinScaleCpGsPP(2,1); numSigIndivsGenotypeNegBinScaleCpGsPPpVal0005(4,1,1); numSigIndivsGenotypeNegBinScaleCpGsPPpVal0001(4,1,1); numSigIndivsGenotypeNegBinScaleCpGsPPpVal00005(4,1,1); numSigIndivsGenotypeNegBinScaleCpGsPPpVal00001(4,1,1)];
save genotype100Indivs1MAF160Reads1EffectSize genotype100Indivs1MAF160Reads1EffectSize
pooled100Indivs1MAF160Reads1EffectSize = [numSigPooledNegBinScaleCpGsPPpVal5(4,1,1); numSigPooledNegBinScaleCpGsPPpVal1(4,1,1); numSigPooledNegBinScaleCpGsPPpVal05(4,1,1); numSigPooledNegBinScaleCpGsPPpVal01(4,1,1); numSigPooledNegBinScaleCpGsPPpVal005(4,1,1); numSigPooled100IndivsNegBinScaleCpGsPP(2,1); numSigPooledNegBinScaleCpGsPPpVal0005(4,1,1); numSigPooledNegBinScaleCpGsPPpVal0001(4,1,1); numSigPooledNegBinScaleCpGsPPpVal00005(4,1,1); numSigPooledNegBinScaleCpGsPPpVal00001(4,1,1)];
save pooled100Indivs1MAF160Reads1EffectSize pooled100Indivs1MAF160Reads1EffectSize
plot(pooled100Indivs1MAF160ReadsNegative/10000, pooled100Indivs1MAF160Reads1EffectSize/10000, 'r--.', 'LineWidth', 4, 'MarkerSize', 25);
hold on
plot(genotype100Indivs1MAF160ReadsNegative/10000, genotype100Indivs1MAF160Reads1EffectSize/10000, 'b--.', 'LineWidth', 4, 'MarkerSize', 25);
xlim([-0.02, 1.02])
ylim([-0.02, 1.02])
set(gca, 'XTick', [0, 0.2, 0.4, 0.6, 0.8, 1.0]);
set(gca, 'YTick', [0, 0.2, 0.4, 0.6, 0.8, 1.0]);
set(gca, 'XTickLabel', {})
set(gca, 'yTickLabel', {})
set(gca, 'LineWidth', 3.0)
hold off
genotype100Indivs1MAF160Reads05EffectSize = [numSigIndivsGenotypeNegBinScaleCpGsPPpVal5(4,10,1); numSigIndivsGenotypeNegBinScaleCpGsPPpVal1(4,10,1); numSigIndivsGenotypeNegBinScaleCpGsPPpVal05(4,10,1); numSigIndivsGenotypeNegBinScaleCpGsPPpVal01(4,10,1); numSigIndivsGenotypeNegBinScaleCpGsPPpVal005(4,10,1); numSigIndivsGenotype100IndivsNegBinScaleCpGsPP(2,10); numSigIndivsGenotypeNegBinScaleCpGsPPpVal0005(4,10,1); numSigIndivsGenotypeNegBinScaleCpGsPPpVal0001(4,10,1); numSigIndivsGenotypeNegBinScaleCpGsPPpVal00005(4,10,1); numSigIndivsGenotypeNegBinScaleCpGsPPpVal00001(4,10,1)];
save genotype100Indivs1MAF160Reads05EffectSize genotype100Indivs1MAF160Reads05EffectSize
pooled100Indivs1MAF160Reads05EffectSize = [numSigPooledNegBinScaleCpGsPPpVal5(4,10,1); numSigPooledNegBinScaleCpGsPPpVal1(4,10,1); numSigPooledNegBinScaleCpGsPPpVal05(4,10,1); numSigPooledNegBinScaleCpGsPPpVal01(4,10,1); numSigPooledNegBinScaleCpGsPPpVal005(4,10,1); numSigPooled100IndivsNegBinScaleCpGsPP(2,10); numSigPooledNegBinScaleCpGsPPpVal0005(4,10,1); numSigPooledNegBinScaleCpGsPPpVal0001(4,10,1); numSigPooledNegBinScaleCpGsPPpVal00005(4,10,1); numSigPooledNegBinScaleCpGsPPpVal00001(4,10,1)];
save pooled100Indivs1MAF160Reads05EffectSize pooled100Indivs1MAF160Reads05EffectSize
plot(pooled100Indivs1MAF160ReadsNegative/10000, pooled100Indivs1MAF160Reads05EffectSize/10000, 'r--.', 'LineWidth', 4, 'MarkerSize', 25);
hold on
plot(genotype100Indivs1MAF160ReadsNegative/10000, genotype100Indivs1MAF160Reads05EffectSize/10000, 'b--.', 'LineWidth', 4, 'MarkerSize', 25);
xlim([-0.02, 1.02])
ylim([-0.02, 1.02])
set(gca, 'XTick', [0, 0.2, 0.4, 0.6, 0.8, 1.0]);
set(gca, 'YTick', [0, 0.2, 0.4, 0.6, 0.8, 1.0]);
set(gca, 'XTickLabel', {})
set(gca, 'yTickLabel', {})
set(gca, 'LineWidth', 3.0)
hold off

pooled100Indivs1MAF640ReadsNegative = [numSigPooledNegBinScaleCpGsPPNegativepVal5(6,1); numSigPooledNegBinScaleCpGsPPNegativepVal1(6,1); numSigPooledNegBinScaleCpGsPPNegativepVal05(6,1); numSigPooledNegBinScaleCpGsPPNegativepVal01(6,1); numSigPooledNegBinScaleCpGsPPNegativepVal005(6,1); numSigPooledNegBinScaleCpGsPPNegativepVal001(6,1); numSigPooledNegBinScaleCpGsPPNegativepVal0005(6,1); numSigPooledNegBinScaleCpGsPPNegativepVal0001(6,1); numSigPooledNegBinScaleCpGsPPNegativepVal00005(6,1); numSigPooledNegBinScaleCpGsPPNegativepVal00001(6,1)];
save pooled100Indivs1MAF640ReadsNegative pooled100Indivs1MAF640ReadsNegative
genotype100Indivs1MAF640ReadsNegative = [numSigIndivsGenotypeNegBinScaleCpGsPPNegativepVal5(6,1); numSigIndivsGenotypeNegBinScaleCpGsPPNegativepVal1(6,1); numSigIndivsGenotypeNegBinScaleCpGsPPNegativepVal05(6,1); numSigIndivsGenotypeNegBinScaleCpGsPPNegativepVal01(6,1); numSigIndivsGenotypeNegBinScaleCpGsPPNegativepVal005(6,1); numSigIndivsGenotypeNegBinScaleCpGsPPNegativepVal001(6,1); numSigIndivsGenotypeNegBinScaleCpGsPPNegativepVal0005(6,1); numSigIndivsGenotypeNegBinScaleCpGsPPNegativepVal0001(6,1); numSigIndivsGenotypeNegBinScaleCpGsPPNegativepVal00005(6,1); numSigIndivsGenotypeNegBinScaleCpGsPPNegativepVal00001(6,1)];
save genotype100Indivs1MAF640ReadsNegative genotype100Indivs1MAF640ReadsNegative
genotype100Indivs1MAF640Reads1EffectSize = [numSigIndivsGenotypeNegBinScaleCpGsPPpVal5(6,1,1); numSigIndivsGenotypeNegBinScaleCpGsPPpVal1(6,1,1); numSigIndivsGenotypeNegBinScaleCpGsPPpVal05(6,1,1); numSigIndivsGenotypeNegBinScaleCpGsPPpVal01(6,1,1); numSigIndivsGenotypeNegBinScaleCpGsPPpVal005(6,1,1); numSigIndivsGenotype100IndivsNegBinScaleCpGsPP(3,1); numSigIndivsGenotypeNegBinScaleCpGsPPpVal0005(6,1,1); numSigIndivsGenotypeNegBinScaleCpGsPPpVal0001(6,1,1); numSigIndivsGenotypeNegBinScaleCpGsPPpVal00005(6,1,1); numSigIndivsGenotypeNegBinScaleCpGsPPpVal00001(6,1,1)];
save genotype100Indivs1MAF640Reads1EffectSize genotype100Indivs1MAF640Reads1EffectSize
pooled100Indivs1MAF640Reads1EffectSize = [numSigPooledNegBinScaleCpGsPPpVal5(6,1,1); numSigPooledNegBinScaleCpGsPPpVal1(6,1,1); numSigPooledNegBinScaleCpGsPPpVal05(6,1,1); numSigPooledNegBinScaleCpGsPPpVal01(6,1,1); numSigPooledNegBinScaleCpGsPPpVal005(6,1,1); numSigPooled100IndivsNegBinScaleCpGsPP(3,1); numSigPooledNegBinScaleCpGsPPpVal0005(6,1,1); numSigPooledNegBinScaleCpGsPPpVal0001(6,1,1); numSigPooledNegBinScaleCpGsPPpVal00005(6,1,1); numSigPooledNegBinScaleCpGsPPpVal00001(6,1,1)];
save pooled100Indivs1MAF640Reads1EffectSize pooled100Indivs1MAF640Reads1EffectSize
plot(pooled100Indivs1MAF640ReadsNegative/10000, pooled100Indivs1MAF640Reads1EffectSize/10000, 'r--.', 'LineWidth', 4, 'MarkerSize', 25);
hold on
plot(genotype100Indivs1MAF640ReadsNegative/10000, genotype100Indivs1MAF640Reads1EffectSize/10000, 'b--.', 'LineWidth', 4, 'MarkerSize', 25);
xlim([-0.02, 1.02])
ylim([-0.02, 1.02])
set(gca, 'XTick', [0, 0.2, 0.4, 0.6, 0.8, 1.0]);
set(gca, 'YTick', [0, 0.2, 0.4, 0.6, 0.8, 1.0]);
set(gca, 'XTickLabel', {})
set(gca, 'yTickLabel', {})
set(gca, 'LineWidth', 3.0)
hold off
genotype100Indivs1MAF640Reads05EffectSize = [numSigIndivsGenotypeNegBinScaleCpGsPPpVal5(6,10,1); numSigIndivsGenotypeNegBinScaleCpGsPPpVal1(6,10,1); numSigIndivsGenotypeNegBinScaleCpGsPPpVal05(6,10,1); numSigIndivsGenotypeNegBinScaleCpGsPPpVal01(6,10,1); numSigIndivsGenotypeNegBinScaleCpGsPPpVal005(6,10,1); numSigIndivsGenotype100IndivsNegBinScaleCpGsPP(3,10); numSigIndivsGenotypeNegBinScaleCpGsPPpVal0005(6,10,1); numSigIndivsGenotypeNegBinScaleCpGsPPpVal0001(6,10,1); numSigIndivsGenotypeNegBinScaleCpGsPPpVal00005(6,10,1); numSigIndivsGenotypeNegBinScaleCpGsPPpVal00001(6,10,1)];
save genotype100Indivs1MAF640Reads05EffectSize genotype100Indivs1MAF640Reads05EffectSize
pooled100Indivs1MAF640Reads05EffectSize = [numSigPooledNegBinScaleCpGsPPpVal5(6,10,1); numSigPooledNegBinScaleCpGsPPpVal1(6,10,1); numSigPooledNegBinScaleCpGsPPpVal05(6,10,1); numSigPooledNegBinScaleCpGsPPpVal01(6,10,1); numSigPooledNegBinScaleCpGsPPpVal005(6,10,1); numSigPooled100IndivsNegBinScaleCpGsPP(3,10); numSigPooledNegBinScaleCpGsPPpVal0005(6,10,1); numSigPooledNegBinScaleCpGsPPpVal0001(6,10,1); numSigPooledNegBinScaleCpGsPPpVal00005(6,10,1); numSigPooledNegBinScaleCpGsPPpVal00001(6,10,1)];
save pooled100Indivs1MAF640Reads05EffectSize pooled100Indivs1MAF640Reads05EffectSize
plot(pooled100Indivs1MAF640ReadsNegative/10000, pooled100Indivs1MAF640Reads05EffectSize/10000, 'r--.', 'LineWidth', 4, 'MarkerSize', 25);
hold on
plot(genotype100Indivs1MAF640ReadsNegative/10000, genotype100Indivs1MAF640Reads05EffectSize/10000, 'b--.', 'LineWidth', 4, 'MarkerSize', 25);
xlim([-0.02, 1.02])
ylim([-0.02, 1.02])
set(gca, 'XTick', [0, 0.2, 0.4, 0.6, 0.8, 1.0]);
set(gca, 'YTick', [0, 0.2, 0.4, 0.6, 0.8, 1.0]);
set(gca, 'XTickLabel', {})
set(gca, 'yTickLabel', {})
set(gca, 'LineWidth', 3.0)
hold off