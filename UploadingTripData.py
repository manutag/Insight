import pandas as pd
import numpy as np
import matplotlib as mp
import scipy as sp
import json as js
import MySQLdb
import time
import datetime
import sklearn as sk
import matplotlib.pyplot as plt
import math
from DistanceLatLon import distanceLatLon



PathData = "/home/m/Documents/Insight/bike/Data/"
PathBike = "/home/m/Documents/Insight/bike/"
FileNames = ['2013-07 - Citi Bike trip data',
             '2013-08 - Citi Bike trip data',
             '2013-09 - Citi Bike trip data',
             '2013-10 - Citi Bike trip data',
             '2013-11 - Citi Bike trip data',
             '2013-12 - Citi Bike trip data',
             '2014-01 - Citi Bike trip data',
             '2014-02 - Citi Bike trip data',
             '2014-03 - Citi Bike trip data',
             '2014-04 - Citi Bike trip data',
             '2014-05 - Citi Bike trip data' ]

# retrieving station ID and capacity

json_data=open(PathBike+'StationCapacity.json').read()
data = js.loads(json_data)
d1 = pd.DataFrame(data['stationBeanList'])
# 332 stations
d1=d1.drop(['altitude','availableBikes','availableDocks','city','landMark','lastCommunicationTime','location','postalCode','stAddress1','stAddress2','statusKey','statusValue','testStation'],1)
d1.to_csv(PathData+'StationINFO.csv')


#stationNames = d1['stationName']
#stationIDs = d1['id'];
#stationCapacities = d1['totalDocks']
#stationLatitude = d1['latitude']
#stationLongitude = d1['longitude']

#################################################################################################################################
# reading and loading the files with trips

TableName = 'TripData'
db = MySQLdb.connect("localhost","root","","CityBikes" )
#db.query('Drop table if exists '+TableName)

length = 0
for i in range(len(FileNames)):
    print (str(i))
    aj = pd.read_csv(PathData+FileNames[i]+'.csv', parse_dates=[1,2,13])
    aj = aj[ (aj['usertype'] != 'Customer') & (aj['birth year'] != '\\N')  ]

    aj.columns =['tripduration', 'starttime', 'stoptime', 'startstationid', 'startstationname', 'startstationlatitude', 'startstationlongitude', 'endstationid', 'endstationname', 'endstationlatitude', 'endstationlongitude', 'bikeid', 'usertype', 'birthyear', 'gender']

    aj['startseconds'] = aj['starttime'].apply(lambda x: x.second)
    aj['startminutes'] = aj['starttime'].apply(lambda x: x.minute)
    aj['starthour'] = aj['starttime'].apply(lambda x: x.hour)
    aj['startday'] = aj['starttime'].apply(lambda x: x.day)
    aj['startmonth'] = aj['starttime'].apply(lambda x: x.month)
    aj['age'] =  aj['starttime'].apply(lambda x: x.year)- aj['birthyear'].apply(int)+aj['startmonth']/12.0

    aj = aj.drop(['startstationname','startstationlatitude','startstationlongitude','endstationname','endstationlatitude','endstationlongitude','usertype','birthyear'], 1)

    aj.index = range(length,length+len(aj),1)
    length = length + len(aj)

    print('load to database')
    db = MySQLdb.connect("localhost","root","","CityBikes" )
    aj.to_sql(con=db, name=TableName, if_exists='append', flavor='mysql')
    print('finish to database')
    print ('Finish '+str(i))


# creating indices

db.query('Create index starttime on CityBikes.TripData(starttime)')
db.query('Create index startstationidendstationid on CityBikes.TripData(startstationid,endstationid)')
db.query('Create index stations on CityBikes.TripData(starttime,startstationid,endstationid)')
db.query('Create index month on CityBikes.TripData(month)')
db.query('Create index day on CityBikes.TripData(day)')
db.query('Create index minute on CityBikes.TripData(minute)')



