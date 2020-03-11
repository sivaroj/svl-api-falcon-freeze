select * from dn_timestamp where @> '{"TRUCK_NO":"L99"}'::jsonb
select jsonb_to_record(data::jsonb) from dn_timestamp

select jsonb_pretty(data) from dn_timestamp
select jsonb_path_query(data,'$.*') from dn_timestamp
select jsonb_path_query(data,'$.POSITION[*]') as position ,
jsonb_path_query(data,'$.TRUCK_POSITION[*]') as truck_position from dn_timestamp


with md5 as (
  select min(data->>'MD5') as md5 from dn_timestamp t where t.data->>'DN_NO' = '2003110055'
)
select * from dn_timestamp d where d.data->>'MD5' = (select md5 from md5)
order by d.data->>'DN_NO',d.data->>'DN_ORDER'
  
select * from dn_timestamp where data ? 'ประจวบ'