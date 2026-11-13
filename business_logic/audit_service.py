
from datetime import datetime
from database.db_connection import get_connection


class AuditService:
    """
    Maintains audit history of system activities.
    """

    def create_audit_record(
        self,
        user,
        action,
        description
    ):

        # Capture current date and time
        current_time = datetime.now()

        # Create audit record
        audit_record = {
            "user": user,
            "action": action,
            "description": description,
            "timestamp": current_time.strftime(
                "%Y-%m-%d %H:%M:%S"
            )
        }

        return audit_record

    def save_audit_record(self, user, action, description):

        # Create audit record
        audit_record = self.create_audit_record(
            user,
            action,
            description
        )

        connection = get_connection()
        cursor = connection.cursor()

        try:
            cursor.execute("""
                INSERT INTO AuditLog (
                    user,
                    action,
                    description,
                    timestamp
                )
                VALUES (?, ?, ?, ?)
            """, (
                audit_record["user"],
                audit_record["action"],
                audit_record["description"],
                audit_record["timestamp"]
            ))

            connection.commit()

            return "Audit record saved successfully."

        finally:
            connection.close()

    def get_audit_history(self):

        connection = get_connection()
        cursor = connection.cursor()

        try:
            cursor.execute("""
                SELECT
                    audit_id,
                    user,
                    action,
                    description,
                    timestamp
                FROM AuditLog
                ORDER BY audit_id
            """)

            return cursor.fetchall()

        finally:
            connection.close()
