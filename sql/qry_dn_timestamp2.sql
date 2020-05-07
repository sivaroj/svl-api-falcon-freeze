with DN as (
  select min(data->>'MD5') as md5 from dn_timestamp t where t.data->>'DN_NO' = '2005010038'
)
select 	d.data->>'MD5' as md5,d.data->>'DN_NO',(d.data->>'DN_ORDER')::int as dn_order,d.data->>'IN_OUT' as in_out
from dn_timestamp d where d.data->>'MD5' = (select md5 from DN)
order by d.data->>'DN_NO' ,(d.data->>'DN_ORDER')::int 
--order by d.id desc limit 1

select t.data->'DN_NO' as DN_NO,t.data->'TRUCK_NO', t.data->'POSITION'->'address',
t.data->'TRUCK_POSITION'->'address', t.data->'t.data->'POSITION'->'address',
t.data->'t.data->'POSITION'->'address'
from dn_timestamp t 
where t.data->>'DN_NO' = '2005010038'

with md5 as (
  select min(data->>'MD5') as md5 from dn_timestamp t where t.data->>'DN_NO' = '2005020022'
)
B0211 2003080024

select * from dn_timestamp where data @> '{"DN_ORDER":99,"IN_OUT": "1"}'::jsonb

select *  from dn_timestamp where to_date(substring(data->>'DN_NO'::text,1,6),'YYMMDD') between '2020-02-01' and '2020-02-29'