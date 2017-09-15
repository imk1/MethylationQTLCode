pooledFTestRegress100Indivs1MAF40ReadsNegative = [numSigPooledNegBinFTestRegressScaleCpGsPPNegativepVal5(1); numSigPooledNegBinFTestRegressScaleCpGsPPNegativepVal1(1); numSigPooledNegBinFTestRegressScaleCpGsPPNegativepVal05(1); numSigPooledNegBinFTestRegressScaleCpGsPPNegativepVal01(1); numSigPooledNegBinFTestRegressScaleCpGsPPNegativepVal005(1); numSigPooledNegBinFTestRegressScaleCpGsPPNegativepVal001(1); numSigPooledNegBinFTestRegressScaleCpGsPPNegativepVal0005(1); numSigPooledNegBinFTestRegressScaleCpGsPPNegativepVal0001(1); numSigPooledNegBinFTestRegressScaleCpGsPPNegativepVal00005(1); numSigPooledNegBinFTestRegressScaleCpGsPPNegativepVal00001(1)];
save pooledFTestRegress100Indivs1MAF40ReadsNegative pooledFTestRegress100Indivs1MAF40ReadsNegative
genotypeFTestRegress100Indivs1MAF40ReadsNegative = [numSigIndivsGenotypeNegBinFTestRegressScaleCpGsPPNegativepVal5(1); numSigIndivsGenotypeNegBinFTestRegressScaleCpGsPPNegativepVal1(1); numSigIndivsGenotypeNegBinFTestRegressScaleCpGsPPNegativepVal05(1); numSigIndivsGenotypeNegBinFTestRegressScaleCpGsPPNegativepVal01(1); numSigIndivsGenotypeNegBinFTestRegressNegativepVal005(1); numSigIndivsGenotypeNegBinFTestRegressNegativepVal001(1); numSigIndivsGenotypeNegBinFTestRegressNegativepVal0005(1); numSigIndivsGenotypeNegBinFTestRegressNegativepVal0001(1); numSigIndivsGenotypeNegBinFTestRegressNegativepVal00005(1); numSigIndivsGenotypeNegBinFTestRegressNegativepVal00001(1)];
save genotypeFTestRegress100Indivs1MAF40ReadsNegative genotypeFTestRegress100Indivs1MAF40ReadsNegative
genotypeFTestRegress100Indivs1MAF40Reads1EffectSize = [numSigIndivsGenotypeNegBinFTestRegressScaleCpGsPPpVal5(2,1,1); numSigIndivsGenotypeNegBinFTestRegressScaleCpGsPPpVal1(2,1,1); numSigIndivsGenotypeNegBinFTestRegressScaleCpGsPPpVal05(2,1,1); numSigIndivsGenotypeNegBinFTestRegressScaleCpGsPPpVal01(2,1,1); numSigIndivsGenotypeNegBinFTestRegressScaleCpGsPPpVal005(2,1,1); numSigIndivsGenotype100IndivsNegBinFTestRegressScaleCpGsPP(1,1); numSigIndivsGenotypeNegBinFTestRegressScaleCpGsPPpVal0005(2,1,1); numSigIndivsGenotypeNegBinFTestRegressScaleCpGsPPpVal0001(2,1,1); numSigIndivsGenotypeNegBinFTestRegressScaleCpGsPPpVal00005(2,1,1); numSigIndivsGenotypeNegBinFTestRegressScaleCpGsPPpVal00001(2,1,1)];
save genotypeFTestRegress100Indivs1MAF40Reads1EffectSize genotypeFTestRegress100Indivs1MAF40Reads1EffectSize
pooledFTestRegress100Indivs1MAF40Reads1EffectSize = [numSigPooledNegBinFTestRegressScaleCpGsPPpVal5(2,1,1); numSigPooledNegBinFTestRegressScaleCpGsPPpVal1(2,1,1); numSigPooledNegBinFTestRegressScaleCpGsPPpVal05(2,1,1); numSigPooledNegBinFTestRegressScaleCpGsPPpVal01(2,1,1); numSigPooledNegBinFTestRegressScaleCpGsPPpVal005(2,1,1); numSigPooled100IndivsNegBinFTestRegressScaleCpGsPP(1,1); numSigPooledNegBinFTestRegressScaleCpGsPPpVal0005(2,1,1); numSigPooledNegBinFTestRegressScaleCpGsPPpVal0001(2,1,1); numSigPooledNegBinFTestRegressScaleCpGsPPpVal00005(2,1,1); numSigPooledNegBinFTestRegressScaleCpGsPPpVal00001(2,1,1)];
save pooledFTestRegress100Indivs1MAF40Reads1EffectSize pooledFTestRegress100Indivs1MAF40Reads1EffectSize
plot(pooledFTestRegress100Indivs1MAF40ReadsNegative/10000, pooledFTestRegress100Indivs1MAF40Reads1EffectSize/10000, 'r--.', 'LineWidth', 4, 'MarkerSize', 25);
hold on
plot(genotypeFTestRegress100Indivs1MAF40ReadsNegative/10000, genotypeFTestRegress100Indivs1MAF40Reads1EffectSize/10000, 'b--.', 'LineWidth', 4, 'MarkerSize', 25);
xlim([-0.02, 1.02])
ylim([-0.02, 1.02])
set(gca, 'XTick', [0, 0.2, 0.4, 0.6, 0.8, 1.0]);
set(gca, 'YTick', [0, 0.2, 0.4, 0.6, 0.8, 1.0]);
set(gca, 'XTickLabel', {})
set(gca, 'yTickLabel', {})
set(gca, 'LineWidth', 3.0)
hold off
genotypeFTestRegress100Indivs1MAF40Reads05EffectSize = [numSigIndivsGenotypeNegBinFTestRegressScaleCpGsPPpVal5(2,10,1); numSigIndivsGenotypeNegBinFTestRegressScaleCpGsPPpVal1(2,10,1); numSigIndivsGenotypeNegBinFTestRegressScaleCpGsPPpVal05(2,10,1); numSigIndivsGenotypeNegBinFTestRegressScaleCpGsPPpVal01(2,10,1); numSigIndivsGenotypeNegBinFTestRegressScaleCpGsPPpVal005(2,10,1); numSigIndivsGenotype100IndivsNegBinFTestRegressScaleCpGsPP(1,10); numSigIndivsGenotypeNegBinFTestRegressScaleCpGsPPpVal0005(2,10,1); numSigIndivsGenotypeNegBinFTestRegressScaleCpGsPPpVal0001(2,10,1); numSigIndivsGenotypeNegBinFTestRegressScaleCpGsPPpVal00005(2,10,1); numSigIndivsGenotypeNegBinFTestRegressScaleCpGsPPpVal00001(2,10,1)];
save genotypeFTestRegress100Indivs1MAF40Reads05EffectSize genotypeFTestRegress100Indivs1MAF40Reads05EffectSize
pooledFTestRegress100Indivs1MAF40Reads05EffectSize = [numSigPooledNegBinFTestRegressScaleCpGsPPpVal5(2,10,1); numSigPooledNegBinFTestRegressScaleCpGsPPpVal1(2,10,1); numSigPooledNegBinFTestRegressScaleCpGsPPpVal05(2,10,1); numSigPooledNegBinFTestRegressScaleCpGsPPpVal01(2,10,1); numSigPooledNegBinFTestRegressScaleCpGsPPpVal005(2,10,1); numSigPooled100IndivsNegBinFTestRegressScaleCpGsPP(1,10); numSigPooledNegBinFTestRegressScaleCpGsPPpVal0005(2,10,1); numSigPooledNegBinFTestRegressScaleCpGsPPpVal0001(2,10,1); numSigPooledNegBinFTestRegressScaleCpGsPPpVal00005(2,10,1); numSigPooledNegBinFTestRegressScaleCpGsPPpVal00001(2,10,1)];
save pooledFTestRegress100Indivs1MAF40Reads05EffectSize pooledFTestRegress100Indivs1MAF40Reads05EffectSize
plot(pooledFTestRegress100Indivs1MAF40ReadsNegative/10000, pooledFTestRegress100Indivs1MAF40Reads05EffectSize/10000, 'r--.', 'LineWidth', 4, 'MarkerSize', 25);
hold on
plot(genotypeFTestRegress100Indivs1MAF40ReadsNegative/10000, genotypeFTestRegress100Indivs1MAF40Reads05EffectSize/10000, 'b--.', 'LineWidth', 4, 'MarkerSize', 25);
xlim([-0.02, 1.02])
ylim([-0.02, 1.02])
set(gca, 'XTick', [0, 0.2, 0.4, 0.6, 0.8, 1.0]);
set(gca, 'YTick', [0, 0.2, 0.4, 0.6, 0.8, 1.0]);
set(gca, 'XTickLabel', {})
set(gca, 'yTickLabel', {})
set(gca, 'LineWidth', 3.0)
hold off

