"""
Entry point: runs extract -> transform -> load in sequence.
Run with: python main.py
"""
import logging
import sys

from config.settings import (
    SOURCE_FILE_PATH, TARGET_TABLE,
    SNOWFLAKE_ACCOUNT, SNOWFLAKE_USER, SNOWFLAKE_PASSWORD,
    SNOWFLAKE_WAREHOUSE, SNOWFLAKE_DATABASE, SNOWFLAKE_SCHEMA,
)
from extract.extract import extract
from transform.transform import transform
from load.load import load

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)
logger = logging.getLogger(__name__)


def run_pipeline():
    try:
        df = extract(SOURCE_FILE_PATH)
        df = transform(df)
        load(
            df,
            SNOWFLAKE_ACCOUNT, SNOWFLAKE_USER, SNOWFLAKE_PASSWORD,
            SNOWFLAKE_WAREHOUSE, SNOWFLAKE_DATABASE, SNOWFLAKE_SCHEMA,
            TARGET_TABLE,
        )
        logger.info("Pipeline finished successfully.")
    except Exception as e:
        logger.error("Pipeline failed:", exc_info=True)
        sys.exit(1)


if __name__ == "__main__":
    run_pipeline()