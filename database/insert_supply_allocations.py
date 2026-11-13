
from db_connection import get_connection

def insert_supply_allocations():
    connection = get_connection()
    cursor = connection.cursor()

    try:
        allocations = [
            ("ALLOC001", "PROD001", "POL001", 80, "2026-11-12 14:00:00"),
            ("ALLOC002", "PROD002", "POL002", 150, "2026-11-12 14:00:00"),
            ("ALLOC003", "PROD003", "POL003", 100, "2026-11-12 14:00:00")
        ]

        cursor.executemany("""
            INSERT OR IGNORE INTO ProductionOrderSupplyAllocation
            (allocation_id, production_order_id, po_line_id,
             allocated_quantity, created_at)
            VALUES (?, ?, ?, ?, ?)
        """, allocations)

        connection.commit()
        print("Production supply allocations inserted successfully!")

    except Exception as error:
        connection.rollback()
        print("Error:", error)

    finally:
        connection.close()


if __name__ == "__main__":
    insert_supply_allocations()
