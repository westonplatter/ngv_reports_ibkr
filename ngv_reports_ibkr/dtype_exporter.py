"""Utility to export pandas DataFrame dtypes for LLM analysis."""

import json
import re
from pathlib import Path
from typing import Any, Dict, List, Union

import pandas as pd
from loguru import logger


def export_dtypes_json(df: pd.DataFrame, filepath: Union[str, Path]) -> None:
    """Export DataFrame dtypes to JSON file.

    Args:
        df: pandas DataFrame to export dtypes from
        filepath: Path to save JSON file

    Example:
        >>> df = pd.read_csv('data.csv')
        >>> export_dtypes_json(df, 'data/dtypes.json')
    """
    dtype_info = {
        "columns": len(df.columns),
        "rows": len(df),
        "dtypes": {col: str(dtype) for col, dtype in df.dtypes.items()},
        "memory_usage_mb": df.memory_usage(deep=True).sum() / (1024 * 1024),
        "nullable_columns": df.columns[df.isnull().any()].tolist(),
    }

    filepath = Path(filepath)
    filepath.parent.mkdir(parents=True, exist_ok=True)

    with open(filepath, "w") as f:
        json.dump(dtype_info, f, indent=2)

    logger.info(f"Exported dtypes to {filepath}")


def export_dtypes_text(df: pd.DataFrame, filepath: Union[str, Path]) -> None:
    """Export DataFrame dtypes to human-readable text file.

    Args:
        df: pandas DataFrame to export dtypes from
        filepath: Path to save text file

    Example:
        >>> df = pd.read_csv('data.csv')
        >>> export_dtypes_text(df, 'data/dtypes.txt')
    """
    filepath = Path(filepath)
    filepath.parent.mkdir(parents=True, exist_ok=True)

    with open(filepath, "w") as f:
        f.write("=" * 80 + "\n")
        f.write("DATAFRAME SCHEMA INFORMATION\n")
        f.write("=" * 80 + "\n\n")

        f.write(f"Shape: {df.shape[0]:,} rows × {df.shape[1]} columns\n")
        f.write(f"Memory: {df.memory_usage(deep=True).sum() / (1024 * 1024):.2f} MB\n\n")

        f.write("-" * 80 + "\n")
        f.write("COLUMN DATA TYPES\n")
        f.write("-" * 80 + "\n")
        f.write(f"{'Column':<40} {'Type':<20} {'Nulls':<10}\n")
        f.write("-" * 80 + "\n")

        for col in df.columns:
            dtype = str(df[col].dtype)
            null_count = df[col].isnull().sum()
            null_pct = f"{null_count:,} ({null_count/len(df)*100:.1f}%)" if null_count > 0 else "0"
            f.write(f"{col:<40} {dtype:<20} {null_pct:<10}\n")

        f.write("\n" + "-" * 80 + "\n")
        f.write("SUMMARY BY DATA TYPE\n")
        f.write("-" * 80 + "\n")
        dtype_counts = df.dtypes.value_counts()
        for dtype, count in dtype_counts.items():
            f.write(f"{str(dtype):<20} {count:>3} columns\n")

    logger.info(f"Exported dtypes to {filepath}")


