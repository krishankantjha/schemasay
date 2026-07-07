import time
import logging
from dataclasses import dataclass
from typing import Tuple, List, Dict, Optional
from sqlalchemy.orm import Session

from app.models.connection import DatabaseConnection, QueryAuditLog
from app.core.connections.connector import get_connection
from app.core.execution.query_executor import execute_query
from app.core.execution.sql_wrapper import wrap_query_with_limit
from app.core.security.sql_validator import validate_sql_structure
from app.core.audit.audit_service import log_audit_transaction

@dataclass
class AssistantQueryResult:
    success: bool
    error_or_sql: Optional[str]
    results: Optional[List[Dict]]
    execution_time_ms: float

    def __iter__(self):
        return iter((self.success, self.error_or_sql, self.results, self.execution_time_ms))

logger = logging.getLogger("schemasay.executor")

def execute_assistant_query(
    user_id: int,
    connection: DatabaseConnection,
    question: str,
    raw_sql: str,
    db: Session
) -> AssistantQueryResult:
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
        return AssistantQueryResult(
            success=False,
            error_or_sql=safety_error,
            results=None,
            execution_time_ms=0.0
        )

    # 2. Hard Paging Wrapper Construction using shared wrapper logic
    wrapped_sql = wrap_query_with_limit(raw_sql, connection.db_type)

    # 3. Connection and Execution Sandbox
    start_time = time.perf_counter()
    try:
        engine = get_connection(connection)
        success, exec_error, cols, results_list, execution_duration_ms = execute_query(
            engine=engine,
            sql_query=wrapped_sql,
            db_type=connection.db_type
        )
        
        if not success:
            log_audit_transaction(
                user_id=user_id,
                connection_id=connection.id,
                question=question,
                sql_query=raw_sql,
                duration_ms=execution_duration_ms,
                status="failed",
                error_message=exec_error,
                db=db
            )
            return AssistantQueryResult(
                success=False,
                error_or_sql=exec_error,
                results=None,
                execution_time_ms=execution_duration_ms
            )

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
        return AssistantQueryResult(
            success=True,
            error_or_sql=raw_sql,
            results=results_list,
            execution_time_ms=execution_duration_ms
        )
        
    except Exception as e:
        execution_duration_ms = (time.perf_counter() - start_time) * 1000.0
        error_msg = str(e)
        logger.error(f"SQL execution initialization failed: {error_msg}")
        
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
        return AssistantQueryResult(
            success=False,
            error_or_sql=error_msg,
            results=None,
            execution_time_ms=execution_duration_ms
        )
        
    finally:
        # Disposing cached pools is handled by pool.py cache ejects; we keep the close safe
        pass
