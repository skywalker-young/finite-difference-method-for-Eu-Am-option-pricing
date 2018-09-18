import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

def dist(aa,bb):
    return abs(aa-bb)

def trans(a):
    l=[]
    for i in range(1,len(a)+1):
        l.append(a[-i])
    return l

def dtw(t,r):
    n=len(t)
    m=len(r)
    d=np.zeros((n,m))
    t=trans(t)
    r=trans(r)
    for i in range(n):
        for j in range(m):
            d[i][j]=dist(t[i],r[j])
    realmax=9999
    D=np.ones((n,m))*realmax
    D[0][0]=d[0][0]
    for i in range(1,n):
        for j in range(0,m):
            D1=D[i-1][j]
            if j>0:
                D2=D[i-1][j-1]
            else:
                D2=realmax
            if j>1:
                D3=D[i][j-1]
            else:
                D3=realmax
            D[i][j]=d[i][j]+min(D1,D2,D3)
    return D[n-1][m-1]

def DTW(a,b):
    m=len(a)
    n=len(b)
    dis=[]
    for i in range(1,m):
        dis.append(dtw(a[0:i],b))
    for j in range(1,n):
        dis.append(dtw(a,b[0:j]))
    return min(dis)

def normalized(a):
    m=np.mean(a)
    s=np.std(a)
    return (a-m)/s

'''
x=[1,1,6,5,2,2]
y=[2,2,5,1,1]

n=len(x)
m=len(y)
d=np.zeros((n,m))
t=trans(x)
r=trans(y)
for i in range(n):
    for j in range(m):
        d[i][j]=dist(t[i],r[j])
print(d)
print(DTW(x,y))
