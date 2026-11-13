
import csv
import json
import random
import hashlib
from pathlib import Path
from datetime import datetime, date, timedelta


# ==========================================================
# 1. CONFIGURATION
# ==========================================================

SEED = 20261022

SUPPLIER_COUNT = 500
PO_COUNT = 10000
ACK_COUNT = 10000
CHANGE_COUNT = 5000

BASE_DIR = Path(__file__).resolve().parent.parent
OUTPUT_DIR = BASE_DIR / "data" / "synthetic"

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

random.seed(SEED)

START_DATE = date(2026, 1, 1)
END_DATE = date(2026, 10, 31)


# ==========================================================
# 2. HELPER FUNCTIONS
# ==========================================================

def random_date(start_date, end_date):
    days = (end_date - start_date).days
    return start_date + timedelta(
        days=random.randint(0, days)
    )


def write_csv(filename, records):

    file_path = OUTPUT_DIR / filename

    with open(
        file_path,
        "w",
        newline="",
        encoding="utf-8"
    ) as file:

        writer = csv.DictWriter(
            file,
            fieldnames=list(records[0].keys())
        )

        writer.writeheader()
        writer.writerows(records)

    print(f"{filename}: {len(records)} records")


def calculate_sha256(file_path):

    sha256 = hashlib.sha256()

    with open(file_path, "rb") as file:

        for chunk in iter(lambda: file.read(4096), b""):
            sha256.update(chunk)

    return sha256.hexdigest()


# ==========================================================
# 3. GENERATE SUPPLIERS
# ==========================================================

print("\nGenerating suppliers...")

suppliers = []

for i in range(1, SUPPLIER_COUNT + 1):

    supplier = {
        "supplier_id": f"SUP-{i:04d}",
        "supplier_name": f"Supplier Company {i}",
        "email": f"supplier{i}@example.com",
        "phone": f"90000{i:05d}",
        "supplier_status": random.choice(
            ["ACTIVE", "ACTIVE", "ACTIVE", "INACTIVE"]
        ),
        "created_at": (
            datetime.combine(START_DATE, datetime.min.time())
            + timedelta(days=i)
        ).isoformat()
    }

    suppliers.append(supplier)


# ==========================================================
# 4. GENERATE PURCHASE ORDERS AND PO LINES
# ==========================================================

print("\nGenerating purchase orders and PO lines...")

purchase_orders = []
po_lines = []

for i in range(1, PO_COUNT + 1):

    supplier = suppliers[(i - 1) % SUPPLIER_COUNT]

    order_date = random_date(START_DATE, END_DATE)

    po_id = f"PO-2026-{i:06d}"

    purchase_orders.append({
        "po_id": po_id,
        "supplier_id": supplier["supplier_id"],
        "order_date": order_date.isoformat(),
        "po_status": random.choice([
            "OPEN",
            "OPEN",
            "PARTIALLY_ACKNOWLEDGED"
        ]),
        "currency": "INR"
    })

    for line_number in range(1, 3):

        po_line_id = f"POL-{i:06d}-{line_number:02d}"

        po_lines.append({
            "po_line_id": po_line_id,
            "po_id": po_id,
            "item_code": f"ITEM-{random.randint(1000, 9999)}",
            "item_description": random.choice([
                "Laptop Components",
                "Computer Memory",
                "Electronic Sensors",
                "Circuit Boards",
                "Power Modules"
            ]),
            "requested_quantity": random.randint(50, 500),
            "unit_price": round(
                random.uniform(100, 5000), 2
            )
        })


# ==========================================================
# 5. GENERATE ACKNOWLEDGEMENTS AND ACKNOWLEDGEMENT LINES
# ==========================================================

print("\nGenerating acknowledgements...")

acknowledgements = []
acknowledgement_lines = []
promise_dates = []

for i in range(1, ACK_COUNT + 1):

    po_index = i - 1

    if i == ACK_COUNT:

        # Second revision belongs to the first PO.
        po = purchase_orders[0]
        revision_no = 2
        ack_id = "ACK-010000"
        ack_status = "SUPERSEDED"

    else:

        po = purchase_orders[po_index]
        revision_no = 1
        ack_id = f"ACK-{i:06d}"
        ack_status = "CURRENT"

    po_id = po["po_id"]
    order_date = date.fromisoformat(po["order_date"])

    received_date = order_date + timedelta(
        days=7 if i == ACK_COUNT else random.randint(1, 5)
    )

    acknowledgements.append({
        "ack_id": ack_id,
        "po_id": po_id,
        "revision_no": revision_no,
        "received_at": datetime.combine(
            received_date,
            datetime.min.time()
        ).isoformat(),
        "ack_status": ack_status
    })

    for line_number in range(1, 3):

        if i == ACK_COUNT:
            # Correctly use both PO lines of PO 1.
            po_line = po_lines[line_number - 1]
        else:
            po_line = po_lines[
                (po_index * 2) + line_number - 1
            ]

        ack_line_number = (i - 1) * 2 + line_number

        ack_line_id = f"ACKL-{ack_line_number:06d}"

        requested = po_line["requested_quantity"]

        accepted = random.randint(
            int(requested * 0.85),
            requested
        )

        rejected = requested - accepted

        referenced_po_line_id = po_line["po_line_id"]

        # Intentional anomaly 2:
        # PO 3 acknowledgement references PO 4 line.
        if i == 3 and line_number == 1:
            referenced_po_line_id = po_lines[6]["po_line_id"]

        acknowledgement_lines.append({
            "ack_line_id": ack_line_id,
            "ack_id": ack_id,
            "po_id": po_id,
            "po_line_id": referenced_po_line_id,
            "accepted_quantity": accepted,
            "rejected_quantity": rejected
        })

        promised_date = received_date + timedelta(
            days=random.randint(5, 30)
        )

        # Intentional anomaly 3:
        # Promised date is before the PO order date.
        if i == 2 and line_number == 1:
            promised_date = order_date - timedelta(days=3)

        promise_dates.append({
            "promise_id": f"PROM-{ack_line_number:06d}",
            "ack_line_id": ack_line_id,
            "promised_date": promised_date.isoformat()
        })


