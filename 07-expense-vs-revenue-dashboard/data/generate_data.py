"""
Dashboard 07 — Expense vs. Revenue Dashboard
Generates expense_revenue_data.csv with ~620 rows covering
Jan 2025 – Dec 2026, mixing actual (Jan 2025–May 2026) and
budget/forecast entries.
"""
import csv
import random
from datetime import date, timedelta
from collections import Counter

random.seed(7)

# ── Constants ────────────────────────────────────────────────────────────────
START_DATE   = date(2025, 1, 1)
END_DATE     = date(2026, 12, 31)
ACTUAL_CUTOFF = date(2026, 6, 1)   # Jun 2026+ is Budget/Forecast

DEPARTMENTS = ["Finance", "Operations", "HR", "Sales", "IT", "Marketing", "R&D"]
REGIONS     = ["North", "South", "East", "West", "Central"]

# Revenue categories and typical monthly ranges
REVENUE_CATS = {
    "Product Sales":    (160_000, 350_000),
    "Service Revenue":  (80_000,  170_000),
    "Subscription Revenue": (55_000, 115_000),
    "Consulting Revenue": (30_000, 90_000),
    "Other Revenue":    (8_000,   30_000),
}

# Expense categories and typical monthly ranges
EXPENSE_CATS = {
    "Cost of Goods Sold": (80_000, 180_000),
    "Salaries & Benefits": (100_000, 200_000),
    "Marketing & Advertising": (15_000, 55_000),
    "Operations & Facilities": (20_000, 60_000),
    "Technology & IT":  (10_000, 40_000),
    "Research & Development": (15_000, 50_000),
    "General & Administrative": (10_000, 35_000),
    "Depreciation":     (8_000,  18_000),
}

# Department assignment per category
REV_DEPT = {
    "Product Sales": "Sales",
    "Service Revenue": "Sales",
    "Subscription Revenue": "Sales",
    "Consulting Revenue": "Sales",
    "Other Revenue": "Finance",
}
EXP_DEPT = {
    "Cost of Goods Sold": "Operations",
    "Salaries & Benefits": "HR",
    "Marketing & Advertising": "Marketing",
    "Operations & Facilities": "Operations",
    "Technology & IT": "IT",
    "Research & Development": "R&D",
    "General & Administrative": "Finance",
    "Depreciation": "Finance",
}


def period_label(y, m):
    return date(y, m, 1).strftime("%b %Y")


def quarter(m):
    return f"Q{(m - 1) // 3 + 1}"


def rand_day(y, m):
    first = date(y, m, 1)
    last  = date(y, m + 1, 1) - timedelta(days=1) if m < 12 else date(y, 12, 31)
    return first + timedelta(days=random.randint(0, (last - first).days))


rows = []
tx_id = 1

months = [(y, m) for y in range(2025, 2027) for m in range(1, 13)
          if date(y, m, 1) <= END_DATE]

