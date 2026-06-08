"""
Dashboard 06 — Cash Flow Forecasting
Generates cash_flow_data.csv with ~620 rows of individual cash transactions
covering Jan 2025 – Dec 2026 (Actual: Jan 2025 – May 2026 | Forecast: Jun 2026 – Dec 2026).
"""
import csv
import random
from datetime import date, timedelta
from collections import Counter

random.seed(42)

# ── Constants ────────────────────────────────────────────────────────────────
ACTUAL_CUTOFF = date(2026, 6, 1)   # Jun 2026+ is Forecast
START_DATE    = date(2025, 1, 1)
END_DATE      = date(2026, 12, 31)

CUSTOMERS = [
    "Apex Retail Group", "Meridian Corp", "Blue Sky Solutions",
    "Harmon Industries", "Nova Technologies", "Summit Enterprises",
    "Pacific Distributors", "ClearPath LLC", "Redwood Consulting",
    "Titan Manufacturing",
]
VENDORS = [
    "Acme Supplies Co.", "TechCore Solutions", "FastShip Logistics",
    "BuildRight Materials", "PowerGrid Utilities", "ProStaff Services",
    "CloudSys Inc.", "MetalWorks Ltd.", "OfficePro Services",
    "SafetyFirst Supplies",
]
DEPARTMENTS = ["Finance", "Operations", "HR", "Sales", "IT"]
REGIONS     = ["North", "South", "East", "West", "Central"]


def month_start(y, m):
    return date(y, m, 1)


def rand_day_in_month(y, m):
    """Return a random date within the given month."""
    first = date(y, m, 1)
    if m == 12:
        last = date(y, 12, 31)
    else:
        last = date(y, m + 1, 1) - timedelta(days=1)
    delta = (last - first).days
    return first + timedelta(days=random.randint(0, delta))


def period_label(y, m):
    return date(y, m, 1).strftime("%b %Y")   # "Jan 2025"


def quarter(m):
    return f"Q{(m - 1) // 3 + 1}"


def data_type(d: date) -> str:
    return "Actual" if d < ACTUAL_CUTOFF else "Forecast"


# ── Transaction generators ───────────────────────────────────────────────────

rows = []
tx_id = 1


def add(tx_date, category, flow_type, dept, cpty, ref,
        budget, actual_or_forecast_base, is_forecast):
    global tx_id
    if is_forecast:
        actual_amt    = 0.0
        # Forecast: budget ± slight random variation
        forecast_amt  = round(actual_or_forecast_base * random.uniform(0.92, 1.08), 2)
        variance      = 0.0
        variance_pct  = 0.0
    else:
        # Actual: budget ± variance
        actual_amt    = round(actual_or_forecast_base * random.uniform(0.88, 1.12), 2)
        forecast_amt  = actual_amt
        variance      = round(actual_amt - budget, 2)
        variance_pct  = round(variance / budget * 100, 1) if budget else 0.0

    # Favorable: inflow higher than budget OR outflow lower than budget
    if variance != 0:
        if flow_type == "Inflow":
            is_favorable = "Yes" if variance >= 0 else "No"
        else:
            is_favorable = "Yes" if variance <= 0 else "No"
    else:
        is_favorable = ""

    rows.append({
        "transaction_id":   f"CF-{tx_id:04d}",
        "date":             tx_date.isoformat(),
        "period":           period_label(tx_date.year, tx_date.month),
        "year":             tx_date.year,
        "month":            tx_date.month,
        "quarter":          quarter(tx_date.month),
        "category":         category,
        "flow_type":        flow_type,
        "department":       dept,
        "region":           random.choice(REGIONS),
        "counterparty":     cpty,
        "reference":        ref,
        "budget_amount":    round(budget, 2),
        "actual_amount":    actual_amt,
        "forecast_amount":  forecast_amt,
        "variance":         variance,
        "variance_pct":     variance_pct,
        "data_type":        data_type(tx_date),
        "is_favorable":     is_favorable,
    })
    tx_id += 1


# ── Generate transactions month by month ────────────────────────────────────
months = [(y, m) for y in range(2025, 2027) for m in range(1, 13)
          if date(y, m, 1) <= END_DATE]

