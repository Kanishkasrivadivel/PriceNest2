import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# Load environment variables from .env file
load_dotenv()

DATABASE_URL = os.getenv("psql 'postgresql://neondb_owner:npg_kUQWi6mv2LhK@ep-floral-surf-aiuvuoqd-pooler.c-4.us-east-1.aws.neon.tech/neondb?sslmode=require&channel_binding=require'")
engine = create_engine(
    DATABASE_URL,
    echo=False
)

SessionLocal = sessionmaker(
    bind=engine,
    autoflush=False,
    autocommit=False
)

Base = declarative_base()
