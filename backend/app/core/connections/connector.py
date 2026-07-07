import io
import os
import uuid
import re
import logging
from typing import Tuple
import pandas as pd
from sqlalchemy import create_engine, text
from sqlalchemy.engine import Engine, URL
from app.models.connection import DatabaseConnection
from app.core.connections.encryptor import decrypt_password
from app.core.connections.pool import engine_registry

logger = logging.getLogger("schemasay.connector")

# Setup base directory for local SQLite spreadsheet uploads
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
DATA_DIR = os.path.join(BASE_DIR, "data")

def sanitize_error_message(msg: str) -> str:
    """
    Regex-masks plaintext credentials and urls inside database driver exceptions.
    """
    # Matches db_type://user:password@host:port/db or similar
    pattern = r'[a-zA-Z0-9\+\-_]+://[^/]+@'
    return re.sub(pattern, '***://***@', msg)

def get_connection_url(db_type: str, host: str, port: int, username: str, password: str, database_name: str) -> URL:
    """
    Constructs the appropriate SQLAlchemy URL object based on database type.
    """
    db_type = db_type.lower()
    
    if db_type == "postgresql":
        return URL.create(
            drivername="postgresql",
            username=username,
            password=password,
            host=host,
            port=port,
            database=database_name
        )
    elif db_type == "mysql":
        return URL.create(
            drivername="mysql+pymysql",
            username=username,
            password=password,
            host=host,
            port=port,
            database=database_name
        )
    elif db_type == "mssql":
        return URL.create(
            drivername="mssql+pymssql",
            username=username,
            password=password,
            host=host,
            port=port,
            database=database_name
        )
    elif db_type in ["sqlite", "file_upload"]:
        # SQLite uses database_name as the absolute local file path
        return URL.create(
            drivername="sqlite",
            database=database_name
        )
    else:
        raise ValueError(f"Unsupported database connection type: {db_type}")

def get_connection_string(db_type: str, host: str, port: int, username: str, password: str, database_name: str) -> str:
    """
    Constructs the appropriate SQLAlchemy connection string based on database type (for backward compatibility).
    """
    return str(get_connection_url(db_type, host, port, username, password, database_name))

def get_connection(record: DatabaseConnection) -> Engine:
    """
    Retrieves the cached connection engine from the thread-safe global registry.
    """
    return engine_registry.get_engine(record)

def dispose_connection_engine(record: DatabaseConnection) -> None:
    """
    Safely disposes of and ejects the target connection pool from the cache registry.
    """
    engine_registry.remove_engine(record.id)

def test_connection(db_type: str, host: str, port: int, username: str, password: str, database_name: str) -> Tuple[bool, str]:
    """
    Attempts to establish a live connection to check credentials and network routing.
    Returns (True, "") on success, or (False, sanitized_error_message) on failure.
    """
    try:
        url = get_connection_url(
            db_type=db_type,
            host=host,
            port=port,
            username=username,
            password=password,
            database_name=database_name
        )
        
        # Configure driver-specific connection timeouts (10 seconds)
        connect_args = {}
        db_type_lower = db_type.lower()
        if db_type_lower == "postgresql":
            connect_args = {"connect_timeout": 10}
        elif db_type_lower == "mysql":
            connect_args = {"connect_timeout": 10}
        elif db_type_lower == "mssql":
            connect_args = {"login_timeout": 10}

        # Instantiate a temporary engine with connection timeouts
        if db_type_lower in ["sqlite", "file_upload"]:
            engine = create_engine(url, connect_args={"check_same_thread": False})
        else:
            engine = create_engine(url, connect_args=connect_args, pool_pre_ping=True)
            
        with engine.connect() as conn:
            # Execute lightweight probe query
            conn.execute(text("SELECT 1"))
            
        return True, ""
    except Exception as e:
        error_msg = sanitize_error_message(str(e))
        logger.error(f"Database connection test failed for {db_type}: {error_msg}")
        return False, error_msg

def process_file_upload(file_name: str, file_content: bytes) -> Tuple[str, str]:
    """
    Loads an uploaded CSV or Excel spreadsheet, writes it to a local SQLite database,
    and returns a tuple containing the (absolute_sqlite_path, table_name).
    """
    # Ensure local data storage directory exists
    os.makedirs(DATA_DIR, exist_ok=True)
    
    # Parse file format
    file_ext = os.path.splitext(file_name)[1].lower()
    if file_ext == ".csv":
        df = pd.read_csv(io.BytesIO(file_content))
    elif file_ext in [".xlsx", ".xls"]:
        df = pd.read_excel(io.BytesIO(file_content))
    else:
        raise ValueError("Unsupported file format. Only CSV and Excel files are supported.")
        
    # Cleanse table name: alphanumeric characters and underscores only
    clean_name = re.sub(r"[^a-zA-Z0-9_]", "_", os.path.splitext(file_name)[0])
    table_name = clean_name.strip("_").lower()
    if not table_name:
        table_name = "uploaded_table"
        
    # Generate unique SQLite database file path
    db_filename = f"{uuid.uuid4().hex}.db"
    db_path = os.path.abspath(os.path.join(DATA_DIR, db_filename))
    
    # Load DataFrame into SQLite
    engine = create_engine(f"sqlite:///{db_path}", connect_args={"check_same_thread": False})
    df.to_sql(table_name, con=engine, index=False, if_exists="replace")
    engine.dispose()
    
    return db_path, table_name
