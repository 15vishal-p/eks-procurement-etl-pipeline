"""
Transform stage: basic cleaning only. No analysis, no aggregation, no stats.
Adjust the column names below to match your actual dataset once you have it.
"""
import logging
import pandas as pd

logger = logging.getLogger(__name__)


def transform(df: pd.DataFrame) -> pd.DataFrame:
    original_count = len(df)

    # 1. Standardize column names: lowercase, no spaces
    df.columns = [c.strip().lower().replace(" ", "_") for c in df.columns]

    # 2. Drop exact duplicate rows
    df = df.drop_duplicates()

    # 3. Strip whitespace from string/object columns
    str_cols = df.select_dtypes(include="object").columns
    for col in str_cols:
        df[col] = df[col].astype(str).str.strip()

    # 4. Drop rows that are entirely empty
    df = df.dropna(how="all")

    # 5. TODO: add dataset-specific rules once you know your real columns, e.g.:
    #    df["amount"] = pd.to_numeric(df["amount"], errors="coerce")
    #    df = df.dropna(subset=["amount", "transaction_date"])

    dropped = original_count - len(df)
    logger.info(f"Transform complete: {dropped:,} rows removed, {len(df):,} rows remain")
    return df
