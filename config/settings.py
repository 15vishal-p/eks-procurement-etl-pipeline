"""
Central config loader. Reads from .env so credentials never live in code.
"""
import os
from urllib.parse import quote_plus
from dotenv import load_dotenv

load_dotenv()

SNOWFLAKE_ACCOUNT = os.getenv("SNOWFLAKE_ACCOUNT", "")
SNOWFLAKE_USER = os.getenv("SNOWFLAKE_USER", "")
SNOWFLAKE_PASSWORD = os.getenv("SNOWFLAKE_PASSWORD", "")
SNOWFLAKE_WAREHOUSE = os.getenv("SNOWFLAKE_WAREHOUSE", "COMPUTE_WH")
SNOWFLAKE_DATABASE = os.getenv("SNOWFLAKE_DATABASE", "ETL_PROJECT")
SNOWFLAKE_SCHEMA = os.getenv("SNOWFLAKE_SCHEMA", "PUBLIC")

SOURCE_FILE_PATH = os.getenv("SOURCE_FILE_PATH", "data/raw/dataset.csv")
TARGET_TABLE = os.getenv("TARGET_TABLE", "transactions")

def get_db_url() -> str:
    """Builds the SQLAlchemy connection string for Snowflake via the snowflake-sqlalchemy dialect.
    User/password are URL-encoded so special characters (e.g. @, /, :) in the password
    don't get misread as part of the URL structure."""
    user = quote_plus(SNOWFLAKE_USER)
    password = quote_plus(SNOWFLAKE_PASSWORD)
    return (
        f"snowflake://{user}:{password}"
        f"@{SNOWFLAKE_ACCOUNT}/{SNOWFLAKE_DATABASE}/{SNOWFLAKE_SCHEMA}"
        f"?warehouse={SNOWFLAKE_WAREHOUSE}"
    )
