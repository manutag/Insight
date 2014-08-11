import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import scipy as sp
import json as js
import urllib
import MySQLdb as sql
import sklearn as skl
import calendar
import time
import os
import sys
from DistanceLatLon import distanceLatLon



db = MySQLdb.connect("localhost","root","","CityBikes" )
sql0 = 'select starthour,count(*),avg(tripduration) from CityBikes.TripData where startstationid=363 and endstationid = 327 and startday>5 group by starthour'


sql1= 'select starthour,startminutes,tripduration from CityBikes.TripData where startstationid=318 and endstationid = 477 order by starthour,startminutes'



rr0 = pd.read_sql(sql0, db)


sql1= 'select starthour,avg(tripduration) as tripduration from CityBikes.TripData ' \
      'where startstationid=318 and endstationid = 477 and startday<6 and gender = 1 group by starthour order by starthour,startminutes'
rr1 = pd.read_sql(sql1, db)
plt.plot(rr1.starthour,rr1.tripduration);#plt.xlabel('hour of the day');plt.ylabel('number of trips');

sql1= 'select starthour,avg(tripduration) as tripduration from CityBikes.TripData ' \
      'where startstationid=318 and endstationid = 477 and startday<6 and gender = 2 group by starthour order by starthour,startminutes'
rr1 = pd.read_sql(sql1, db)
plt.plot(rr1.starthour,rr1.tripduration);#plt.xlabel('hour of the day');plt.ylabel('number of trips');










sql1= 'select starthour+startminutes/60.0 as time,tripduration from CityBikes.TripData ' \
      'where startstationid=318 and endstationid = 477 and startday<6 and gender = 2 order by starthour,startminutes'
rr1 = pd.read_sql(sql1, db)
plt.figure(0)
plt.plot(rr1['starthour'],rr1['avg(tripduration)']);plt.xlabel('hour of the day');plt.ylabel('number of trips');
plt.show(0)


sql1= 'select starthour+startminutes/60.0 as time,tripduration from CityBikes.TripData ' \
      'where startstationid=318 and endstationid = 477 and startday<6 and gender = 1 order by starthour,startminutes'
rr1 = pd.read_sql(sql1, db)
plt.figure(0)
plt.plot(rr0['starthour'],rr0['avg(tripduration)']);plt.xlabel('hour of the day');plt.ylabel('number of trips');
plt.show(0)



mpl.pyplot.scatter(rr1.time,rr1.tripduration)
mpl.pyplot.show()



#plt.axis(0,25,0,10000)
plt.show()



plt.figure(0)
plt.plot(rr0['starthour'],rr0['avg(tripduration)']);plt.xlabel('hour of the day');plt.ylabel('number of trips');
plt.plot(rr['starthour'],rr['avg(tripduration)']);plt.xlabel('hour of the day');plt.ylabel('number of trips');
plt.show(0)

plt.figure(1)
plt.plot(rr['starthour'],rr['avg(tripduration)'],yerr =rr['stddev(tripduration)']);plt.xlabel('hour of the day');plt.ylabel('average trip duration');plt.show(1)

plt.errorbar(rr['starthour'],rr['avg(tripduration)'], yerr=rr['stddev(tripduration)'], fmt='', color='b')
