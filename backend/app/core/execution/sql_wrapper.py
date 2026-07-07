def wrap_query_with_limit(sql: str, db_type: str, limit: int = 10000) -> str:
    """
    Wraps a raw SQL query with a hard limit constraint to prevent server memory exhaustion.
    Supports dialect-specific limits (e.g. TOP N for MSSQL).
    """
    sanitized_sql = sql.strip().rstrip(";")
    db_type_lower = db_type.lower()
    
    if db_type_lower == "mssql":
        return f"SELECT TOP {limit} * FROM ({sanitized_sql}) AS _schemasay_limit"
    else:
        return f"SELECT * FROM ({sanitized_sql}) AS _schemasay_limit LIMIT {limit}"
