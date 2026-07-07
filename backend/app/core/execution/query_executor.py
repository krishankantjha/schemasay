import time
import logging
import re
from dataclasses import dataclass
from typing import Tuple, List, Dict, Any, Optional
import pandas as pd
from sqlalchemy import text
from sqlalchemy.engine import Engine

@dataclass
class QueryResult:
    success: bool
    error_message: Optional[str]
    columns: Optional[List[str]]
    rows: Optional[List[Dict[str, Any]]]
    execution_time_ms: float

    def __iter__(self):
        return iter((self.success, self.error_message, self.columns, self.rows, self.execution_time_ms))

logger = logging.getLogger("schemasay.query_executor")

def parse_database_exception(err: Exception, db_type: str) -> str:
    """
    Parses database exceptions to return clean, user-friendly error messages
    describing syntax errors, column/table absence, or timeouts.
    """
    err_msg = str(err).lower()
    db_type = db_type.lower()

    # 1. Timeout Check
    if any(x in err_msg for x in ["timeout", "canceling statement", "canceled", "timed out", "execution time exceeded", "interrupted", "query aborted"]):
        return "Query execution cancelled: The operation exceeded the 30-second time limit."

    # 2. SQLite Error Mapping
    if db_type in ["sqlite", "file_upload"]:
        if "no such table" in err_msg:
            parts = str(err).split("no such table:")
            tbl = parts[1].strip() if len(parts) > 1 else "unknown"
            return f"Database Error: Table '{tbl}' does not exist in the database."
        if "no such column" in err_msg:
            parts = str(err).split("no such column:")
            col = parts[1].strip() if len(parts) > 1 else "unknown"
            return f"Database Error: Column '{col}' does not exist on the target table."
        if "syntax error" in err_msg:
            return "Database Error: SQL syntax error. Please verify SELECT statement format."

    # 3. PostgreSQL Error Mapping
    elif db_type == "postgresql":
        if "relation" in err_msg and "does not exist" in err_msg:
            match = re.search(r'relation "([^"]+)" does not exist', str(err))
            tbl = match.group(1) if match else "unknown"
            return f"Database Error: Table '{tbl}' does not exist in the database."
        if "column" in err_msg and "does not exist" in err_msg:
            match = re.search(r'column "([^"]+)" does not exist', str(err))
            col = match.group(1) if match else "unknown"
            return f"Database Error: Column '{col}' does not exist on the target table."
        if "syntax error at or near" in err_msg:
            return "Database Error: SQL syntax error near query keywords."

    # 4. MySQL Error Mapping
    elif db_type == "mysql":
        if "table" in err_msg and "doesn't exist" in err_msg:
            match = re.search(r"table '([^']+)' doesn't exist", str(err))
            tbl = match.group(1).split(".")[-1] if match else "unknown"
            return f"Database Error: Table '{tbl}' does not exist in the database."
        if "unknown column" in err_msg:
            match = re.search(r"unknown column '([^']+)' in 'field list'", str(err))
            col = match.group(1) if match else "unknown"
            return f"Database Error: Column '{col}' does not exist on the target table."

    # 5. Fallback message (Sanitized for security)
    return "Database Execution Error: An unexpected database error occurred during query execution."

def execute_query(
    engine: Engine,
    sql_query: str,
    db_type: str
) -> QueryResult:
    """
    Executes a read-only SQL query against the database engine connection pool.
    Enforces a strict 30-second query timeout across dialects.
    """
    start_time = time.perf_counter()
    db_type_lower = db_type.lower()
    
    try:
        with engine.connect() as conn:
            # 1. Enforce 30-second timeouts per dialect (commit removed to avoid session reset)
            if db_type_lower == "postgresql":
                conn.execute(text("SET statement_timeout = 30000"))
            elif db_type_lower == "mysql":
                conn.execute(text("SET max_execution_time = 30000"))

            # Execute query and load results in chunks of 2000 rows to prevent driver buffer bloat
            chunks = pd.read_sql_query(sql_query, conn, chunksize=2000)
            df_list = []
            for chunk in chunks:
                df_list.append(chunk)
            
            if df_list:
                df = pd.concat(df_list, ignore_index=True)
            else:
                df = pd.DataFrame()
            
        execution_duration_ms = (time.perf_counter() - start_time) * 1000.0
        columns_list = list(df.columns)
        results_list = df.to_dict(orient="records")
        
        return QueryResult(
            success=True,
            error_message=None,
            columns=columns_list,
            rows=results_list,
            execution_time_ms=execution_duration_ms
        )

    except Exception as e:
        execution_duration_ms = (time.perf_counter() - start_time) * 1000.0
        parsed_error = parse_database_exception(e, db_type_lower)
        logger.error(f"Query execution failed: {parsed_error}")
        return QueryResult(
            success=False,
            error_message=parsed_error,
            columns=None,
            rows=None,
            execution_time_ms=execution_duration_ms
        )
