"""
Dashboard 09 — Customer Credit Risk Dashboard
Generates credit_risk_data.csv with ~600 rows covering
Jan 2025 – Mar 2026 (15 months), one record per customer per month.
40 customers across 5 segments.
"""
import csv
import random
from datetime import date

random.seed(9)

# ── Constants ────────────────────────────────────────────────────────────────
START_DATE = date(2025, 1, 1)
END_DATE   = date(2026, 3, 31)

SEGMENTS = ["Enterprise", "SMB", "Retail", "Government", "Startup"]
REGIONS  = ["North", "South", "East", "West", "Central"]
PAYMENT_HISTORY = ["Good", "Good", "Good", "Fair", "Fair", "Poor"]  # weighted

# 40 customers (8 per segment)
CUSTOMERS = []
for seg in SEGMENTS:
    for i in range(1, 9):
        short = seg[:3].upper()
        # Credit limits vary by segment
        if seg == "Enterprise":
            limit_lo, limit_hi = 500_000, 2_000_000
        elif seg == "Government":
            limit_lo, limit_hi = 300_000, 1_500_000
        elif seg == "SMB":
            limit_lo, limit_hi = 100_000, 500_000
        elif seg == "Retail":
            limit_lo, limit_hi = 50_000, 200_000
        else:  # Startup
            limit_lo, limit_hi = 30_000, 150_000

        credit_limit = round(random.randint(limit_lo // 1000, limit_hi // 1000) * 1000)
        payment_hist = random.choice(PAYMENT_HISTORY)

        # Base risk: Startups and Poor payers are riskier
        if seg == "Startup":
            base_risk = random.uniform(35, 80)
        elif seg == "Enterprise":
            base_risk = random.uniform(10, 50)
        elif seg == "Government":
            base_risk = random.uniform(5, 35)
        else:
            base_risk = random.uniform(15, 65)

        if payment_hist == "Poor":
            base_risk = min(100, base_risk + 20)
        elif payment_hist == "Good":
            base_risk = max(0, base_risk - 10)

        CUSTOMERS.append({
            "customer_id":   f"C-{short}-{i:02d}",
            "customer_name": f"{seg} Client {i:02d}",
            "segment":       seg,
            "region":        random.choice(REGIONS),
            "credit_limit":  credit_limit,
            "payment_history": payment_hist,
            "base_risk":     round(base_risk, 1),
            # Base utilization rate (0.0–1.0)
            "base_util":     round(random.uniform(0.3, 0.92), 2),
        })


def period_label(y, m):
    return date(y, m, 1).strftime("%b %Y")


def quarter(m):
    return f"Q{(m - 1) // 3 + 1}"


def risk_category(score):
    if score <= 25:
        return "Low"
    elif score <= 50:
        return "Medium"
    elif score <= 75:
        return "High"
    else:
        return "Critical"


rows = []
rec_id = 1

months = []
y, m = 2025, 1
while date(y, m, 1) <= END_DATE:
    months.append((y, m))
    m += 1
    if m > 12:
        m = 1
        y += 1

for yr, mo in months:
    period = period_label(yr, mo)
    qtr    = quarter(mo)

    for c in CUSTOMERS:
        # Risk score drifts slightly each month
        risk = round(min(100, max(0, c["base_risk"] + random.uniform(-5, 5))), 1)
        cat  = risk_category(risk)

        # Utilization drifts; higher risk → higher utilization tendency
        util_noise = random.uniform(-0.08, 0.08)
        if cat in ("High", "Critical"):
            util_noise += 0.05
        util = round(min(1.0, max(0.05, c["base_util"] + util_noise)), 4)

        credit_used       = round(c["credit_limit"] * util)
        outstanding       = round(credit_used * random.uniform(0.3, 0.85))
        overdue_ratio     = 0.0 if risk <= 30 else random.uniform(0, min(0.6, risk / 100))
        overdue_balance   = round(outstanding * overdue_ratio)
        days_overdue      = 0 if overdue_balance == 0 else random.randint(1, min(180, int(risk * 2)))
        on_time_payments  = random.randint(1, 10)
        late_payments     = 0 if c["payment_history"] == "Good" else random.randint(0, 4)
        write_off_amount  = 0.0 if risk < 70 else round(random.uniform(0, overdue_balance * 0.15), 2)

        rows.append({
            "record_id":        f"CR-{rec_id:04d}",
            "customer_id":      c["customer_id"],
            "customer_name":    c["customer_name"],
            "segment":          c["segment"],
            "region":           c["region"],
            "credit_limit":     c["credit_limit"],
            "credit_used":      credit_used,
            "credit_utilization": util,
            "outstanding_balance": outstanding,
            "overdue_balance":  overdue_balance,
            "days_overdue":     days_overdue,
            "risk_score":       risk,
            "risk_category":    cat,
            "payment_history":  c["payment_history"],
            "on_time_payments": on_time_payments,
            "late_payments":    late_payments,
            "write_off_amount": write_off_amount,
            "period":           period,
            "year":             yr,
            "month":            mo,
            "quarter":          qtr,
        })
        rec_id += 1

# Sort by period then customer
rows.sort(key=lambda r: (r["year"], r["month"], r["customer_id"]))

# Write CSV
out = (
    "C:/Users/User/Project Program/dashboard-tools-10-ap-and-ar/"
    "09-customer-credit-risk-dashboard/data/credit_risk_data.csv"
)
cols = list(rows[0].keys())
with open(out, "w", newline="", encoding="utf-8") as f:
    w = csv.DictWriter(f, fieldnames=cols)
    w.writeheader()
    w.writerows(rows)

# Summary
from collections import Counter
print(f"Total rows: {len(rows)}")
print("segment:", dict(Counter(r["segment"] for r in rows)))
print("risk_category:", dict(Counter(r["risk_category"] for r in rows)))
print("payment_history:", dict(Counter(r["payment_history"] for r in rows)))

total_exposure = sum(r["credit_limit"] for r in rows)
total_used     = sum(r["credit_used"] for r in rows)
total_outstd   = sum(r["outstanding_balance"] for r in rows)
avg_risk       = sum(r["risk_score"] for r in rows) / len(rows)
avg_util       = sum(r["credit_utilization"] for r in rows) / len(rows)
high_risk_cust = len({r["customer_id"] for r in rows if r["risk_category"] in ("High", "Critical")})

print(f"\nTotal Credit Exposure: ${total_exposure:>16,.0f}")
print(f"Total Credit Used:     ${total_used:>16,.0f}")
print(f"Total Outstanding:     ${total_outstd:>16,.0f}")
print(f"Avg Risk Score:        {avg_risk:.1f}")
print(f"Avg Utilization:       {avg_util:.1%}")
print(f"High/Critical Customers (unique): {high_risk_cust}")
