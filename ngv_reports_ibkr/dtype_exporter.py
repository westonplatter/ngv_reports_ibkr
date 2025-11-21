"""Utility to export pandas DataFrame dtypes for LLM analysis."""

import json
from pathlib import Path
from typing import List, Union

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
