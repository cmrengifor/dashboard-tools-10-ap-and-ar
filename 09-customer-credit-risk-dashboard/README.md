# Dashboard 09 — Customer Credit Risk Dashboard

## Overview

A Power BI dashboard that provides a comprehensive view of customer credit risk exposure, utilization, and portfolio health across segments and regions.

**File:** `customer_credit_risk_dashboard.pbix`
**Data source:** `data/credit_risk_data.csv` (600 rows, 21 columns)

---

## Visuals (11 total)

### Row 1 — KPI Cards
| # | Title | Measure | Position (X,Y) | Size (W×H) |
|---|-------|---------|----------------|------------|
| 1 | Total Credit Exposure | `SUM(credit_limit)` | 20, 20 | 260×120 |
| 2 | Credit Utilization % | `credit_used / credit_limit` | 300, 20 | 260×120 |
| 3 | Avg Risk Score | `AVERAGE(risk_score)` | 580, 20 | 260×120 |
| 4 | High Risk Customers | `DISTINCTCOUNT` where risk_category IN {High, Critical} | 860, 20 | 260×120 |

### Row 2 — Column Charts
| # | Title | X-axis | Y-axis | Position (X,Y) | Size (W×H) |
|---|-------|--------|--------|----------------|------------|
| 5 | Outstanding Balance by Risk Category | risk_category | outstanding_balance | 20, 160 | 560×210 |
| 6 | Credit Utilization by Segment | segment | credit_utilization | 600, 160 | 560×210 |

### Row 3 — Detail Visuals
| # | Type | Fields | Position (X,Y) | Size (W×H) |
|---|------|--------|----------------|------------|
| 7 | Donut Chart | Values: outstanding_balance / Legend: risk_category | 20, 390 | 280×200 |
| 8 | Table | customer_name, outstanding_balance, credit_limit, risk_category, risk_score, segment | 320, 390 | 580×200 |

### Row 4 — Slicers
| # | Field | Position (X,Y) | Size (W×H) |
|---|-------|----------------|------------|
| 9 | segment | 20, 610 | 370×80 |
| 10 | risk_category | 410, 610 | 370×80 |
| 11 | region | 800, 610 | 360×80 |

---

## DAX Measures

```dax
Total Credit Exposure = SUM(credit_risk_data[credit_limit])

Credit Utilization % = DIVIDE(
    SUM(credit_risk_data[credit_used]),
    SUM(credit_risk_data[credit_limit]),
    0
)

Avg Risk Score = AVERAGE(credit_risk_data[risk_score])

High Risk Customers = CALCULATE(
    DISTINCTCOUNT(credit_risk_data[customer_id]),
    credit_risk_data[risk_category] IN {"High", "Critical"}
)
```

---

## Data Dictionary

| Column | Type | Description |
|--------|------|-------------|
| record_id | int | Unique record identifier |
| customer_id | string | Customer identifier |
| customer_name | string | Customer display name |
| segment | string | Customer segment (Enterprise, SMB, Startup, Government, Retail) |
| region | string | Geographic region (Central, East, North, South, West) |
| credit_limit | float | Total approved credit limit |
| credit_used | float | Amount of credit currently used |
| credit_utilization | float | credit_used / credit_limit ratio |
| outstanding_balance | float | Current outstanding balance |
| overdue_balance | float | Balance past due date |
| days_overdue | int | Number of days past due |
| risk_score | float | Computed risk score (0–1000) |
| risk_category | string | Risk tier (Low, Medium, High, Critical) |
| payment_history | string | Payment behavior descriptor |
| on_time_payments | int | Count of on-time payments |
| late_payments | int | Count of late payments |
| write_off_amount | float | Amount written off |
| period | string | Period label |
| year | int | Year |
| month | int | Month number |
| quarter | string | Quarter label |

---

## How to Use

1. Open `customer_credit_risk_dashboard.pbix` in Power BI Desktop.
2. Use the **segment**, **risk_category**, and **region** slicers (bottom row) to filter the entire dashboard.
3. KPI cards update dynamically to reflect filtered totals.
4. The donut chart shows the outstanding balance distribution across risk tiers.
5. The table provides customer-level detail for drill-down analysis.
