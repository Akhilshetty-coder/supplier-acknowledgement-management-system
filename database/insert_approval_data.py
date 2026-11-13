
from db_connection import get_connection


def insert_approval_data():

    connection = get_connection()
    cursor = connection.cursor()

    try:

        approvals = [

            (
                "APR001",
                "CHG001",
                "PLANNER",
                "PENDING",
                None,
                None,
                "Waiting for planner review"
            ),

            (
                "APR002",
                "CHG001",
                "MANAGER",
                "PENDING",
                None,
                None,
                "Waiting for manager review"
            ),

            (
                "APR003",
                "CHG002",
                "PLANNER",
                "PENDING",
                None,
                None,
                "Waiting for planner review"
            ),

            (
                "APR004",
                "CHG002",
                "MANAGER",
                "PENDING",
                None,
                None,
                "Waiting for manager review"
            )
        ]

        cursor.executemany("""
            INSERT OR IGNORE INTO Approval
            (
                approval_id,
                change_id,
                approval_level,
                decision,
                approver_role,
                decided_at,
                comments
            )
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, approvals)

        connection.commit()

        print("Approval records inserted successfully!")

    except Exception as error:

        connection.rollback()
        print("Error:", error)

    finally:

        connection.close()


if __name__ == "__main__":
    insert_approval_data()
