
from db_connection import get_connection


def insert_change_requests():

    connection = get_connection()
    cursor = connection.cursor()

    try:

        change_requests = [

            (
                "CHG001",
                "POL001",
                "ACKL001",
                "QUANTITY",
                "100",
                "90",
                "PENDING",
                "2026-11-12 12:00:00"
            ),

            (
                "CHG002",
                "POL001",
                "ACKL001",
                "DELIVERY_DATE",
                "2026-11-20",
                "2026-11-25",
                "PENDING",
                "2026-11-12 12:05:00"
            )
        ]

        cursor.executemany("""
            INSERT OR IGNORE INTO ChangeRequest
            (
                change_id,
                po_line_id,
                ack_line_id,
                change_type,
                old_value,
                new_value,
                approval_status,
                created_at
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, change_requests)

        connection.commit()

        print("Purchase order change requests inserted successfully!")

    except Exception as error:

        connection.rollback()
        print("Error:", error)

    finally:

        connection.close()


if __name__ == "__main__":
    insert_change_requests()
