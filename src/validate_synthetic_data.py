
import csv
from pathlib import Path
from datetime import date
from collections import defaultdict


# ==========================================================
# 1. CONFIGURATION
# ==========================================================

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data" / "synthetic"
REPORT_DIR = BASE_DIR / "reports"

REPORT_DIR.mkdir(exist_ok=True)

EXPECTED_COUNTS = {
    "suppliers": 500,
    "purchase_orders": 10000,
    "po_lines": 20000,
    "acknowledgements": 10000,
    "acknowledgement_lines": 20000,
    "promise_dates": 20000,
    "change_requests": 5000,
    "inventory_plans": 20000,
    "ground_truth": 4
}

results = []


# ==========================================================
# 2. HELPER FUNCTIONS
# ==========================================================

def load_csv(filename):

    file_path = DATA_DIR / filename

    with open(
        file_path,
        "r",
        encoding="utf-8",
        newline=""
    ) as file:

        return list(csv.DictReader(file))


def add_check(name, actual, expected, passed):

    results.append({
        "check": name,
        "actual": str(actual),
        "expected": str(expected),
        "status": "PASS" if passed else "FAIL"
    })


def duplicate_count(records, field):

    values = [row[field] for row in records]

    return len(values) - len(set(values))


# ==========================================================
# 3. LOAD DATASETS
# ==========================================================

print("\nLoading synthetic datasets...")

suppliers = load_csv("suppliers.csv")
purchase_orders = load_csv("purchase_orders.csv")
po_lines = load_csv("po_lines.csv")
acknowledgements = load_csv("acknowledgements.csv")
acknowledgement_lines = load_csv("acknowledgement_lines.csv")
promise_dates = load_csv("promise_dates.csv")
change_requests = load_csv("change_requests.csv")
inventory_plans = load_csv("inventory_plans.csv")
ground_truth = load_csv("ground_truth.csv")

print("All datasets loaded successfully.")


# ==========================================================
# 4. RECORD COUNT VALIDATION
# ==========================================================

print("\nChecking record counts...")

datasets = {
    "suppliers": suppliers,
    "purchase_orders": purchase_orders,
    "po_lines": po_lines,
    "acknowledgements": acknowledgements,
    "acknowledgement_lines": acknowledgement_lines,
    "promise_dates": promise_dates,
    "change_requests": change_requests,
    "inventory_plans": inventory_plans,
    "ground_truth": ground_truth
}

for name, records in datasets.items():

    actual = len(records)
    expected = EXPECTED_COUNTS[name]

    add_check(
        f"{name} record count",
        actual,
        expected,
        actual == expected
    )


# ==========================================================
# 5. DUPLICATE ID VALIDATION
# ==========================================================

print("\nChecking duplicate IDs...")

primary_keys = {
    "suppliers": (suppliers, "supplier_id"),
    "purchase_orders": (purchase_orders, "po_id"),
    "po_lines": (po_lines, "po_line_id"),
    "acknowledgements": (acknowledgements, "ack_id"),
    "acknowledgement_lines": (
        acknowledgement_lines, "ack_line_id"
    ),
    "promise_dates": (promise_dates, "promise_id"),
    "change_requests": (change_requests, "change_id"),
    "inventory_plans": (
        inventory_plans, "inventory_plan_id"
    ),
    "ground_truth": (ground_truth, "anomaly_id")
}

for name, (records, field) in primary_keys.items():

    duplicates = duplicate_count(records, field)

    add_check(
        f"{name} duplicate IDs",
        duplicates,
        0,
        duplicates == 0
    )


# ==========================================================
# 6. LOOKUP DICTIONARIES
# ==========================================================

supplier_map = {
    row["supplier_id"]: row for row in suppliers
}

po_map = {
    row["po_id"]: row for row in purchase_orders
}

po_line_map = {
    row["po_line_id"]: row for row in po_lines
}

ack_map = {
    row["ack_id"]: row for row in acknowledgements
}

ack_line_map = {
    row["ack_line_id"]: row for row in acknowledgement_lines
}

change_map = {
    row["change_id"]: row for row in change_requests
}


# ==========================================================
# 7. FOREIGN KEY VALIDATION
# ==========================================================

print("\nChecking foreign-key relationships...")

missing_supplier = sum(
    row["supplier_id"] not in supplier_map
    for row in purchase_orders
)

missing_po = sum(
    row["po_id"] not in po_map
    for row in po_lines
)

missing_ack_po = sum(
    row["po_id"] not in po_map
    for row in acknowledgements
)

missing_ack = sum(
    row["ack_id"] not in ack_map
    for row in acknowledgement_lines
)

