# coding=UTF8
import pandas as pd
import requests,time,sys,urllib.parse,cx_Oracle,os,re,arrow
from bs4 import BeautifulSoup
from datetime import date,datetime ,timedelta

def traceback(err):
    '''
    紀錄錯誤資訊。
    包含時間點(now)，錯誤內容(traceback)，以及行數。
    '''
    now = time.strftime('%H:%M:%S', time.localtime(time.time()))
    traceback = sys.exc_info()[2]
    print (str(now)+' '+str(err)+'\n'+'exception in line '+str(traceback.tb_lineno))

def date_range(start,stop,step):
    while start < stop :
        yield start
        start += step
        
weather=pd.DataFrame(columns=['YEAR','MONTH','DAY','HOUR','STATION','TEMP','RH','RAIN'])

#202003所有使用的氣象站,在此只列出一站
station={'466880':'板橋'}
count=0
error=[]

#想要抓取的日期(當天會沒資料，有時候會延遲2天才會更新
t=arrow.get(2019,12,5)
now=arrow.now().shift(days=1)

#重複爬取，當時間跑到今天的時候就跳出
for i in  ['']*10000:
    t=t.shift(days=1)
    print(t)
    if t == arrow.get(now.year,now.month,now.day):
        break
    for i in station.keys():
        count+=1
        station_no=i
        station_name=station[i]

        try:
            year=str(t.year).zfill(2)
            month=str(t.month).zfill(2)
            day=str(t.day).zfill(2)
            date=year+'-'+month+'-'+day
            
            url=('https://e-service.cwb.gov.tw/HistoryDataQuery/DayDataController.do?command=viewMain&station={}&stname={}&datepicker={}').format(station_no,urllib.parse.quote(station_name).replace('%',"%25"),date)
            r = requests.get(url)
            soup = BeautifulSoup(r.text,'lxml')
            for j in range(4,28):
                Hour=j-3
                Temperature=soup.find_all('tr')[j].find_all('td')[3].text
                RH=soup.find_all('tr')[j].find_all('td')[5].text
                Precp=soup.find_all('tr')[j].find_all('td')[10].text

                weather1=pd.DataFrame([[year,month,day,Hour,station_no,Temperature,RH,Precp]],columns=['YEAR','MONTH','DAY','HOUR','STATION','TEMP','RH','RAIN'])
                print(weather1)
                weather=pd.concat([weather,weather1],axis=0)

        except Exception as err:
            traceback(err)
            error.append(i)
            continue
    time.sleep(5)
