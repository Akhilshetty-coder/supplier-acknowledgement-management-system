
import sqlite3
import pandas as pd
import json
from pathlib import Path
from datetime import datetime

# =====================================================
# SYNTHETIC DATA IMPORT
# Supplier Acknowledgement Management System
# =====================================================

BASE_DIR = Path(__file__).resolve().parent.parent
CSV_DIR = BASE_DIR / "data" / "synthetic"
DB_PATH = BASE_DIR / "database" / "supplier_management.db"

BATCH_ID = datetime.now().strftime("%Y%m%d_%H%M%S")


def load_csv(filename):
    path = CSV_DIR / filename

    if not path.exists():
        raise FileNotFoundError(f"Missing CSV: {path}")

    return pd.read_csv(path)


def clean(value):
    if pd.isna(value):
        return None
    return value


def record_dict(row):
    return {
        str(key): clean(value)
        for key, value in row.to_dict().items()
    }


def quarantine(cursor, table, record_id, reason, row):
    cursor.execute("""
        INSERT INTO DataQualityException
        (batch_id, source_table, source_record_id,
         reason, source_json, created_at)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (
        BATCH_ID,
        table,
        str(record_id),
        reason,
        json.dumps(record_dict(row), default=str),
        datetime.now().isoformat(timespec="seconds")
    ))


def main():

    print("\n======================================")
    print("SYNTHETIC DATA IMPORT")
    print("======================================")

    # -------------------------------------------------
    # 1. Load CSV files
    # -------------------------------------------------

    suppliers = load_csv("suppliers.csv")
    pos = load_csv("purchase_orders.csv")
    po_lines = load_csv("po_lines.csv")
    acknowledgements = load_csv("acknowledgements.csv")
    ack_lines = load_csv("acknowledgement_lines.csv")
    promises = load_csv("promise_dates.csv")
    changes = load_csv("change_requests.csv")
    inventory = load_csv("inventory_plans.csv")

    print("All eight CSV files loaded.")

    # -------------------------------------------------
    # 2. Basic ID validation
    # -------------------------------------------------

    datasets = [
        ("Supplier", suppliers, "supplier_id"),
        ("PurchaseOrder", pos, "po_id"),
        ("POLine", po_lines, "po_line_id"),
        ("Acknowledgement", acknowledgements, "ack_id"),
        ("AcknowledgementLine", ack_lines, "ack_line_id"),
        ("PromiseDate", promises, "promise_id"),
        ("ChangeRequest", changes, "change_id"),
        ("InventoryPlan", inventory, "inventory_plan_id")
    ]

    for name, df, id_column in datasets:
        if df[id_column].isna().any():
            raise ValueError(f"{name}: missing primary key")

        if df[id_column].duplicated().any():
            raise ValueError(f"{name}: duplicate primary key")

    # -------------------------------------------------
    # 3. Create lookup dictionaries
    # -------------------------------------------------

    po_map = dict(zip(pos.po_id, pos.supplier_id))
    po_date_map = dict(zip(pos.po_id, pos.order_date))

    line_map = dict(zip(po_lines.po_line_id, po_lines.po_id))

    ack_map = dict(zip(
        acknowledgements.ack_id,
        acknowledgements.po_id
    ))

    ackline_map = {
        row.ack_line_id: {
            "po_id": row.po_id,
            "po_line_id": row.po_line_id,
            "ack_id": row.ack_id
        }
        for row in ack_lines.itertuples(index=False)
    }

    change_map = set(changes.change_id)

    # -------------------------------------------------
    # 4. Connect and start transaction
    # -------------------------------------------------

    connection = sqlite3.connect(DB_PATH)
    connection.execute("PRAGMA foreign_keys = ON")

    cursor = connection.cursor()

    try:
        cursor.execute("BEGIN IMMEDIATE")

        # Create a table to retain rejected source records.
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS DataQualityException (
                exception_id INTEGER PRIMARY KEY AUTOINCREMENT,
                batch_id TEXT NOT NULL,
                source_table TEXT NOT NULL,
                source_record_id TEXT NOT NULL,
                reason TEXT NOT NULL,
                source_json TEXT NOT NULL,
                created_at TEXT NOT NULL
            )
        """)

        # -------------------------------------------------
        # 5. Clear old dependent records in safe order
        # -------------------------------------------------

        delete_tables = [
            "Notification",
            "Approval",
            "ProductionOrderSupplyAllocation",
            "InventoryPlan",
            "PromiseDate",
            "ChangeRequest",
            "AcknowledgementLine",
            "Acknowledgement",
            "POLine",
            "PurchaseOrder",
            "Supplier"
        ]

        for table in delete_tables:
            cursor.execute(f"DELETE FROM {table}")

        print("Old sample workflow records cleared.")

        # -------------------------------------------------
        # 6. Import suppliers
        # -------------------------------------------------

        for row in suppliers.itertuples(index=False):
            cursor.execute("""
                INSERT INTO Supplier
                (supplier_id, supplier_name, email,
                 phone, status, created_at)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (
                row.supplier_id,
                row.supplier_name,
                clean(row.email),
                clean(row.phone),
                row.supplier_status,
                row.created_at
            ))

        # -------------------------------------------------
        # 7. Import purchase orders
        # -------------------------------------------------

        for row in pos.itertuples(index=False):
            cursor.execute("""
                INSERT INTO PurchaseOrder
                (po_id, supplier_id, order_date,
                 currency, status)
                VALUES (?, ?, ?, ?, ?)
            """, (
                row.po_id,
                row.supplier_id,
                row.order_date,
                row.currency,
                row.po_status
            ))

        # -------------------------------------------------
        # 8. Import PO lines
        # requested_date uses PO order_date as fallback.
        # -------------------------------------------------

        for row in po_lines.itertuples(index=False):
            requested_date = po_date_map[row.po_id]

            cursor.execute("""
                INSERT INTO POLine
                (po_line_id, po_id, product_name,
                 requested_quantity, unit_price,
                 requested_date)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (
                row.po_line_id,
                row.po_id,
                row.item_description,
                row.requested_quantity,
                row.unit_price,
                requested_date
            ))

        # -------------------------------------------------
        # 9. Import acknowledgements
        # -------------------------------------------------

        for row in acknowledgements.itertuples(index=False):
            cursor.execute("""
                INSERT INTO Acknowledgement
                (ack_id, po_id, revision_no,
                 received_at, status)
                VALUES (?, ?, ?, ?, ?)
            """, (
                row.ack_id,
                row.po_id,
                row.revision_no,
                row.received_at,
                row.ack_status
            ))

        # -------------------------------------------------
        # 10. Validate acknowledgement lines
        # -------------------------------------------------

        valid_ackline_ids = set()

        for _, row in ack_lines.iterrows():

            ack_id = row["ack_id"]
            po_id = row["po_id"]
            po_line_id = row["po_line_id"]

            reason = None

            if ack_id not in ack_map:
                reason = "Acknowledgement does not exist"

            elif ack_map[ack_id] != po_id:
                reason = "Acknowledgement PO mismatch"

            elif po_line_id not in line_map:
                reason = "PO line does not exist"

            elif line_map[po_line_id] != po_id:
                reason = "AN002: PO line belongs to another PO"

            if reason:
                quarantine(
                    cursor,
                    "AcknowledgementLine",
                    row["ack_line_id"],
                    reason,
                    row
                )
                continue

            cursor.execute("""
                INSERT INTO AcknowledgementLine
                (ack_line_id, ack_id, po_id, po_line_id,
                 accepted_quantity, rejected_quantity,
                 proposed_unit_price)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (
                row["ack_line_id"],
                ack_id,
                po_id,
                po_line_id,
                row["accepted_quantity"],
                row["rejected_quantity"],
                None
            ))

            valid_ackline_ids.add(row["ack_line_id"])

        # -------------------------------------------------
        # 11. Import promise dates
        # effective_from uses acknowledgement received_at.
        # -------------------------------------------------

        for _, row in promises.iterrows():

            ack_line_id = row["ack_line_id"]

            if ack_line_id not in valid_ackline_ids:
                quarantine(
                    cursor,
                    "PromiseDate",
                    row["promise_id"],
                    "Referenced acknowledgement line was quarantined",
                    row
                )
                continue

            ack_id = ackline_map[ack_line_id]["ack_id"]

            received_at = acknowledgements.loc[
                acknowledgements["ack_id"] == ack_id,
                "received_at"
            ].iloc[0]

            cursor.execute("""
                INSERT INTO PromiseDate
                (promise_id, ack_line_id, promised_date,
                 effective_from, effective_to, is_current)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (
                row["promise_id"],
                ack_line_id,
                row["promised_date"],
                received_at,
                None,
                1
            ))

        # -------------------------------------------------
        # 12. Import change requests
        # -------------------------------------------------

        valid_change_ids = set()

        for _, row in changes.iterrows():

            ack_line_id = row["ack_line_id"]
            po_line_id = row["po_line_id"]
            po_id = row["po_id"]

            reason = None

            if ack_line_id not in valid_ackline_ids:
                reason = "Referenced acknowledgement line was quarantined"

            elif po_line_id not in line_map:
                reason = "Referenced PO line does not exist"

            elif line_map[po_line_id] != po_id:
                reason = "Change request PO and PO line mismatch"

            elif (
                ackline_map[ack_line_id]["po_line_id"] != po_line_id
                or ackline_map[ack_line_id]["po_id"] != po_id
            ):
                reason = "Change request and acknowledgement line mismatch"

            if reason:
                quarantine(
                    cursor,
                    "ChangeRequest",
                    row["change_id"],
                    reason,
                    row
                )
                continue

            cursor.execute("""
                INSERT INTO ChangeRequest
                (change_id, po_line_id, ack_line_id,
                 change_type, old_value, new_value,
                 approval_status, created_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                row["change_id"],
                po_line_id,
                ack_line_id,
                row["change_type"],
                str(row["old_quantity"]),
                str(row["new_quantity"]),
                row["approval_status"],
                row["created_at"]
            ))

            valid_change_ids.add(row["change_id"])

        # -------------------------------------------------
        # 13. Import inventory plans
        # -------------------------------------------------

        valid_inventory_count = 0

        for _, row in inventory.iterrows():

            po_line_id = row["po_line_id"]
            source_change_id = clean(row["source_change_id"])

            if po_line_id not in line_map:
                quarantine(
                    cursor,
                    "InventoryPlan",
                    row["inventory_plan_id"],
                    "Referenced PO line does not exist",
                    row
                )
                continue

            if (
                source_change_id is not None
                and source_change_id not in valid_change_ids
            ):
                quarantine(
                    cursor,
                    "InventoryPlan",
                    row["inventory_plan_id"],
                    "Referenced change request was not imported",
                    row
                )
                continue

            if source_change_id is not None:
                effective_from = changes.loc[
                    changes["change_id"] == source_change_id,
                    "created_at"
                ].iloc[0]
            else:
                po_id = line_map[po_line_id]
                effective_from = po_date_map[po_id]

            cursor.execute("""
                INSERT INTO InventoryPlan
                (inventory_plan_id, po_line_id, source_change_id,
                 projected_quantity, effective_from,
                 effective_to, version_no, status)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                row["inventory_plan_id"],
                po_line_id,
                source_change_id,
                row["planned_quantity"],
                effective_from,
                None,
                1,
                row["plan_status"]
            ))

            valid_inventory_count += 1

        # -------------------------------------------------
        # 14. Write audit entry
        # -------------------------------------------------

        cursor.execute("""
            INSERT INTO AuditLog
            (user, action, description, timestamp)
            VALUES (?, ?, ?, ?)
        """, (
            "SYSTEM",
            "SYNTHETIC_DATA_IMPORT",
            f"Synthetic data import batch {BATCH_ID}",
            datetime.now().isoformat(timespec="seconds")
        ))

        # -------------------------------------------------
        # 15. Verify before commit
        # -------------------------------------------------

        fk_errors = cursor.execute(
            "PRAGMA foreign_key_check"
        ).fetchall()

        if fk_errors:
            raise RuntimeError(
                f"Foreign key errors found: {fk_errors[:10]}"
            )

        expected_counts = {
            "Supplier": len(suppliers),
            "PurchaseOrder": len(pos),
            "POLine": len(po_lines),
            "Acknowledgement": len(acknowledgements)
        }

        for table, expected in expected_counts.items():
            actual = cursor.execute(
                f"SELECT COUNT(*) FROM {table}"
            ).fetchone()[0]

            if actual != expected:
                raise RuntimeError(
                    f"{table}: expected {expected}, got {actual}"
                )

        # Commit only after successful verification.
        connection.commit()

        print("\n======================================")
        print("IMPORT SUCCESSFUL")
        print("======================================")

        tables = [
            "Supplier",
            "PurchaseOrder",
            "POLine",
            "Acknowledgement",
            "AcknowledgementLine",
            "PromiseDate",
            "ChangeRequest",
            "InventoryPlan",
            "Approval",
            "Notification",
            "ProductionOrder",
            "ProductionOrderSupplyAllocation",
            "AuditLog",
            "DataQualityException"
        ]

        print("\nFINAL DATABASE RECORD COUNTS")

        for table in tables:
            count = connection.execute(
                f"SELECT COUNT(*) FROM {table}"
            ).fetchone()[0]

            print(f"{table}: {count:,}")

        exception_count = connection.execute("""
            SELECT COUNT(*)
            FROM DataQualityException
            WHERE batch_id = ?
        """, (BATCH_ID,)).fetchone()[0]

        print("\nQuarantined source records:", exception_count)
        print("Inventory records imported:", valid_inventory_count)
        print("Foreign key errors:", len(fk_errors))
        print("Batch ID:", BATCH_ID)

    except Exception as error:
        connection.rollback()

        print("\nIMPORT FAILED")
        print("All database changes rolled back.")
        print("Reason:", error)

        raise

    finally:
        connection.close()


if __name__ == "__main__":
    main()
