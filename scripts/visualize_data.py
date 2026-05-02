import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sqlalchemy import create_engine
import os

# Setup
engine = create_engine("sqlite:///db/cta_analytics.db")
df = pd.read_sql("SELECT * FROM ridership", engine)
df["service_date"] = pd.to_datetime(df["service_date"])
df["year"] = df["service_date"].dt.year
df["month"] = df["service_date"].dt.month
df["month_name"] = df["service_date"].dt.strftime("%B")

# Output folder
os.makedirs("processed/charts", exist_ok=True)

# Style
sns.set_theme(style="darkgrid")
plt.rcParams["figure.figsize"] = (12, 5)

# ── 1. Yearly Ridership Trend ─────────────────────────────────
yearly = df.groupby("year")["total_rides"].sum().reset_index()

plt.figure()
sns.lineplot(data=yearly, x="year", y="total_rides", marker="o", color="steelblue")
plt.title("CTA Yearly Ridership (2001–2026)", fontsize=14)
plt.xlabel("Year")
plt.ylabel("Total Rides")
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig("processed/charts/yearly_ridership.png")
plt.close()
print("✅ Saved: yearly_ridership.png")

# ── 2. COVID Impact ───────────────────────────────────────────
covid = yearly[yearly["year"].between(2017, 2025)]

plt.figure()
bars = sns.barplot(data=covid, x="year", y="total_rides", palette="coolwarm")
plt.axvline(x=2.5, color="red", linestyle="--", label="COVID-19 (2020)")
plt.title("CTA Ridership: COVID Impact & Recovery (2017–2025)", fontsize=14)
plt.xlabel("Year")
plt.ylabel("Total Rides")
plt.legend()
plt.tight_layout()
plt.savefig("processed/charts/covid_impact.png")
plt.close()
print("✅ Saved: covid_impact.png")

# ── 3. Average Rides by Month ─────────────────────────────────
month_order = ["January","February","March","April","May","June",
               "July","August","September","October","November","December"]
monthly = df.groupby("month_name")["total_rides"].mean().reindex(month_order).reset_index()

plt.figure()
sns.barplot(data=monthly, x="month_name", y="total_rides", palette="viridis")
plt.title("Average Daily Rides by Month", fontsize=14)
plt.xlabel("Month")
plt.ylabel("Average Rides")
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig("processed/charts/monthly_avg.png")
plt.close()
print("✅ Saved: monthly_avg.png")

# ── 4. Bus vs Rail Over Time ──────────────────────────────────
bus_rail = df.groupby("year")[["bus", "rail_boardings"]].sum().reset_index()

plt.figure()
plt.plot(bus_rail["year"], bus_rail["bus"], marker="o", label="Bus", color="orange")
plt.plot(bus_rail["year"], bus_rail["rail_boardings"], marker="o", label="Rail", color="steelblue")
plt.title("Bus vs Rail Ridership Over Time", fontsize=14)
plt.xlabel("Year")
plt.ylabel("Total Rides")
plt.legend()
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig("processed/charts/bus_vs_rail.png")
plt.close()
print("✅ Saved: bus_vs_rail.png")

print("\n🎉 All charts saved to processed/charts/")
