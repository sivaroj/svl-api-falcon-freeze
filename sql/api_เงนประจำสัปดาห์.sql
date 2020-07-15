commit
---- 0 inert into tmp_emp_ly_weekly_api
----- select * from tmp_emp_lh_weekly_api
select * from tmp_emp_lh_weekly_api

insert into tmp_emp_lh_weekly_api
(
  select * 
  from (
      select distinct eb.processdate,eb.emp_no
      from emp_lh_weekly_balance eb 
      inner join employee e on e.emp_no=eb.emp_no
--      where e.social_no= '3770400034458' 
        where e.emp_no='L0804' 
      order by 1 desc
  ) 
  where rownum<=10
)

-------------------------------------------------------- query --------------------------------------------------------
insert into tmp_emp_lh_weekly(
    select * from (  
          select DISTINCT 
                ew.processdate  , '0' as type
                ,e.name||' '||e.surname as emp_name
                ,A.TRUCK_NO
                ,L.DN_NO,L.DN_DATE
                ,ew.emp_no,ew.adv_gas_amount,ew.gas_cash,ew.adv_cash,ew.oth_amount
                ,(ew.adv_gas_amount+ew.gas_cash+ew.adv_cash+ew.oth_amount) as net
                ,0 as prv_balance,0 as this_balance,0 as balance
          from tmp_emp_lh_weekly_api wk 
          inner join employee e on e.emp_no = wk.emp_no
          inner join emp_lh_weekly ew on ew.emp_no=wk.emp_no  and ew.processdate = wk.processdate 
                   AND (EW.ADV_GAS_AMOUNT <>0 OR EW.GAS_CASH <>0 OR EW.ADV_CASH <>0 OR EW.OTH_AMOUNT <>0) 
          inner join advance_lh a on a.adv_no = ew.adv_no and a.emp_no = wk.emp_no
          inner join truck t on t.truck_no=a.truck_no
          inner join lh_dn l on L.DN_NO = A.DN_NO AND L.CAR_REGIS_NO=T.TRUCK_REGISTER_NO


          union all

          select 
                  eb.processdate ,'1'
                  ,e.name||' '||e.surname as emp_name
                  ,NULL
                  ,'ใช้เกินครั้งก่อน', 
                  (select max(eb3.processdate) from emp_lh_weekly_balance eb3 where eb3.processdate<wk.processdate  AND EB3.EMP_NO=EB.EMP_NO)
                  ,eb.emp_no
                  ,(case when eb.balance>0 then eb.balance else 0 end ) as next_balance
                  ,0,0,0
                  ,eb.balance
                  ,0,0,0
          from tmp_emp_lh_weekly_api wk 
          inner join employee e on e.emp_no = wk.emp_no
          inner join  emp_lh_weekly_balance eb on  eb.emp_no = wk.emp_no and 
                    eb.processdate= 
                   (select max(eb3.processdate) from emp_lh_weekly_balance eb3 
                   where eb3.processdate< wk.processdate  AND EB3.EMP_NO=EB.EMP_NO   )
                                          

          union all
                  select eb.processdate ,'2'
                  ,e.name||' '||e.surname as emp_name
                  ,NULL
                  ,'ยอดยกมา',null
                  ,eb.emp_no,0,0,0,0,0,eb.prv_balance,eb.this_balance
                  ,case when eb.balance>0 then eb.balance else 0 end as next_balance
                  from tmp_emp_lh_weekly_api wk
                  inner join emp_lh_weekly_balance eb on eb.processdate=wk.processdate and eb.emp_no=wk.emp_no
                  inner join employee e on e.emp_no = wk.emp_no

    ) x
    where ( x.adv_gas_amount <> 0 or x.gas_cash <> 0 or x.adv_cash <> 0 or x.oth_amount <> 0)
)
----------------------------------------------------------------------------------------------------
--call svl_api.ins_tmp_emp_lh_weekly_api('L1294',10)
call svl_api.prepare_emp_lh_weekly('L1294')
commit

select * from tmp_emp_lh_weekly tw 
order by 1 desc,2 desc,5

select ta.processdate,ta.emp_no,ta.prv_balance
,sum(tw.adv_gas_amount) as sum_
,sum(tw.gas_cash)
,sum(tw.adv_cash)
,sum(tw.oth_amount)
,sum(tw.net)
from tmp_emp_lh_weekly_api ta
inner join tmp_emp_lh_weekly tw on ta.processdate=tw.processdate and ta.emp_no=tw.emp_no
group by ta.processdate,ta.emp_no,ta.prv_balance
order by 1 desc

select  tw.processdate
,sum(tw.adv_gas_amount)
,sum(tw.gas_cash)
,sum(tw.adv_cash)
,sum(tw.oth_amount)
,sum(tw.net)
from tmp_emp_lh_weekly  tw
group by tw.processdate

