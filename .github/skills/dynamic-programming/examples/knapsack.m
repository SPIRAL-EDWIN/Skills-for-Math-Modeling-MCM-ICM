function maxValue = knapsack(weights, values, capacity)
% KNAPSACK 求解 0-1 背包问题的最大价值
%   maxValue = knapsack(weights, values, capacity)
%
%   参数:
%       weights  - 物品重量向量 (1 x n)
%       values   - 物品价值向量 (1 x n)
%       capacity - 背包容量 (标量)
%
%   返回:
%       maxValue - 最大价值

    n = length(weights);  % 物品数量
    % 初始化动态规划表 (n+1) x (capacity+1)
    dp = zeros(n+1, capacity+1);

    % 动态规划求解
    for i = 2:n+1
        for j = 1:capacity+1
            if j-1 < weights(i-1)   % 背包容量不足，不能放入第 i-1 个物品
                dp(i, j) = dp(i-1, j);
            else
                % 比较：不放 or 放入第 i-1 个物品
                dp(i, j) = max(dp(i-1, j), dp(i-1, j - weights(i-1)) + values(i-1));
            end
        end
    end

    % 最大价值在 dp(n+1, capacity+1)
    maxValue = dp(n+1, capacity+1);
end
