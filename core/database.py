
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import psycopg2
from psycopg2.extras import RealDictCursor
import time
from sqlalchemy import text
import os
from dotenv import load_dotenv
load_dotenv()

SQLALCHEMY_URL=f"postgresql+psycopg2://{os.getenv('POSTGRES_USER')}:{os.getenv('POSTGRES_PASSWORD')}@{os.getenv('POSTGRES_HOST')}:{os.getenv('POSTGRES_PORT')}/{os.getenv('POSTGRES_DB')}"
engine=create_engine(SQLALCHEMY_URL,echo=True)
SessionLocal=sessionmaker(autoflush=False,autocommit=False,bind=engine)

def get_db():
    db=SessionLocal()
    try:
        yield db
    finally:
        db.close()

# with engine.connect() as conn:
#     result = conn.execute(text("select 'hello world'"))
#     print(result.all())
# while True:
#     try:
#         conn=psycopg2.connect(dbname=os.getenv('POSTGRES_DB'), user=os.getenv('POSTGRES_USER') ,host=os.getenv('POSTGRES_HOST'),port=os.getenv('POSTGRES_PORT'),password=os.getenv("POSTGRES_PASSWORD"),cursor_factory=RealDictCursor)
#         cursor=conn.cursor()
#         print("Databse Connect Successful")
#         break
#     except:
#         print("Sorry UNable to conncet to database")
#         time.sleep(4)

