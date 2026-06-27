% 定义图的边和权重
s = [9 9 1 1 3 3 3 2 2 5 5 7 7 8]; % 起始节点编号
t = [1 2 2 3 4 6 7 4 5 4 7 6 8 6]; % 终止节点编号
w = [4 8 3 8 2 7 4 1 6 6 2 14 10 9]; % 边的权重

% 创建一个图形对象 G
G = graph(s,t,w);

% 绘制图形 G，并将边的权重添加到图形上
% G.Edges.Weight 表示图形对象 G 中所有边的权重值，'EdgeLabel' 表示在图形上显示这些权重值
plot(G, 'EdgeLabel', G.Edges.Weight, 'linewidth', 2)
% 隐藏图形的坐标轴
set( gca, 'XTick', [], 'YTick', [] );

% shortestpath 函数计算从节点 9 到节点 8 的最短路径和路径长度，并将路径和路径长度分别存储在 P 和 d 中
[P,d] = shortestpath(G, 9, 8)
% 在图形 G 中高亮显示最短路径
% highlight 函数高亮图形对象 myplot 中的路径 P，'EdgeColor', 'r' 表示将路径颜色设置为红色。
myplot = plot(G, 'EdgeLabel', G.Edges.Weight, 'linewidth', 2);
highlight(myplot, P, 'EdgeColor', 'r')


% 计算图形 G 中任意两点之间的最短路径矩阵
D = distances(G)
% 输出 1 到 2 的最短路径
D(1,2)
% 输出 9 到 4 的最短路径
D(9,4)
% 找出图形 G 中距离节点 2 不超过 10 的所有节点
[nodeIDs,dist] = nearest(G, 2, 10)