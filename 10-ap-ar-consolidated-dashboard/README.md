# Dashboard 10 — AP/AR Consolidated Dashboard

## Overview

A Power BI dashboard that provides a unified executive view of both Accounts Payable (AP) and Accounts Receivable (AR) outstanding balances, collection efficiency, aging distribution, and net working capital position.

**File:** `ap_ar_consolidated_dashboard.pbix`
**Data source:** `data/consolidated_data.csv` (700 rows, 17 columns)

---

## Visuals (11 total)

### Row 1 — KPI Cards
| # | Title | Measure | Position (X,Y) | Size (W×H) |
|---|-------|---------|----------------|------------|
| 1 | Total AR Outstanding | `CALCULATE(SUM(outstanding_balance), transaction_type="AR")` | 20, 20 | 260×120 |
| 2 | Total AP Outstanding | `CALCULATE(SUM(outstanding_balance), transaction_type="AP")` | 300, 20 | 260×120 |
| 3 | Net Working Capital | `Total AR Outstanding - Total AP Outstanding` | 580, 20 | 260×120 |
| 4 | Collection Efficiency % | `SUM(paid_amount) / SUM(invoice_amount)` | 860, 20 | 260×120 |

### Row 2 — Column Charts
| # | Title | X-axis | Y-axis | Legend | Position (X,Y) | Size (W×H) |
|---|-------|--------|--------|--------|----------------|------------|
| 5 | Outstanding by Period | period (hierarchy) | outstanding_balance | transaction_type | 20, 160 | 560×210 |
| 6 | Outstanding by Aging Bucket | aging_bucket | outstanding_balance | — | 600, 160 | 560×210 |

### Row 3 — Detail Visuals
| # | Type | Fields | Position (X,Y) | Size (W×H) |
|---|------|--------|----------------|------------|
| 7 | Donut Chart | Values: outstanding_balance / Legend: transaction_type | 20, 390 | 280×200 |
| 8 | Table | entity_name, transaction_type, outstanding_balance, overdue_amount, aging_bucket, status | 320, 390 | 580×200 |

### Row 4 — Slicers
| # | Field | Position (X,Y) | Size (W×H) |
|---|-------|----------------|------------|
| 9 | transaction_type | 20, 610 | 370×80 |
| 10 | region | 410, 610 | 370×80 |
| 11 | year | 800, 610 | 360×80 |

---

## DAX Measures

```dax
Total AR Outstanding = CALCULATE(
    SUM(consolidated_data[outstanding_balance]),
    consolidated_data[transaction_type] = "AR"
)

Total AP Outstanding = CALCULATE(
    SUM(consolidated_data[outstanding_balance]),
    consolidated_data[transaction_type] = "AP"
)

Net Working Capital = [Total AR Outstanding] - [Total AP Outstanding]

Collection Efficiency % = DIVIDE(
    SUM(consolidated_data[paid_amount]),
    SUM(consolidated_data[invoice_amount]),
    0
)
```

---

## Data Dictionary

| Column | Type | Description |
|--------|------|-------------|
| record_id | int | Unique record identifier |
| period | string | Month label (e.g., "2025-01") |
| year | int | Year |
| month | int | Month number |
| quarter | string | Quarter label (Q1–Q4) |
| transaction_type | string | "AR" (receivable) or "AP" (payable) |
| entity_name | string | Customer name (AR) or vendor name (AP) |
| entity_segment | string | Segment/category of entity |
| region | string | Geographic region (North, South, East, West, Central) |
| invoice_amount | float | Original invoice amount |
| paid_amount | float | Amount paid to date |
| outstanding_balance | float | Remaining unpaid balance |
| overdue_amount | float | Amount past due date |
| days_overdue | int | Days past due |
| aging_bucket | string | Aging tier (Current, 1-30, 31-60, 61-90, 90+) |
| status | string | Payment status (Current, Partial, Overdue, Paid) |
| payment_terms | string | Payment terms (Net 30, Net 45, Net 60, Net 90, 2/10 Net 30) |

---

## How to Use

1. Open `ap_ar_consolidated_dashboard.pbix` in Power BI Desktop.
2. Use the **transaction_type** slicer to filter to AR only, AP only, or both.
3. Use the **region** slicer to focus on a specific geographic area.
4. Use the **year** range slicer to narrow the time window (2025–2026).
5. KPI cards update dynamically to show filtered AR outstanding, AP outstanding, net working capital, and collection efficiency.
6. The donut chart shows the AP vs. AR balance split visually.
7. The table provides entity-level drill-down with aging and status detail.
