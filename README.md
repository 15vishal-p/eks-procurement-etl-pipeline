# EKS Procurement ETL Pipeline

A Python ETL pipeline that extracts, cleans, and loads 500,000+ Slovak public procurement records into Snowflake, with a Power BI dashboard connected on top.

## Overview

- **Source**: EKS (Slovak electronic procurement system) - real government procurement data, ~514,000 rows, 102 columns
- **Data quality handled**: European decimal-comma number formats, non-standard date formats, mixed-type columns, Slovak-to-English column translation
- **Destination**: Snowflake (cloud data warehouse)
- **Visualization**: Power BI dashboard connected live to Snowflake

## Dashboard

![Power BI Dashboard](docs/dashboard.png)

Power BI dashboard connected directly to the Snowflake `TRANSACTIONS` table - total contract count, top buyers by spend, and contract value trends over time.

## Setup

1. Open this folder in VS Code.
2. Create and activate a virtual environment:
   ```
   python -m venv venv
   venv\Scripts\activate        # Windows
   source venv/bin/activate     # Mac/Linux
   ```
3. Install dependencies:
   ```
   pip install -r requirements.txt
   ```
4. Copy `.env.example` to `.env` and fill in your real Snowflake credentials.
5. Put your dataset CSV in `data/raw/` and update `SOURCE_FILE_PATH` in `.env` to match its filename.

## Run it

```
python main.py
```

Runs extract -> transform -> load in sequence, with progress logged at each stage.

## Structure

```
extract/    - reads the raw CSV into a DataFrame
transform/  - cleans decimal-comma numbers, parses dates, translates Slovak columns to English
load/       - creates the Snowflake table and loads data in parameter-safe batches
config/     - loads Snowflake credentials and paths from .env
main.py     - runs the full pipeline
docs/       - dashboard screenshot
```

## Notes

- Loading uses manually batched INSERT statements rather than Snowflake's `write_pandas()`, due to a compatibility issue between its internal pandas-version check and newer Python releases.
- Batch size is calculated dynamically to stay under Snowflake's per-statement bind-parameter limit.