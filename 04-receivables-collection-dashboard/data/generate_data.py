import csv
import random
from datetime import date, timedelta

random.seed(77)

CUSTOMERS = [
    ("Grupo Alfa SA",        "Enterprise"), ("Retail Mega Corp",    "Retail"),
    ("TechVentures Ltd",     "SMB"),        ("Ministerio de Obras", "Government"),
    ("Distribuidora Norte",  "Retail"),     ("Inversiones Sur",     "Enterprise"),
    ("StartupHub Inc",       "SMB"),        ("Almacenes Central",   "Retail"),
    ("Constructora Pacifico","Enterprise"), ("Agencia Federal XYZ", "Government"),
    ("MedSupply Co",         "SMB"),        ("Fashion Group SA",    "Retail"),
    ("AutoParts Corp",       "Enterprise"), ("Ciudad Servicios",    "Government"),
    ("FoodChain Ltd",        "Retail"),     ("Pharma Distributors", "Enterprise"),
    ("Digital Agency Pro",   "SMB"),        ("Import Export SA",    "Enterprise"),
    ("EduTech Systems",      "SMB"),        ("Regional Health Gov", "Government"),
    ("LuxuryGoods SA",       "Retail"),     ("ConsultPro Group",    "SMB"),
    ("HeavyMachinery Corp",  "Enterprise"), ("GreenEnergy Ltd",     "SMB"),
    ("SportsBrands SA",      "Retail"),
]

REGIONS    = ["North", "South", "East", "West", "Central"]
SALES_REPS = ["Maria Gonzalez", "Pedro Alvarez", "Laura Chen",
              "Roberto Silva", "Ana Fernandez", "Carlos Reyes",
              "Sofia Martinez", "David Wong"]
COLLECTORS = ["Elena Ruiz", "Marco Torres", "Isabela Costa",
              "Felipe Morales", "Natalia Vega"]
PAY_METHODS = ["ACH", "Wire", "Check", "Credit Card"]

REF_DATE = date(2025, 6, 1)

rows = []
inv_counter = 1

for cust_idx, (customer_name, customer_segment) in enumerate(CUSTOMERS):
    customer_id = f"CUST-{cust_idx+1:03d}"
    region      = random.choice(REGIONS)
    sales_rep   = random.choice(SALES_REPS)
    collector   = random.choice(COLLECTORS)
    num_invoices = random.randint(25, 45)

    for _ in range(num_invoices):
        invoice_id     = f"RCV-{inv_counter:04d}"
        inv_counter   += 1

        invoice_date  = REF_DATE - timedelta(days=random.randint(5, 180))
        payment_terms = random.choice([15, 30, 45, 60, 90])
        due_date      = invoice_date + timedelta(days=payment_terms)
        invoice_amount = round(random.uniform(2000, 120000), 2)
        payment_method = random.choice(PAY_METHODS)

        days_outstanding = max(0, (REF_DATE - invoice_date).days)
        days_overdue     = max(0, (REF_DATE - due_date).days)

        # Collection status bucket
        if days_overdue == 0:
            collection_status = "Current"
        elif days_overdue <= 30:
            collection_status = "1-30 DPD"
        elif days_overdue <= 60:
            collection_status = "31-60 DPD"
        elif days_overdue <= 90:
            collection_status = "61-90 DPD"
        else:
            collection_status = "90+ DPD"

        r = random.random()

        if days_overdue == 0:
            # Current / not yet due
            if r < 0.30:
                payment_status = "Paid"
                paid_amount    = invoice_amount
                payment_date   = invoice_date + timedelta(days=random.randint(1, payment_terms))
            else:
                payment_status = "Current"
                paid_amount    = 0.0
                payment_date   = None
        elif r < 0.45:
            payment_status = "Paid"
            paid_amount    = invoice_amount
            pay_offset     = random.randint(0, days_outstanding)
            payment_date   = invoice_date + timedelta(days=pay_offset)
        elif r < 0.60:
            payment_status = "Partial"
            paid_amount    = round(invoice_amount * random.uniform(0.10, 0.75), 2)
            payment_date   = invoice_date + timedelta(days=random.randint(1, days_outstanding))
        elif r < 0.75:
            payment_status = "Overdue"
            paid_amount    = 0.0
            payment_date   = None
        else:
            payment_status = "Paid"          # paid late
            pay_offset     = payment_terms + random.randint(1, 45)
            payment_date   = invoice_date + timedelta(days=min(pay_offset, days_outstanding))
            paid_amount    = invoice_amount

        outstanding_balance = round(invoice_amount - paid_amount, 2)

        # Promise to pay date (for overdue/partial)
        if payment_status in ("Overdue", "Partial") and random.random() < 0.55:
            ptp_date = REF_DATE + timedelta(days=random.randint(3, 30))
            promise_to_pay_date = ptp_date.strftime("%Y-%m-%d")
        else:
            promise_to_pay_date = ""

        # Last contact date
        if payment_status in ("Overdue", "Partial"):
            last_contact_date = (REF_DATE - timedelta(days=random.randint(0, 14))).strftime("%Y-%m-%d")
        else:
            last_contact_date = ""

        rows.append({
            "invoice_id":           invoice_id,
            "customer_id":          customer_id,
            "customer_name":        customer_name,
            "customer_segment":     customer_segment,
            "region":               region,
            "sales_rep":            sales_rep,
            "collector":            collector,
            "invoice_date":         invoice_date.strftime("%Y-%m-%d"),
            "due_date":             due_date.strftime("%Y-%m-%d"),
            "payment_terms":        payment_terms,
            "invoice_amount":       invoice_amount,
            "paid_amount":          paid_amount,
            "outstanding_balance":  outstanding_balance,
            "payment_date":         payment_date.strftime("%Y-%m-%d") if payment_date else "",
            "days_outstanding":     days_outstanding,
            "days_overdue":         days_overdue,
            "payment_status":       payment_status,
            "collection_status":    collection_status,
            "payment_method":       payment_method,
            "promise_to_pay_date":  promise_to_pay_date,
            "last_contact_date":    last_contact_date,
        })

