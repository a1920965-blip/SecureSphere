from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import psycopg2
from psycopg2.extras import RealDictCursor
import os
from dotenv import load_dotenv
load_dotenv()

SQLALCHEMY_URL=f"postgresql+psycopg2://{os.getenv('POSTGRES_USER')}:{os.getenv('POSTGRES_PASSWORD')}@{os.getenv('POSTGRES_HOST')}:{os.getenv('POSTGRES_PORT')}/{os.getenv('POSTGRES_DB')}"
print("DB URL =", SQLALCHEMY_URL)
engine=create_engine(SQLALCHEMY_URL,echo=True)
SessionLocal=sessionmaker(autoflush=False,autocommit=False,bind=engine)

def get_db():
    db=SessionLocal()
    try:
        yield db
    finally:
        db.close()