def export_dtypes_markdown(df: pd.DataFrame, filepath: Union[str, Path]) -> None:
    """Export DataFrame dtypes to markdown file for LLM analysis.

    Args:
        df: pandas DataFrame to export dtypes from
        filepath: Path to save markdown file

    Example:
        >>> df = pd.read_csv('data.csv')
        >>> export_dtypes_markdown(df, 'docs/schema.md')
    """
    filepath = Path(filepath)
    filepath.parent.mkdir(parents=True, exist_ok=True)

    with open(filepath, "w") as f:
        f.write("# DataFrame Schema\n\n")

        f.write("## Overview\n\n")
        f.write(f"- **Rows**: {df.shape[0]:,}\n")
        f.write(f"- **Columns**: {df.shape[1]}\n")
        f.write(f"- **Memory Usage**: {df.memory_usage(deep=True).sum() / (1024 * 1024):.2f} MB\n\n")

        f.write("## Column Details\n\n")
        f.write("| Column | Data Type | Null Count | Null % | Sample Values |\n")
        f.write("|--------|-----------|------------|--------|---------------|\n")

        for col in df.columns:
            dtype = str(df[col].dtype)
            null_count = df[col].isnull().sum()
            null_pct = f"{null_count/len(df)*100:.1f}%"

            # Get sample non-null values
            sample_values = df[col].dropna().head(3).tolist()
            sample_str = ", ".join([str(v)[:30] for v in sample_values])
            if len(sample_str) > 60:
                sample_str = sample_str[:57] + "..."

            f.write(f"| `{col}` | `{dtype}` | {null_count:,} | {null_pct} | {sample_str} |\n")

        f.write("\n## Data Type Summary\n\n")
        dtype_counts = df.dtypes.value_counts()
        for dtype, count in dtype_counts.items():
            f.write(f"- **{dtype}**: {count} columns\n")

        if df.isnull().any().any():
            f.write("\n## Columns with Missing Data\n\n")
            null_cols = df.columns[df.isnull().any()].tolist()
            for col in null_cols:
                null_count = df[col].isnull().sum()
                null_pct = null_count / len(df) * 100
                f.write(f"- `{col}`: {null_count:,} nulls ({null_pct:.1f}%)\n")

    logger.info(f"Exported dtypes to {filepath}")


def export_dtypes_all(
    df: pd.DataFrame,
    base_path: Union[str, Path],
    prefix: str = "schema",
    only_export: List[str] = ["json", "txt", "md"],
) -> None:
    """Export DataFrame dtypes to all formats (JSON, text, markdown).

    Args:
        df: pandas DataFrame to export dtypes from
        base_path: Directory to save files in
        prefix: Filename prefix for all exports

    Example:
        >>> df = pd.read_csv('data.csv')
        >>> export_dtypes_all(df, 'data', prefix='my_data')
        # Creates: data/my_data.json, data/my_data.txt, data/my_data.md
    """
    base_path = Path(base_path)
    base_path.mkdir(parents=True, exist_ok=True)

    if "json" in only_export:
        export_dtypes_json(df, base_path / f"{prefix}.json")
    if "txt" in only_export:
        export_dtypes_text(df, base_path / f"{prefix}.txt")
    if "md" in only_export:
        export_dtypes_markdown(df, base_path / f"{prefix}.md")

    logger.info(f"All dtype exports saved to {base_path}/")


