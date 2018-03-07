import numpy as np
import matplotlib.pyplot as plt
S0=5
M=16  #time step
K=10   #strike price


TT=np.linspace(0,1,16)   #time to maturity

T=1
dt=TT/M


r=0.06  #risk free rate
sigma=0.3  #volatility ,SD
A=0.5*(np.exp(-r*dt)+np.exp((r+sigma**2)*dt))
a=A+np.sqrt(A**2-1) #u
b=A-np.sqrt(A**2-1) #d
p=(np.exp(r*dt)-b)/(a-b)

SM=np.zeros((M+1,1))  ##M+1行 1列，用来存放到期价格

for i in range (M+1):
    SM[i][0]=b**(M-i)*a**(i)*S0
VM=np.zeros((M+1,1))
for i in range (M+1):
  VM[i][0]=max(K-SM[i][0],0)



V2=VM

for k in range (M,0,-1):
    V1=np.zeros((k,1))
    for m in range(k):
        V1[m][0]=np.exp(-r*dt)*(p*V2[m+1][0]+(1-p)*V2[m][0])

    V2=V1

price=V1
print (price)

'''
T=0
price=np.zeros((M,1))
for i in range(M):

    T=T+TT[i]
    dt=T/M
    r = 0.06  # risk free rate
    sigma = 0.3  # volatility ,SD
    A = 0.5 * (np.exp(-r * dt) + np.exp((r + sigma ** 2) * dt))
    a = A + np.sqrt(A ** 2 - 1)  # u
    b = A - np.sqrt(A ** 2 - 1)  # d
    p = (np.exp(r * dt) - b) / (a - b)

    SM = np.zeros((M + 1, 1))  ##M+1行 1列，用来存放到期价格

    for i in range(M + 1):
        SM[i][0] = b ** (M - i) * a ** (i) * S0
    VM = np.zeros((M + 1, 1))
    for i in range(M + 1):
        VM[i][0] = max(K - SM[i][0], 0)

    V2 = VM

    for k in range(M, 0, -1):
        V1 = np.zeros((k, 1))
        for m in range(k):
            V1[m][0] = np.exp(-r * dt) * (p * V2[m + 1][0] + (1 - p) * V2[m][0])

        V2 = V1

    price[i]=V1
    
'''