pooledFTestRegress100Indivs1MAF160ReadsNegative = [numSigPooledNegBinFTestRegressScaleCpGsPPNegativepVal5(2); numSigPooledNegBinFTestRegressScaleCpGsPPNegativepVal1(2); numSigPooledNegBinFTestRegressScaleCpGsPPNegativepVal05(2); numSigPooledNegBinFTestRegressScaleCpGsPPNegativepVal01(2); numSigPooledNegBinFTestRegressScaleCpGsPPNegativepVal005(2); numSigPooledNegBinFTestRegressScaleCpGsPPNegativepVal001(2); numSigPooledNegBinFTestRegressScaleCpGsPPNegativepVal0005(2); numSigPooledNegBinFTestRegressScaleCpGsPPNegativepVal0001(2); numSigPooledNegBinFTestRegressScaleCpGsPPNegativepVal00005(2); numSigPooledNegBinFTestRegressScaleCpGsPPNegativepVal00001(2)];
save pooledFTestRegress100Indivs1MAF160ReadsNegative pooledFTestRegress100Indivs1MAF160ReadsNegative
genotypeFTestRegress100Indivs1MAF160ReadsNegative = [numSigIndivsGenotypeNegBinFTestRegressScaleCpGsPPNegativepVal5(2); numSigIndivsGenotypeNegBinFTestRegressScaleCpGsPPNegativepVal1(2); numSigIndivsGenotypeNegBinFTestRegressScaleCpGsPPNegativepVal05(2); numSigIndivsGenotypeNegBinFTestRegressScaleCpGsPPNegativepVal01(2); numSigIndivsGenotypeNegBinFTestRegressNegativepVal005(2); numSigIndivsGenotypeNegBinFTestRegressNegativepVal001(2); numSigIndivsGenotypeNegBinFTestRegressNegativepVal0005(2); numSigIndivsGenotypeNegBinFTestRegressNegativepVal0001(2); numSigIndivsGenotypeNegBinFTestRegressNegativepVal00005(2); numSigIndivsGenotypeNegBinFTestRegressNegativepVal00001(2)];
save genotypeFTestRegress100Indivs1MAF160ReadsNegative genotypeFTestRegress100Indivs1MAF160ReadsNegative
genotypeFTestRegress100Indivs1MAF160Reads1EffectSize = [numSigIndivsGenotypeNegBinFTestRegressScaleCpGsPPpVal5(4,1,1); numSigIndivsGenotypeNegBinFTestRegressScaleCpGsPPpVal1(4,1,1); numSigIndivsGenotypeNegBinFTestRegressScaleCpGsPPpVal05(4,1,1); numSigIndivsGenotypeNegBinFTestRegressScaleCpGsPPpVal01(4,1,1); numSigIndivsGenotypeNegBinFTestRegressScaleCpGsPPpVal005(4,1,1); numSigIndivsGenotype100IndivsNegBinFTestRegressScaleCpGsPP(2,1); numSigIndivsGenotypeNegBinFTestRegressScaleCpGsPPpVal0005(4,1,1); numSigIndivsGenotypeNegBinFTestRegressScaleCpGsPPpVal0001(4,1,1); numSigIndivsGenotypeNegBinFTestRegressScaleCpGsPPpVal00005(4,1,1); numSigIndivsGenotypeNegBinFTestRegressScaleCpGsPPpVal00001(4,1,1)];
save genotypeFTestRegress100Indivs1MAF160Reads1EffectSize genotypeFTestRegress100Indivs1MAF160Reads1EffectSize
pooledFTestRegress100Indivs1MAF160Reads1EffectSize = [numSigPooledNegBinFTestRegressScaleCpGsPPpVal5(4,1,1); numSigPooledNegBinFTestRegressScaleCpGsPPpVal1(4,1,1); numSigPooledNegBinFTestRegressScaleCpGsPPpVal05(4,1,1); numSigPooledNegBinFTestRegressScaleCpGsPPpVal01(4,1,1); numSigPooledNegBinFTestRegressScaleCpGsPPpVal005(4,1,1); numSigPooled100IndivsNegBinFTestRegressScaleCpGsPP(2,1); numSigPooledNegBinFTestRegressScaleCpGsPPpVal0005(4,1,1); numSigPooledNegBinFTestRegressScaleCpGsPPpVal0001(4,1,1); numSigPooledNegBinFTestRegressScaleCpGsPPpVal00005(4,1,1); numSigPooledNegBinFTestRegressScaleCpGsPPpVal00001(4,1,1)];
save pooledFTestRegress100Indivs1MAF160Reads1EffectSize pooledFTestRegress100Indivs1MAF160Reads1EffectSize
plot(pooledFTestRegress100Indivs1MAF160ReadsNegative/10000, pooledFTestRegress100Indivs1MAF160Reads1EffectSize/10000, 'r--.', 'LineWidth', 4, 'MarkerSize', 25);
hold on
plot(genotypeFTestRegress100Indivs1MAF160ReadsNegative/10000, genotypeFTestRegress100Indivs1MAF160Reads1EffectSize/10000, 'b--.', 'LineWidth', 4, 'MarkerSize', 25);
xlim([-0.02, 1.02])
ylim([-0.02, 1.02])
set(gca, 'XTick', [0, 0.2, 0.4, 0.6, 0.8, 1.0]);
set(gca, 'YTick', [0, 0.2, 0.4, 0.6, 0.8, 1.0]);
set(gca, 'XTickLabel', {})
set(gca, 'yTickLabel', {})
set(gca, 'LineWidth', 3.0)
hold off
genotypeFTestRegress100Indivs1MAF160Reads05EffectSize = [numSigIndivsGenotypeNegBinFTestRegressScaleCpGsPPpVal5(4,10,1); numSigIndivsGenotypeNegBinFTestRegressScaleCpGsPPpVal1(4,10,1); numSigIndivsGenotypeNegBinFTestRegressScaleCpGsPPpVal05(4,10,1); numSigIndivsGenotypeNegBinFTestRegressScaleCpGsPPpVal01(4,10,1); numSigIndivsGenotypeNegBinFTestRegressScaleCpGsPPpVal005(4,10,1); numSigIndivsGenotype100IndivsNegBinFTestRegressScaleCpGsPP(2,10); numSigIndivsGenotypeNegBinFTestRegressScaleCpGsPPpVal0005(4,10,1); numSigIndivsGenotypeNegBinFTestRegressScaleCpGsPPpVal0001(4,10,1); numSigIndivsGenotypeNegBinFTestRegressScaleCpGsPPpVal00005(4,10,1); numSigIndivsGenotypeNegBinFTestRegressScaleCpGsPPpVal00001(4,10,1)];
save genotypeFTestRegress100Indivs1MAF160Reads05EffectSize genotypeFTestRegress100Indivs1MAF160Reads05EffectSize
pooledFTestRegress100Indivs1MAF160Reads05EffectSize = [numSigPooledNegBinFTestRegressScaleCpGsPPpVal5(4,10,1); numSigPooledNegBinFTestRegressScaleCpGsPPpVal1(4,10,1); numSigPooledNegBinFTestRegressScaleCpGsPPpVal05(4,10,1); numSigPooledNegBinFTestRegressScaleCpGsPPpVal01(4,10,1); numSigPooledNegBinFTestRegressScaleCpGsPPpVal005(4,10,1); numSigPooled100IndivsNegBinFTestRegressScaleCpGsPP(2,10); numSigPooledNegBinFTestRegressScaleCpGsPPpVal0005(4,10,1); numSigPooledNegBinFTestRegressScaleCpGsPPpVal0001(4,10,1); numSigPooledNegBinFTestRegressScaleCpGsPPpVal00005(4,10,1); numSigPooledNegBinFTestRegressScaleCpGsPPpVal00001(4,10,1)];
save pooledFTestRegress100Indivs1MAF160Reads05EffectSize pooledFTestRegress100Indivs1MAF160Reads05EffectSize
plot(pooledFTestRegress100Indivs1MAF160ReadsNegative/10000, pooledFTestRegress100Indivs1MAF160Reads05EffectSize/10000, 'r--.', 'LineWidth', 4, 'MarkerSize', 25);
hold on
plot(genotypeFTestRegress100Indivs1MAF160ReadsNegative/10000, genotypeFTestRegress100Indivs1MAF160Reads05EffectSize/10000, 'b--.', 'LineWidth', 4, 'MarkerSize', 25);
xlim([-0.02, 1.02])
ylim([-0.02, 1.02])
set(gca, 'XTick', [0, 0.2, 0.4, 0.6, 0.8, 1.0]);
set(gca, 'YTick', [0, 0.2, 0.4, 0.6, 0.8, 1.0]);
set(gca, 'XTickLabel', {})
set(gca, 'yTickLabel', {})
set(gca, 'LineWidth', 3.0)
hold off

