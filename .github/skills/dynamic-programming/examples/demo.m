clc; clear;

w = input('请输入物品的重量列表（用逗号分隔）：', 's');
v = input('请输入物品的价值列表（用逗号分隔）：', 's');
c = input('请输入背包的容量：');

% 将字符串按逗号分割并转为数值向量
weights = str2double(strsplit(w, ','));

values  = str2double(strsplit(v, ','));

res = knapsack(weights, values, c);
fprintf('最大价值为: %d\n', res);