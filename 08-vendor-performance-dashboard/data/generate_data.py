"""
Dashboard 08 — Vendor Performance Dashboard
Generates vendor_performance_data.csv with ~600 rows covering
Jan 2025 – Aug 2026 (20 months), one record per vendor per month.
30 vendors across 5 categories.
"""
import csv
import random
from datetime import date, timedelta

random.seed(8)

# ── Constants ────────────────────────────────────────────────────────────────
START_DATE = date(2025, 1, 1)
END_DATE   = date(2026, 8, 31)

CATEGORIES = ["Technology", "Office Supplies", "Raw Materials", "Logistics", "Professional Services"]
REGIONS    = ["North", "South", "East", "West", "Central"]
STATUSES   = ["Active", "Active", "Active", "Active", "Probation", "Inactive"]  # weighted

# 30 vendors (6 per category)
VENDORS = []
for cat in CATEGORIES:
    for i in range(1, 7):
        short = cat.split()[0][:3].upper()
        VENDORS.append({
            "vendor_id":   f"V-{short}-{i:02d}",
            "vendor_name": f"{cat} Vendor {i:02d}",
            "category":    cat,
            "region":      random.choice(REGIONS),
            "status":      random.choice(STATUSES),
            # Baseline quality (varies per vendor, 60–95)
            "base_quality": round(random.uniform(60, 95), 1),
            # Baseline payment days (20–75 days)
            "base_pay_days": random.randint(20, 75),
            # Baseline monthly spend range
            "spend_lo": random.randint(20_000, 80_000),
            "spend_hi": random.randint(90_000, 300_000),
        })


def period_label(y, m):
    return date(y, m, 1).strftime("%b %Y")


def quarter(m):
    return f"Q{(m - 1) // 3 + 1}"


rows = []
tx_id = 1

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

    for v in VENDORS:
        # Skip inactive vendors ~40% of the time (they still have some records)
        if v["status"] == "Inactive" and random.random() < 0.4:
            continue

        invoice_amount = round(random.uniform(v["spend_lo"], v["spend_hi"]), 2)

        # Payment days: base ± some noise
        payment_days = max(1, v["base_pay_days"] + random.randint(-10, 20))

        # On-time: probability based on payment days relative to 45-day standard
        on_time_prob = max(0.3, min(0.98, 1.0 - (payment_days - 45) / 90))
        on_time = "Yes" if random.random() < on_time_prob else "No"

        # Quality score: base ± noise, bounded 0–100
        quality_score = round(min(100, max(0, v["base_quality"] + random.uniform(-8, 8))), 1)

        # Defect rate: inversely related to quality
        defect_rate = round(max(0.0, (100 - quality_score) / 100 * random.uniform(0.5, 1.5)), 4)

        # Order count: 1–15
        order_count = random.randint(1, 15)

        # Dispute count: 0–2 (higher if quality is low)
        dispute_prob = max(0, (85 - quality_score) / 100)
        dispute_count = sum(random.random() < dispute_prob for _ in range(3))

        rows.append({
            "record_id":       f"VP-{tx_id:04d}",
            "vendor_id":       v["vendor_id"],
            "vendor_name":     v["vendor_name"],
            "category":        v["category"],
            "region":          v["region"],
            "status":          v["status"],
            "period":          period,
            "year":            yr,
            "month":           mo,
            "quarter":         qtr,
            "invoice_amount":  invoice_amount,
            "payment_days":    payment_days,
            "on_time":         on_time,
            "quality_score":   quality_score,
            "defect_rate":     defect_rate,
            "order_count":     order_count,
            "dispute_count":   dispute_count,
        })
        tx_id += 1

# Sort by period then vendor
rows.sort(key=lambda r: (r["year"], r["month"], r["vendor_id"]))

# Write CSV
out = (
    "C:/Users/User/Project Program/dashboard-tools-10-ap-and-ar/"
    "08-vendor-performance-dashboard/data/vendor_performance_data.csv"
)
cols = list(rows[0].keys())
with open(out, "w", newline="", encoding="utf-8") as f:
    w = csv.DictWriter(f, fieldnames=cols)
    w.writeheader()
    w.writerows(rows)

# Summary
from collections import Counter
print(f"Total rows: {len(rows)}")
print("category:", dict(Counter(r["category"] for r in rows)))
print("status:", dict(Counter(r["status"] for r in rows)))
print("on_time:", dict(Counter(r["on_time"] for r in rows)))

total_spend = sum(r["invoice_amount"] for r in rows)
avg_quality = sum(r["quality_score"] for r in rows) / len(rows)
avg_pay     = sum(r["payment_days"] for r in rows) / len(rows)
on_time_pct = sum(1 for r in rows if r["on_time"] == "Yes") / len(rows) * 100

print(f"\nTotal Spend:          ${total_spend:>14,.2f}")
print(f"Avg Quality Score:    {avg_quality:.1f}")
print(f"On-Time Delivery %:   {on_time_pct:.1f}%")
print(f"Avg Payment Days:     {avg_pay:.1f}")
