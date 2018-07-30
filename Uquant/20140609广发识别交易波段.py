import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

test=DataAPI.MktIdxdGet(indexID=u"000001.ZICN",ticker=u"",exchangeCD=u"XSHG",beginDate=u"20160608",endDate=u"20180401",field=['openIndex','closeIndex','highestIndex','lowestIndex'],pandas="1")

Aopen=list(test.openIndex)
Bclose=list(test.closeIndex)
#print(len(Bclose) )#440组数据/20=22，布林通道中间数为20日均线
pMean=[0]*420
pHigh=[0]*420
pLow=[0]*420
for i in range(420):
    tmp=Bclose[i:i+20]
    pMean[i]=(np.mean(tmp))
    pHigh[i]=pMean[i]+2*np.std(tmp)
    pLow[i]=pMean[i]-2*np.std(tmp)

    
pMean=np.array(pMean)
pHigh=np.array(pHigh)
pLow=np.array(pLow)
close=np.array(Bclose[20:440])
percentB=(close-pLow)/(pHigh-pLow) #array类型
#只有list类型才能调用.index记录索引

  
recordValue=[0]*411#440-20(日布林通道)-10（日一区间计算）+1
 
 
for i in range(411):
    tmp=percentB[i:i+10]
    recordValue[i]=max(tmp)
    

s=pd.Series(percentB)
recordIndex=[s[i:i+10].idxmax() for i in range(len(s)-9)]
#print(len(recordIndex)) #411
#print(np.array(recordValue)[0:100])
Std=np.std(percentB) 

record=[]

#print(np.array(percentB)[0:100])
for i in range(419):
    #count=0
    if (percentB[i+1]>=percentB[i]):
        record.append(i+1)
    elif(percentB[i+1]<percentB[i]):
        if(abs(percentB[i]-percentB[i+1])<Std):#+count
            continue #count=count+1
        else:
            record.append(1+i)#+count

#print(np.array(record) )记录下来的是要连线的percentB的索引

dot=[]
for i in range(len(record)):
    dot.append(percentB[record[i]])

#dot记录的是percentB里分割过的值


#研报之前说是分割，这里是裁剪，实际上换汤不换药    
 
Std2=1.01*Std
ct=0
dot2=list(dot)           #dot2是基于dot再次裁剪
record2=list(record)
#print(len(record )) 
for i in range(len(record)-3):
    
    t1=dot2[i -ct]
    t2=dot2[i+1-ct ]
    t3=dot2[i+2 -ct]
    if(t3>t1):
        if(abs(t2-t3)<Std2):
            record2.pop(i+1-ct)
            dot2.pop(i+1 -ct)
            ct=ct+1
    elif(t3<t1):
        if(abs(t1-t2)<Std2):
            record2.pop(i+1-ct)       #记录dot2对应的索引，用来返回到最初的价格
            dot2.pop(i+1-ct )
            ct=ct+1
            
  

newValue=[0]*len(record2)
for i in range(len(record2)):
    newValue[i]=Bclose[record2[i]]   #根据索引得到的修剪过的percentB对应的收盘价

#print(len(newValue))#41
newValue2=newValue[1:] #40个数据，方便8个一组做5组

tmpSum=[]
for i in range(len(newValue2)-8-1):
    add=0 
    tmp2=newValue2[i :i+9]
    for j in range(8-2):
        add=add+abs(abs(tmp2[j+1])-abs(tmp2[j])-abs(abs(tmp2[j+2])-abs(tmp2[j+1])))  
    tmpSum.append(add/7)
#print(len(tmpSum))

#print(np.array(   (newValue2[9:])) )


buy1=[]
buy2=[]
sell=[]
for i in range(len(tmpSum)):
    if(tmpSum[i]<=40):
        buy1.append(i)
    elif(tmpSum[i]>=60):
        buy2.append(i)
    elif(40<tmpSum[i]<60):
        sell.append(i)
index3=[]
paint3=[]
paint1=[]
paint2=[]
index1=[]
index2=[]
for i in range(len(buy1)):
    paint1.append(record2[buy1[i]])
    index1.append(newValue2[buy1[i]-1])
for i in range(len(buy2)):
    paint2.append(record2[buy2[i]])
    index2.append(newValue2[buy2[i]-1])
for i in range(len(sell)):
    paint3.append(record2[sell[i]])
    index3.append(newValue2[sell[i]-1])
    
xxlabel=np.arange(20,440,420/207)
 

xlabel=np.arange(20,440,1)
fig=plt.figure(figsize=(15,15))

plt.subplot(4,1,1)           
plt.plot(Bclose,label='ClosePrice')

plt.legend()
plt.subplot(4,1,2)
plt.plot( xlabel, percentB,'r',label='%B')
plt.legend()
plt.subplot(4,1,3) 
record=np.array(record)
plt.plot( record+20, dot,'b',label='1st modify')
 
plt.legend()
plt.subplot(4,1,4)
record2=np.array(record2)
plt.plot(record2+20 ,newValue)
plt.plot(np.array(paint1)+20,index1,'ro',label='bottom fishing')
plt.plot(np.array(paint2)+20,index2,'ro' )
paint3=paint3[1:]+[418]
index3=index3[1:]+[3292]
plt.plot(np.array(paint3)+20,index3,'bo' )
plt.legend()
#plt.subplot(4,1,4) 
#record2=np.array(record2)
#plt.plot(20+record2,dot2)
 

plt.show()
print('sell',sell)
print('index3',index3)
print('paint3',np.array(paint3))
print('record+20',record2+20)
print('newValue',np.array(newValue))
