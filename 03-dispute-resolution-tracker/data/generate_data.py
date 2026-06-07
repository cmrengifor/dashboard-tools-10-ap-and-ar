import csv
import random
from datetime import date, timedelta

random.seed(42)

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

DISPUTE_TYPES = [
    "Price Discrepancy",
    "Damaged Goods",
    "Missing Goods",
    "Duplicate Invoice",
    "Service Quality",
    "Contract Terms",
]

PRIORITIES = ["Low", "Medium", "High", "Critical"]
PRIORITY_WEIGHTS = [0.25, 0.40, 0.25, 0.10]

RESOLVERS = [
    "Ana Torres", "Carlos Mendez", "Sofia Ruiz", "Luis Herrera",
    "Marta Lopez", "Diego Castillo", "Valeria Moreno", "Juan Vargas",
]

REF_DATE = date(2025, 6, 1)

rows = []
inv_counter = 1001   # offset from dashboard-02 invoice IDs

for idx, (vendor_name, vendor_category) in enumerate(VENDORS):
    vendor_id = f"VND-{idx+1:03d}"
    region = random.choice(REGIONS)
    num_disputes = random.randint(20, 35)

    for _ in range(num_disputes):
        dispute_id = f"DIS-{len(rows)+1:04d}"
        invoice_id = f"INV-{inv_counter:04d}"
        inv_counter += 1

        dispute_date = REF_DATE - timedelta(days=random.randint(1, 365))
        invoice_amount = round(random.uniform(5000, 100000), 2)
        dispute_amount = round(invoice_amount * random.uniform(0.05, 0.80), 2)

        priority = random.choices(PRIORITIES, weights=PRIORITY_WEIGHTS)[0]
        dispute_type = random.choice(DISPUTE_TYPES)
        assigned_to = random.choice(RESOLVERS)

        days_open = (REF_DATE - dispute_date).days

        # Determine status based on age and priority
        r = random.random()
        if days_open <= 10:
            # Very new — mostly Open
            if r < 0.70:
                status = "Open"
            else:
                status = "In Progress"
            resolution_date = None
            resolution_days = None
            resolution_outcome = "Pending"
            credit_amount = 0.0
        elif days_open <= 30:
            if r < 0.35:
                status = "Open"
            elif r < 0.65:
                status = "In Progress"
            elif r < 0.80:
                status = "Resolved"
            elif r < 0.90:
                status = "Escalated"
            else:
                status = "Closed"
        elif days_open <= 90:
            if r < 0.15:
                status = "Open"
            elif r < 0.30:
                status = "In Progress"
            elif r < 0.70:
                status = "Resolved"
            elif r < 0.85:
                status = "Escalated"
            else:
                status = "Closed"
        else:
            if r < 0.05:
                status = "Open"
            elif r < 0.10:
                status = "In Progress"
            elif r < 0.65:
                status = "Resolved"
            elif r < 0.80:
                status = "Escalated"
            else:
                status = "Closed"

        # Assign resolution details if resolved/closed
        if days_open > 10 and status not in ("Open", "In Progress"):
            res_days = random.randint(3, min(days_open, 120))
            resolution_date = dispute_date + timedelta(days=res_days)
            resolution_days = res_days

            ro_r = random.random()
            if ro_r < 0.40:
                resolution_outcome = "Full Credit"
                credit_amount = dispute_amount
            elif ro_r < 0.65:
                resolution_outcome = "Partial Credit"
                credit_amount = round(dispute_amount * random.uniform(0.20, 0.80), 2)
            elif ro_r < 0.80:
                resolution_outcome = "Payment Adjusted"
                credit_amount = round(dispute_amount * random.uniform(0.10, 0.50), 2)
            elif ro_r < 0.92:
                resolution_outcome = "No Action"
                credit_amount = 0.0
            else:
                resolution_outcome = "Pending"
                credit_amount = 0.0
        elif days_open <= 10 or status in ("Open", "In Progress"):
            resolution_date = None
            resolution_days = None
            resolution_outcome = "Pending"
            credit_amount = 0.0

        rows.append({
            "dispute_id": dispute_id,
            "invoice_id": invoice_id,
            "vendor_id": vendor_id,
            "vendor_name": vendor_name,
            "vendor_category": vendor_category,
            "region": region,
            "dispute_date": dispute_date.strftime("%Y-%m-%d"),
            "dispute_type": dispute_type,
            "invoice_amount": invoice_amount,
            "dispute_amount": dispute_amount,
            "priority": priority,
            "assigned_to": assigned_to,
            "status": status,
            "days_open": days_open,
            "resolution_date": resolution_date.strftime("%Y-%m-%d") if resolution_date else "",
            "resolution_days": resolution_days if resolution_days is not None else "",
            "resolution_outcome": resolution_outcome,
            "credit_amount": credit_amount,
        })

output = "C:/Users/User/Project Program/dashboard-tools-10-ap-and-ar/03-dispute-resolution-tracker/data/disputes_data.csv"
fields = [
    "dispute_id", "invoice_id", "vendor_id", "vendor_name", "vendor_category",
    "region", "dispute_date", "dispute_type", "invoice_amount", "dispute_amount",
    "priority", "assigned_to", "status", "days_open", "resolution_date",
    "resolution_days", "resolution_outcome", "credit_amount",
]

with open(output, "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=fields)
    writer.writeheader()
    writer.writerows(rows)

print(f"Generated {len(rows)} rows -> {output}")

# Summary stats
statuses = {}
for r in rows:
    statuses[r["status"]] = statuses.get(r["status"], 0) + 1

total_dispute_amt = sum(r["dispute_amount"] for r in rows)
open_amt = sum(r["dispute_amount"] for r in rows if r["status"] in ("Open", "In Progress", "Escalated"))
resolved = [r for r in rows if r["resolution_days"] != ""]
avg_res_days = sum(int(r["resolution_days"]) for r in resolved) / len(resolved) if resolved else 0
escalated = statuses.get("Escalated", 0)
total_active = sum(v for k, v in statuses.items() if k in ("Open", "In Progress", "Escalated"))
escalation_rate = escalated / len(rows) * 100

print(f"\nStatus breakdown:")
for s, c in sorted(statuses.items()):
    print(f"  {s}: {c}")
print(f"\nTotal dispute amount: ${total_dispute_amt:,.2f}")
print(f"Open/active dispute amount: ${open_amt:,.2f}")
print(f"Avg resolution days: {avg_res_days:.1f}")
print(f"Escalation rate: {escalation_rate:.1f}%")
print(f"Total rows: {len(rows)}")
