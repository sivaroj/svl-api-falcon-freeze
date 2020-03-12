-- SEQUENCE: public.dn_timestamp_id_seq

-- DROP SEQUENCE public.dn_timestamp_id_seq;

CREATE SEQUENCE public.dn_timestamp_id_seq
    INCREMENT 1
    START 21
    MINVALUE 1
    MAXVALUE 2147483647
    CACHE 1;

ALTER SEQUENCE public.dn_timestamp_id_seq
    OWNER TO postgres;

GRANT ALL ON SEQUENCE public.dn_timestamp_id_seq TO admin;

GRANT ALL ON SEQUENCE public.dn_timestamp_id_seq TO csdplan;

GRANT SELECT ON SEQUENCE public.dn_timestamp_id_seq TO hr;

GRANT ALL ON SEQUENCE public.dn_timestamp_id_seq TO hrconnect;

GRANT SELECT ON SEQUENCE public.dn_timestamp_id_seq TO line;

GRANT ALL ON SEQUENCE public.dn_timestamp_id_seq TO postgres;

GRANT ALL ON SEQUENCE public.dn_timestamp_id_seq TO transport;