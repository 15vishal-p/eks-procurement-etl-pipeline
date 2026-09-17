
import logging
import pandas as pd
import snowflake.connector

logger = logging.getLogger(__name__)

MAX_BIND_PARAMS = 16000


def _sql_type_for(dtype) -> str:
    if pd.api.types.is_integer_dtype(dtype):
        return "NUMBER"
    if pd.api.types.is_float_dtype(dtype):
        return "FLOAT"
    if pd.api.types.is_bool_dtype(dtype):
        return "BOOLEAN"
    if pd.api.types.is_datetime64_any_dtype(dtype):
        return "TIMESTAMP_NTZ"
    return "VARCHAR"


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
    table = table_name.upper()
    n_cols = len(df.columns)
    chunksize = max(1, (MAX_BIND_PARAMS // n_cols) - 10)

    conn = snowflake.connector.connect(
        account=account, user=user, password=password,
        warehouse=warehouse, database=database, schema=schema,
        login_timeout=30,
    )
    cur = conn.cursor()

    logger.info(f"Creating table '{table}' ({n_cols} columns)")
    col_defs = ", ".join(f"{col} {_sql_type_for(df[col].dtype)}" for col in df.columns)
    cur.execute(f"DROP TABLE IF EXISTS {table}")
    cur.execute(f"CREATE TABLE {table} ({col_defs})")

    logger.info(f"Loading {len(df):,} rows in batches of {chunksize} rows")
    col_list = ", ".join(df.columns)
    placeholders = ", ".join(["%s"] * n_cols)
    insert_sql = f"INSERT INTO {table} ({col_list}) VALUES ({placeholders})"

    total_rows = len(df)
    loaded = 0

    def _convert(v):
        if pd.isna(v):
            return None
        if isinstance(v, pd.Timestamp):
            return v.to_pydatetime()
        return v

    for start in range(0, total_rows, chunksize):
        batch = df.iloc[start:start + chunksize]
        rows = [
            tuple(_convert(v) for v in row)
            for row in batch.itertuples(index=False, name=None)
        ]
        cur.executemany(insert_sql, rows)
        loaded += len(rows)
        logger.info(f"  Loaded {loaded:,} / {total_rows:,} rows")

    conn.commit()
    cur.close()
    conn.close()
    logger.info("Load complete")