def _anonymize_value(value: Any, column_name: str, counters: Dict[str, int]) -> Any:
    """Anonymize a single value based on column name and type.

    Args:
        value: Value to anonymize
        column_name: Name of the column (used to determine anonymization strategy)
        counters: Dictionary tracking counters for sequential ID generation

    Returns:
        Anonymized value preserving type and format
    """
    # Handle pandas NA/None values
    try:
        if pd.isna(value):
            return value
    except (ValueError, TypeError):
        # pd.isna() can raise ValueError for array-like objects
        pass

    # Handle numpy arrays, lists, and other array-like objects
    if hasattr(value, "__iter__") and not isinstance(value, (str, bytes)):
        # Return string representation for arrays/lists
        return str(value)

    value_str = str(value)
    col_lower = column_name.lower()

    # Account IDs: U1234567, U9999999
    if "account" in col_lower and "id" in col_lower:
        if not col_lower in counters:
            counters[col_lower] = 1234567
        anon_val = f"U{counters[col_lower]}"
        counters[col_lower] += 1
        return anon_val

    # Contract IDs: 123456789, 234567890, etc.
    if "conid" in col_lower or ("contract" in col_lower and "id" in col_lower):
        key = "contract_id"
        if key not in counters:
            counters[key] = 123456789
        anon_val = counters[key]
        counters[key] += 111111111
        return anon_val

    # Trade IDs: 1000000001, 1000000002, etc.
    if "trade" in col_lower and "id" in col_lower:
        key = "trade_id"
        if key not in counters:
            counters[key] = 1000000001
        anon_val = counters[key]
        counters[key] += 1
        return anon_val

    # Transaction IDs: 5000000001, 5000000002, etc.
    if "transaction" in col_lower and "id" in col_lower:
        key = "transaction_id"
        if key not in counters:
            counters[key] = 5000000001
        anon_val = counters[key]
        counters[key] += 1
        return anon_val

    # Order IDs: 9000000001, 9000000002, etc.
    if "order" in col_lower and "id" in col_lower:
        key = "order_id"
        if key not in counters:
            counters[key] = 9000000001
        anon_val = counters[key]
        counters[key] += 1
        return anon_val

    # Permission IDs: 8888888, 9999999, etc.
    if "perm" in col_lower and "id" in col_lower:
        key = "perm_id"
        if key not in counters:
            counters[key] = 8888888
        anon_val = counters[key]
        counters[key] += 1111111
        return anon_val

    # Execution IDs: 0000abcd.12345678.01.01
    if "exec" in col_lower and "id" in col_lower:
        key = "exec_id"
        if key not in counters:
            counters[key] = 0
        hex_parts = ["abcd", "efgh", "ijkl", "mnop", "qrst", "uvwx"]
        hex_part = hex_parts[counters[key] % len(hex_parts)]
        anon_val = f"0000{hex_part}.{12345678 + counters[key]}.01.01"
        counters[key] += 1
        return anon_val

    # Brokerage Order IDs: 00aabbcc.00ddeeff.11223344.000
    if "brokerage" in col_lower and "order" in col_lower:
        key = "brokerage_order_id"
        if key not in counters:
            counters[key] = 0
        anon_val = f"00aabbcc.00ddeeff.{11223344 + counters[key]:08d}.{counters[key]:03d}"
        counters[key] += 1
        return anon_val

    # External Execution IDs: ABC123XYZ000001
    if "ext" in col_lower and "exec" in col_lower:
        key = "ext_exec_id"
        if key not in counters:
            counters[key] = 1
        prefixes = ["ABC123XYZ", "DEF456UVW", "GHI789RST"]
        prefix = prefixes[counters[key] % len(prefixes)]
        anon_val = f"{prefix}{counters[key]:06d}"
        counters[key] += 1
        return anon_val

    # DateTime fields: Replace with generic dates/times
    if "date" in col_lower or "time" in col_lower:
        # Check if it looks like a datetime
        if re.search(r"\d{4}-\d{2}-\d{2}", value_str):
            key = "date_counter"
            if key not in counters:
                counters[key] = 15  # Start at Jan 15
            day = counters[key]
            counters[key] += 1
            if counters[key] > 31:
                counters[key] = 15

            # Replace date portion
            anon_val = re.sub(r"\d{4}-\d{2}-\d{2}", f"2025-01-{day:02d}", value_str)
            # Replace time portion with generic times
            time_key = "time_counter"
            if time_key not in counters:
                counters[time_key] = 0
            times = ["10:30:00", "11:45:00", "14:15:00", "15:30:00", "16:15:00"]
            time_str = times[counters[time_key] % len(times)]
            anon_val = re.sub(r"\d{2}:\d{2}:\d{2}", time_str, anon_val)
            counters[time_key] += 1
            return anon_val

    # Client IDs, Trader IDs: Sequential numbers
    if ("client" in col_lower or "trader" in col_lower) and "id" in col_lower:
        key = f"{col_lower}_id"
        if key not in counters:
            counters[key] = 1
        anon_val = counters[key]
        counters[key] += 1
        return anon_val

    # Default: return original value (for symbols, exchanges, prices, etc.)
    return value


