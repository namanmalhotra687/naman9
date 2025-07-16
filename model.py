from sqlalchemy import Column, Integer, String, Date, Boolean, create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
import os
from dotenv import load_dotenv

load_dotenv()  # Load env vars for local dev

DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    raise ValueError("DATABASE_URL is not set. Add it to .env or Render env.")

# If hosted on Render, force SSL
connect_args = {"sslmode": "require"} if "render" in DATABASE_URL else {}

engine = create_engine(DATABASE_URL, connect_args=connect_args)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)
Base = declarative_base()

# ✅ Define User model
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    password = Column(String)

# ✅ Define Item model (task)
class Item(Base):
    __tablename__ = "items"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    description = Column(String)
    status = Column(String, default="pending")
    deadline = Column(Date)
    created_by = Column(String)
    is_completed = Column(Boolean, default=False)
    is_generated = Column(Boolean, default=False)
    category = Column(String, default="General")
    recurrence = Column(String, default="none")  # daily/weekly/none

# ✅ Create tables if they don't exist
Base.metadata.create_all(bind=engine)
