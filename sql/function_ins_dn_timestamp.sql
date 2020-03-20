-- FUNCTION: public.ins_dn_timestamp(jsonb)

-- DROP FUNCTION public.ins_dn_timestamp(jsonb);

CREATE OR REPLACE FUNCTION public.ins_dn_timestamp(
	v_data jsonb)
    RETURNS integer
    LANGUAGE 'plpgsql'

    COST 100
    VOLATILE 
    
AS $BODY$
DECLARE 
	rtn integer;
	records integer;
	DN_NO character varying(10);
	SOURCE_POINT character varying(10);
	DN_ORDER integer;
	IN_OUT character varying(1);
BEGIN
	/*
	DN_NO := v_data->>'DN_NO';
	SOURCE_POINT := v_data->>'SOURCE_POINT';
	DN_ORDER := v_data->>'DN_ORDER';
	IN_OUT := v_data->>'IN_OUT';
	*/
	select count(*)
	into records
	from dn_timestamp 
	where data @> v_data;
	
	if (records = 0) then
	   insert into dn_timestamp(data) values (v_data);
	end if;	
    RETURN records;
END;
$BODY$;

ALTER FUNCTION public.ins_dn_timestamp(jsonb)
    OWNER TO postgres;

GRANT EXECUTE ON FUNCTION public.ins_dn_timestamp(jsonb) TO transport;

GRANT EXECUTE ON FUNCTION public.ins_dn_timestamp(jsonb) TO hrconnect;

GRANT EXECUTE ON FUNCTION public.ins_dn_timestamp(jsonb) TO postgres;

GRANT EXECUTE ON FUNCTION public.ins_dn_timestamp(jsonb) TO PUBLIC;

GRANT EXECUTE ON FUNCTION public.ins_dn_timestamp(jsonb) TO line;

GRANT EXECUTE ON FUNCTION public.ins_dn_timestamp(jsonb) TO hr;

GRANT EXECUTE ON FUNCTION public.ins_dn_timestamp(jsonb) TO csdplan;

GRANT EXECUTE ON FUNCTION public.ins_dn_timestamp(jsonb) TO admin;

