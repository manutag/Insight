import pandas as pd
import numpy as np
import matplotlib as mp
import scipy as sp
import json as js
import urllib
import MySQLdb as sql
import sklearn as skl
import calendar
import time
import os
import sys

PathData = "/home/m/Documents/Insight/bike/Data/"
PathBike = "/home/m/Documents/Insight/bike/"


json_data=open(PathBike+'StationCapacity.json').read()
data = js.loads(json_data)
#pprint(data) type(data['stationBeanList'])
d1 = pd.DataFrame(data['stationBeanList'])
# 332 stations
d1.to_csv(PathData+'StationINFO.csv')

stationNames = d1['stationName']
stationIDs = d1['id'];
stationCapacities = d1['totalDocks']
stationLatitude = d1['latitude']
stationLongitude = d1['longitude']









startTime = '0:00'
endTime   = '23:59'
startDate = '20140301'
endDate   = '20140531'


MonthsIni = [ ['2013','07'],['2013','10'],['2014','01'],['2014','04']]
MonthsEnd = [ ['2013','09'],['2013','12'],['2014','03'],['2014','05']]

#Dates = ['20130701','20130801','20130901','20131001','20131101','20131201','20130801','20140301','20140301','20140301','20140301','20140301','20140301','20140301','20140301','20140301','20140301']

for j in range(len(MonthsIni)):
    for i in [60,70,72,97,42,62,74]:#( len(d1)):
        #i = 0
        station = d1['stationName'][i]
        st = pd.DataFrame()
        stationID = d1['id'][i]
        CSVfile = PathData + 'Stations3/' + str(i)+'_'+station + '_part' + str(j)+ '.csv'
        startDate = MonthsIni[j][0]+MonthsIni[j][1]+'01'
        endDate = MonthsEnd[j][0]+MonthsEnd[j][1]+str(calendar.monthrange(int(MonthsEnd[j][0]),int(MonthsEnd[j][1]))[1])
        url=r"http://data.citibik.es/render/?target="
        url = url+  station.replace("&",r"%26").replace(" ","-")+".available_bikes&from="+startTime+"_"+startDate+"&until="+endTime+"_"+endDate+"&format=csv"
        print('station ' + str(i) + '_' +url +'      month'+str(j))
        urllib.urlretrieve(url, CSVfile)
        time.sleep(1)


for j in range(len(MonthsIni)):
    print (str(j))
    for i in [60,70,72,97,42,62,74]:#range( len(d1)):
        #i = 0
        station = d1['stationName'][i]
        st = pd.DataFrame()
        stationID = d1['id'][i]
        CSVfile = PathData + 'Stations3/' + str(i)+'_'+station + '_part' + str(j)+ '.csv'
        startDate = MonthsIni[j][0]+MonthsIni[j][1]+'01'
        endDate = MonthsEnd[j][0]+MonthsEnd[j][1]+str(calendar.monthrange(int(MonthsEnd[j][0]),int(MonthsEnd[j][1]))[1])
        url=r"http://data.citibik.es/render/?target="
        url = url+  station.replace("&",r"%26").replace(" ","-")+".available_bikes&from="+startTime+"_"+startDate+"&until="+endTime+"_"+endDate+"&format=csv"

        df0 = pd.read_csv(CSVfile, parse_dates=[1],names = ['station','time','AvailableBikes'])
        try:
            lastday = df0['time'][len(df0)-1].day
            filesize = os.path.getsize(CSVfile)/1e6
            if (filesize < 0.01) | ( (lastday<28) & (lastday>1)):
                print('station ' + str(i) + '_' +url +'      month'+str(j))
        except:
            pass
            print('station ' + str(i) + '_' +url +'      month'+str(j))



            #urllib.urlretrieve(url, CSVfile)
            #time.sleep(1)



# dropping the tables
db = MySQLdb.connect("localhost","root","","CityBikes" )
for i in range( len(d1)):
    stationID = d1['id'][i]
    TableName = 'station'+str(stationID)
    db.query('Drop table if exists '+TableName)




