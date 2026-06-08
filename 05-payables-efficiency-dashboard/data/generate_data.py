"""
Dashboard 05 — Payables Efficiency Dashboard
Generates payables_data.csv with ~750 rows of AP invoice data
for tracking DPO, on-time payment rates, and early discount capture.
"""
import csv
import random
from datetime import date, timedelta

random.seed(42)

VENDORS = [
    ("VND-001", "Acme Supplies Co.",      "Materials"),
    ("VND-002", "TechCore Solutions",     "IT"),
    ("VND-003", "FastShip Logistics",     "Logistics"),
    ("VND-004", "BuildRight Materials",   "Materials"),
    ("VND-005", "CloudSys Inc.",          "IT"),
    ("VND-006", "PowerGrid Utilities",    "Utilities"),
    ("VND-007", "ProStaff Services",      "Services"),
    ("VND-008", "GreenEnergy Corp.",      "Utilities"),
    ("VND-009", "MetalWorks Ltd.",        "Materials"),
    ("VND-010", "DataBridge IT",          "IT"),
    ("VND-011", "QuickFreight Inc.",      "Logistics"),
    ("VND-012", "FacilityPro Services",   "Facilities"),
    ("VND-013", "SafetyFirst Supplies",   "Materials"),
    ("VND-014", "NetConnect Systems",     "IT"),
    ("VND-015", "ExpressRoute Logistics", "Logistics"),
    ("VND-016", "CleanWater Utilities",   "Utilities"),
    ("VND-017", "OfficePro Services",     "Services"),
    ("VND-018", "BuildFast Materials",    "Materials"),
    ("VND-019", "SkyNet IT Solutions",    "IT"),
    ("VND-020", "TrustBuild Facilities",  "Facilities"),
    ("VND-021", "PrimePack Logistics",    "Logistics"),
    ("VND-022", "Apex Consulting",        "Services"),
    ("VND-023", "CoolTech Systems",       "IT"),
    ("VND-024", "EliteFacilities Corp.",  "Facilities"),
    ("VND-025", "RapidShip Co.",          "Logistics"),
]

REGIONS = ["North", "South", "East", "West", "Central"]
APPROVERS = ["Sofia Reyes", "Marco Diaz", "Laura Chen", "Pedro Alvarez", "Ana Torres"]
PAY_METHODS = ["ACH", "Wire", "Check", "Credit Card"]
TERMS = [15, 30, 30, 30, 45, 60, 60, 90]   # weighted toward 30

# Early-payment discount terms (% if paid within X days)
DISCOUNT_TERMS = {
    15: (0.02, 5),   # 2% if paid within 5 days
    30: (0.01, 10),  # 1% if paid within 10 days
    45: (0.015, 15), # 1.5% if paid within 15 days
    60: (0.01, 20),  # 1% if paid within 20 days
    90: (0.005, 30), # 0.5% if paid within 30 days
}

BASE_DATE = date(2025, 1, 1)
END_DATE  = date(2026, 5, 31)

rows = []
total_days = (END_DATE - BASE_DATE).days

