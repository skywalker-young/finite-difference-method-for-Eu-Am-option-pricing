import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
def getInputData(startTime,endTime,indexID):
    data=DataAPI.MktIdxdGet(indexID=indexID,ticker=u"",tradeDate=u"",\
                        beginDate=startTime,endDate=endTime,exchangeCD=u"XSHE,XSHG",field=['tradeDate','closeIndex','turnoverVol','CHGPct'],pandas="1")
    return data

def constructTable(data,days):
    close=data['closeIndex']
    length=len(close)
    Table={'Change':[],'Flag':[]}
    for i in range(length-days):
        tmp=(close[days+i]-close[i])/close[i]
        Table.get('Change').append(tmp)
        if tmp>=0.05:
            Table.get('Flag').append(1)
        elif -0.05<tmp<0.05:
            Table.get('Flag').append(0)
        elif tmp<=-0.05:
            Table.get('Flag').append(-1)
    return pd.DataFrame(Table)

def handleVol(data,N):
    vol=data['turnoverVol']
    length=len(vol)
    tmp=[0]*N
    rank=[]
    for i in range(length-N):
        tmp=[np.log(j)for j in vol[i:i+N]]
    
        tmp=[round(i,4) for i in tmp]
    
        v=tmp[N-1]
        tmp.sort()
        tmp=list(tmp)
        n=tmp.index(v)
        rank.append((n-0)*1.0/N) 
    return rank
 

def joint(rank,Table,N):
    Table=Table[N-10:]
    Table=Table.reset_index(drop=True)
    rank=pd.DataFrame(rank)
    Table['Rank']=rank
    return Table

data=getInputData("20140630","20190212","000300.ZICN")
#000016.ZICN  2004-01-02           上证50
#000010.ZICN  2002-07-01          上证180
#000002.ZICN  1992-02-21           上证A股
#000300.ZICN  2005-04-08           沪深300 
Table=constructTable(data,10)#10days区分行情
N=20#20,30,40,光大报告取30
rank=handleVol(data,N)
newTable=joint(rank,Table,N)
#newTable.to_csv('volOrderedByTime.csv')
in1 = newTable[(newTable.Flag==1) & (newTable.Rank>=0.6) ].index.tolist() 
out2=newTable[(newTable.Flag==-1) & (newTable.Rank>=0.6)].index.tolist()
in3=newTable[(newTable.Flag==0) & (newTable.Rank>=0.9)].index.tolist()
#in1.extend(in2)
in1.extend(in3)
print(len(in1))

close=data['closeIndex']
dotIn=[]
dotOut=[]
for i in in1:
    dotIn.append(close[i])
for i in out2:
    dotOut.append(close[i])
plt.figure(figsize=(20,20))
plt.plot(close)
plt.plot(in1,dotIn,'ro',out2,dotOut,'g^')
plt.show()
