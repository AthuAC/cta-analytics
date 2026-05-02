import pandas as pd
from sqlalchemy import create_engine
import os

# Paths
DATA_PATH = "data/cta_ridership.csv"
DB_PATH = "db/cta_analytics.db"

# Load CSV
print("Loading data...")
df = pd.read_csv(DATA_PATH, parse_dates=["service_date"])

# Basic cleanup
df.columns = df.columns.str.strip().str.lower()
df = df.dropna()
df = df.sort_values("service_date")

print(f"Loaded {len(df)} rows")
print(df.head())

# Save to SQLite
print("\nSaving to database...")
engine = create_engine(f"sqlite:///{DB_PATH}")
df.to_sql("ridership", engine, if_exists="replace", index=False)
print(f"Done! Database saved to {DB_PATH}")