import csv
import random
from datetime import date, timedelta

random.seed(99)

VENDORS = [
    ("Acero Nacional SA", "Materials"), ("TechSupplies Inc", "IT"),
    ("LogiExpress", "Logistics"), ("Grupo Servicios Pro", "Services"),
    ("EnergyPlus Corp", "Utilities"), ("MegaParts Ltd", "Materials"),
    ("CloudSoft Solutions", "IT"), ("Rapi Cargo SA", "Logistics"),
    ("Consulting Masters", "Services"), ("AquaServ", "Utilities"),
    ("SteelBuild Co", "Materials"), ("DataCenter Pro", "IT"),
    ("FreightKing", "Logistics"), ("FacilityPro", "Services"),
    ("PowerGrid SA", "Utilities"), ("MetalWorks Corp", "Materials"),
    ("NetSystems Ltd", "IT"), ("SwiftShip SA", "Logistics"),
    ("CleanOffice Services", "Services"), ("GasNetwork", "Utilities"),
]

REGIONS = ["North", "South", "East", "West", "Central"]

REF_DATE = date(2025, 6, 1)

rows = []
inv_counter = 1

for vendor_name, vendor_category in VENDORS:
    vendor_id = f"VND-{VENDORS.index((vendor_name, vendor_category))+1:03d}"
    num_invoices = random.randint(20, 45)
    region = random.choice(REGIONS)

    for _ in range(num_invoices):
        invoice_id = f"INV-{inv_counter:04d}"
        inv_counter += 1

        invoice_date = REF_DATE - timedelta(days=random.randint(5, 180))
        payment_terms = random.choice([15, 30, 45, 60, 90])
        due_date = invoice_date + timedelta(days=payment_terms)
        invoice_amount = round(random.uniform(1000, 80000), 2)

        # Early payment discount rate available
        discount_rate = random.choice([0.0, 0.01, 0.02, 0.025])

        days_outstanding = max(0, (REF_DATE - invoice_date).days)
        days_overdue = max(0, (REF_DATE - due_date).days)

        r = random.random()
        if days_overdue == 0:
            # Not yet due
            payment_status = "Pending"
            paid_amount = 0.0
            payment_date = None
            discount_captured = 0.0
        elif r < 0.40:
            # Paid on time (within due_date)
            payment_status = "Paid"
            pay_offset = random.randint(0, payment_terms)
            payment_date = invoice_date + timedelta(days=pay_offset)
            paid_amount = invoice_amount
            # Captured discount if paid early (within payment_terms - 5 days)
            if pay_offset <= payment_terms - 5 and discount_rate > 0:
                discount_captured = round(invoice_amount * discount_rate, 2)
            else:
                discount_captured = 0.0
        elif r < 0.55:
            # Partial payment
            payment_status = "Partial"
            paid_amount = round(invoice_amount * random.uniform(0.1, 0.80), 2)
            payment_date = invoice_date + timedelta(days=random.randint(1, days_outstanding))
            discount_captured = 0.0
        elif r < 0.70:
            # Overdue
            payment_status = "Overdue"
            paid_amount = 0.0
            payment_date = None
            discount_captured = 0.0
        else:
            # Paid late
            payment_status = "Paid"
            payment_date = due_date + timedelta(days=random.randint(1, 30))
            paid_amount = invoice_amount
            discount_captured = 0.0

        outstanding_balance = round(invoice_amount - paid_amount, 2)

        rows.append({
            "vendor_id": vendor_id,
            "vendor_name": vendor_name,
            "vendor_category": vendor_category,
            "region": region,
            "invoice_id": invoice_id,
            "invoice_date": invoice_date.strftime("%Y-%m-%d"),
            "due_date": due_date.strftime("%Y-%m-%d"),
            "payment_terms": payment_terms,
            "invoice_amount": invoice_amount,
            "paid_amount": paid_amount,
            "outstanding_balance": outstanding_balance,
            "payment_date": payment_date.strftime("%Y-%m-%d") if payment_date else "",
            "days_outstanding": days_outstanding,
            "days_overdue": days_overdue,
            "payment_status": payment_status,
            "discount_rate": discount_rate,
            "discount_captured": discount_captured,
        })

output = "C:/Users/User/Project Program/dashboard-tools-10-ap-and-ar/02-vendor-payment-tracker/data/vendor_payment_data.csv"
fields = [
    "vendor_id", "vendor_name", "vendor_category", "region",
    "invoice_id", "invoice_date", "due_date", "payment_terms",
    "invoice_amount", "paid_amount", "outstanding_balance",
    "payment_date", "days_outstanding", "days_overdue",
    "payment_status", "discount_rate", "discount_captured",
]

with open(output, "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=fields)
    writer.writeheader()
    writer.writerows(rows)

print(f"Generated {len(rows)} rows -> {output}")

# Summary stats
total_outstanding = sum(r["outstanding_balance"] for r in rows)
total_discount = sum(r["discount_captured"] for r in rows)
overdue = [r for r in rows if r["payment_status"] == "Overdue"]
paid = [r for r in rows if r["payment_status"] == "Paid"]
pending = [r for r in rows if r["payment_status"] == "Pending"]
partial = [r for r in rows if r["payment_status"] == "Partial"]

print(f"  Paid:     {len(paid)}")
print(f"  Pending:  {len(pending)}")
print(f"  Partial:  {len(partial)}")
print(f"  Overdue:  {len(overdue)}")
print(f"  Total outstanding: ${total_outstanding:,.2f}")
print(f"  Total discount captured: ${total_discount:,.2f}")
