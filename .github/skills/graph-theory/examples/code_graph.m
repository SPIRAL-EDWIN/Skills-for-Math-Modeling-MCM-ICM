%% Matlab作无向图
% （1）无权重（每条边的权重默认为1）
% 函数graph(s,t)：可在 s 和 t 中的对应节点之间创建边，并生成一个图
% s 和 t 都必须具有相同的元素数；这些节点必须都是从1开始的正整数，或都是字符串元胞数组。
% 注意哦，编号最好是从1开始连续编号，不要自己随便定义编号
s1 = [1,2,3,4];
t1 = [2,3,1,1];
G1 = graph(s1, t1);
plot(G1)
% 下面的命令是在画图后不显示坐标
set( gca, 'XTick', [], 'YTick', [] );  


% 注意字符串元胞数组是用大括号包起来的哦
s2 = {'学校','电影院','网吧','酒店'};
t2 = {'电影院','酒店','酒店','KTV'};
G2 = graph(s2, t2);
plot(G2, 'linewidth', 2)  % 设置线的宽度
% 下面的命令是在画图后不显示坐标
set( gca, 'XTick', [], 'YTick', [] );  

% （2）有权重
% 函数graph(s,t,w)：可在 s 和 t 中的对应节点之间以w的权重创建边，并生成一个图
s = [1,2,3,4];
t = [2,3,1,1];
w = [3,8,9,2];
G = graph(s, t, w);
% G.Edges.Weight 表示图形对象 G 中所有边的权重值，'EdgeLabel' 表示在图形上显示这些权重值
plot(G, 'EdgeLabel', G.Edges.Weight, 'linewidth', 2) 
set( gca, 'XTick', [], 'YTick', [] );  

% 函数graph(a)：a为邻接矩阵，0表示没有边
a=[0 3 9 2;
   3 0 8 0;
   9 8 0 0;
   2 0 0 0];
G = graph(a);
% a=[0 3 9 2;
%    0 0 8 0;
%    0 0 0 0;
%    0 0 0 0];
% G = graph(a,'upper'); %'upper'仅使用上三角矩阵来构造图
% G.Edges.Weight 表示图形对象 G 中所有边的权重值，'EdgeLabel' 表示在图形上显示这些权重值
plot(G, 'EdgeLabel', G.Edges.Weight, 'linewidth', 2) 
set( gca, 'XTick', [], 'YTick', [] );  
%% Matlab作有向图
% 无权图 digraph(s,t)
s = [1,2,3,4,1];
t = [2,3,1,1,4];
G = digraph(s, t);
plot(G)
set( gca, 'XTick', [], 'YTick', [] );  

% 有权图 digraph(s,t,w)
s = [1,2,3,4];
t = [2,3,1,1];
w = [3,8,9,2];
G = digraph(s, t, w);
plot(G, 'EdgeLabel', G.Edges.Weight, 'linewidth', 2) 
set( gca, 'XTick', [], 'YTick', [] );  
%digraph(a) a为邻接矩阵
a=[0 3 0 0;
   0 0 8 0;
   9 0 0 0;
   2 0 0 0];
G = digraph(a);
% s=cellstr(strcat('顶点',int2str([1:4]')));
% % 给每个顶点标注名称，int2str([1:4]')将整数1到4六个数转化为字符
% % strcat把字符串水平串联起来
% % strcat('顶点',int2str([1:4]'))把顶点和字符1到4拼起来
% G = digraph(a,s);
plot(G, 'EdgeLabel', G.Edges.Weight, 'linewidth', 2) 
set( gca, 'XTick', [], 'YTick', [] );  


