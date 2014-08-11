import json as js

PathBike = "/home/m/Documents/Insight/bike/"

json_data=open(PathBike+'StationCapacity.json').read()
data = js.loads(json_data)
d1 = pd.DataFrame(data['stationBeanList'])

ChooseStation = range(len(d1))

PositionString = '['
for i in ChooseStation:
    PositionString = PositionString + '[\''+  'Station '+str(d1.id[i])+', '+  d1.stationName[i]+'\','+str(d1.latitude[i])+','+str(d1.longitude[i])+','+'],'

PositionString = PositionString[:-1] + '];'


print(PositionString)