def export_dtypes_markdown_anonymized(
    df: pd.DataFrame,
    base_path: Union[str, Path],
    prefix: str = "schema",
    sample_size: int = 3,
) -> None:
    """Export DataFrame dtypes to markdown with ANONYMIZED sample data.

    This function creates a schema documentation file that is safe to share publicly.
    It anonymizes all personal and sensitive identifiers while preserving:
    - Data types and structure
    - Market data (symbols, exchanges, prices)
    - Null percentages and patterns

    Anonymization follows the guidelines in prompt-ibkr-sample-data.md:
    - Account IDs → U1234567, U9999999
    - Contract IDs → 123456789, 234567890
    - Trade IDs → 1000000001, 1000000002
    - Transaction IDs → 5000000001, 5000000002
    - Order IDs → 9000000001, 9000000002
    - Execution IDs → 0000abcd.12345678.01.01
    - Dates → 2025-01-15, 2025-01-16
    - Times → 10:30:00, 11:45:00
    - Keeps real: symbols, exchanges, prices, quantities

    Args:
        df: pandas DataFrame to export dtypes from
        base_path: Directory to save file in
        prefix: Filename prefix (default: "schema")
        sample_size: Number of sample values to show (default: 3)

    Example:
        >>> df = pd.read_csv('ibkr_trades.csv')
        >>> export_dtypes_markdown_anonymized(df, 'docs', prefix='ibkr_trades')
        # Creates: docs/ibkr_trades.md - Safe to share publicly

        >>> # Export to schemas directory
        >>> export_dtypes_markdown_anonymized(df, 'ngv_reports_ibkr/schemas', prefix='flex_query')
        # Creates: ngv_reports_ibkr/schemas/flex_query.md
    """
    base_path = Path(base_path)
    base_path.mkdir(parents=True, exist_ok=True)

    filepath = base_path / f"{prefix}.md"

    # Counter dictionary for generating sequential anonymous IDs
    counters: Dict[str, int] = {}

    with open(filepath, "w") as f:
        f.write("# DataFrame Schema (Anonymized)\n\n")
        f.write("> ⚠️ **Privacy Notice**: All sample values have been anonymized according to ")
        f.write("[IBKR Sample Data Anonymization Guidelines](../prompt-ibkr-sample-data.md). ")
        f.write("Account IDs, transaction IDs, dates, and other personal identifiers have been ")
        f.write("replaced with generic values. Market data (symbols, exchanges, prices) remains realistic.\n\n")

        f.write("## Overview\n\n")
        f.write(f"- **Rows**: {df.shape[0]:,}\n")
        f.write(f"- **Columns**: {df.shape[1]}\n")
        f.write(f"- **Memory Usage**: {df.memory_usage(deep=True).sum() / (1024 * 1024):.2f} MB\n\n")

        f.write("## Column Details\n\n")
        f.write("| Column | Data Type | Null Count | Null % | Sample Values (Anonymized) |\n")
        f.write("|--------|-----------|------------|--------|---------------------------|\n")

        for col in df.columns:
            dtype = str(df[col].dtype)
            null_count = df[col].isnull().sum()
            null_pct = f"{null_count/len(df)*100:.1f}%"

            # Get sample non-null values and anonymize them
            sample_values = df[col].dropna().head(sample_size).tolist()
            anonymized_samples = [_anonymize_value(v, col, counters) for v in sample_values]
            sample_str = ", ".join([str(v)[:30] for v in anonymized_samples])
            if len(sample_str) > 60:
                sample_str = sample_str[:57] + "..."

            f.write(f"| `{col}` | `{dtype}` | {null_count:,} | {null_pct} | {sample_str} |\n")

        f.write("\n## Data Type Summary\n\n")
        dtype_counts = df.dtypes.value_counts()
        for dtype, count in dtype_counts.items():
            f.write(f"- **{dtype}**: {count} columns\n")

        if df.isnull().any().any():
            f.write("\n## Columns with Missing Data\n\n")
            null_cols = df.columns[df.isnull().any()].tolist()
            for col in null_cols:
                null_count = df[col].isnull().sum()
                null_pct = null_count / len(df) * 100
                f.write(f"- `{col}`: {null_count:,} nulls ({null_pct:.1f}%)\n")

        f.write("\n## Anonymization Notes\n\n")
        f.write("This schema documentation uses anonymized sample data:\n\n")
        f.write("- **Account/Transaction IDs**: Replaced with sequential generic IDs\n")
        f.write("- **Dates/Times**: Replaced with generic January 2025 dates and round times\n")
        f.write("- **Personal Identifiers**: All replaced with non-identifying values\n")
        f.write("- **Market Data**: Preserved real symbols, exchanges, and realistic prices\n")
        f.write("- **Data Structure**: Exact types, null percentages, and formats maintained\n\n")
        f.write("**This documentation is safe to share publicly and with LLMs for schema analysis.**\n")

    logger.info(f"Exported anonymized dtypes to {filepath}")
    logger.info("✓ All personal data anonymized - safe for public sharing")
