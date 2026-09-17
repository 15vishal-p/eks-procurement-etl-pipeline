"""
Standalone Snowflake connection test - isolates connectivity issues
from the full ETL pipeline. Run this BEFORE running main.py.
"""
import time
import snowflake.connector
from config.settings import (
    SNOWFLAKE_ACCOUNT, SNOWFLAKE_USER, SNOWFLAKE_PASSWORD,
    SNOWFLAKE_WAREHOUSE, SNOWFLAKE_DATABASE, SNOWFLAKE_SCHEMA,
)

print("Attempting connection...")
print(f"Account: {SNOWFLAKE_ACCOUNT}")
print(f"User: {SNOWFLAKE_USER}")
start = time.time()

try:
    conn = snowflake.connector.connect(
        account=SNOWFLAKE_ACCOUNT,
        user=SNOWFLAKE_USER,
        password=SNOWFLAKE_PASSWORD,
        warehouse=SNOWFLAKE_WAREHOUSE,
        database=SNOWFLAKE_DATABASE,
        schema=SNOWFLAKE_SCHEMA,
        login_timeout=30,  # fail fast instead of hanging for 20 minutes
    )
    elapsed = time.time() - start
    print(f"Connected successfully in {elapsed:.1f} seconds")

    cur = conn.cursor()
    cur.execute("SELECT CURRENT_VERSION()")
    print("Snowflake version:", cur.fetchone()[0])
    cur.close()
    conn.close()

except Exception as e:
    elapsed = time.time() - start
    print(f"Failed after {elapsed:.1f} seconds")
    print(f"Error: {e}")