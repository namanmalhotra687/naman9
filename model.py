import os
from sqlalchemy import Column, Integer, String, Date, create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

# ✅ Use PostgreSQL from Render OR fallback to SQLite locally
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./test.db")

# ✅ Only add connect_args if using SQLite
connect_args = {"check_same_thread": False} if DATABASE_URL.startswith("sqlite") else {}

# ✅ Create SQLAlchemy engine
engine = create_engine(DATABASE_URL, connect_args=connect_args)

# ✅ Create session factory
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)

# ✅ Declare base class
Base = declarative_base()

# ✅ Define Item model
class Item(Base):
    __tablename__ = "items"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(String)
    username = Column(String)
    status = Column(String)
    deadline = Column(String)
