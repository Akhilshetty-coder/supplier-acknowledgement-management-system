
from db_connection import get_connection


def insert_promise_dates():

    connection = get_connection()
    cursor = connection.cursor()

    try:

        promise_dates = [
            ("PROM001", "ACKL001", "2026-11-25",
             "2026-11-12", None, 1),

            ("PROM002", "ACKL002", "2026-11-22",
             "2026-11-12", None, 1),

            ("PROM003", "ACKL003", "2026-11-28",
             "2026-11-12", None, 1)
        ]

        cursor.executemany("""
            INSERT OR IGNORE INTO PromiseDate
            (
                promise_id,
                ack_line_id,
                promised_date,
                effective_from,
                effective_to,
                is_current
            )
            VALUES (?, ?, ?, ?, ?, ?)
        """, promise_dates)

        connection.commit()

        print("Promised delivery dates inserted successfully!")

    except Exception as error:

        connection.rollback()
        print("Error:", error)

    finally:

        connection.close()


if __name__ == "__main__":
    insert_promise_dates()