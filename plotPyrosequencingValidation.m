y = vertcat(ref1Kids, het1Kids, alt1Kids);
x = vertcat(ones(length(ref1Kids), 1), 2*ones(length(het1Kids), 1), 3*ones(length(alt1Kids), 1));
% Used 800 instead of 1000 for parents, but in figure picture was at 65%
% instead of 52%
scatter(x, y, 1000, '.', 'MarkerEdgeColor', [0.678; 0.922; 1], 'MarkerFaceColor', [0.678; 0.922; 1], 'jitter', 'on', 'jitterAmount', .05);
hold on
% Used 20 instead of 25 for parents, but in figure picture was at 65%
% instead of 52%
plot([1;2;3], [mean(ref1Kids); mean(het1Kids); mean(alt1Kids)], '+k', 'MarkerSize', 25)
xlim([.5, 3.5])
ylim([0, 100])
set(gca, 'XTick', [1, 2, 3])
set(gca, 'YTick', [0, 20, 40, 60, 80, 100])
set(gca, 'XTickLabel', {})
set(gca, 'YTickLabel', {})
hold off