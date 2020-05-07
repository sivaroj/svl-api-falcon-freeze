
with dn as (
 select min(data->>'MD5') as md5 from dn_timestamp t where t.data->>'DN_NO' = '2005050015'
)
select d.data->'DN_NO' as dn_no,d.data->'TRUCK_NO' as truck_no,d.data->'EMP_NO' as emp_no,d.data->'SOURCE_POINT' as source_point
,d.data->'LAT_LNG' as lat_lng
,d.data->'IN_OUT' as in_out
,d.data->'POSITION'->'timestamp' as mo_timestamp
,d.data->'POSITION'->'latitude' as mo_lattitude 
,d.data->'POSITION'->'longitude' as mo_longitude
,d.data->'POSITION'->'address' as mo_address
,d.data->'POSITION'->'far_from'->'distance' as mo_far_from_distance
,d.data->'POSITION'->'far_from'->'travel_time' as mo_far_from_travel_time
,d.data->'TRUCK_POSITION'->'datetime' as tr_datetime
,d.data->'TRUCK_POSITION'->'latitude' as mo_lattitude 
,d.data->'TRUCK_POSITION'->'longitude' as mo_longitude
,d.data->'TRUCK_POSITION'->'address' as tr_address
,d.data->'TRUCK_POSITION'->'far_from'->'distance' as tr_far_from_distance
,d.data->'TRUCK_POSITION'->'far_from'->'travel_time' as tr_far_from_travel_time
from dn_timestamp d where d.data->>'MD5' = (select md5 from DN)
order by d.data->>'DN_NO' ,(d.data->>'DN_ORDER')::int 

