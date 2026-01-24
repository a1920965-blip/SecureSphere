import psycopg2
from psycopg2.extras import RealDictCursor
import time

try:
    conn=psycopg2.connect(dbname="fastapiDB",user="postgres" ,host="localhost",port="5432",password="Kewal@990",cursor_factory=RealDictCursor)
    cursor=conn.cursor()
    print("Databse Connect Successful")
except:
    print("Sorry UNable to conncet to database")
    time.sleep(4)
