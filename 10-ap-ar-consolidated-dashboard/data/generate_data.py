"""
Generate consolidated_data.csv for Dashboard 10 — AP/AR Consolidated Dashboard
700 rows combining Accounts Payable (AP) and Accounts Receivable (AR) transactions
covering Jan 2025 – Jun 2026 (18 months)
"""
import csv
import random
import math

random.seed(42)

# --- Reference data ---
AR_ENTITIES = [
    ("Apex Corp", "Enterprise"), ("BlueSky Ltd", "Enterprise"), ("Cedar Group", "Enterprise"),
    ("Delta Inc", "SMB"), ("Echo Solutions", "SMB"), ("Falcon Tech", "SMB"),
    ("Global Retail", "Retail"), ("Harbor Shops", "Retail"), ("IronClad Stores", "Retail"),
    ("Jupiter Startup", "Startup"), ("Kite Ventures", "Startup"), ("Lumen Digital", "Startup"),
    ("Metro Bank", "Government"), ("National Agency", "Government"), ("Oak Institute", "Government"),
    ("Peak Analytics", "Enterprise"), ("Quantum Ltd", "SMB"), ("River Trade", "Retail"),
]

AP_ENTITIES = [
    ("Acme Supplies", "Office"), ("BrightTech Parts", "Technology"), ("Crown Logistics", "Logistics"),
    ("Dura Materials", "Manufacturing"), ("Elite Services", "Consulting"), ("FirmBase Infra", "Technology"),
    ("General Utilities", "Utilities"), ("HarbourFreight", "Logistics"), ("InfoSys Partners", "Consulting"),
    ("Java Components", "Manufacturing"), ("Keystone Energy", "Utilities"), ("LightHouse Media", "Marketing"),
    ("Master Builders", "Manufacturing"), ("Network Pro", "Technology"), ("OmniSource", "Office"),
    ("Prime Vendors", "Consulting"), ("Quality Goods", "Office"), ("Reliant Power", "Utilities"),
]

REGIONS = ["North", "South", "East", "West", "Central"]
AGING_BUCKETS = ["Current", "1-30", "31-60", "61-90", "90+"]
STATUSES = ["Current", "Partial", "Overdue", "Paid"]
PAYMENT_TERMS = ["Net 30", "Net 45", "Net 60", "Net 90", "2/10 Net 30"]

# 18 months: Jan 2025 – Jun 2026
PERIODS = []
for year in [2025, 2026]:
    max_month = 12 if year == 2025 else 6
    for month in range(1, max_month + 1):
        quarter = f"Q{math.ceil(month/3)}"
        label = f"{year}-{month:02d}"
        PERIODS.append((label, year, month, quarter))

def aging_to_days(bucket):
    mapping = {"Current": 0, "1-30": random.randint(1, 30),
               "31-60": random.randint(31, 60), "61-90": random.randint(61, 90),
               "90+": random.randint(91, 180)}
    return mapping[bucket]

def make_amounts(invoice_base, status, aging_bucket):
    if status == "Paid":
        paid = invoice_base
        outstanding = 0.0
        overdue = 0.0
    elif status == "Partial":
        paid = round(invoice_base * random.uniform(0.2, 0.7), 2)
        outstanding = round(invoice_base - paid, 2)
        overdue = outstanding if aging_bucket != "Current" else 0.0
    elif status == "Overdue":
        paid = round(invoice_base * random.uniform(0.0, 0.15), 2)
        outstanding = round(invoice_base - paid, 2)
        overdue = outstanding
    else:  # Current
        paid = 0.0
        outstanding = invoice_base
        overdue = 0.0
    return round(invoice_base, 2), round(paid, 2), round(outstanding, 2), round(overdue, 2)

rows = []
record_id = 1