pooledFTestRegress100Indivs1MAF640ReadsNegative = [numSigPooledNegBinFTestRegressScaleCpGsPPNegativepVal5(3); numSigPooledNegBinFTestRegressScaleCpGsPPNegativepVal1(3); numSigPooledNegBinFTestRegressScaleCpGsPPNegativepVal05(3); numSigPooledNegBinFTestRegressScaleCpGsPPNegativepVal01(3); numSigPooledNegBinFTestRegressScaleCpGsPPNegativepVal005(3); numSigPooledNegBinFTestRegressScaleCpGsPPNegativepVal001(3); numSigPooledNegBinFTestRegressScaleCpGsPPNegativepVal0005(3); numSigPooledNegBinFTestRegressScaleCpGsPPNegativepVal0001(3); numSigPooledNegBinFTestRegressScaleCpGsPPNegativepVal00005(3); numSigPooledNegBinFTestRegressScaleCpGsPPNegativepVal00001(3)];
save pooledFTestRegress100Indivs1MAF640ReadsNegative pooledFTestRegress100Indivs1MAF640ReadsNegative
genotypeFTestRegress100Indivs1MAF640ReadsNegative = [numSigIndivsGenotypeNegBinFTestRegressScaleCpGsPPNegativepVal5(3); numSigIndivsGenotypeNegBinFTestRegressScaleCpGsPPNegativepVal1(3); numSigIndivsGenotypeNegBinFTestRegressScaleCpGsPPNegativepVal05(3); numSigIndivsGenotypeNegBinFTestRegressScaleCpGsPPNegativepVal01(3); numSigIndivsGenotypeNegBinFTestRegressNegativepVal005(3); numSigIndivsGenotypeNegBinFTestRegressNegativepVal001(3); numSigIndivsGenotypeNegBinFTestRegressNegativepVal0005(3); numSigIndivsGenotypeNegBinFTestRegressNegativepVal0001(3); numSigIndivsGenotypeNegBinFTestRegressNegativepVal00005(3); numSigIndivsGenotypeNegBinFTestRegressNegativepVal00001(3)];
save genotypeFTestRegress100Indivs1MAF640ReadsNegative genotypeFTestRegress100Indivs1MAF640ReadsNegative
genotypeFTestRegress100Indivs1MAF640Reads1EffectSize = [numSigIndivsGenotypeNegBinFTestRegressScaleCpGsPPpVal5(6,1,1); numSigIndivsGenotypeNegBinFTestRegressScaleCpGsPPpVal1(6,1,1); numSigIndivsGenotypeNegBinFTestRegressScaleCpGsPPpVal05(6,1,1); numSigIndivsGenotypeNegBinFTestRegressScaleCpGsPPpVal01(6,1,1); numSigIndivsGenotypeNegBinFTestRegressScaleCpGsPPpVal005(6,1,1); numSigIndivsGenotype100IndivsNegBinFTestRegressScaleCpGsPP(3,1); numSigIndivsGenotypeNegBinFTestRegressScaleCpGsPPpVal0005(6,1,1); numSigIndivsGenotypeNegBinFTestRegressScaleCpGsPPpVal0001(6,1,1); numSigIndivsGenotypeNegBinFTestRegressScaleCpGsPPpVal00005(6,1,1); numSigIndivsGenotypeNegBinFTestRegressScaleCpGsPPpVal00001(6,1,1)];
save genotypeFTestRegress100Indivs1MAF640Reads1EffectSize genotypeFTestRegress100Indivs1MAF640Reads1EffectSize
pooledFTestRegress100Indivs1MAF640Reads1EffectSize = [numSigPooledNegBinFTestRegressScaleCpGsPPpVal5(6,1,1); numSigPooledNegBinFTestRegressScaleCpGsPPpVal1(6,1,1); numSigPooledNegBinFTestRegressScaleCpGsPPpVal05(6,1,1); numSigPooledNegBinFTestRegressScaleCpGsPPpVal01(6,1,1); numSigPooledNegBinFTestRegressScaleCpGsPPpVal005(6,1,1); numSigPooled100IndivsNegBinFTestRegressScaleCpGsPP(3,1); numSigPooledNegBinFTestRegressScaleCpGsPPpVal0005(6,1,1); numSigPooledNegBinFTestRegressScaleCpGsPPpVal0001(6,1,1); numSigPooledNegBinFTestRegressScaleCpGsPPpVal00005(6,1,1); numSigPooledNegBinFTestRegressScaleCpGsPPpVal00001(6,1,1)];
save pooledFTestRegress100Indivs1MAF640Reads1EffectSize pooledFTestRegress100Indivs1MAF640Reads1EffectSize
plot(pooledFTestRegress100Indivs1MAF640ReadsNegative/10000, pooledFTestRegress100Indivs1MAF640Reads1EffectSize/10000, 'r--.', 'LineWidth', 4, 'MarkerSize', 25);
hold on
plot(genotypeFTestRegress100Indivs1MAF640ReadsNegative/10000, genotypeFTestRegress100Indivs1MAF640Reads1EffectSize/10000, 'b--.', 'LineWidth', 4, 'MarkerSize', 25);
xlim([-0.02, 1.02])
ylim([-0.02, 1.02])
set(gca, 'XTick', [0, 0.2, 0.4, 0.6, 0.8, 1.0]);
set(gca, 'YTick', [0, 0.2, 0.4, 0.6, 0.8, 1.0]);
set(gca, 'XTickLabel', {})
set(gca, 'yTickLabel', {})
set(gca, 'LineWidth', 3.0)
hold off
genotypeFTestRegress100Indivs1MAF640Reads05EffectSize = [numSigIndivsGenotypeNegBinFTestRegressScaleCpGsPPpVal5(6,10,1); numSigIndivsGenotypeNegBinFTestRegressScaleCpGsPPpVal1(6,10,1); numSigIndivsGenotypeNegBinFTestRegressScaleCpGsPPpVal05(6,10,1); numSigIndivsGenotypeNegBinFTestRegressScaleCpGsPPpVal01(6,10,1); numSigIndivsGenotypeNegBinFTestRegressScaleCpGsPPpVal005(6,10,1); numSigIndivsGenotype100IndivsNegBinFTestRegressScaleCpGsPP(3,10); numSigIndivsGenotypeNegBinFTestRegressScaleCpGsPPpVal0005(6,10,1); numSigIndivsGenotypeNegBinFTestRegressScaleCpGsPPpVal0001(6,10,1); numSigIndivsGenotypeNegBinFTestRegressScaleCpGsPPpVal00005(6,10,1); numSigIndivsGenotypeNegBinFTestRegressScaleCpGsPPpVal00001(6,10,1)];
save genotypeFTestRegress100Indivs1MAF640Reads05EffectSize genotypeFTestRegress100Indivs1MAF640Reads05EffectSize
pooledFTestRegress100Indivs1MAF640Reads05EffectSize = [numSigPooledNegBinFTestRegressScaleCpGsPPpVal5(6,10,1); numSigPooledNegBinFTestRegressScaleCpGsPPpVal1(6,10,1); numSigPooledNegBinFTestRegressScaleCpGsPPpVal05(6,10,1); numSigPooledNegBinFTestRegressScaleCpGsPPpVal01(6,10,1); numSigPooledNegBinFTestRegressScaleCpGsPPpVal005(6,10,1); numSigPooled100IndivsNegBinFTestRegressScaleCpGsPP(3,10); numSigPooledNegBinFTestRegressScaleCpGsPPpVal0005(6,10,1); numSigPooledNegBinFTestRegressScaleCpGsPPpVal0001(6,10,1); numSigPooledNegBinFTestRegressScaleCpGsPPpVal00005(6,10,1); numSigPooledNegBinFTestRegressScaleCpGsPPpVal00001(6,10,1)];
save pooledFTestRegress100Indivs1MAF640Reads05EffectSize pooledFTestRegress100Indivs1MAF640Reads05EffectSize
plot(pooledFTestRegress100Indivs1MAF640ReadsNegative/10000, pooledFTestRegress100Indivs1MAF640Reads05EffectSize/10000, 'r--.', 'LineWidth', 4, 'MarkerSize', 25);
hold on
plot(genotypeFTestRegress100Indivs1MAF640ReadsNegative/10000, genotypeFTestRegress100Indivs1MAF640Reads05EffectSize/10000, 'b--.', 'LineWidth', 4, 'MarkerSize', 25);
xlim([-0.02, 1.02])
ylim([-0.02, 1.02])
set(gca, 'XTick', [0, 0.2, 0.4, 0.6, 0.8, 1.0]);
set(gca, 'YTick', [0, 0.2, 0.4, 0.6, 0.8, 1.0]);
set(gca, 'XTickLabel', {})
set(gca, 'yTickLabel', {})
set(gca, 'LineWidth', 3.0)
hold off