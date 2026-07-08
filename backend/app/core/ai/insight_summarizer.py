import re
import math
import pandas as pd
from typing import List, Dict, Any

# Detects common ID column name patterns (e.g. "id", "user_id") to exclude them from numeric statistics
ID_PATTERN = re.compile(r'^(id|id_|_id)$|(_id|id)$', re.IGNORECASE)

def summarize_query_dataset(columns: List[str], rows: List[Dict[str, Any]]) -> str:
    """
    Computes a robust statistical summary of the query results.
    Includes count, mean, min, max, median, standard deviation, null counts, distinct counts,
    and a representative 5-row random sample.
    """
    if not columns or not rows:
        return "No records returned."

    try:
        df = pd.DataFrame(rows, columns=columns)
    except Exception:
        return "Data format compilation failed."

    row_count = len(df)
    col_count = len(columns)

    summary_lines = [
        "Dataset overview:",
        f"- Total Rows: {row_count}",
        f"- Total Columns: {col_count} ({', '.join(columns)})"
    ]

    # Calculate statistics for non-ID numeric columns
    numeric_cols = []
    for col in columns:
        col_series = df[col]
        is_id = bool(ID_PATTERN.search(str(col).lower()))
        if pd.api.types.is_numeric_dtype(col_series) and not is_id:
            numeric_cols.append(col)

    if numeric_cols:
        summary_lines.append("\nNumerical Column Statistics:")
        for col in numeric_cols:
            # Map None and NaN cleanly for statistical computations
            col_series = df[col].apply(
                lambda x: None if (x is None or (isinstance(x, float) and math.isnan(x))) else x
            ).dropna()
            
            null_count = df[col].isna().sum()
            distinct_count = df[col].nunique()

            if not col_series.empty:
                try:
                    min_val = col_series.min()
                    max_val = col_series.max()
                    mean_val = col_series.mean()
                    median_val = col_series.median()
                    std_val = col_series.std()
                    std_str = f"{std_val:.2f}" if not pd.isna(std_val) else "N/A"

                    summary_lines.append(
                        f"  * {col}: Min={min_val:.2f}, Max={max_val:.2f}, Mean={mean_val:.2f}, "
                        f"Median={median_val:.2f}, StdDev={std_str}, Nulls={null_count}, Unique={distinct_count}"
                    )
                except Exception:
                    pass
            else:
                summary_lines.append(f"  * {col}: All values are NULL. Nulls={null_count}, Unique=0")

    # Add a representative sample of up to 5 rows using deterministic random sampling
    if len(df) > 5:
        sample_df = df.sample(n=5, random_state=42)
    else:
        sample_df = df.copy()

    def clean_val(x):
        if x is None:
            return "NULL"
        if isinstance(x, float) and math.isnan(x):
            return "NULL"
        return str(x)[:100]

    # Use .map() (pandas >= 2.1) or fall back to .applymap() for older pandas versions
    if hasattr(sample_df, "map"):
        sample_df = sample_df.map(clean_val)
    else:
        sample_df = sample_df.applymap(clean_val)

    summary_lines.append("\nRepresentative Data Sample (Up to 5 rows):")
    try:
        summary_lines.append(sample_df.to_markdown(index=False))
    except Exception:
        # Fallback to plain text formatting if to_markdown() is unavailable
        summary_lines.append("  " + " | ".join(columns))
        for _, row in sample_df.iterrows():
            summary_lines.append("  " + " | ".join(str(row[c]) for c in columns))

    return "\n".join(summary_lines)