missing_ack_line_po = sum(
    row["po_id"] not in po_map
    for row in acknowledgement_lines
)

missing_ack_line_po_line = sum(
    row["po_line_id"] not in po_line_map
    for row in acknowledgement_lines
)

missing_promise_ack_line = sum(
    row["ack_line_id"] not in ack_line_map
    for row in promise_dates
)

missing_change_po = sum(
    row["po_id"] not in po_map
    for row in change_requests
)

missing_change_po_line = sum(
    row["po_line_id"] not in po_line_map
    for row in change_requests
)

missing_change_ack_line = sum(
    row["ack_line_id"] not in ack_line_map
    for row in change_requests
)

missing_inventory_po_line = sum(
    row["po_line_id"] not in po_line_map
    for row in inventory_plans
)

missing_inventory_change = sum(
    bool(row["source_change_id"])
    and row["source_change_id"] not in change_map
    for row in inventory_plans
)

foreign_key_checks = {
    "PO supplier references": missing_supplier,
    "PO line references": missing_po,
    "Acknowledgement PO references": missing_ack_po,
    "Acknowledgement line references": missing_ack,
    "Acknowledgement line PO references": missing_ack_line_po,
    "Acknowledgement line PO-line references": missing_ack_line_po_line,
    "Promise date references": missing_promise_ack_line,
    "Change request PO references": missing_change_po,
    "Change request PO-line references": missing_change_po_line,
    "Change request acknowledgement references": missing_change_ack_line,
    "Inventory PO-line references": missing_inventory_po_line,
    "Inventory change references": missing_inventory_change
}

for name, errors in foreign_key_checks.items():

    add_check(
        name,
        errors,
        0,
        errors == 0
    )


# ==========================================================
# 8. COMPOSITE RELATIONSHIP VALIDATION
# ==========================================================

print("\nChecking acknowledgement relationships...")

ack_po_mismatches = 0
po_line_mismatches = []

for row in acknowledgement_lines:

    ack = ack_map.get(row["ack_id"])
    po_line = po_line_map.get(row["po_line_id"])

    if ack and row["po_id"] != ack["po_id"]:
        ack_po_mismatches += 1

    if po_line and row["po_id"] != po_line["po_id"]:
        po_line_mismatches.append(row["ack_line_id"])


add_check(
    "Acknowledgement versus acknowledgement-line PO",
    ack_po_mismatches,
    0,
    ack_po_mismatches == 0
)

expected_wrong_line = ["ACKL-000005"]

add_check(
    "Intentional wrong PO-line reference",
    po_line_mismatches,
    expected_wrong_line,
    po_line_mismatches == expected_wrong_line
)


# ==========================================================
# 9. STATUS VALIDATION
# ==========================================================

print("\nChecking allowed statuses...")

allowed_statuses = {
    "supplier": {"ACTIVE", "INACTIVE", "BLOCKED"},
    "purchase_order": {
        "OPEN",
        "PARTIALLY_ACKNOWLEDGED",
        "ACKNOWLEDGED",
        "CLOSED",
        "CANCELLED"
    },
    "acknowledgement": {
        "RECEIVED",
        "CURRENT",
        "SUPERSEDED",
        "INVALID"
    },
    "change": {
        "NOT_REQUIRED",
        "PENDING",
        "APPROVED",
        "REJECTED"
    },
    "inventory": {"CURRENT", "SUPERSEDED"}
}

status_errors = 0

for row in suppliers:
    if row["supplier_status"] not in allowed_statuses["supplier"]:
        status_errors += 1

for row in purchase_orders:
    if row["po_status"] not in allowed_statuses["purchase_order"]:
        status_errors += 1

for row in acknowledgements:
    if row["ack_status"] not in allowed_statuses["acknowledgement"]:
        status_errors += 1

for row in change_requests:
    if row["approval_status"] not in allowed_statuses["change"]:
        status_errors += 1

for row in inventory_plans:
    if row["plan_status"] not in allowed_statuses["inventory"]:
        status_errors += 1

add_check(
    "Allowed status values",
    status_errors,
    0,
    status_errors == 0
)


# ==========================================================
# 10. QUANTITY AND PRICE VALIDATION
# ==========================================================

print("\nChecking quantities and prices...")

quantity_errors = 0
price_errors = 0

for row in po_lines:

    if int(row["requested_quantity"]) <= 0:
        quantity_errors += 1

    if float(row["unit_price"]) <= 0:
        price_errors += 1

for row in acknowledgement_lines:

    accepted = int(row["accepted_quantity"])
    rejected = int(row["rejected_quantity"])

    if accepted < 0 or rejected < 0:
        quantity_errors += 1

