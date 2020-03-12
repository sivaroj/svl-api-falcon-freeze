with md5 as (
  select min(data->>'MD5') as md5 from dn_timestamp t where t.data->>'DN_NO' = '2003110055'
)
select 	d.data->>'MD5' as md5,d.data->>'DN_NO' as dn_no,(d.data->>'DN_ORDER')::int as dn_order,
		d.data->>'SOURCE_POINT' as source_point,d.data->>'IN_OUT' as in_out,
		json_path_query(data,'IN_OUT')
from dn_timestamp d where d.data->>'MD5' = (select md5 from md5)
order by d.data->>'DN_NO',(d.data->>'DN_ORDER')::int


explain
select max((data->>'IN_OUT')::int)
from dn_timestamp where data @> '{"DN_NO":"2003110055","SOURCE_POINT":"YARDL"}'::jsonb