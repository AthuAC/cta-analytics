import pandas as pd
import snowflake.connector
from snowflake.connector.pandas_tools import write_pandas
from dotenv import load_dotenv
import os

# ── Load environment variables ────────────────────────────────
load_dotenv()

# ── Snowflake Connection ──────────────────────────────────────
conn = snowflake.connector.connect(
    user=os.getenv("SNOWFLAKE_USER"),
    password=os.getenv("SNOWFLAKE_TOKEN"),
    account=os.getenv("SNOWFLAKE_ACCOUNT"),
    warehouse=os.getenv("SNOWFLAKE_WAREHOUSE"),
    database=os.getenv("SNOWFLAKE_DATABASE"),
    schema=os.getenv("SNOWFLAKE_SCHEMA")
)


print("✅ Connected to Snowflake!")

# ── Load Data ─────────────────────────────────────────────────
print("Loading data from CSV...")
df = pd.read_csv("raw/cta_ridership_raw.csv")
df.columns = df.columns.str.upper()
df = df.dropna()
df = df.sort_values("SERVICE_DATE")
df = df.reset_index(drop=True)

# Convert date to string so Snowflake handles it cleanly
df["SERVICE_DATE"] = pd.to_datetime(df["SERVICE_DATE"]).dt.strftime("%Y-%m-%d")

print(f"Loaded {len(df)} rows")

# ── Write to Snowflake ────────────────────────────────────────
print("Writing to Snowflake...")
success, nchunks, nrows, _ = write_pandas(
    conn=conn,
    df=df,
    table_name="RIDERSHIP",
    database="CTA_DB",
    schema="CTA_SCHEMA"
)

if success:
    print(f"✅ Successfully loaded {nrows} rows into Snowflake!")
else:
    print("❌ Something went wrong")

conn.close()
print("Connection closed.")