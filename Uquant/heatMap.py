import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
dfcf=DataAPI.MktEqudGet(secID=u"300059.XSHE",ticker=u"",tradeDate=u"",beginDate=u"20160630",endDate=u"20180730",isOpen="",field=['closePrice','turnoverVol'],pandas="1")
Vol=dfcf['turnoverVol']
close=dfcf['closePrice'] #509
def ema(array,days):
    tmp=[0]*(len(array)-days)
    tmp[0]=array[0]
    for i in range(len(array)-days-1):
        tmp[i+1]=((2.0/(days+1))*array[i+1]+((days-1)*1.0/(days+1))*tmp[i])
    return (tmp )
     
close=np.array(close)
profit=(close[1:]-close[0:-1])/close[0:-1] 
 
#print(len(profit ))#508
fastMA=ema(close,10)#499
slowMA=ema(close,20)#489

fastMA=np.array(fastMA[10:])
slowMA=np.array(slowMA)

difference=fastMA-slowMA #快线减慢线，macd
profit=profit[19:] #489
Vol=Vol[20:]#489
find_profit=np.where(profit>0)#所有上涨天数的索引

find_diff=np.where(difference>0)
#print( (find_diff[0]))#184
#print(  (find_profit[0]) )#225

setFP=set( (find_profit[0] ))
setFD=set( (find_diff[0]))

out=setFD&setFP
#print((out))#75
outcome =list(out)
outcome=sorted(outcome)
 

#print(outcome ) #macd金叉且当天是上涨的交集的索引
#print (profit)

tmp=[]
for i in range(len(outcome)):
    tmp.append(profit[outcome[i]])
tmpVol=[]
for i in range(len(outcome)):
    tmpVol.append(Vol[outcome[i]])
#print(np.array(tmp))
#通过outcome这个索引把macd金叉也拿出来做分段
macd=[]

for i in range(len(outcome)):
    macd.append(difference[outcome[i]])


#macd.sort()
#print(np.asarray((macd))) 
#print(outcome)
 

dic = dict(map(lambda x,y:[x,y],tmp,macd)) #搞个字典类，把盈利和macd大于0且收盘涨的记录下来
dic=sorted(dic.items(),key=lambda a: a[1],reverse=False) #根据macd值从小到大排序
#print(dic)

indices=[(0,15),(16,33),(34,61),(62,len(dic))] #分段依据是自己找的
split=[]
for i in range(4):
    split=([dic[s:e+1] for s,e in indices])
#print(split) #根据macd值分段
plt.scatter(macd,tmp)
plt.xlabel('macd')
plt.ylabel('return')
plt.legend()
plt.show()
 
df=pd.DataFrame({'MACD':macd,'Return':tmp,'vol':tmpVol})
df.head()
pt=df.pivot_table(index='MACD',columns='Return',values='vol',fill_value=0)
#pt.head()
plt.figure(figsize=((15,15)))
sns.heatmap(pt)
