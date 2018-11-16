import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

import datetime

def st_remove(source_universe, st_date=None):
 
    st_date = st_date if st_date is not None else datetime.datetime.now().strftime('%Y-%m-%d')
    df_ST = DataAPI.SecSTGet(secID=source_universe, beginDate=st_date, endDate=st_date, field=['secID'])
    return [s for s in source_universe if s not in list(df_ST['secID'])]


universe=set_universe('A')
#print(len(universe))#3558
universe=st_remove(universe, '20170616') #去掉当天st的 还应该去掉未上市的,停牌的
#print(np.asarray(universe[0:900]))
#print(len(universe))#3485
universe=universe[0:3400]# 测试
out={'secID':[],'LFLO':[],'PE':[],'PB':[],'EPS':[]}#,'LFLO':[],'PE':[],'PB':[],'EPS':[]}
#print(universe[443])

 


for i in universe:
    tmp=DataAPI.MktStockFactorsDateRangeGet(secID=i,ticker=u"",beginDate=u"20170616",endDate=u"20170616",\
    field=['secID','LFLO','PE','PB','EPS'],pandas="1")#['secID','LFLO','PE','PB','EPS']
    if(len(tmp['secID'])):  
        out.get('secID').append(tmp['secID'][0])
        out.get('LFLO').append(tmp['LFLO'][0])
        out.get('PE').append(tmp['PE'][0])
        out.get('PB').append(tmp['PB'][0])
        out.get('EPS').append(tmp['EPS'][0])
    
    
show=pd.DataFrame(out)
#print(show)
    
LFLO=show.sort(columns='LFLO',ascending=False)    
LFLO=LFLO.reset_index(drop=True)
percent=int(round(len(LFLO)*0.8))
setfor1=LFLO['secID'][0:percent]
 
 
PE= show.sort(columns='PE',ascending=True) #最小的
PE=PE[PE.PE>0] #剔除0
percent=int(round(len(PE)*0.4))
PE=PE.reset_index(drop=True)
setfor2=PE['secID'][0:percent]

PB=show.sort(columns='PB',ascending=True)#最小的
PB=PB[PB.PB>0]
percent=int(round(len(PB)*0.4))
PB=PB.reset_index(drop=True)
setfor3=PB['secID'][0:percent]


EPS=show.sort(columns='EPS',ascending=True)#最小的
EPS=EPS[EPS.EPS<2.50]
setfor4=EPS['secID']

ToDo=set(setfor1) & set (setfor2) & set(setfor3) & set (setfor4)

GP={'GP_ratio':[],'secID':[]}
for i in ToDo:
    tmp=tmp=DataAPI.MktStockFactorsDateRangeGet(secID=i,ticker=u"",beginDate=u"20170616",endDate=u"20170616",\
    field=['ETOP','secID'],pandas="1")
    GP.get('GP_ratio').append(tmp['ETOP'][0])
    GP.get('secID').append(tmp['secID'][0])

showGP=pd.DataFrame(GP)

results=showGP.sort(columns='GP_ratio',ascending=False)
results=results.reset_index(drop=True)
results=results[0:20]
#results.to_csv('GP_ratio.csv')
print(results)
 
