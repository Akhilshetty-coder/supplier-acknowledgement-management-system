
from db_connection import get_connection


def insert_sample_data():

    connection = get_connection()
    cursor = connection.cursor()

    try:

        # Insert suppliers
        suppliers = [
            ("SUP001", "ABC Electronics", "abc@gmail.com",
             "9876543210", "ACTIVE"),

            ("SUP002", "Global Components", "global@gmail.com",
             "9876543211", "ACTIVE")
        ]

        cursor.executemany("""
            INSERT OR IGNORE INTO Supplier
            (supplier_id, supplier_name, email, phone, status)
            VALUES (?, ?, ?, ?, ?)
        """, suppliers)

        # Insert purchase orders
        purchase_orders = [
            ("PO001", "SUP001", "2026-11-01", "INR", "OPEN"),
            ("PO002", "SUP002", "2026-11-02", "INR", "OPEN")
        ]

        cursor.executemany("""
            INSERT OR IGNORE INTO PurchaseOrder
            (po_id, supplier_id, order_date, currency, status)
            VALUES (?, ?, ?, ?, ?)
        """, purchase_orders)

        # Insert purchase order lines
        po_lines = [
            ("POL001", "PO001", "Laptop Components",
             100, 5000, "2026-11-20"),

            ("POL002", "PO001", "Computer Memory",
             200, 1500, "2026-11-22"),

            ("POL003", "PO002", "Electronic Sensors",
             150, 800, "2026-11-25")
        ]

        cursor.executemany("""
            INSERT OR IGNORE INTO POLine
            (po_line_id, po_id, product_name,
             requested_quantity, unit_price, requested_date)
            VALUES (?, ?, ?, ?, ?, ?)
        """, po_lines)

        connection.commit()

        print("Sample master data inserted successfully!")

    except Exception as error:

        connection.rollback()
        print("Error:", error)

    finally:

        connection.close()


if __name__ == "__main__":
    insert_sample_data()
