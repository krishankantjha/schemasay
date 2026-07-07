import time
import logging
from typing import Tuple, List, Dict, Optional
import pandas as pd
from sqlalchemy import text
from sqlalchemy.orm import Session
import sqlglot
from sqlglot import exp

from app.models.connection import DatabaseConnection, QueryAuditLog
from app.core.connections.connector import get_connection

logger = logging.getLogger("schemasay.executor")

def validate_sql_structure(raw_sql: str) -> Tuple[bool, str]:
    """
    Parses the SQL input into an Abstract Syntax Tree (AST) using sqlglot,
    enforcing that the input is a single, read-only SELECT statement.
    """
    try:
        # Parse query string using sqlglot
        expressions = sqlglot.parse(raw_sql)
    except Exception as e:
        return False, f"SQL Syntax Error: Unable to parse query structure: {str(e)}"

    if not expressions:
        return False, "Access Denied: Empty query statement."

    if len(expressions) > 1:
        return False, "Access Denied: Stacked query statements containing semicolons are blocked for security."

    expr = expressions[0]

    # Explicitly block mutating operation nodes, unions, and procedural calls anywhere in the AST
    blocked_nodes = (
        exp.Insert, exp.Update, exp.Delete, exp.Drop, exp.Alter, exp.Create,
        exp.Merge, exp.Command, exp.TruncateTable, exp.Union
    )

    for node in expr.walk():
        if isinstance(node, blocked_nodes):
            node_name = node.__class__.__name__
            if node_name == "Union":
                return False, "Access Denied: UNION operations are blocked for security."
            if node_name == "Command":
                return False, "Access Denied: Stored procedure or utility query commands are blocked for security."
            return False, f"Access Denied: Unsafe mutating operation ({node_name.replace('Table', '')}) is blocked. The database is read-only."

    # The root node must be SELECT (or PRAGMA for SQLite schema checks)
    if not isinstance(expr, (exp.Select, exp.Pragma)):
        return False, "Access Denied: Only read-only SELECT statements are allowed."

    return True, ""

def execute_assistant_query(
    user_id: int,
    connection: DatabaseConnection,
    question: str,
    raw_sql: str,
    db: Session
) -> Tuple[bool, Optional[str], Optional[List[Dict]], float]:
    """
    Validates a query statement using AST-based checks, runs the query wrapped inside
    a hard limit query wrapper, measures performance, and writes log metrics.
    """
    # 1. AST Security Gate
    is_safe, safety_error = validate_sql_structure(raw_sql)
    if not is_safe:
        log_audit_transaction(
            user_id=user_id,
            connection_id=connection.id,
            question=question,
            sql_query=raw_sql,
            duration_ms=0.0,
            status="failed",
            error_message=safety_error,
            db=db
        )
        return False, safety_error, None, 0.0

    # 2. Hard Paging Wrapper Construction
    sanitized_sql = raw_sql.strip().rstrip(";")
    db_type_lower = connection.db_type.lower()
    
    if db_type_lower == "mssql":
        # MSSQL syntax uses SELECT TOP N
        wrapped_sql = f"SELECT TOP 10000 * FROM ({sanitized_sql}) AS _schemasay_limit"
    else:
        # Standard ANSI syntax
        wrapped_sql = f"SELECT * FROM ({sanitized_sql}) AS _schemasay_limit LIMIT 10000"

    # 3. Connection and Execution Sandbox
    engine = None
    start_time = time.perf_counter()
    try:
        engine = get_connection(connection)
        with engine.connect() as conn:
            # Enforce 5-second statement timeout for PostgreSQL databases
            if db_type_lower == "postgresql":
                conn.execute(text("SET statement_timeout = 5000"))
                conn.commit()
                
            # Execute query and parse results into a pandas Dataframe
            df = pd.read_sql_query(wrapped_sql, conn)
            
        execution_duration_ms = (time.perf_counter() - start_time) * 1000.0
        results_list = df.to_dict(orient="records")
        
        # Log successful query execution
        log_audit_transaction(
            user_id=user_id,
            connection_id=connection.id,
            question=question,
            sql_query=raw_sql,
            duration_ms=execution_duration_ms,
            status="success",
            error_message=None,
            db=db
        )
        return True, raw_sql, results_list, execution_duration_ms
        
    except Exception as e:
        execution_duration_ms = (time.perf_counter() - start_time) * 1000.0
        error_msg = str(e)
        
        # Provide user-friendly description for database connection or timeout cancellations
        if "statement_timeout" in error_msg or "canceling statement" in error_msg:
            error_msg = "Query execution cancelled: Query execution exceeded the 5-second timeout limit."
            
        logger.error(f"SQL execution failed on connection {connection.name}: {error_msg}")
        
        # Log failed query execution
        log_audit_transaction(
            user_id=user_id,
            connection_id=connection.id,
            question=question,
            sql_query=raw_sql,
            duration_ms=execution_duration_ms,
            status="failed",
            error_message=error_msg,
            db=db
        )
        return False, error_msg, None, execution_duration_ms
        
    finally:
        # Disposing cached pools is handled by pool.py cache ejects; we keep the close safe
        pass

def log_audit_transaction(
    user_id: int,
    connection_id: int,
    question: str,
    sql_query: str,
    duration_ms: float,
    status: str,
    error_message: Optional[str],
    db: Session
) -> None:
    """
    Inserts a query execution record into the local platform audit log table.
    """
    try:
        audit_log = QueryAuditLog(
            user_id=user_id,
            connection_id=connection_id,
            question=question,
            sql_query=sql_query,
            execution_duration_ms=int(duration_ms),
            status=status,
            error_message=error_message
        )
        db.add(audit_log)
        db.commit()
    except Exception as e:
        db.rollback()
        logger.error(f"Failed to save QueryAuditLog transaction metrics: {str(e)}")