output = "C:/Users/User/Project Program/dashboard-tools-10-ap-and-ar/04-receivables-collection-dashboard/data/receivables_data.csv"
fields = [
    "invoice_id", "customer_id", "customer_name", "customer_segment",
    "region", "sales_rep", "collector", "invoice_date", "due_date",
    "payment_terms", "invoice_amount", "paid_amount", "outstanding_balance",
    "payment_date", "days_outstanding", "days_overdue", "payment_status",
    "collection_status", "payment_method", "promise_to_pay_date", "last_contact_date",
]

with open(output, "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=fields)
    writer.writeheader()
    writer.writerows(rows)

print(f"Generated {len(rows)} rows -> {output}")

statuses   = {}
col_status = {}
for r in rows:
    statuses[r["payment_status"]]    = statuses.get(r["payment_status"], 0) + 1
    col_status[r["collection_status"]] = col_status.get(r["collection_status"], 0) + 1

total_invoiced    = sum(r["invoice_amount"] for r in rows)
total_outstanding = sum(r["outstanding_balance"] for r in rows)
total_paid        = sum(r["paid_amount"] for r in rows)
collection_rate   = total_paid / total_invoiced * 100
paid_rows         = [r for r in rows if r["payment_status"] == "Paid"]
avg_days_paid     = sum(r["days_outstanding"] for r in paid_rows) / len(paid_rows) if paid_rows else 0
overdue_amt       = sum(r["outstanding_balance"] for r in rows if r["days_overdue"] > 0)
pct_overdue       = overdue_amt / total_outstanding * 100 if total_outstanding else 0

print(f"\nPayment status:")
for s, c in sorted(statuses.items()):    print(f"  {s}: {c}")
print(f"\nCollection buckets:")
for s, c in sorted(col_status.items()): print(f"  {s}: {c}")
print(f"\nTotal invoiced:      ${total_invoiced:,.2f}")
print(f"Total outstanding:   ${total_outstanding:,.2f}")
print(f"Collection rate:     {collection_rate:.1f}%")
print(f"Avg DSO (paid):      {avg_days_paid:.1f} days")
print(f"Overdue amount:      ${overdue_amt:,.2f}")
print(f"% Overdue:           {pct_overdue:.1f}%")
print(f"Total rows:          {len(rows)}")
