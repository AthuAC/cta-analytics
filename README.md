# CTA Performance Analytics Platform

## Project Overview
A data pipeline and analytics project built to analyze 25 years of Chicago Transit Authority (CTA) ridership data. The pipeline ingests, cleans, stores, and analyzes daily ridership trends from 2001 to 2026.

---

## Live Demo & Repository

- 🌐 **Live Dashboard:** [https://cta-analytics.onrender.com](https://cta-analytics.onrender.com)
- 💻 **GitHub Repository:** [https://github.com/AthuAC/cta-analytics](https://github.com/AthuAC/cta-analytics)

> Note: The dashboard is hosted on Render's free tier and may take up to 50 seconds to load if it has been inactive.

---

## Data Source
- **Platform:** Chicago Data Portal (data.cityofchicago.org)
- **Dataset:** CTA Daily Boardings
- **Dataset ID:** `6iiy-9s97`
- **Access:** Public REST API, no authentication required
- **Format:** CSV
- **Coverage:** January 1, 2001 → February 28, 2026
- **Total Records:** 9,190 rows

---

## Dataset Columns
| Column | Description |
|--------|-------------|
| `service_date` | Date of service |
| `day_type` | W = Weekday, A = Saturday, U = Sunday/Holiday |
| `bus` | Total bus boardings |
| `rail_boardings` | Total train boardings |
| `total_rides` | Combined bus + rail boardings |

---

## Key Findings

### Overall Stats
- **Total rides (25 years):** 11,110,964,887 (11.1 billion)
- **Average rides per day:** 1,209,028 (1.2 million)
- **Peak year:** 2012 — 545,577,922 rides
- **Busiest single day:** July 3, 2008 — 2,049,519 rides
- **Busiest month:** October | **Slowest month:** December

### COVID Impact
| Year | Total Rides | Change |
|------|-------------|--------|
| 2019 (pre-COVID) | 455,743,540 | baseline |
| 2020 (COVID hit) | 197,499,791 | -57% |
| 2021 (still low) | 195,980,570 | -57% |
| 2022 | 243,538,810 | recovering |
| 2023 | 279,146,498 | recovering |
| 2024 | 309,197,034 | recovering |
| 2025 | 338,041,690 | recovering |

### Notable Observations
- November 4, 2008 (Obama election night in Chicago) is the 2nd busiest day ever
- Ridership declined steadily from 2012–2019 even before COVID
- Post-COVID recovery has been consistent but hasn't reached pre-COVID levels yet
- 2026 is partial year data (January–February only)

---

## Tech Stack
- **Language:** Python 3.14.4
- **Libraries:** pandas, numpy, matplotlib, seaborn, plotly, dash, sqlalchemy, requests, openpyxl
- **Database:** SQLite (via SQLAlchemy)
- **Environment:** Virtual environment (.venv)
- **Tools:** Homebrew, VS Code

---

