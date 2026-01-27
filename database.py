import psycopg2
from psycopg2.extras import RealDictCursor
import time
import os
from dotenv import load_dotenv
load_dotenv()
while True:
    try:
        conn=psycopg2.connect(dbname=os.getenv('POSTGRES_DB'), user=os.getenv('POSTGRES_USER') ,host=os.getenv('POSTGRES_HOST'),port=os.getenv('POSTGRES_PORT'),password=os.getenv("POSTGRES_PASSWORD"),cursor_factory=RealDictCursor)
        cursor=conn.cursor()
        print("Databse Connect Successful")
        break
    except:
        print("Sorry UNable to conncet to database")
        time.sleep(4)

