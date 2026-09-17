"""
Extract stage: reads the raw dataset (CSV or Excel) into a pandas DataFrame.
No analysis, no transformation here - just get the data in and confirm it's readable.
"""
import logging
import pandas as pd
from pathlib import Path

logger = logging.getLogger(__name__)


def extract(file_path: str) -> pd.DataFrame:
    """
    Reads a CSV or XLSX file into a DataFrame.
    Raises FileNotFoundError early with a clear message if the path is wrong.
    """
    path = Path(file_path)
    if not path.exists():
        raise FileNotFoundError(f"Source file not found at: {file_path}")

    logger.info(f"Extracting data from {file_path}")

    if path.suffix.lower() == ".csv":
        df = pd.read_csv(path)
    elif path.suffix.lower() in (".xlsx", ".xls"):
        df = pd.read_excel(path)
    else:
        raise ValueError(f"Unsupported file type: {path.suffix}")

    logger.info(f"Extracted {len(df):,} rows, {len(df.columns)} columns")
    return df