for invoice_num in range(1, 751):
    vendor = random.choice(VENDORS)
    vid, vname, vcat = vendor
    region = random.choice(REGIONS)
    approver = random.choice(APPROVERS)
    method = random.choice(PAY_METHODS)
    terms = random.choice(TERMS)

    invoice_date = BASE_DATE + timedelta(days=random.randint(0, total_days))
    if invoice_date > END_DATE:
        invoice_date = END_DATE - timedelta(days=random.randint(1, 30))
    due_date = invoice_date + timedelta(days=terms)

    # Invoice amount: varies by category
    base = {"IT": (5000, 80000), "Materials": (2000, 50000),
            "Logistics": (1000, 20000), "Services": (3000, 40000),
            "Utilities": (500, 15000), "Facilities": (2000, 35000)}
    lo, hi = base.get(vcat, (1000, 50000))
    invoice_amount = round(random.uniform(lo, hi), 2)

    # Discount terms for this invoice (70% have discount terms)
    has_discount_terms = random.random() < 0.70
    disc_rate, disc_window = DISCOUNT_TERMS.get(terms, (0.01, 10)) if has_discount_terms else (0.0, 0)

    # Payment behavior: 85% paid, 10% partial, 5% still outstanding
    roll = random.random()
    if due_date > date(2026, 4, 1) and random.random() < 0.4:
        # Recent invoices more likely pending
        payment_status = "Pending"
        paid_amount = 0.0
        payment_date = ""
        days_to_pay = None
        days_early_late = None
        is_on_time = None
        discount_captured = False
        discount_amount = 0.0
    elif roll < 0.78:
        payment_status = "Paid"
        # Actual payment: most on-time, some early, some late
        bias = random.gauss(0, 8)   # days relative to due_date
        delta = int(bias)
        actual_pay = due_date + timedelta(days=delta)
        actual_pay = max(invoice_date + timedelta(days=1), actual_pay)
        actual_pay = min(actual_pay, END_DATE)
        payment_date = actual_pay.isoformat()
        paid_amount = invoice_amount
        days_to_pay = (actual_pay - invoice_date).days
        days_early_late = (due_date - actual_pay).days   # positive = early
        is_on_time = days_early_late >= 0
        # Discount capture: paid early enough?
        discount_captured = has_discount_terms and days_early_late >= (terms - disc_window)
        discount_amount = round(invoice_amount * disc_rate, 2) if discount_captured else 0.0
    elif roll < 0.90:
        payment_status = "Partial"
        paid_amount = round(invoice_amount * random.uniform(0.3, 0.8), 2)
        actual_pay = due_date + timedelta(days=random.randint(-5, 20))
        actual_pay = max(invoice_date + timedelta(days=1), actual_pay)
        actual_pay = min(actual_pay, END_DATE)
        payment_date = actual_pay.isoformat()
        days_to_pay = (actual_pay - invoice_date).days
        days_early_late = (due_date - actual_pay).days
        is_on_time = days_early_late >= 0
        discount_captured = False
        discount_amount = 0.0
    else:
        payment_status = "Overdue"
        paid_amount = 0.0
        payment_date = ""
        days_to_pay = None
        days_early_late = (due_date - END_DATE).days   # negative (past due)
        is_on_time = False
        discount_captured = False
        discount_amount = 0.0

    outstanding_balance = round(invoice_amount - paid_amount, 2)

    rows.append({
        "invoice_id":         f"AP-{invoice_num:04d}",
        "vendor_id":          vid,
        "vendor_name":        vname,
        "vendor_category":    vcat,
        "region":             region,
        "approver":           approver,
        "invoice_date":       invoice_date.isoformat(),
        "due_date":           due_date.isoformat(),
        "payment_terms":      terms,
        "invoice_amount":     invoice_amount,
        "paid_amount":        paid_amount,
        "outstanding_balance":outstanding_balance,
        "payment_date":       payment_date,
        "payment_status":     payment_status,
        "payment_method":     method,
        "days_to_pay":        days_to_pay if days_to_pay is not None else "",
        "days_early_late":    days_early_late if days_early_late is not None else "",
        "is_on_time":         ("Yes" if is_on_time else "No") if is_on_time is not None else "",
        "has_discount_terms": "Yes" if has_discount_terms else "No",
        "discount_rate":      disc_rate,
        "discount_captured":  "Yes" if discount_captured else "No",
        "discount_amount":    discount_amount,
    })


# Write CSV
cols = list(rows[0].keys())
out = "C:/Users/User/Project Program/dashboard-tools-10-ap-and-ar/05-payables-efficiency-dashboard/data/payables_data.csv"
with open(out, "w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=cols)
    w.writeheader()
    w.writerows(rows)

# Print summary
from collections import Counter
print(f"Total rows: {len(rows)}")
print("payment_status:", dict(Counter(r["payment_status"] for r in rows)))
print("vendor_category:", dict(Counter(r["vendor_category"] for r in rows)))
print("is_on_time (paid):", dict(Counter(r["is_on_time"] for r in rows if r["is_on_time"])))
total_ap = sum(r["outstanding_balance"] for r in rows)
total_disc = sum(r["discount_amount"] for r in rows)
paid_rows = [r for r in rows if r["payment_status"] == "Paid"]
avg_dtp = sum(int(r["days_to_pay"]) for r in paid_rows) / len(paid_rows)
print(f"Total AP Outstanding: ${total_ap:,.2f}")
print(f"Total Discounts Captured: ${total_disc:,.2f}")
print(f"Avg Days to Pay (Paid invoices): {avg_dtp:.1f}")
on_time = sum(1 for r in rows if r["is_on_time"] == "Yes")
paid_partial = sum(1 for r in rows if r["payment_status"] in ("Paid", "Partial"))
print(f"On-Time Rate: {on_time}/{paid_partial} = {on_time/paid_partial*100:.1f}%")
