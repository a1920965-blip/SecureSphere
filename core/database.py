
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import psycopg2
from psycopg2.extras import RealDictCursor
import time
from sqlalchemy import text
import os


SQLALCHEMY_URL=f"postgresql+psycopg2://{os.getenv('POSTGRES_USER')}:{os.getenv('POSTGRES_PASSWORD')}@{os.getenv('POSTGRES_HOST')}:{os.getenv('POSTGRES_PORT')}/{os.getenv('POSTGRES_DB')}"
engine=create_engine(SQLALCHEMY_URL,echo=True)
SessionLocal=sessionmaker(autoflush=False,autocommit=False,bind=engine)

def get_db():
    db=SessionLocal()
    try:
        yield db
    finally:
        db.close()