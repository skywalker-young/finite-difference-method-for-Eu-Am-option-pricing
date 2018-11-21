import numpy as np
import pandas as pd
import datetime
import matplotlib.pyplot as plt
from sklearn.linear_model import LogisticRegression as LR

a=DataAPI.EquIndustryGet(secID=u"",ticker=u"",industryVersionCD=u"",
                         industry=u"申万行业",industryID=u"",industryID1=u"01030308",industryID2=u"",industryID3=u"",
                         intoDate=u"",field=u"",pandas="1") #电气设备

 
b=DataAPI.EquIndustryGet(secID=u"",ticker=u"",industryVersionCD=u"",
                         industry=u"申万行业",industryID=u"",industryID1=u"01030305",industryID2=u"",industryID3=u"",
                         intoDate=u"",field=u"",pandas="1") #有色金属

c=DataAPI.EquIndustryGet(secID=u"",ticker=u"",industryVersionCD=u"",
                         industry=u"申万行业",industryID=u"",industryID1=u"01030312",industryID2=u"",industryID3=u"",
                         intoDate=u"",field=u"",pandas="1") #电子板块

d=DataAPI.EquIndustryGet(secID=u"",ticker=u"",industryVersionCD=u"",
                         industry=u"申万行业",industryID=u"",industryID1=u"01030327",industryID2=u"",industryID3=u"",
                         intoDate=u"",field=u"",pandas="1") #通信

e=DataAPI.EquIndustryGet(secID=u"",ticker=u"",industryVersionCD=u"",
                         industry=u"申万行业",industryID=u"",industryID1=u"01030325",industryID2=u"",industryID3=u"",
                         intoDate=u"",field=u"",pandas="1") #计算机


f=DataAPI.EquIndustryGet(secID=u"",ticker=u"",industryVersionCD=u"",
                         industry=u"申万行业",industryID=u"",industryID1=u"01030323",industryID2=u"",industryID3=u"",
                         intoDate=u"",field=u"",pandas="1") #商业贸易

g=DataAPI.EquIndustryGet(secID=u"",ticker=u"",industryVersionCD=u"",
                         industry=u"申万行业",industryID=u"",industryID1=u"01030314",industryID2=u"",industryID3=u"",
                         intoDate=u"",field=u"",pandas="1") #食品饮料

h=DataAPI.EquIndustryGet(secID=u"",ticker=u"",industryVersionCD=u"",
                         industry=u"申万行业",industryID=u"",industryID1=u"01030301",industryID2=u"",industryID3=u"",
                         intoDate=u"",field=u"",pandas="1") #农林牧渔
i=DataAPI.EquIndustryGet(secID=u"",ticker=u"",industryVersionCD=u"",
                         industry=u"申万行业",industryID=u"",industryID1=u"01030333",industryID2=u"",industryID3=u"",
                         intoDate=u"",field=u"",pandas="1") #金融服务
j=DataAPI.EquIndustryGet(secID=u"",ticker=u"",industryVersionCD=u"",
                         industry=u"申万行业",industryID=u"",industryID1=u"01030317",industryID2=u"",industryID3=u"",
                         intoDate=u"",field=u"",pandas="1") #生物医药
k=DataAPI.EquIndustryGet(secID=u"",ticker=u"",industryVersionCD=u"",
                         industry=u"申万行业",industryID=u"",industryID1=u"01030318",industryID2=u"",industryID3=u"",
                         intoDate=u"",field=u"",pandas="1") #公用事业
l=DataAPI.EquIndustryGet(secID=u"",ticker=u"",industryVersionCD=u"",
                         industry=u"申万行业",industryID=u"",industryID1=u"01030334",industryID2=u"",industryID3=u"",
                         intoDate=u"",field=u"",pandas="1") #信息服务

m=DataAPI.EquIndustryGet(secID=u"",ticker=u"",industryVersionCD=u"",
                         industry=u"申万行业",industryID=u"",industryID1=u"01030303",industryID2=u"",industryID3=u"",
                         intoDate=u"",field=u"",pandas="1") #国防军工
a=set(a.secID)
b=set(b.secID)
c=set(c.secID)
d=set(d.secID)
e=set(e.secID)
f=set(f.secID)
g=set(g.secID)
h=set(h.secID)
i=set(i.secID)
j=set(j.secID)
k=set(k.secID)
l=set(l.secID)
m=set(m.secID)
universe=b|c|e|g|h|i|j|l|m

def strtodatetime(datestr):      
    format='%Y-%m-%d'
    return datetime.datetime.strptime(datestr,format)

def datediff(beginDate,endDate):  
       
    bd=strtodatetime(beginDate )  
    ed=strtodatetime(endDate )      
    oneday=datetime.timedelta(days=1)  
    count=0
    while bd!=ed:  
        ed=ed-oneday  
        count+=1
    return count
 
universefor2017=[]
#print(list(universe)[108])

for i in universe:
    tmp=DataAPI.EquGet(secID=i,ticker=u"",equTypeCD=u"A",listStatusCD=u"",\
                         field=['listDate'],pandas="1")
    tmp=tmp.fillna(datetime.datetime.today().strftime('%Y-%m-%d'))
    if len(tmp)!=0:
        a=strtodatetime((tmp['listDate'][0]))
        b=strtodatetime('2017-11-10')
        if a<b:
            universefor2017.append(i)
     
        
