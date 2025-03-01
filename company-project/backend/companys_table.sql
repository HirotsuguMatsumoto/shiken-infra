CREATE TABLE IF NOT EXISTS public.companys (
    id SERIAL NOT NULL,
    name character varying(200) NOT NULL,
    created timestamp without time zone DEFAULT now() NOT NULL,
    updated timestamp without time zone DEFAULT now() NOT NULL,
    PRIMARY KEY (id)
)