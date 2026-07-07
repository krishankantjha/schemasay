import logging
from typing import Optional
from sqlalchemy.orm import Session
from app.models.connection import QueryAuditLog

logger = logging.getLogger("schemasay.audit")

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
    Inserts a query execution record into the local platform audit log table
    using an isolated session transaction block to prevent session corruption.
    """
    from sqlalchemy.orm import sessionmaker
    SessionLocal = sessionmaker(bind=db.get_bind())
    isolated_db = SessionLocal()
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
        isolated_db.add(audit_log)
        isolated_db.commit()
    except Exception as e:
        isolated_db.rollback()
        logger.error(f"Failed to save QueryAuditLog transaction metrics inside isolated session: {str(e)}")
    finally:
        isolated_db.close()
