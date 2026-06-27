import random
from util import *
import matplotlib.pyplot as plt

with open("points.json","r") as f:
    txt=f.readline()
points=json.loads(txt)

N=len(points)

eta=[[0 for _ in range(N)]for _ in range(N)]
gamma=[[0.2 for _ in range(N)]for _ in range(N)]
alpha=1
beta=1
ants=10
evap=0.4
D=10
for i in range(N):
    for j in range(i+1,N):
        dist=((points[i][0]-points[j][0])**2+(points[i][1]-points[j][1])**2)**0.5
        eta[i][j]=1/dist
        eta[j][i]=1/dist

def choose_path(start,eta,gamma,alpha,beta,points):
    N = len(points)
    visited = [False] * N
    visited[start] = True
    ans = [start]

    for _ in range(N - 1):
        cur=ans[-1]
        nxt = 0
        candidate=[x for x in range(N) if not visited[x]]
        min_len = 1e9
        weight=[]
        for x in candidate:
            weight.append(eta[cur][x]**alpha*gamma[cur][x]**beta)
        nxt=random.choices(candidate,weights=weight,k=1)[0]
        ans.append(nxt)
        visited[nxt] = True
    # ans.append(start)
    return ans

best_dist=1e10
best=[]
rec=[]

for iter in range(10):
    delta_gamma=[[0 for _ in range(N)]for _ in range(N)]
    for ant in range(ants):
        p=choose_path(ant,eta,gamma,alpha,beta,points)
        cur_dist=calc(p,points)
        if cur_dist<best_dist:
            best_dist=cur_dist
            best=p
        for i in range(N-1):
            delta=D/(((points[p[i]][0]-points[p[i+1]][0])**2+(points[p[i]][1]-points[p[i+1]][1])**2)**0.5)
            delta_gamma[p[i]][p[i+1]]+=delta
            delta_gamma[p[i+1]][p[i]] += delta
        delta = D / (((points[p[0]][0] - points[p[-1]][0]) ** 2 + (points[p[0]][1] - points[p[-1]][1]) ** 2) ** 0.5)
        delta_gamma[p[0]][p[-1]] += delta
        delta_gamma[p[-1]][p[0]] += delta
    for i in range(N):
        for j in range(N):
            gamma[i][j]=gamma[i][j]*evap+delta_gamma[i][j]

    print("iter {}: cur_l={}".format(iter, best_dist))
    rec.append(best_dist)

plot_ans(best,points)
plt.plot(rec)
plt.show()