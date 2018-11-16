import numpy as np
import scipy as sp
import pandas as pd
import matplotlib.pyplot as plt

test=DataAPI.IdxCloseWeightGet(secID=u"000016.ZICN",ticker=u"",beginDate=u"20180901",endDate=u"",field=['secShortName','consShortName','consTickerSymbol','weight'],pandas="1")

s=DataAPI.SecIDGet(partyID=u"",ticker=u"000016",cnSpell=u"",assetClass=u"",field=u"",pandas="1")

#print(test.sort(columns=['weight'],ascending=False))
tmp=test.sort(columns=['weight'],ascending=False)

show1=DataAPI.MktEqudGet(secID=u"601318.XSHG",ticker=u"",tradeDate=u"",beginDate=u"20160103",endDate=u"",isOpen="",\
                         field=['closePrice'],pandas="1")

show2=DataAPI.MktEqudGet(secID=u"600519.XSHG",ticker=u"",tradeDate=u"",beginDate=u"20160103",endDate=u"",isOpen="",\
                         field=['closePrice'],pandas="1")
 


weight=tmp['weight']
ww=weight.reset_index(drop=True)


labels=tmp['consTickerSymbol']
ll=labels.reset_index(drop=True)
'''
ll[0]='ZGPA'
ll[1]='GZMT'
ll[2]='ZSYH'
ll[3]='XYYH'
ll[4]='MSYH'
ll[5]='JTYH'
ll[6]='YLGF'
#plt.pie(ww,labels=ll)
#plt.show()
''' 
newWeight=[]
newLL=['ZGPA','GZMT','ZSYH','XYYH','MSYH','JTYH','YLGF']

ww=ww[0:7]
 

for i in range(7):
    newWeight.append(ww[i]/sum(ww))
#plt.pie(newWeight,labels=newLL)
#plt.show()

currentshares=[0]*7
for i in range(7):
    tmp=DataAPI.EquGet(secID=u"",ticker=ll[i],equTypeCD=u"A",listStatusCD=u"",field=['nonrestfloatA'],pandas="1")
    currentshares[i]=tmp['nonrestfloatA']


 
 
   
closeprice=[0]*7

for i in range(7):
    tmp=DataAPI.MktEqudGet(secID=u"",ticker=ll[i],tradeDate=u"20181029",beginDate=u"",endDate=u"",isOpen="",field=['closePrice'],pandas="1")
    closeprice[i]=tmp['closePrice']
     
 
 
closeprice=np.array(closeprice)
currentshares=np.array(currentshares)
toshow=currentshares*closeprice
priceWeight=[]
for i in range(7):
    priceWeight.append(toshow[i]/sum(toshow))

plt.pie(priceWeight,labels=newLL)
plt.show()

