import pandas as pd
from sqlalchemy import create_engine

# Connect to database
engine = create_engine("sqlite:///db/cta_analytics.db")

# Load data
df = pd.read_sql("SELECT * FROM ridership", engine)
df["service_date"] = pd.to_datetime(df["service_date"])

# Add useful columns
df["year"] = df["service_date"].dt.year
df["month"] = df["service_date"].dt.month
df["month_name"] = df["service_date"].dt.strftime("%B")

# ── 1. Overall stats ──────────────────────────────────────────
print("=" * 45)
print("OVERALL STATS")
print("=" * 45)
print(f"Date range:   {df['service_date'].min().date()} → {df['service_date'].max().date()}")
print(f"Total days:   {len(df)}")
print(f"Total rides:  {df['total_rides'].sum():,.0f}")
print(f"Average/day:  {df['total_rides'].mean():,.0f}")

# ── 2. Busiest days ever ──────────────────────────────────────
print("\n" + "=" * 45)
print("TOP 5 BUSIEST DAYS")
print("=" * 45)
top5 = df.nlargest(5, "total_rides")[["service_date", "day_type", "total_rides"]]
print(top5.to_string(index=False))

# ── 3. Yearly ridership ───────────────────────────────────────
print("\n" + "=" * 45)
print("YEARLY RIDERSHIP")
print("=" * 45)
yearly = df.groupby("year")["total_rides"].sum().reset_index()
yearly.columns = ["year", "total_rides"]
print(yearly.to_string(index=False))

# ── 4. Busiest months ─────────────────────────────────────────
print("\n" + "=" * 45)
print("AVERAGE RIDES BY MONTH")
print("=" * 45)
monthly = df.groupby("month_name")["total_rides"].mean().reset_index()
monthly.columns = ["month", "avg_rides"]
monthly = monthly.sort_values("avg_rides", ascending=False)
print(monthly.to_string(index=False))

# ── 5. COVID impact ───────────────────────────────────────────
print("\n" + "=" * 45)
print("COVID IMPACT (2019 vs 2020 vs 2021)")
print("=" * 45)
covid = df[df["year"].isin([2019, 2020, 2021])]
covid_yearly = covid.groupby("year")["total_rides"].sum()
print(covid_yearly.to_string())