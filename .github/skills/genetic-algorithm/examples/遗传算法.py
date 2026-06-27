import random
from util import *
import matplotlib.pyplot as plt

with open("points.json","r") as f:
    txt=f.readline()
points=json.loads(txt)

N=len(points)
M=10
p_cross=1
p_perm=0.1

def select(population,M,points):
    ranking = []
    for p in population:
        ranking.append((calc(p, points), p))
    ranking.sort()
    ans = [t[1] for t in ranking[:M]]
    return ans
def perm(route):
    i=random.randint(1,N-1)
    j=random.randint(1,N-1)
    if i>j:
        i,j=j,i
    route=route[:i]+route[j:i-1:-1]+route[j+1:]
    return route

def cross(r1,r2):
    i = random.randint(1, N - 1)
    j = random.randint(1, N - 1)
    if i > j:
        i, j = j, i
    takeout=r1[i:j+1]
    takein=[]
    r1_tmp=r1[:i]+r1[j+1:]
    r2_tmp=[]
    for i in r2:
        if i in takeout:
            takein.append(i)
        else:
            r2_tmp.append(i)
    r1_tmp=r1_tmp+takein
    r2_tmp=r2_tmp+takeout
    return r1_tmp,r2_tmp

population=[]
for _ in range(M*10):
    ls=list(range(N))
    random.shuffle(ls)
    population.append(ls)
population=select(population,M,points)

rec=[]
for iter in range(10):
    new_gen = []
    for p in population:
        new_gen.append(p)
    #交配
    for p1 in population:
        for p2 in population:
            if random.random()<p_cross:
                n1,n2=cross(p1, p2)
                new_gen.append(n1)
                new_gen.append(n2)
    #变异
    for p in new_gen:
        if random.random()<p_perm:
            p=perm(p)
    #选择
    population=select(new_gen,M,points)
    best=calc(population[0],points)
    print("iter {}: cur_l={}".format(iter,best))
    rec.append(best)

ans=population[0]
plot_ans(ans,points)
plt.plot(rec)
plt.show()
