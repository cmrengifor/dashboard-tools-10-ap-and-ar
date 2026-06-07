import csv
import random
from datetime import date, timedelta

random.seed(42)

CUSTOMERS = [
    ("Acme Corp", "Corporate"), ("BlueStar Ltd", "Corporate"), ("CityRetail SA", "Retail"),
    ("Delta Supplies", "SMB"), ("Eagle Trading", "SMB"), ("FastMart Inc", "Retail"),
    ("Global Parts Co", "Corporate"), ("Harbor Goods", "SMB"), ("Intex Solutions", "Corporate"),
    ("JetLine Inc", "Retail"), ("KeyStone LLC", "SMB"), ("Luminary Corp", "Corporate"),
    ("MegaBuy SA", "Retail"), ("NovaTech Ltd", "Corporate"), ("Omega Retail", "Retail"),
    ("PrimeParts Co", "SMB"), ("QualityGoods", "Retail"), ("RedLine Corp", "Corporate"),
    ("SkyLink SA", "SMB"), ("TechWorld Inc", "Corporate"), ("UniMart Ltd", "Retail"),
    ("Vertex Supply", "SMB"), ("WaveCo Corp", "Corporate"), ("XcelBuy SA", "Retail"),
    ("YieldTech", "SMB"), ("Zenith Corp", "Corporate"), ("Apex Retail", "Retail"),
    ("Bravo Trading", "SMB"), ("Crest Corp", "Corporate"), ("DynaBuy Inc", "Retail"),
]

REGIONS = ["North", "South", "East", "West", "Central"]

SALES_REPS = [
    "Maria Lopez", "Carlos Perez", "Ana Torres", "Luis Mendez",
    "Sofia Ruiz", "Diego Herrera", "Valentina Cruz", "Andres Gomez",
]

REF_DATE = date(2025, 6, 1)

rows = []
for i in range(1, 801):
    customer, segment = random.choice(CUSTOMERS)
    region = random.choice(REGIONS)
    sales_rep = random.choice(SALES_REPS)

    invoice_date = REF_DATE - timedelta(days=random.randint(1, 180))
    payment_terms = random.choice([15, 30, 45, 60])
    due_date = invoice_date + timedelta(days=payment_terms)

    invoice_amount = round(random.uniform(500, 50000), 2)

    days_overdue = max(0, (REF_DATE - due_date).days)

    # Determine status and paid amount
    if days_overdue == 0:
        status = "Current"
        paid_amount = 0.0
        outstanding_balance = invoice_amount
    else:
        r = random.random()
        if r < 0.30:
            status = "Paid"
            paid_amount = invoice_amount
            outstanding_balance = 0.0
            days_overdue = 0
        elif r < 0.55:
            status = "Partial"
            paid_amount = round(invoice_amount * random.uniform(0.1, 0.85), 2)
            outstanding_balance = round(invoice_amount - paid_amount, 2)
        else:
            status = "Overdue"
            paid_amount = 0.0
            outstanding_balance = invoice_amount

    # Aging bucket
    if status in ("Paid", "Current"):
        aging_bucket = "Current"
    elif days_overdue <= 30:
        aging_bucket = "1-30"
    elif days_overdue <= 60:
        aging_bucket = "31-60"
    elif days_overdue <= 90:
        aging_bucket = "61-90"
    else:
        aging_bucket = "90+"

    rows.append({
        "invoice_id": f"INV-{i:04d}",
        "customer_name": customer,
        "customer_segment": segment,
        "invoice_date": invoice_date.strftime("%Y-%m-%d"),
        "due_date": due_date.strftime("%Y-%m-%d"),
        "invoice_amount": invoice_amount,
        "paid_amount": paid_amount,
        "outstanding_balance": outstanding_balance,
        "days_overdue": days_overdue,
        "aging_bucket": aging_bucket,
        "status": status,
        "region": region,
        "sales_rep": sales_rep,
    })

output = "C:/Users/User/Project Program/dashboard-tools-10-ap-and-ar/01-invoice-aging-dashboard/data/invoice_aging_data.csv"
fields = [
    "invoice_id", "customer_name", "customer_segment", "invoice_date",
    "due_date", "invoice_amount", "paid_amount", "outstanding_balance",
    "days_overdue", "aging_bucket", "status", "region", "sales_rep",
]

with open(output, "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=fields)
    writer.writeheader()
    writer.writerows(rows)

print(f"Generated {len(rows)} rows -> {output}")

# Quick summary
overdue = [r for r in rows if r["status"] == "Overdue"]
partial = [r for r in rows if r["status"] == "Partial"]
paid    = [r for r in rows if r["status"] == "Paid"]
current = [r for r in rows if r["status"] == "Current"]
total_outstanding = sum(r["outstanding_balance"] for r in rows)

print(f"  Current:  {len(current)}")
print(f"  Overdue:  {len(overdue)}")
print(f"  Partial:  {len(partial)}")
print(f"  Paid:     {len(paid)}")
print(f"  Total outstanding: ${total_outstanding:,.2f}")