for yr, mo in months:
    is_fc = date(yr, mo, 1) >= ACTUAL_CUTOFF
    qtr   = quarter(mo)

    # ── INFLOWS ────────────────────────────────────────────────────────────

    # AR Collections: 4–6 per month
    for _ in range(random.randint(4, 6)):
        bgt = random.uniform(18000, 75000)
        add(rand_day_in_month(yr, mo),
            "AR Collections", "Inflow",
            "Finance", random.choice(CUSTOMERS),
            f"INV-{random.randint(10000,99999)}",
            bgt, bgt * random.uniform(0.90, 1.10), is_fc)

    # Product Sales: 3–5 per month
    for _ in range(random.randint(3, 5)):
        bgt = random.uniform(25000, 110000)
        add(rand_day_in_month(yr, mo),
            "Product Sales", "Inflow",
            "Sales", random.choice(CUSTOMERS),
            f"ORD-{random.randint(5000,9999)}",
            bgt, bgt * random.uniform(0.88, 1.12), is_fc)

    # Service Revenue: 2–4 per month
    for _ in range(random.randint(2, 4)):
        bgt = random.uniform(12000, 55000)
        add(rand_day_in_month(yr, mo),
            "Service Revenue", "Inflow",
            "Sales", random.choice(CUSTOMERS),
            f"SVC-{random.randint(1000,4999)}",
            bgt, bgt * random.uniform(0.90, 1.08), is_fc)

    # Interest Income: 1 per month
    bgt = random.uniform(1000, 5500)
    add(month_start(yr, mo) + timedelta(days=random.randint(25, 28)),
        "Interest Income", "Inflow",
        "Finance", "Bank of Commerce",
        f"INT-{yr}{mo:02d}",
        bgt, bgt * random.uniform(0.95, 1.05), is_fc)

    # ── OUTFLOWS ───────────────────────────────────────────────────────────

    # AP Payments: 4–6 per month
    for _ in range(random.randint(4, 6)):
        bgt = random.uniform(6000, 42000)
        add(rand_day_in_month(yr, mo),
            "AP Payments", "Outflow",
            "Finance", random.choice(VENDORS),
            f"PO-{random.randint(20000,79999)}",
            bgt, bgt * random.uniform(0.92, 1.05), is_fc)

    # Payroll: 2 per month (bi-weekly)
    for wk in [7, 21]:
        day = min(wk, 28)
        pay_date = date(yr, mo, day)
        bgt = random.uniform(80000, 180000)
        add(pay_date,
            "Payroll", "Outflow",
            "HR", "Payroll Processing",
            f"PAY-{yr}{mo:02d}-{1 if wk==7 else 2}",
            bgt, bgt * random.uniform(0.98, 1.02), is_fc)

    # Operating Expenses: 3–4 per month
    for _ in range(random.randint(3, 4)):
        bgt = random.uniform(5000, 28000)
        add(rand_day_in_month(yr, mo),
            "Operating Expenses", "Outflow",
            random.choice(DEPARTMENTS),
            random.choice(VENDORS),
            f"EXP-{random.randint(3000,9999)}",
            bgt, bgt * random.uniform(0.90, 1.12), is_fc)

    # CAPEX: 1–2 per month (some months skip)
    capex_count = random.choices([0, 1, 2], weights=[20, 55, 25])[0]
    for _ in range(capex_count):
        bgt = random.uniform(22000, 120000)
        add(rand_day_in_month(yr, mo),
            "CAPEX", "Outflow",
            random.choice(["IT", "Operations"]),
            random.choice(VENDORS),
            f"CAP-{random.randint(1000,3999)}",
            bgt, bgt * random.uniform(0.85, 1.15), is_fc)

    # Tax Payments: quarterly (Mar, Jun, Sep, Dec)
    if mo in (3, 6, 9, 12):
        bgt = random.uniform(55000, 160000)
        add(date(yr, mo, random.randint(12, 18)),
            "Tax Payments", "Outflow",
            "Finance", "IRS / Tax Authority",
            f"TAX-{yr}-{qtr}",
            bgt, bgt * random.uniform(0.95, 1.05), is_fc)

# ── Sort by date ─────────────────────────────────────────────────────────────
rows.sort(key=lambda r: r["date"])

# ── Write CSV ─────────────────────────────────────────────────────────────────
out_path = (
    "C:/Users/User/Project Program/dashboard-tools-10-ap-and-ar/"
    "06-cash-flow-forecasting/data/cash_flow_data.csv"
)
cols = list(rows[0].keys())
with open(out_path, "w", newline="", encoding="utf-8") as f:
    w = csv.DictWriter(f, fieldnames=cols)
    w.writeheader()
    w.writerows(rows)

# ── Summary ──────────────────────────────────────────────────────────────────
print(f"Total rows: {len(rows)}")
print("flow_type:", dict(Counter(r["flow_type"] for r in rows)))
print("data_type:", dict(Counter(r["data_type"] for r in rows)))
print("category:", dict(Counter(r["category"] for r in rows)))
inflows  = sum(r["forecast_amount"] for r in rows if r["flow_type"] == "Inflow")
outflows = sum(r["forecast_amount"] for r in rows if r["flow_type"] == "Outflow")
net      = inflows - outflows
print(f"\nTotal Inflows  (forecast): ${inflows:>14,.2f}")
print(f"Total Outflows (forecast): ${outflows:>14,.2f}")
print(f"Net Cash Flow:             ${net:>14,.2f}")
print(f"Coverage Ratio:            {inflows/outflows:.3f}")
actual_in  = sum(r["actual_amount"] for r in rows if r["flow_type"] == "Inflow"  and r["data_type"] == "Actual")
actual_out = sum(r["actual_amount"] for r in rows if r["flow_type"] == "Outflow" and r["data_type"] == "Actual")
print(f"\nActual Inflows  (Jan25–May26): ${actual_in:>14,.2f}")
print(f"Actual Outflows (Jan25–May26): ${actual_out:>14,.2f}")
