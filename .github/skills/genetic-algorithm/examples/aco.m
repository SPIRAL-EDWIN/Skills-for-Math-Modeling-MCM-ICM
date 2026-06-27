clc; clear; close all;

%% 读取点集
raw = jsondecode(fileread('points.json'));
if iscell(raw)
    points = vertcat(raw{:});   % 若解析成元胞，拼成 N×2
else
    points = raw;               % 已是数值矩阵
end
points = double(points);
N = size(points, 1);

%% 参数
alpha = 1;          % 启发式信息因子
beta  = 1;          % 信息素因子
ants  = 10;         % 蚂蚁数量
evap  = 0.4;        % 信息素挥发系数
D     = 10;         % 信息素释放强度
iters = 10;         % 迭代次数（与 Python 中 for iter in range(10) 一致）

%% 启发式信息 eta(i,j) = 1 / dist(i,j)，对角为 0
eta   = zeros(N, N);
for i = 1:N
    for j = i+1:N
        d = hypot(points(i,1)-points(j,1), points(i,2)-points(j,2));
        if d <= 0, d = eps; end
        eta(i,j) = 1/d;
        eta(j,i) = 1/d;
    end
end

%% 初始信息素 gamma，全部 0.2（对角为 0）
gamma = 0.2 * ones(N, N);
gamma(1:N+1:end) = 0;  % 置对角为 0（可选）

%% 主循环
best_dist = inf;
best_route = [];
rec = zeros(iters, 1);

for iter = 1:iters
    delta_gamma = zeros(N, N);

    for ant = 1:ants
        % Python: choose_path(ant, ...) —— 用 ant 作为起点（0-based）
        % MATLAB：用 1-based，且为了避免 ants>N 的越界，按环绕方式取起点
        start_idx = mod(ant-1, N) + 1;

        p = choose_path(start_idx, eta, gamma, alpha, beta, points); % 访问顺序（长度 N，不含回到起点）

        cur_dist = calc(p, points);   % 回路长度（calc 内部包含首尾闭合边）

        if cur_dist < best_dist
            best_dist  = cur_dist;
            best_route = p;
        end

        % 累积信息素增量：每条边加 D / distance，与 Python 逻辑一致
        for k = 1:N-1
            d = hypot(points(p(k),1)-points(p(k+1),1), points(p(k),2)-points(p(k+1),2));
            if d <= 0, d = eps; end
            delta = D / d;
            delta_gamma(p(k),   p(k+1)) = delta_gamma(p(k),   p(k+1)) + delta;
            delta_gamma(p(k+1), p(k)  ) = delta_gamma(p(k+1), p(k)  ) + delta;
        end
        d = hypot(points(p(1),1)-points(p(end),1), points(p(1),2)-points(p(end),2));
        if d <= 0, d = eps; end
        delta = D / d;
        delta_gamma(p(1),  p(end)) = delta_gamma(p(1),  p(end)) + delta;
        delta_gamma(p(end), p(1) ) = delta_gamma(p(end), p(1) ) + delta;
    end

    % 信息素挥发 + 增强
    gamma = gamma * evap + delta_gamma;

    fprintf('iter %d: cur_l = %.6f\n', iter-1, best_dist);  % Python 从 0 计，展示对齐
    rec(iter) = best_dist;
end

%% 结果与作图
disp('最优路径（1-based 索引）:');
disp(best_route.');

figure; 
plot_ans(best_route, points);
title('ACO 最优路径');

figure;
plot(rec, 'LineWidth', 1.5);
grid on; xlabel('iteration'); ylabel('best tour length');
title('ACO 收敛曲线');

%% ==================== 局部函数 ====================

function route = choose_path(start_idx, eta, gamma, alpha, beta, points)
% 轮盘赌选择：按权重 w = (eta^alpha) * (gamma^beta) 在未访问集合中采样
    N = size(points, 1);
    visited = false(N, 1);
    route   = zeros(N, 1);
    route(1) = start_idx;
    visited(start_idx) = true;

    for t = 2:N
        cur = route(t-1);
        candidates = find(~visited).';
        % 计算每个候选的权重
        w = zeros(size(candidates));
        for idx = 1:numel(candidates)
            j = candidates(idx);
            w(idx) = (eta(cur,j)^alpha) * (gamma(cur,j)^beta);
        end
        % 若全为 0，退化为均匀随机
        if all(w <= 0)
            probs = ones(size(w)) / numel(w);
        else
            s = sum(w);
            probs = w / s;
        end
        % 轮盘赌
        r = rand;
        cs = cumsum(probs);
        pick = candidates(find(r <= cs, 1, 'first'));
        if isempty(pick)
            pick = candidates(end);
        end
        route(t) = pick;
        visited(pick) = true;
    end
end
