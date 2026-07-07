from typing import Tuple
import sqlglot
from sqlglot import exp

def validate_sql_structure(raw_sql: str) -> Tuple[bool, str]:
    """
    Parses the SQL input into an Abstract Syntax Tree (AST) using sqlglot,
    enforcing that the input is a single, read-only SELECT statement.
    Timing attacks, CTE write bypasses, and schema modifications are blocked.
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
        exp.Merge, exp.Command, exp.TruncateTable, exp.Union, exp.Into
    )

    for node in expr.walk():
        # Check standard and anonymous function names for timing attacks
        if isinstance(node, exp.Anonymous) and node.name.lower() in ["pg_sleep", "sleep", "waitfor"]:
            return False, f"Access Denied: Timing functions ({node.name}) are blocked for security."

        if isinstance(node, blocked_nodes):
            node_name = node.__class__.__name__
            if node_name == "Union":
                return False, "Access Denied: UNION operations are blocked for security."
            if node_name == "Command":
                if "waitfor" in str(node).lower():
                    return False, "Access Denied: Timing delay commands are blocked for security."
                return False, "Access Denied: Stored procedure or utility query commands are blocked for security."
            if node_name == "Into":
                return False, "Access Denied: Unsafe mutating operation (Into) is blocked. The database is read-only."
            return False, f"Access Denied: Unsafe mutating operation ({node_name.replace('Table', '')}) is blocked. The database is read-only."

    # The root node must be SELECT (or PRAGMA for SQLite schema checks)
    if not isinstance(expr, (exp.Select, exp.Pragma)):
        return False, "Access Denied: Only read-only SELECT statements are allowed."

    return True, ""
