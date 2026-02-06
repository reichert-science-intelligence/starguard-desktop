"""
StarGuard AI - Database Connection Layer
Handles PostgreSQL and SQLite database connections for Shiny application
Uses same connection logic as Streamlit project
"""

import os
from pathlib import Path
from typing import Optional
import pandas as pd
from sqlalchemy import create_engine, text
from sqlalchemy.pool import QueuePool

# Database connection engine (singleton)
_engine = None
_db_type = None  # 'postgres' or 'sqlite'


def get_postgres_config() -> dict:
    """
    Get PostgreSQL configuration from environment variables.
    Uses same defaults as Streamlit project.
    
    Priority: Environment variables > defaults
    """
    port = os.getenv("DB_PORT", "5432")
    if isinstance(port, str):
        port = int(port)
    
    return {
        "host": os.getenv("DB_HOST", "localhost"),
        "database": os.getenv("DB_NAME", "hedis_portfolio"),
        "user": os.getenv("DB_USER", "hedis_api"),
        "password": os.getenv("DB_PASSWORD", "hedis_password"),
        "port": port,
    }


def get_sqlite_path() -> str:
    """Get path to SQLite database file (same location as Streamlit project)."""
    # Path to Streamlit project's SQLite database
    streamlit_db_path = Path(__file__).parent.parent.parent / "Artifacts" / "project" / "phase4_dashboard" / "data" / "hedis_portfolio.db"
    
    if streamlit_db_path.exists():
        return str(streamlit_db_path)
    
    # Fallback: local SQLite database
    local_db_path = Path(__file__).parent.parent / "data" / "hedis_portfolio.db"
    return str(local_db_path)


def get_db_type() -> str:
    """
    Detect which database to use.
    Priority: SQLite (if file exists) > PostgreSQL fallback
    Same logic as Streamlit project.
    """
    global _db_type
    
    if _db_type:
        return _db_type
    
    # FIRST: Check if SQLite database file exists
    sqlite_path = get_sqlite_path()
    if os.path.exists(sqlite_path):
        try:
            # Test SQLite connection
            import sqlite3
            test_conn = sqlite3.connect(sqlite_path)
            test_conn.close()
            _db_type = 'sqlite'
            print(f"[OK] Using SQLite database: {sqlite_path}")
            return 'sqlite'
        except Exception:
            pass
    
    # SECOND: Try PostgreSQL if SQLite is not available
    has_postgres_config = (
        os.getenv("DB_HOST") or 
        os.getenv("DB_NAME") or 
        os.getenv("DB_USER")
    )
    
    if has_postgres_config:
        try:
            config = get_postgres_config()
            import psycopg2
            test_conn = psycopg2.connect(**config)
            test_conn.close()
            _db_type = 'postgres'
            print(f"[OK] Using PostgreSQL database: {config['host']}:{config['port']}/{config['database']}")
            return 'postgres'
        except Exception:
            pass
    
    # Fallback to SQLite (will create file if it doesn't exist)
    _db_type = 'sqlite'
    print(f"[OK] Using SQLite database (fallback): {sqlite_path}")
    return 'sqlite'


def get_engine():
    """
    Get SQLAlchemy engine with connection pooling.
    Creates engine on first call, reuses on subsequent calls.
    Supports both PostgreSQL and SQLite.
    """
    global _engine
    
    if _engine is not None:
        return _engine
    
    db_type = get_db_type()
    
    try:
        if db_type == 'postgres':
            config = get_postgres_config()
            
            # Build PostgreSQL connection string
            connection_string = (
                f"postgresql://{config['user']}:{config['password']}"
                f"@{config['host']}:{config['port']}/{config['database']}"
            )
            
            # Create PostgreSQL engine with connection pooling
            _engine = create_engine(
                connection_string,
                poolclass=QueuePool,
                pool_size=5,
                max_overflow=10,
                pool_pre_ping=True,
                echo=False
            )
            
            # Test connection
            with _engine.connect() as conn:
                result = conn.execute(text("SELECT current_database()"))
                db_name = result.scalar()
                print(f"[OK] Connected to PostgreSQL database: {db_name}")
                print(f"     Host: {config['host']}:{config['port']}")
                print(f"     User: {config['user']}")
        
        else:
            # SQLite
            sqlite_path = get_sqlite_path()
            connection_string = f"sqlite:///{sqlite_path}"
            
            # Create SQLite engine (no pooling needed for SQLite)
            _engine = create_engine(
                connection_string,
                echo=False,
                connect_args={"check_same_thread": False}  # Allow multi-threaded access
            )
            
            # Test connection
            with _engine.connect() as conn:
                result = conn.execute(text("SELECT 1"))
                print(f"[OK] Connected to SQLite database: {sqlite_path}")
        
        return _engine
        
    except Exception as e:
        print(f"[ERROR] Database connection error: {e}")
        if db_type == 'postgres':
            print(f"        Check your DB_HOST, DB_NAME, DB_USER, DB_PASSWORD environment variables")
        else:
            print(f"        Check SQLite database file: {get_sqlite_path()}")
        raise


def query(sql: str, params: Optional[dict] = None) -> pd.DataFrame:
    """
    Execute a SQL query and return results as a pandas DataFrame.
    
    Args:
        sql: SQL query string
        params: Optional dictionary of parameters for parameterized queries
        
    Returns:
        DataFrame with query results
        
    Raises:
        Exception: If query execution fails
    """
    try:
        engine = get_engine()
        
        # Use pandas read_sql for better compatibility
        if params:
            df = pd.read_sql(sql, engine, params=params)
        else:
            df = pd.read_sql(sql, engine)
        
        return df
        
    except Exception as e:
        error_msg = f"Database query error: {e}"
        print(f"[ERROR] {error_msg}")
        raise Exception(error_msg)


def test_connection() -> bool:
    """
    Test database connection and return True if successful.
    Returns False if connection fails.
    """
    try:
        engine = get_engine()
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        return True
    except Exception:
        return False
