-- Table: public.dn_timestamp

-- DROP TABLE public.dn_timestamp;

CREATE TABLE public.dn_timestamp
(
    id integer NOT NULL DEFAULT nextval('dn_timestamp_id_seq'::regclass),
    data jsonb NOT NULL,
    CONSTRAINT dn_timestamp_pkey PRIMARY KEY (id)
)

TABLESPACE pg_default;

ALTER TABLE public.dn_timestamp
    OWNER to postgres;

GRANT ALL ON TABLE public.dn_timestamp TO admin;

GRANT UPDATE, SELECT, INSERT, DELETE ON TABLE public.dn_timestamp TO csdplan;

GRANT SELECT ON TABLE public.dn_timestamp TO hr;

GRANT DELETE, UPDATE, SELECT, INSERT ON TABLE public.dn_timestamp TO hrconnect;

GRANT SELECT ON TABLE public.dn_timestamp TO line;

GRANT ALL ON TABLE public.dn_timestamp TO postgres;

GRANT ALL ON TABLE public.dn_timestamp TO transport;