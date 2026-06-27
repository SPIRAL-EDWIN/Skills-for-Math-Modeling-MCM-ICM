%% 非线性规划的函数
% [x,fval] = fmincon(fun,x0,A,b,Aeq,beq,lb,ub,nonlfun,option)
% x0表示给定的初始值（用行向量或者列向量表示），必须得写
% A b表示线性不等式约束
% Aeq beq 表示线性等式约束
% lb ub 表示上下界约束
% fun表示目标函数
% nonlfun表示非线性约束的函数
% option 表示求解非线性规划使用的方法
clear;clc
format long g   %可以将Matlab的计算结果显示为一般的长数字格式（默认会保留四位小数，或使用科学计数法）

%% 例题1的求解
% max f(x) = x1^2 +x2^2 -x1*x2 -2x1 -5x2
% s.t. -(x1-1)^2 +x2 >= 0 ;  2x1-3x2+6 >= 0
x0 = [0 0];  %任意给定一个初始值 
A = [-2 3]; b = 6;
[x,fval] = fmincon(@fun1,x0,A,b,[],[],[],[],@nonlfun1)  % 注意 fun1.m文件和nonlfun1.m文件都必须在当前文件夹目录下
fval = -fval

%% 使用其他算法对例题1求解
% Matlab默认使用的算法是'interior-point' 内点法
% 使用interior point算法 （内点法）
option = optimoptions('fmincon','Algorithm','interior-point')
[x,fval] = fmincon(@fun1,x0,A,b,[],[],[],[],@nonlfun1,option)  
fval = -fval
% 使用SQP算法 （序列二次规划法）
option = optimoptions('fmincon','Algorithm','sqp')
[x,fval] = fmincon(@fun1,x0,A,b,[],[],[],[],@nonlfun1,option)  
fval = -fval   %得到-4.358，远远大于内点法得到的-1,猜想是初始值的影响
% 改变初始值试试
x0 = [1 1];  %任意给定一个初始值 
[x,fval] = fmincon(@fun1,x0,A,b,[],[],[],[],@nonlfun1,option)  % 最小值为-1，和内点法相同（这说明内点法的适应性要好）
fval = -fval  

%% 使用蒙特卡罗的方法来找初始值(推荐）
clc,clear;
n=10000000; %生成的随机数组数
x1=unifrnd(-100,100,n,1);  % 生成在[-100,100]之间均匀分布的随机数组成的n行1列的向量构成x1
x2=unifrnd(-100,100,n,1);  % 生成在[-100,100]之间均匀分布的随机数组成的n行1列的向量构成x2
fmin=+inf; % 初始化函数f的最小值为正无穷（后续只要找到一个比它小的我们就对其更新）
for i=1:n
    x = [x1(i), x2(i)];  %构造x向量, 这里千万别写成了：x =[x1, x2]
    if ((x(1)-1)^2-x(2)<=0)  & (-2*x1(i)+3*x2(i)-6 <= 0)     % 判断是否满足条件
        result = -x(1)^2-x(2)^2 +x(1)*x(2)+2*x(1)+5*x(2) ;  % 如果满足条件就计算函数值
        if  result  < fmin  % 如果这个函数值小于我们之前计算出来的最小值
            fmin = result;  % 那么就更新这个函数值为新的最小值
            x0 = x;  % 并且将此时的x1 x2更新为初始值
        end
    end
end
disp('蒙特卡罗选取的初始值为：'); disp(x0)
A = [-2 3]; b = 6;
[x,fval] = fmincon(@fun1,x0,A,b,[],[],[],[],@nonlfun1)
fval = -fval  
