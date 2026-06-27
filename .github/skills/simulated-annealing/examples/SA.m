clc; clear; close all;

%% 读取点集（points.json: [[x1,y1],[x2,y2],...])
raw = jsondecode(fileread('points.json'));
if iscell(raw)
    % JSON 若解为 1xN 元胞，每格 1x2 数值，拼接成 N×2
    points = vertcat(raw{:});
else
    points = raw;    % 已是数值矩阵
end

% 基本参数
N = size(points, 1);

% 最近邻初解（Python 里是 greedy(0,...)；MATLAB 索引从 1 开始）
last = greedy(1, points);   % 长度 N 的访问顺序（不含回到起点）
best = last;

% 记录收敛曲线
rec = zeros(10000, 1);

% 模拟退火参数
T = 20;
alpha = 0.999;

% 当前路径长度
cur_l = calc(last, points);

%% 主循环（10000 次）
for iter = 1:10000
    % 2-opt 风格的区间反转扰动（固定首点：下标从 2..N）
    tmp = perm_rev(last);

    % 新路径长度
    new_l = calc(tmp, points);

    % 接受判据
    if new_l < cur_l
        last  = tmp;
        cur_l = new_l;
        best  = tmp;
    else
        if rand < exp( -(new_l - cur_l) / T )
            last  = tmp;
            cur_l = new_l;
        end
    end

    % 温度衰减 & 记录
    T = T * alpha;
    rec(iter) = cur_l;

    if mod(iter, 1000) == 0
        fprintf('iter %d: cur_l = %.6f\n', iter, cur_l);
    end
end

ans_route = best;
disp('最优访问顺序（1-based 索引）:');
disp(ans_route.');

%% 画最优路径
figure;
plot_ans(ans_route, points);
title('最优路径');

%% 画收敛曲线
figure;
plot(rec, 'LineWidth', 1.5);
grid on;
xlabel('iteration');
ylabel('tour length');
title('SA 收敛曲线');

%% —— 局部函数：区间反转扰动（固定首点不动，对应 Python 的 perm）——
function out = perm_rev(route)
    N = numel(route);
    % Python 中随机区间在 1..N-1（0-based，固定起点）；MATLAB 取 2..N
    i = randi([2, N]);
    j = randi([2, N]);
    if i > j
        t = i; i = j; j = t;
    end
    out = route;
    out(i:j) = route(j:-1:i);
end
