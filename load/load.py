"""
Load stage: writes the cleaned DataFrame into Snowflake using write_pandas,
which bulk-loads via Snowflake's internal stage (PUT + COPY INTO) instead of
row-by-row INSERT statements. This avoids the bind-parameter limits that
break large to_sql() loads on wide tables (this dataset is 102 columns).
"""
import logging
import pandas as pd
import snowflake.connector
from snowflake.connector.pandas_tools import write_pandas

logger = logging.getLogger(__name__)


def load(
    df: pd.DataFrame,
    account: str,
    user: str,
    password: str,
    warehouse: str,
    database: str,
    schema: str,
    table_name: str,
) -> None:
    logger.info(f"Connecting to Snowflake to load {len(df):,} rows into table '{table_name}'")

    conn = snowflake.connector.connect(
        account=account,
        user=user,
        password=password,
        warehouse=warehouse,
        database=database,
        schema=schema,
        login_timeout=30,
    )

    try:
        success, nchunks, nrows, _ = write_pandas(
            conn,
            df,
            table_name.upper(),
            auto_create_table=True,
            overwrite=True,
        )
        logger.info(f"Load complete: success={success}, chunks={nchunks}, rows={nrows:,}")
    finally:
        conn.close()
