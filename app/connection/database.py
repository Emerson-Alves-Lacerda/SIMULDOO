from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker

SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"  # ou PostgreSQL

#engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
engine = create_engine("sqlite:///simulados.db", echo=True)
SessionLocal = sessionmaker(bind=engine, autoflush=False)
Base = declarative_base()
