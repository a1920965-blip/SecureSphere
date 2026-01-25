import psycopg2
from psycopg2.extras import RealDictCursor
import time

while True:
    try:
        conn=psycopg2.connect(dbname="postgres",user="postgres" ,host="db",port="5432",password="akash123",cursor_factory=RealDictCursor)
        cursor=conn.cursor()
        print("Databse Connect Successful")
        break
    except:
        print("Sorry UNable to conncet to database")
        time.sleep(4)