#print(len(universe) )    #1711 
#print(len(universefor2017)) #1613   


out={'secID':[],'EPS':[],'totalPS':[],'closePrice':[],'Y_gsz':[],'IsNew':[]}
'''
#test=['603799.XSHG']
for i in universefor2017:
    out.get('secID').append(i)
    tmp1=DataAPI.FdmtIndiPSGet(ticker=u"",secID=i,endDate="",beginDate="",beginYear=u"2017",endYear=u"2017",reportType=u"CQ3",\
                               field=['EPS','sReserPS','rePS'],pandas="1") ###end
    tmp1=tmp1.fillna(0)
    if len(tmp1)==0:
        out.get('EPS').append(0)
        out.get('totalPS').append(0)
    else:
        out.get('EPS').append(tmp1['EPS'][0])
        out.get('totalPS').append(tmp1['sReserPS'][0]+tmp1['rePS'][0])  
        
    tmp2=DataAPI.MktEqudGet(secID=i,ticker=u"",tradeDate=u"20171110",beginDate=u"",endDate=u"",isOpen="",field=['closePrice'],pandas="1") ####end
    tmp2=tmp2.fillna(0)
    if len(tmp2)==0:
        out.get('closePrice').append(0)
    else:
        out.get('closePrice').append(tmp2['closePrice'][0])
        
    tmp3=DataAPI.EquGet(secID=i,ticker=u"",equTypeCD=u"A",listStatusCD=u"",\
                        field=['listDate'],pandas="1") ###end 
    
    a=datediff((tmp3['listDate'][0]),'2017-11-10')
    
    if a/360<3:
        out.get('IsNew').append(1)
    else:
        out.get('IsNew').append(0)

    tmp4=DataAPI.EquDivGet(secID=i,ticker=u"",eventProcessCD=u"",exDivDate="",beginDate=u"20170101",endDate=u"20171231",\
                          beginPublishDate=u"",endPublishDate=u"",beginRecordDate=u"",endRecordDate=u"",\
                           field=['perShareDivRatio','perShareTransRatio'],pandas="1")###end
    tmp4=tmp4.fillna(0)
    
    if (len(tmp4)==0):
        out.get('Y_gsz').append(0)
    else:
        ttt=tmp4['perShareDivRatio'][0]+tmp4['perShareTransRatio'][0]
        if (ttt>=0.5):
            out.get('Y_gsz').append(1)
        else:
            out.get('Y_gsz').append(0)
    

#print(out)#输出成功
'''
universefor2018=[]
for i in universe:
    tmp=DataAPI.EquGet(secID=i,ticker=u"",equTypeCD=u"A",listStatusCD=u"",\
                         field=['listDate'],pandas="1")
    tmp=tmp.fillna(datetime.datetime.today().strftime('%Y-%m-%d'))
    if len(tmp)!=0:
        a=strtodatetime((tmp['listDate'][0]))
        b=strtodatetime('2018-11-12')
        if a<b:
            universefor2018.append(i)
#print(len(universefor2016))#1419

for i in universefor2018:
    out.get('secID').append(i)
    tmp1=DataAPI.FdmtIndiPSGet(ticker=u"",secID=i,endDate="",beginDate="",beginYear=u"2018",endYear=u"2018",reportType=u"CQ3",\
                               field=['EPS','sReserPS','rePS'],pandas="1") ###end
    tmp1=tmp1.fillna(0)
    if len(tmp1)==0:
        out.get('EPS').append(0)
        out.get('totalPS').append(0)
    else:
        out.get('EPS').append(tmp1['EPS'][0])
        out.get('totalPS').append(tmp1['sReserPS'][0]+tmp1['rePS'][0])  
        
    tmp2=DataAPI.MktEqudGet(secID=i,ticker=u"",tradeDate=u"20181112",beginDate=u"",endDate=u"",isOpen="",field=['closePrice'],pandas="1") ####end
    tmp2=tmp2.fillna(0)
    if len(tmp2)==0:
        out.get('closePrice').append(0)
    else:
        out.get('closePrice').append(tmp2['closePrice'][0])
        
    tmp3=DataAPI.EquGet(secID=i,ticker=u"",equTypeCD=u"A",listStatusCD=u"",\
                        field=['listDate'],pandas="1") ###end 
    
    a=datediff((tmp3['listDate'][0]),'2018-11-12')
    
    if a/360<3:
        out.get('IsNew').append(1)
    else:
        out.get('IsNew').append(0)

    tmp4=DataAPI.EquDivGet(secID=i,ticker=u"",eventProcessCD=u"",exDivDate="",beginDate=u"20180101",endDate=u"20181112",\
                          beginPublishDate=u"",endPublishDate=u"",beginRecordDate=u"",endRecordDate=u"",\
                           field=['perShareDivRatio','perShareTransRatio'],pandas="1")###end
    tmp4=tmp4.fillna(0)
    
    if (len(tmp4)==0):
        out.get('Y_gsz').append(0)
    else:
        ttt=tmp4['perShareDivRatio'][0]+tmp4['perShareTransRatio'][0]
        if (ttt>=0.5):
            out.get('Y_gsz').append(1)
        else:
            out.get('Y_gsz').append(0)


 
df2=pd.DataFrame(out)
df2['intercept']=1.0 #加入常数项
print(df2.head())
#df2.to_csv('universefor2018.csv')
