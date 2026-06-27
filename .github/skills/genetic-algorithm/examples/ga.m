% ga_tsp.m — 遗传算法 (GA) 解 TSP（与给定 Python 脚本等价）
% 依赖：calc.m, plot_ans.m
% 数据文件：points.json  内容形如 [[x1,y1],[x2,y2],...]

clc; clear; close all;
rng('shuffle');

%% 读取点集
raw = jsondecode(fileread('points.json'));
if iscell(raw)
    points = vertcat(raw{:});   % 若为元胞，拼成 N×2
else
    points = raw;               % 已是数值矩阵
end
points = double(points);
N = size(points, 1);

%% 参数（与 Python 一致）
M       = 10;     % 种群规模（保留前 M 个）
p_cross = 1.0;    % 交叉概率
p_perm  = 0.1;    % 变异概率
iters   = 10;     % 迭代次数

%% 初始种群：随机排列（MATLAB 使用 1..N 的索引）
population = cell(M*10, 1);
for k = 1:(M*10)
    population{k} = randperm(N);     % 一条个体 = 路径（长度 N 的排列）
end

% 选择前 M 个（按路径长度升序）
population = select_pop(population, M, points);

rec = zeros(iters, 1);

%% 主循环
for iter = 1:iters
    new_gen = population;  % 先把当前代直接复制过去

    % 交叉：对所有有序对 (p1,p2) 以概率 p_cross 交配
    for a = 1:numel(population)
        for b = 1:numel(population)
            if rand < p_cross
                [n1, n2] = cross_op(population{a}, population{b});
                new_gen{end+1} = n1; %#ok<*AGROW>
                new_gen{end+1} = n2;
            end
        end
    end

    % 变异：以概率 p_perm 做区间反转（保持首城市不动，等价 Python 的切片范围 1..N-1）
    for k = 1:numel(new_gen)
        if rand < p_perm
            new_gen{k} = perm_mut(new_gen{k});
        end
    end

    % 选择：保留前 M 个最优个体
    population = select_pop(new_gen, M, points);

    % 记录并打印
    best_len = calc(population{1}, points);
    fprintf('iter %d: cur_l = %.6f\n', iter-1, best_len);  % Python 从 0 计
    rec(iter) = best_len;
end

ans_route = population{1};
fprintf('最优路径长度：%.6f\n', calc(ans_route, points));
disp('最优路径（1-based 索引）:');
disp(ans_route);

% 画最优路径
figure;
plot_ans(ans_route, points);
title('GA 最优路径');

% 画收敛曲线
figure;
plot(rec, 'LineWidth', 1.5);
grid on; xlabel('iteration'); ylabel('best tour length');
title('GA 收敛曲线');

%% ==================== 局部函数 ====================

function selected = select_pop(population, M, points)
    % 对每个个体计算路径长度，升序排序，取前 M 个
    L = numel(population);
    vals = zeros(L,1);
    for i = 1:L
        vals(i) = calc(population{i}, points);
    end
    [~, idx] = sort(vals, 'ascend');
    idx = idx(1:min(M,L));
    selected = population(idx);
end

function out = perm_mut(route)
    % 区间反转变异：随机选 i,j in [2..N]（保持首城市不动，贴近原 Python）
    N = numel(route);
    if N <= 2
        out = route; return;
    end
    i = randi([2, N]);
    j = randi([2, N]);
    if i > j
        t = i; i = j; j = t;
    end
    out = route;
    out(i:j) = route(j:-1:i);
end

function [child1, child2] = cross_op(r1, r2)
    % 交叉算子：与 Python 逻辑一致
    % 1) 随机选 [i..j] (2..N)，从 r1 中取出 takeout = r1(i:j)
    % 2) r1_tmp = r1 去掉该段；r2 中按次序扫描：在 takeout 中的元素收集为 takein，其余留在 r2_tmp
    % 3) child1 = r1_tmp + takein, child2 = r2_tmp + takeout
    N = numel(r1);
    if N ~= numel(r2)
        error('父代长度不一致');
    end
    if N <= 2
        child1 = r1; child2 = r2; return;
    end

    i = randi([2, N]);
    j = randi([2, N]);
    if i > j
        t = i; i = j; j = t;
    end

    takeout = r1(i:j);
    r1_tmp  = [r1(1:i-1), r1(j+1:end)];
    % 从 r2 中剥离：在 takeout 中的 -> takein；否则 -> r2_tmp
    takein = [];
    r2_tmp = [];
    mask = false(1, N);  % 快速查找是否在 takeout
    mask(takeout) = true;
    for k = 1:N
        v = r2(k);
        if mask(v)
            takein(end+1) = v; %#ok<AGROW>
        else
            r2_tmp(end+1) = v; %#ok<AGROW>
        end
    end
    child1 = [r1_tmp, takein];
    child2 = [r2_tmp, takeout];
end
