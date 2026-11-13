
from db_connection import get_connection

def insert_notification_data():
    connection = get_connection()
    cursor = connection.cursor()

    try:
        notifications = [
            (
                "NOT001",
                "PO001",
                "CHG001",
                "PROD001",
                "Planner",
                "Supplier acknowledged 90 of 100 Laptop Components; quantity change pending approval.",
                "PENDING",
                "2026-11-12 15:00:00"
            ),
            (
                "NOT002",
                "PO001",
                "CHG002",
                "PROD001",
                "Manager",
                "Supplier proposed delivery date change from 2026-11-20 to 2026-11-25; approval pending.",
                "PENDING",
                "2026-11-12 15:05:00"
            ),
            (
                "NOT003",
                "PO002",
                None,
                "PROD003",
                "Planner",
                "Supplier confirmed delivery of Electronic Sensors for 2026-11-28.",
                "PENDING",
                "2026-11-12 15:10:00"
            )
        ]

        cursor.executemany("""
            INSERT OR IGNORE INTO Notification
            (
                notification_id,
                po_id,
                change_id,
                production_order_id,
                recipient_role,
                message,
                notification_status,
                created_at
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, notifications)

        connection.commit()
        print("Notifications inserted successfully!")

    except Exception as error:
        connection.rollback()
        print("Error:", error)

    finally:
        connection.close()


if __name__ == "__main__":
    insert_notification_data()
