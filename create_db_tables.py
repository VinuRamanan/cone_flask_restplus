import psycopg2 as pg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
import time
import json

with open('settings.json', 'r') as f:
    settings = json.load(f)
    POSTGRES, POSTGRES_PWD, CONE_USER, CONE_PASSWORD, CONE_DBNAME = settings['POSTGRES'], settings[
        'POSTGRES_PWD'], settings['CONE_USER'], settings['CONE_PASSWORD'], settings['CONE_DBNAME'],


def create_user():
    global POSTGRES, POSTGRES_PWD, CONE_USER, CONE_PASSWORD
    con = pg2.connect(host='localhost', port=5432,
                      user=POSTGRES, password=POSTGRES_PWD)
    cur = con.cursor()
    con.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
    s = """CREATE ROLE {CONE_USER} WITH
	LOGIN
	SUPERUSER
	CREATEDB
	CREATEROLE
	INHERIT
	NOREPLICATION
	CONNECTION LIMIT -1
	PASSWORD '{CONE_PASSWORD}';
    alter user {CONE_USER} CREATEDB;""".format(
        CONE_USER=CONE_USER, CONE_PASSWORD=CONE_PASSWORD)
    print(s)
    cur.execute(s)
    con.commit()


def create_db():
    global CONE_USER, CONE_DBNAME, CONE_PASSWORD, POSTGRES, POSTGRES_PWD
    print(CONE_USER, CONE_DBNAME, CONE_PASSWORD)
    con = pg2.connect(host='localhost', port=5432,
                      user=CONE_USER, password=CONE_PASSWORD, dbname='postgres')
    db = con.cursor()

    con.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)

    statement = """CREATE DATABASE {CONE_DBNAME}
        WITH 
        OWNER = {CONE_USER}
        ENCODING = 'UTF8'
        LC_COLLATE = 'English_India.1252'
        LC_CTYPE = 'English_India.1252'
        TABLESPACE = pg_default
        CONNECTION LIMIT = -1;""".format(CONE_DBNAME=CONE_DBNAME, CONE_USER=CONE_USER)

    db.execute(statement)
    con.commit()

    db.close()
    con.close()


def create_tables():
    global CONE_USER, CONE_PASSWORD, CONE_DBNAME
    con = pg2.connect(host='localhost', port=5432,
                      user=CONE_USER, password=CONE_PASSWORD, dbname=CONE_DBNAME)
    cur = con.cursor()

    def execute(statement, con, cursor):
        cursor.execute(statement)
        con.commit()

    cone_records = """CREATE TABLE public.cone_records
    (
        date date DEFAULT date(now()),
        time_stamp integer DEFAULT date_part('epoch'::text, now()),
        lot_number text COLLATE pg_catalog."default",
        yarn_type text COLLATE pg_catalog."default",
        customer_name text COLLATE pg_catalog."default",
        lot_weight double precision,
        yarn_count text COLLATE pg_catalog."default",
        sample_number integer,
        density double precision,
        error_type text COLLATE pg_catalog."default",
        laser_raw_output double precision,
        outer_diameter double precision,
        volume double precision,
        weight_raw_output double precision,
        mass double precision,
        barcode_raw_input double precision,
        id serial primary key,
        start_lot_height double precision,
        end_lot_height double precision,
        weight double precision,
        spindle_number text COLLATE pg_catalog."default"
    )

    TABLESPACE pg_default;

    GRANT INSERT, SELECT ON TABLE public.cone_records TO {CONE_USER};""".format(CONE_USER=CONE_USER)

    execute(cone_records, con, cur)

    port = """create table port(id serial primary key, laser_port text, weight_port text);
    GRANT INSERT, SELECT ON TABLE public.cone_records TO {CONE_USER};""".format(CONE_USER=CONE_USER)

    execute(port, con, cur)

    error = """create table error(id serial primary key, min_density double precision, max_density double precision, min_outer_diameter double precision, max_outer_diameter double precision, min_weight double precision, max_weight double precision);
    GRANT INSERT, SELECT ON TABLE public.cone_records TO {CONE_USER};""".format(CONE_USER=CONE_USER)

    execute(error, con, cur)

    param = """create table param(id serial primary key, empty_tube_diameter double precision, calibration double precision);
    GRANT INSERT, SELECT ON TABLE public.cone_records TO {CONE_USER};""".format(CONE_USER=CONE_USER)

    execute(param, con, cur)

    cur.close()
    con.close()


def create_uri():
    settings['SQLALCHEMY_URI'] = "postgres://{}:{}@localhost:5432/{}".format(
        CONE_USER, CONE_PASSWORD, CONE_DBNAME)
    with open('settings.json', 'w') as f:
        json.dump(settings, f)


if __name__ == '__main__':
    create_user()
    create_db()
    create_tables()
    create_uri()