for yr, mo in months:
    is_forecast = date(yr, mo, 1) >= ACTUAL_CUTOFF
    period      = period_label(yr, mo)
    qtr         = quarter(mo)
    dtype       = "Forecast" if is_forecast else "Actual"

    # ── REVENUE ──────────────────────────────────────────────────────────────
    for cat, (lo, hi) in REVENUE_CATS.items():
        # slight seasonality: Q4 higher for sales
        seasonal = 1.15 if (mo in (10, 11, 12) and "Sales" in cat) else 1.0
        budget = round(random.uniform(lo, hi) * seasonal, 2)

        if is_forecast:
            actual  = 0.0
            forecast = round(budget * random.uniform(0.93, 1.07), 2)
            variance = 0.0
            var_pct  = 0.0
            favorable = ""
        else:
            actual   = round(budget * random.uniform(0.88, 1.12), 2)
            forecast = actual
            variance = round(actual - budget, 2)
            var_pct  = round(variance / budget * 100, 1) if budget else 0.0
            favorable = "Yes" if variance >= 0 else "No"

        rows.append({
            "transaction_id":  f"ER-{tx_id:04d}",
            "date":            rand_day(yr, mo).isoformat(),
            "period":          period,
            "year":            yr,
            "month":           mo,
            "quarter":         qtr,
            "type":            "Revenue",
            "category":        cat,
            "department":      REV_DEPT[cat],
            "region":          random.choice(REGIONS),
            "budget_amount":   round(budget, 2),
            "actual_amount":   actual,
            "forecast_amount": forecast,
            "variance":        variance,
            "variance_pct":    var_pct,
            "data_type":       dtype,
            "is_favorable":    favorable,
        })
        tx_id += 1

    # ── EXPENSES ─────────────────────────────────────────────────────────────
    for cat, (lo, hi) in EXPENSE_CATS.items():
        budget = round(random.uniform(lo, hi), 2)

        if is_forecast:
            actual   = 0.0
            forecast = round(budget * random.uniform(0.94, 1.06), 2)
            variance = 0.0
            var_pct  = 0.0
            favorable = ""
        else:
            actual   = round(budget * random.uniform(0.90, 1.10), 2)
            forecast = actual
            variance = round(actual - budget, 2)
            var_pct  = round(variance / budget * 100, 1) if budget else 0.0
            # For expenses: favorable = under budget (variance <= 0)
            favorable = "Yes" if variance <= 0 else "No"

        rows.append({
            "transaction_id":  f"ER-{tx_id:04d}",
            "date":            rand_day(yr, mo).isoformat(),
            "period":          period,
            "year":            yr,
            "month":           mo,
            "quarter":         qtr,
            "type":            "Expense",
            "category":        cat,
            "department":      EXP_DEPT[cat],
            "region":          random.choice(REGIONS),
            "budget_amount":   round(budget, 2),
            "actual_amount":   actual,
            "forecast_amount": forecast,
            "variance":        variance,
            "variance_pct":    var_pct,
            "data_type":       dtype,
            "is_favorable":    favorable,
        })
        tx_id += 1

# Sort by date
rows.sort(key=lambda r: r["date"])

# Write CSV
out = (
    "C:/Users/User/Project Program/dashboard-tools-10-ap-and-ar/"
    "07-expense-vs-revenue-dashboard/data/expense_revenue_data.csv"
)
cols = list(rows[0].keys())
with open(out, "w", newline="", encoding="utf-8") as f:
    w = csv.DictWriter(f, fieldnames=cols)
    w.writeheader()
    w.writerows(rows)

# Summary
print(f"Total rows: {len(rows)}")
print("type:", dict(Counter(r["type"] for r in rows)))
print("data_type:", dict(Counter(r["data_type"] for r in rows)))
print("category counts:", dict(Counter(r["category"] for r in rows)))

revenue  = sum(r["forecast_amount"] for r in rows if r["type"] == "Revenue")
expenses = sum(r["forecast_amount"] for r in rows if r["type"] == "Expense")
net      = revenue - expenses
margin   = net / revenue * 100 if revenue else 0

print(f"\nTotal Revenue  (forecast): ${revenue:>14,.2f}")
print(f"Total Expenses (forecast): ${expenses:>14,.2f}")
print(f"Net Profit:                ${net:>14,.2f}")
print(f"Profit Margin:             {margin:.1f}%")

act_rev  = sum(r["actual_amount"] for r in rows if r["type"] == "Revenue"  and r["data_type"] == "Actual")
act_exp  = sum(r["actual_amount"] for r in rows if r["type"] == "Expense"  and r["data_type"] == "Actual")
print(f"\nActual Revenue  (Jan25–May26): ${act_rev:>14,.2f}")
print(f"Actual Expenses (Jan25–May26): ${act_exp:>14,.2f}")
print(f"Actual Net Profit:             ${act_rev - act_exp:>14,.2f}")
