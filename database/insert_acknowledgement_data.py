
from db_connection import get_connection


def insert_acknowledgement_data():

    connection = get_connection()
    cursor = connection.cursor()

    try:

        # Insert acknowledgement headers
        acknowledgements = [
            ("ACK001", "PO001", 1, "2026-11-12 10:00:00", "CURRENT"),
            ("ACK002", "PO002", 1, "2026-11-12 11:00:00", "CURRENT")
        ]

        cursor.executemany("""
            INSERT OR IGNORE INTO Acknowledgement
            (ack_id, po_id, revision_no, received_at, status)
            VALUES (?, ?, ?, ?, ?)
        """, acknowledgements)

        # Insert acknowledgement lines
        acknowledgement_lines = [
            ("ACKL001", "ACK001", "PO001", "POL001", 90, 10, None),
            ("ACKL002", "ACK001", "PO001", "POL002", 200, 0, None),
            ("ACKL003", "ACK002", "PO002", "POL003", 150, 0, None)
        ]

        cursor.executemany("""
            INSERT OR IGNORE INTO AcknowledgementLine
            (ack_line_id, ack_id, po_id, po_line_id,
             accepted_quantity, rejected_quantity, proposed_unit_price)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, acknowledgement_lines)

        connection.commit()

        print("Supplier acknowledgement data inserted successfully!")

    except Exception as error:

        connection.rollback()
        print("Error:", error)

    finally:

        connection.close()


if __name__ == "__main__":
    insert_acknowledgement_data()
