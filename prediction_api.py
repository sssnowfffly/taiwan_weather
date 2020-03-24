import arrow,requests,json,cx_Oracle,os

authnum="你的氣象驗證碼"
#要自己去氣象局申請開放資料的驗證碼
#使用台灣氣象局的開放資料：36小時預報API

url=('https://opendata.cwb.gov.tw/api/v1/rest/datastore/F-C0032-001?Authorization={}').format(authnum)
r = requests.get(url)

#記錄本地資料
localdata={}
#紀錄資料屬性
elementName={}

#收集網站資料後，找尋各地資訊
for i in json.loads(r.text)['records']['location']:
    locationName=i['locationName']
    for j in i['weatherElement']:
        for k in j['time']:
            startTime=arrow.get(k['startTime'])
            parameter=k['parameter']['parameterName']
            elementName[(k['startTime'],j['elementName'])]=parameter
   
   #重新整理時區 
   time_data={}        
    for i in elementName.keys():
        if i[1] == 'Wx': #氣象描述
            if i[0] in time_data.keys():
                time_data[i[0]].append(elementName[i])
            else:
                time_data[i[0]]=[]
                time_data[i[0]].append(elementName[i])
        elif i[1] == 'PoP': #降雨率
            if i[0] in time_data.keys():
                time_data[i[0]].append(elementName[i])
            else:
                time_data[i[0]]=[]
                time_data[i[0]].append(elementName[i])
        elif i[1] == 'MinT': #最低氣溫
            if i[0] in time_data.keys():
                time_data[i[0]].append(elementName[i])
            else:
                time_data[i[0]]=[]
                time_data[i[0]].append(elementName[i])
        elif i[1] == 'MaxT': #最高氣溫
            if i[0] in time_data.keys():
                time_data[i[0]].append(elementName[i])
            else:
                time_data[i[0]]=[]
                time_data[i[0]].append(elementName[i])

    local_data[locationName]=time_data

#判斷時區重新整理成可以進資料庫的模式
for i in local_data.keys():
    for j in local_data[i].keys():
        if arrow.get(j).format("YYYY-MM-DD") == arrow.now().format("YYYY-MM-DD"):
            if arrow.get(j).hour == 18:
                timet=2 #今天晚上（18:00-6:00）
            else:timet=1 #今天白天（6:00-18:00）
        else:
            if arrow.get(j).hour == 18:
                timet=4 #明天晚上（18:00-6:00）
            else:timet=3 #明天白天（6:00-18:00）

        #分別為縣市、時間點、氣象敘述、降雨機率、最低氣溫、最高氣溫、預測時區
        print(i,j,local_data[i][j][0],local_data[i][j][1],local_data[i][j][2],local_data[i][j][3],timet)
