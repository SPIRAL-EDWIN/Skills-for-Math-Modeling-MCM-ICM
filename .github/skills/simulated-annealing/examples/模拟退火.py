import random
from util import *
import matplotlib.pyplot as plt

with open("points.json","r") as f:
    txt=f.readline()
points=json.loads(txt)

N=len(points)

last = greedy(0,points)

def perm(ans):
    i=random.randint(1,N-1)
    j=random.randint(1,N-1)
    if i>j:
        i,j=j,i
    ans=ans[:i]+ans[j:i-1:-1]+ans[j+1:]
    return ans

rec=[]

T=20
alpha=0.999
cur_l=calc(last,points)
best=last

for iter in range(10000):
    tmp=perm(last)
    new_l=calc(tmp,points)
    if new_l<cur_l:
        last=tmp
        best=tmp
        cur_l = new_l
    else:
        rand=random.random()
        if rand<math.exp(-(new_l-cur_l)/T):
            last=tmp
            cur_l = new_l
    T *= alpha
    rec.append(cur_l)
    if iter%1000==0:
        print("iter {}: cur_l={}".format(iter,cur_l))

ans=best
print(ans)

plot_ans(ans,points)
plt.plot(rec)
plt.show()