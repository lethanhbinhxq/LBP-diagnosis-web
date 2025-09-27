# create_db.py
from sqlalchemy import text
from core.db_connection import admin_engine, engine, Base
from models import *
import os
from dotenv import load_dotenv

load_dotenv()
DB_NAME = os.getenv("DB_NAME")

def init_db():
    """Create database if not exists, then create all tables."""
    create_database()
    create_tables()

def create_database():
    with admin_engine.connect() as conn:
        result = conn.execute(
            text(f"SELECT 1 FROM pg_database WHERE datname='{DB_NAME}'")
        )
        exists = result.scalar() is not None
        if not exists:
            conn.execute(text(f'CREATE DATABASE "{DB_NAME}"'))
            print(f"Database '{DB_NAME}' created!")
        else:
            print(f"Database '{DB_NAME}' already exists.")

def create_tables():
    Base.metadata.create_all(bind=engine)
    print("Tables created (if not existing).")
