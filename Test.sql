use CityBikes


select distinct startstationid,endstationid
from CityBikes.TripData 
group by startstationid,endstationid
-- there are 97868 combination, out of 332^2=110224


select starttime,tripduration from CityBikes.TripData 
where startstationid=318 and endstationid = 477 
order by starthour,startminutes


select startstationid,endstationid,count(*) 
from CityBikes.TripData 
group by startstationid,endstationid
having count(*) > 1200
order by 3 desc

select startstationid,startday,count(*) 
from CityBikes.TripData 
group by startstationid,startday
order by 3 desc

select dististartstationid,startday 
from CityBikes.TripData 
group by startstationid,startday
order by 3 desc





select startstationid,count(*) 
from CityBikes.TripData 
group by startstationid
order by 2 desc




select starthour+startminutes/60.0,tripduration from CityBikes.TripData 
where startstationid=318 and endstationid = 477 and startday<5
order by 1



SELECT table_name AS "Table", 
round(((data_length + index_length) / 1024 / 1024), 2) "Size in MB" 
FROM (Select * from information_schema.TABLES limit 30) as s

