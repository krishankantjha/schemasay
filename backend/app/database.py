from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from app.config import settings

# Create the SQLAlchemy engine with explicit connection pool configuration
engine = create_engine(
    settings.DATABASE_URL,
    pool_size=5,
    max_overflow=10,
    pool_timeout=30
)

# Session factory used by FastAPI's get_db() dependency for per-request database sessions
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

# Base class that all SQLAlchemy ORM models inherit from
Base = declarative_base()

def get_db():
    """
    FastAPI dependency that yields a database session.
    Automatically rolls back transactions if exceptions are encountered.
    Handles session closing after the request completes.
    """
    db = SessionLocal()
    try:
        yield db
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()
