with c as (
	select l.customer_no,l.dn_date ,l.product
	--,lc.customer_no  as supplier
	,count(distinct l.car_regis_no) as trucks
	,sum(l.wgt) as wgt
	,0 as coil_remain
	from lh_dn l 
	inner join line_lh_car_regis lc on lc.car_regis  = l.car_regis_no and lc.status ='N'
	where l.dn_date = '2020-06-16' and l.status ='A'
	group by l.customer_no,l.dn_date ,l.product 
	union all
	select cr.customer_no ,cr.dn_date ,cr.product ,0 as trucks,0 as wgt,coil_remain 
	from coil_remain cr 
	where cr.dn_date  = '2020-06-16'
) select  c.customer_no,c.product,sum(c.trucks) as trucks
, sum(c.wgt) as wgt ,sum(c.coil_remain) as coil_remain
,case when ac.logistics ='LH' then 'true' else 'false' end as associated
from c 
left outer  join associated_comp ac on ac.company =c.customer_no
group by c.customer_no,c.product, associated
order by c.customer_no,c.product