# uploading the tables
for i in range(42,len(d1),1):
    station = d1['stationName'][i]
    TableName =  str(i) +'station'+str(stationID)
    db = MySQLdb.connect("localhost","root","","CityBikes" )
    db.query('DROP TABLE IF EXISTS '+ TableName)
    length=0
    for j in range(len(MonthsIni)):
        #i = 0;j=0
        stationID = d1['id'][i]
        CSVfile = PathData + 'Stations3/' + str(i)+'_'+station + '_part' + str(j)+ '.csv'
        df0 = pd.read_csv(CSVfile, parse_dates=[1],names = ['station','time','AvailableBikes'])
        print('start '+CSVfile + '' + str(datetime.datetime.now()))

        #df0['AvailableBikes'] = df0['AvailableBikes'].fillna(method='ffill')
        df0 = df0[ df0['AvailableBikes']>=0]
        df0 = df0.drop('station', 1)

        df0['minute'] = df0['time'].apply(lambda x: x.minute)
        df0['hour'] = df0['time'].apply(lambda x: x.hour)
        df0['day'] = df0['time'].apply(lambda x: x.day)
        df0['month'] = df0['time'].apply(lambda x: x.month)

        df0['ind'] = range(length,length+len(df0),1)
        length = length + len(df0)



        print('begin upload '+str(i)+' '+str(j))
        df0.to_sql(con=db, name=TableName, if_exists='append', flavor='mysql', index=False)
        print('end upload '+str(i)+' '+str(j))

# creating indices,
    db.query('Create index time on '+TableName+'(time)')
    db.query('Create index month on '+TableName+'(month)')
    db.query('Create index hour on '+TableName+'(hour)')
    db.query('Create index day on '+TableName+'(day)')
    db.query('Create index minute on '+TableName+'(minute)')
    db.query('Create index ind on '+TableName+'(ind)')
    print('end '+CSVfile + ' ' + str(datetime.datetime.now()) + ' rows=' + str(length) )



db = MySQLdb.connect("localhost","root","","CityBikes" )
sql = 'select hour,avg(AvailableBikes) from CityBikes.'+TableName+ ' group by hour'

df = pd.read_sql(sql, db)




cursor = db.cursor()
cursor.execute(sql)
results = cursor.fetchall()

rr =zip(*results)
xx=rr[2]

plt.plot(rr[0],rr[1]);plt.xlabel('hour of the day');plt.ylabel('number of trips');plt.show()
plt.plot(rr[0],rr[2]);plt.xlabel('hour of the day');plt.ylabel('average trip duration');plt.show()









# looping through the stations
#for i in range(len(d1)):
    i = 0
    station = d1['stationName'][i]
    stationID = d1['id'][i]
    #station ='Atlantic Ave %26 Fort Greene Pl'
    CSVfile = PathData + 'Stations/' + station + '.csv'
    st = pd.read_csv(CSVfile, parse_dates=[1],names = ['station','time','AvailableBikes'  ])
    st = st.drop('station', 1)
    #cleaning the NaN fields
    st['AvailableBikes'] = st['AvailableBikes'].fillna(method='ffill')
    #st['AvailableBikes'] = st.groupby(['time'])['AvailableBikes'].transform(lambda grp: grp.fillna(method='ffill'))

    TableName = 'station'+str(stationID)
    db = MySQLdb.connect("localhost","root","","CityBikes" )
    db.query('DROP TABLE IF EXISTS '+ TableName + ';CREATE TABLE ' + TableName + '(Time timestamp primary key, AvailableBikes integer );')
    result = db.use_result()

    st.to_sql(con=db, name='station'+str(stationID), if_exists='replace', flavor='mysql')

df = pd.DataFrame({'id': [1,1,2,2,1,2,1,1], 'x':[10,20,100,200,np.nan,np.nan,300,np.nan]})
print(df)






a[:5]


d1=pd.DataFrame(d1)
d1[1]['totalDocks']

data['stationBeanList'].


data['stationBeanList']


d2=pd.DataFrame(data['stationBeanList'])


d

d2.id
d2.totalDocks
d2[['id','totalDocks']]



def buildCitibikesURL(station,startDate,startTime,endDate,endTime):
#http://data.citibik.es/render/?target=Montague-St-%26-Clinton-St.available_bikes&from=0:00_20130615&until=0:00_20130715&format=csv
#http://data.citibik.es/render/?target=Montague-St-%26-Clinton-St.available_bikes&from=0:00_20130701&until=0:00_20130715&format=csv'


    url=r"http://data.citibik.es/render/?target="
    url = url+station.replace("&",r"%26")+".available_bikes&from="+startTime+"_"+\
           startDate+"&until="+endTime+"_"+endDate+"&format=csv"
    return url



    dirfilestation=file_input.split(",")
    station_dir=dirfilestation[0]
    station=dirfilestation[-1]
    fileName=station+".csv"


    dirname =os.path.dirname(sys.argv[0])
    directory = dirname+"\\"+station_dir+"\\"



    CSVfile=directory+fileName
    if os.path.isfile(CSVfile) is False:
        if not os.path.exists(directory):
            os.makedirs(directory)
        print "Downloading data from station", station+"... \nThis may take a few minutes."
        urllib.urlretrieve (url, CSVfile)
        #downloadFile(url, CSVfile)
        print "Done downloading!\n"
    else:
        print "\nFile already exists:\n", CSVfile,"\n"