# ==========================================================
# 6. GENERATE CHANGE REQUESTS
# ==========================================================

print("\nGenerating change requests...")

change_requests = []

for i in range(1, CHANGE_COUNT + 1):

    po_line = po_lines[(i - 1) * 2]
    ack_line = acknowledgement_lines[(i - 1) * 2]

    old_quantity = po_line["requested_quantity"]

    if i == 1:

        change_type = "QUANTITY"
        new_quantity = int(old_quantity * 0.75)
        approval_status = "PENDING"

    else:

        change_type = random.choice([
            "QUANTITY",
            "PRICE",
            "DELIVERY_DATE"
        ])

        if change_type == "QUANTITY":

            new_quantity = random.randint(
                max(1, int(old_quantity * 0.85)),
                max(1, int(old_quantity * 1.15))
            )

            approval_status = "PENDING"

        else:

            new_quantity = old_quantity

            approval_status = random.choice([
                "PENDING",
                "APPROVED",
                "NOT_REQUIRED"
            ])

    # Deterministic timestamp based on acknowledgement.
    created_at = acknowledgements[i - 1]["received_at"]

    change_requests.append({
        "change_id": f"CHG-{i:06d}",
        "po_id": po_line["po_id"],
        "po_line_id": po_line["po_line_id"],
        "ack_line_id": ack_line["ack_line_id"],
        "change_type": change_type,
        "old_quantity": old_quantity,
        "new_quantity": new_quantity,
        "approval_status": approval_status,
        "created_at": created_at
    })


# ==========================================================
# 7. GENERATE INVENTORY PLANS
# ==========================================================

print("\nGenerating inventory plans...")

inventory_plans = []

for i, po_line in enumerate(po_lines, start=1):

    source_change_id = ""
    planned_quantity = po_line["requested_quantity"]

    # Intentional anomaly 1:
    # Inventory updated before approval.
    if i == 1:

        source_change_id = "CHG-000001"
        planned_quantity = change_requests[0]["new_quantity"]

    inventory_plans.append({
        "inventory_plan_id": f"INV-{i:06d}",
        "po_id": po_line["po_id"],
        "po_line_id": po_line["po_line_id"],
        "source_change_id": source_change_id,
        "planned_quantity": planned_quantity,
        "plan_status": "CURRENT"
    })


# ==========================================================
# 8. GENERATE GROUND TRUTH
# ==========================================================

print("\nGenerating ground truth...")

ground_truth = [
    {
        "anomaly_id": "AN001",
        "record_id": "CHG-000001",
        "scenario": "Unapproved quantity change updates inventory",
        "expected": "ANOMALY",
        "severity": "HIGH"
    },
    {
        "anomaly_id": "AN002",
        "record_id": "ACKL-000005",
        "scenario": "Acknowledgement references wrong PO line",
        "expected": "ANOMALY",
        "severity": "HIGH"
    },
    {
        "anomaly_id": "AN003",
        "record_id": "PROM-000003",
        "scenario": "Promised date before order date",
        "expected": "ANOMALY",
        "severity": "MEDIUM"
    },
    {
        "anomaly_id": "AN004",
        "record_id": "PO-2026-000001",
        "scenario": "Older acknowledgement revision remains current",
        "expected": "ANOMALY",
        "severity": "HIGH"
    }
]


# ==========================================================
# 9. EXPORT DATASETS
# ==========================================================

print("\nExporting CSV datasets...")

datasets = {
    "suppliers.csv": suppliers,
    "purchase_orders.csv": purchase_orders,
    "po_lines.csv": po_lines,
    "acknowledgements.csv": acknowledgements,
    "acknowledgement_lines.csv": acknowledgement_lines,
    "promise_dates.csv": promise_dates,
    "change_requests.csv": change_requests,
    "inventory_plans.csv": inventory_plans,
    "ground_truth.csv": ground_truth
}

for filename, records in datasets.items():
    write_csv(filename, records)


# ==========================================================
# 10. GENERATION REPORT
# ==========================================================

print("\nCreating generation report...")

checksums = {}

for filename in datasets:

    file_path = OUTPUT_DIR / filename

    checksums[filename] = calculate_sha256(file_path)

generation_report = {
    "project": "Supplier Acknowledgement Management System",
    "random_seed": SEED,
    "generation_date": "2026-11-13",
    "generation_method": "Deterministic synthetic CSV generation",
    "record_counts": {
        filename: len(records)
        for filename, records in datasets.items()
    },
    "total_acknowledgement_and_change_events": (
        len(acknowledgements) + len(change_requests)
    ),
    "injected_anomalies": len(ground_truth),
    "sha256_checksums": checksums
}

with open(
    OUTPUT_DIR / "generation_report.json",
    "w",
    encoding="utf-8"
) as file:

    json.dump(generation_report, file, indent=4)


# ==========================================================
# 11. FINAL SUMMARY
# ==========================================================

print("\n======================================")
print("SYNTHETIC DATA GENERATION COMPLETED")
print("======================================")

for filename, records in datasets.items():
    print(f"{filename}: {len(records)}")

print(
    "\nTotal acknowledgement and change events:",
    len(acknowledgements) + len(change_requests)
)

print("Random seed:", SEED)
print("Output folder:", OUTPUT_DIR)
print("\nGeneration report created successfully.")