for row in change_requests:

    if int(row["old_quantity"]) <= 0:
        quantity_errors += 1

    if int(row["new_quantity"]) <= 0:
        quantity_errors += 1

for row in inventory_plans:

    if int(row["planned_quantity"]) <= 0:
        quantity_errors += 1

add_check(
    "Negative or zero quantity errors",
    quantity_errors,
    0,
    quantity_errors == 0
)

add_check(
    "Negative or zero price errors",
    price_errors,
    0,
    price_errors == 0
)


# ==========================================================
# 11. PROMISED DATE VALIDATION
# ==========================================================

print("\nChecking promised dates...")

invalid_promised_dates = []

for row in promise_dates:

    ack_line = ack_line_map.get(row["ack_line_id"])

    if not ack_line:
        continue

    ack = ack_map.get(ack_line["ack_id"])

    if not ack:
        continue

    po = po_map.get(ack["po_id"])

    if not po:
        continue

    promised = date.fromisoformat(row["promised_date"])
    order = date.fromisoformat(po["order_date"])

    if promised < order:
        invalid_promised_dates.append(row["promise_id"])


add_check(
    "Intentional promised-date anomaly",
    invalid_promised_dates,
    ["PROM-000003"],
    invalid_promised_dates == ["PROM-000003"]
)


# ==========================================================
# 12. ACKNOWLEDGEMENT REVISION VALIDATION
# ==========================================================

print("\nChecking acknowledgement revisions...")

ack_by_po = defaultdict(list)

for row in acknowledgements:
    ack_by_po[row["po_id"]].append(row)

revision_anomalies = []

for po_id, records in ack_by_po.items():

    latest = max(
        records,
        key=lambda row: int(row["revision_no"])
    )

    if latest["ack_status"] != "CURRENT":
        revision_anomalies.append(po_id)


add_check(
    "Intentional revision anomaly",
    revision_anomalies,
    ["PO-2026-000001"],
    revision_anomalies == ["PO-2026-000001"]
)


# ==========================================================
# 13. INVENTORY AND APPROVAL VALIDATION
# ==========================================================

print("\nChecking inventory and approval consistency...")

inventory_anomalies = []

for row in inventory_plans:

    change_id = row["source_change_id"]

    if not change_id:
        continue

    change = change_map.get(change_id)

    if not change:
        continue

    if (
        change["approval_status"] == "PENDING"
        and int(row["planned_quantity"]) == int(change["new_quantity"])
        and int(change["new_quantity"]) != int(change["old_quantity"])
    ):
        inventory_anomalies.append(change_id)


add_check(
    "Intentional pending approval inventory anomaly",
    inventory_anomalies,
    ["CHG-000001"],
    inventory_anomalies == ["CHG-000001"]
)


# ==========================================================
# 14. GROUND TRUTH VALIDATION
# ==========================================================

print("\nChecking ground truth labels...")

expected_anomalies = {
    "AN001": "CHG-000001",
    "AN002": "ACKL-000005",
    "AN003": "PROM-000003",
    "AN004": "PO-2026-000001"
}

actual_anomalies = {
    row["anomaly_id"]: row["record_id"]
    for row in ground_truth
}

add_check(
    "Ground truth anomaly labels",
    actual_anomalies,
    expected_anomalies,
    actual_anomalies == expected_anomalies
)


# ==========================================================
# 15. SAVE VALIDATION REPORT
# ==========================================================

print("\nCreating validation report...")

report_path = REPORT_DIR / "synthetic_validation_report.csv"

with open(
    report_path,
    "w",
    newline="",
    encoding="utf-8"
) as file:

    writer = csv.DictWriter(
        file,
        fieldnames=["check", "actual", "expected", "status"]
    )

    writer.writeheader()
    writer.writerows(results)


# ==========================================================
# 16. FINAL SUMMARY
# ==========================================================

passed = sum(
    row["status"] == "PASS"
    for row in results
)

failed = sum(
    row["status"] == "FAIL"
    for row in results
)

print("\n======================================")
print("SYNTHETIC DATA VALIDATION SUMMARY")
print("======================================")

for row in results:

    print(
        f"{row['status']:4} | {row['check']} "
        f"| Actual: {row['actual']} "
        f"| Expected: {row['expected']}"
    )

print("\nTotal checks:", len(results))
print("Passed:", passed)
print("Failed:", failed)

print("\nValidation report:", report_path)

if failed == 0:
    print("\nAll validation checks passed!")
else:
    print("\nSome validation checks failed. Review the report.")
