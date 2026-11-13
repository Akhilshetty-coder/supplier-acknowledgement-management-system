
from db_connection import get_connection

def verify_all_data():
    connection = get_connection()
    cursor = connection.cursor()

    tables = [
        "Supplier",
        "PurchaseOrder",
        "POLine",
        "Acknowledgement",
        "AcknowledgementLine",
        "PromiseDate",
        "ChangeRequest",
        "Approval",
        "InventoryPlan",
        "ProductionOrder",
        "ProductionOrderSupplyAllocation",
        "Notification"
    ]

    try:
        print("FINAL DATABASE VALIDATION")
        print("=========================")

        for table in tables:
            cursor.execute(f"SELECT COUNT(*) FROM {table}")
            count = cursor.fetchone()[0]
            print(f"{table}: {count} records")

        print("\nFOREIGN KEY VALIDATION")
        print("=====================")

        cursor.execute("PRAGMA foreign_key_check")
        errors = cursor.fetchall()

        if errors:
            print("Foreign key errors found:")
            for error in errors:
                print(error)
        else:
            print("Foreign key validation passed!")
            print("No relationship errors found.")

        print("\nTotal tables:", len(tables))

    except Exception as error:
        print("Error:", error)

    finally:
        connection.close()


if __name__ == "__main__":
    verify_all_data()
