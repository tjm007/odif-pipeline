from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent

DATA_DIR = PROJECT_ROOT / "data"
SQL_DIR = PROJECT_ROOT / "sql"

DB_PATH = DATA_DIR / "odif_demo.db"

SCHEMA_FILE = SQL_DIR / "schema.sql"
QUERIES_FILE = SQL_DIR / "queries.sql"

RAW_DATA_DIR = DATA_DIR / "raw"
PROCESSED_DATA_DIR = DATA_DIR / "processed"
SAMPLE_DATA_DIR = DATA_DIR / "sample"

SALES_DATA_FILE = RAW_DATA_DIR / "sales_data.csv"