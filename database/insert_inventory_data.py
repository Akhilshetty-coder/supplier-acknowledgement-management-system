
from db_connection import get_connection


def insert_inventory_data():

    connection = get_connection()
    cursor = connection.cursor()

    try:

        inventory_records = [

            (
                "INV001",
                "POL001",
                None,
                100,
                "2026-11-12",
                None,
                1,
                "CURRENT"
            ),

            (
                "INV002",
                "POL002",
                None,
                200,
                "2026-11-12",
                None,
                1,
                "CURRENT"
            ),

            (
                "INV003",
                "POL003",
                None,
                150,
                "2026-11-12",
                None,
                1,
                "CURRENT"
            )
        ]

        cursor.executemany("""
            INSERT OR IGNORE INTO InventoryPlan
            (
                inventory_plan_id,
                po_line_id,
                source_change_id,
                projected_quantity,
                effective_from,
                effective_to,
                version_no,
                status
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, inventory_records)

        connection.commit()

        print("Inventory planning data inserted successfully!")

    except Exception as error:

        connection.rollback()
        print("Error:", error)

    finally:

        connection.close()


if __name__ == "__main__":
    insert_inventory_data()
