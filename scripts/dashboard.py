import pandas as pd
import snowflake.connector
from dotenv import load_dotenv
import os
from dash import Dash, dcc, html
import plotly.express as px

load_dotenv()

# ── Load Data from Snowflake ──────────────────────────────────
conn = snowflake.connector.connect(
    user=os.getenv("SNOWFLAKE_USER"),
    password=os.getenv("SNOWFLAKE_PASSWORD"),
    account=os.getenv("SNOWFLAKE_ACCOUNT"),
    warehouse=os.getenv("SNOWFLAKE_WAREHOUSE"),
    database=os.getenv("SNOWFLAKE_DATABASE"),
    schema=os.getenv("SNOWFLAKE_SCHEMA")
)

cursor = conn.cursor()
cursor.execute("""
    SELECT * FROM CTA_DB.CTA_SCHEMA.RIDERSHIP 
    WHERE YEAR(SERVICE_DATE) <= 2025
""")
df = cursor.fetch_pandas_all()
conn.close()

# Fix column names to lowercase
df.columns = df.columns.str.lower()
df["service_date"] = pd.to_datetime(df["service_date"])
df["year"] = df["service_date"].dt.year
df["month_name"] = df["service_date"].dt.strftime("%B")

# ── Prepare Charts ────────────────────────────────────────────
# 1. Yearly ridership
yearly = df.groupby("year")["total_rides"].sum().reset_index()
fig_yearly = px.line(
    yearly, x="year", y="total_rides",
    title="CTA Yearly Ridership (2001–2025)",
    markers=True,
    labels={"year": "Year", "total_rides": "Total Rides"}
)

# 2. COVID impact
covid = yearly[yearly["year"].between(2017, 2025)]
fig_covid = px.bar(
    covid, x="year", y="total_rides",
    title="COVID Impact & Recovery (2017–2025)",
    labels={"year": "Year", "total_rides": "Total Rides"},
    color="total_rides",
    color_continuous_scale="RdYlGn"
)

# 3. Bus vs Rail
bus_rail = df.groupby("year")[["bus", "rail_boardings"]].sum().reset_index()
fig_bus_rail = px.line(
    bus_rail, x="year", y=["bus", "rail_boardings"],
    title="Bus vs Rail Ridership Over Time",
    markers=True,
    labels={"year": "Year", "value": "Total Rides", "variable": "Mode"}
)

# 4. Monthly average
month_order = ["January","February","March","April","May","June",
               "July","August","September","October","November","December"]
monthly = df.groupby("month_name")["total_rides"].mean().reindex(month_order).reset_index()
fig_monthly = px.bar(
    monthly, x="month_name", y="total_rides",
    title="Average Daily Rides by Month",
    labels={"month_name": "Month", "total_rides": "Average Rides"},
    color="total_rides",
    color_continuous_scale="Blues"
)

# ── Build App ─────────────────────────────────────────────────
app = Dash(__name__)

app.layout = html.Div([

    # Header
    html.Div([
        html.H1("CTA Performance Analytics Platform",
                style={"color": "white", "margin": "0", "fontSize": "24px"}),
        html.P("25 Years of Chicago Transit Authority Ridership Data (2001–2025)",
               style={"color": "#ccc", "margin": "5px 0 0 0"})
    ], style={
        "backgroundColor": "#003087",
        "padding": "20px 30px",
        "marginBottom": "20px"
    }),

    # KPI Cards
    html.Div([
        html.Div([
            html.H3("11.1 Billion", style={"margin": "0", "color": "#003087"}),
            html.P("Total Rides (2001–2025)", style={"margin": "5px 0 0 0", "color": "#666"})
        ], style={"backgroundColor": "white", "padding": "20px", "borderRadius": "8px",
                  "boxShadow": "0 2px 4px rgba(0,0,0,0.1)", "flex": "1", "textAlign": "center"}),

        html.Div([
            html.H3("1.2 Million", style={"margin": "0", "color": "#003087"}),
            html.P("Average Rides Per Day", style={"margin": "5px 0 0 0", "color": "#666"})
        ], style={"backgroundColor": "white", "padding": "20px", "borderRadius": "8px",
                  "boxShadow": "0 2px 4px rgba(0,0,0,0.1)", "flex": "1", "textAlign": "center"}),

        html.Div([
            html.H3("2,049,519", style={"margin": "0", "color": "#003087"}),
            html.P("Busiest Day (Jul 3, 2008)", style={"margin": "5px 0 0 0", "color": "#666"})
        ], style={"backgroundColor": "white", "padding": "20px", "borderRadius": "8px",
                  "boxShadow": "0 2px 4px rgba(0,0,0,0.1)", "flex": "1", "textAlign": "center"}),

        html.Div([
            html.H3("-57%", style={"margin": "0", "color": "#cc0000"}),
            html.P("COVID Ridership Drop (2020)", style={"margin": "5px 0 0 0", "color": "#666"})
        ], style={"backgroundColor": "white", "padding": "20px", "borderRadius": "8px",
                  "boxShadow": "0 2px 4px rgba(0,0,0,0.1)", "flex": "1", "textAlign": "center"}),

    ], style={"display": "flex", "gap": "15px", "padding": "0 30px", "marginBottom": "20px"}),

    # Charts Row 1
    html.Div([
        html.Div([dcc.Graph(figure=fig_yearly)],
                 style={"flex": "1", "backgroundColor": "white", "borderRadius": "8px",
                        "boxShadow": "0 2px 4px rgba(0,0,0,0.1)"}),
        html.Div([dcc.Graph(figure=fig_covid)],
                 style={"flex": "1", "backgroundColor": "white", "borderRadius": "8px",
                        "boxShadow": "0 2px 4px rgba(0,0,0,0.1)"}),
    ], style={"display": "flex", "gap": "15px", "padding": "0 30px", "marginBottom": "15px"}),

    # Charts Row 2
    html.Div([
        html.Div([dcc.Graph(figure=fig_bus_rail)],
                 style={"flex": "1", "backgroundColor": "white", "borderRadius": "8px",
                        "boxShadow": "0 2px 4px rgba(0,0,0,0.1)"}),
        html.Div([dcc.Graph(figure=fig_monthly)],
                 style={"flex": "1", "backgroundColor": "white", "borderRadius": "8px",
                        "boxShadow": "0 2px 4px rgba(0,0,0,0.1)"}),
    ], style={"display": "flex", "gap": "15px", "padding": "0 30px", "marginBottom": "30px"}),

    # Footer
    html.Div([
        html.P("⚡ Powered by Snowflake | 📊 Data: Chicago Data Portal | 🚀 Deployed on Render",
            style={"textAlign": "center", "color": "#999",
                    "fontSize": "12px", "padding": "15px",
                    "borderTop": "1px solid #ddd",
                    "marginTop": "10px"})
    ], style={"backgroundColor": "#f0f2f5"})

], style={"backgroundColor": "#f0f2f5", "minHeight": "100vh", "fontFamily": "Arial, sans-serif"})


server = app.server

if __name__ == "__main__":
    app.run(debug=True)