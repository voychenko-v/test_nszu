import psycopg2
from psycopg2 import sql

conn = psycopg2.connect('postgres://postgres:passworddb@localhost:5432/info_utilization')
cursor = conn.cursor()

creator_utilization = sql.SQL('''
CREATE TABLE IF NOT EXISTS utilization (
    id_utilization SERIAL PRIMARY KEY,
    date TIMESTAMP NOT NULL,
    cpu_utilization TEXT NOT NULL,
    ram_utilization TEXT NOT NULL
    );
    ''')

with conn:
    cursor.execute(creator_utilization)


INSERT_UTILIZATION = sql.SQL('''INSERT INTO utilization (date, cpu_utilization, ram_utilization) 
VALUES (%s, %s, %s) RETURNING id_utilization''')
