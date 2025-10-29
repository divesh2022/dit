import os
import urllib.parse
from typing import Generator

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session

# Configuration - prefer environment variables for production
DB_NAME = os.getenv("DB_NAME", "stud_man")
DB_SERVER = os.getenv("DB_SERVER", "localhost")
DB_DRIVER = os.getenv("DB_DRIVER", "ODBC Driver 18 for SQL Server")  # adjust if you have 17/13 etc.

# Build ODBC connection string for Windows (Trusted) authentication.
# If you need SQL authentication replace Trusted_Connection with UID/PWD.
odbc_str = (
    f"DRIVER={{{DB_DRIVER}}};"
    f"SERVER={DB_SERVER};"
    f"DATABASE={DB_NAME};"
    "Trusted_Connection=yes;"
    "Encrypt=no;"
)
odbc_conn = urllib.parse.quote_plus(odbc_str)
DATABASE_URL = f"mssql+pyodbc:///?odbc_connect={odbc_conn}"

# Create engine and session factory
engine = create_engine(
    DATABASE_URL,
    echo=False,
    pool_pre_ping=True,
)

SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False, future=True)


def get_db() -> Generator[Session, None, None]:
    """
    FastAPI dependency that yields a SQLAlchemy Session and ensures it's closed.
    Usage:
        db: Session = Depends(get_db)
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()