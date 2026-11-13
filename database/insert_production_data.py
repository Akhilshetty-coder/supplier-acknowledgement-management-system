
from db_connection import get_connection


def insert_production_data():

    connection = get_connection()
    cursor = connection.cursor()

    try:

        production_orders = [

            (
                "PROD001",
                "Laptop Components",
                80,
                "2026-11-24",
                "PLANNED"
            ),

            (
                "PROD002",
                "Computer Memory",
                150,
                "2026-11-23",
                "PLANNED"
            ),

            (
                "PROD003",
                "Electronic Sensors",
                100,
                "2026-11-27",
                "PLANNED"
            )
        ]

        cursor.executemany("""
            INSERT OR IGNORE INTO ProductionOrder
            (
                production_order_id,
                product_name,
                required_quantity,
                required_date,
                status
            )
            VALUES (?, ?, ?, ?, ?)
        """, production_orders)

        connection.commit()

        print("Production orders inserted successfully!")

    except Exception as error:

        connection.rollback()
        print("Error:", error)

    finally:

        connection.close()


if __name__ == "__main__":
    insert_production_data()