# Generate AR rows (350)
for _ in range(350):
    period_info = random.choice(PERIODS)
    entity, segment = random.choice(AR_ENTITIES)
    region = random.choice(REGIONS)
    aging_bucket = random.choices(AGING_BUCKETS, weights=[35, 25, 18, 12, 10])[0]
    if aging_bucket == "Current":
        status = random.choices(["Current", "Partial"], weights=[70, 30])[0]
    elif aging_bucket in ("1-30", "31-60"):
        status = random.choices(["Partial", "Overdue", "Paid"], weights=[40, 40, 20])[0]
    else:
        status = random.choices(["Overdue", "Partial"], weights=[80, 20])[0]

    invoice_base = round(random.uniform(5000, 250000), 2)
    terms = random.choice(PAYMENT_TERMS)
    days = aging_to_days(aging_bucket)
    inv_amt, paid, outstanding, overdue = make_amounts(invoice_base, status, aging_bucket)

    rows.append({
        "record_id": record_id,
        "period": period_info[0],
        "year": period_info[1],
        "month": period_info[2],
        "quarter": period_info[3],
        "transaction_type": "AR",
        "entity_name": entity,
        "entity_segment": segment,
        "region": region,
        "invoice_amount": inv_amt,
        "paid_amount": paid,
        "outstanding_balance": outstanding,
        "overdue_amount": overdue,
        "days_overdue": days,
        "aging_bucket": aging_bucket,
        "status": status,
        "payment_terms": terms,
    })
    record_id += 1

# Generate AP rows (350)
for _ in range(350):
    period_info = random.choice(PERIODS)
    entity, category = random.choice(AP_ENTITIES)
    region = random.choice(REGIONS)
    aging_bucket = random.choices(AGING_BUCKETS, weights=[40, 28, 16, 10, 6])[0]
    if aging_bucket == "Current":
        status = random.choices(["Current", "Partial"], weights=[65, 35])[0]
    elif aging_bucket in ("1-30", "31-60"):
        status = random.choices(["Partial", "Overdue", "Paid"], weights=[35, 45, 20])[0]
    else:
        status = random.choices(["Overdue", "Partial"], weights=[85, 15])[0]

    invoice_base = round(random.uniform(3000, 180000), 2)
    terms = random.choice(PAYMENT_TERMS)
    days = aging_to_days(aging_bucket)
    inv_amt, paid, outstanding, overdue = make_amounts(invoice_base, status, aging_bucket)

    rows.append({
        "record_id": record_id,
        "period": period_info[0],
        "year": period_info[1],
        "month": period_info[2],
        "quarter": period_info[3],
        "transaction_type": "AP",
        "entity_name": entity,
        "entity_segment": category,
        "region": region,
        "invoice_amount": inv_amt,
        "paid_amount": paid,
        "outstanding_balance": outstanding,
        "overdue_amount": overdue,
        "days_overdue": days,
        "aging_bucket": aging_bucket,
        "status": status,
        "payment_terms": terms,
    })
    record_id += 1

# Shuffle rows
random.shuffle(rows)

# Write CSV
fieldnames = ["record_id","period","year","month","quarter","transaction_type",
              "entity_name","entity_segment","region","invoice_amount","paid_amount",
              "outstanding_balance","overdue_amount","days_overdue","aging_bucket",
              "status","payment_terms"]

with open("consolidated_data.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(rows)

print(f"Generated {len(rows)} rows")
ar_count = sum(1 for r in rows if r["transaction_type"] == "AR")
ap_count = sum(1 for r in rows if r["transaction_type"] == "AP")
total_ar_outstanding = sum(r["outstanding_balance"] for r in rows if r["transaction_type"] == "AR")
total_ap_outstanding = sum(r["outstanding_balance"] for r in rows if r["transaction_type"] == "AP")
print(f"AR rows: {ar_count}, AP rows: {ap_count}")
print(f"Total AR Outstanding: ${total_ar_outstanding:,.0f}")
print(f"Total AP Outstanding: ${total_ap_outstanding:,.0f}")
print(f"Net Working Capital: ${total_ar_outstanding - total_ap_outstanding:,.0f}")
