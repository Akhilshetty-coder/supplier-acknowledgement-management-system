
from database.db_connection import get_connection


class ApprovalService:
    """
    Handles approval decisions for purchase order changes.
    """

    def check_approval_required(self, ordered_quantity, new_quantity):

        if ordered_quantity <= 0:
            return False, "Ordered quantity must be greater than zero."

        difference = abs(ordered_quantity - new_quantity)

        percentage_change = (difference / ordered_quantity) * 100

        if percentage_change > 10:
            return True, "Operations Manager approval required."

        return False, "Planner can handle this change."

    def validate_approval_status(self, status):

        allowed_statuses = [
            "PENDING",
            "APPROVED",
            "REJECTED"
        ]

        if status not in allowed_statuses:
            return False, "Invalid approval status."

        return True, "Approval status is valid."

    def get_pending_approvals(self):

        connection = get_connection()
        cursor = connection.cursor()

        try:
            cursor.execute("""
                SELECT
                    Approval.approval_id,
                    Approval.change_id,
                    ChangeRequest.change_type,
                    Approval.approval_level,
                    Approval.decision,
                    Approval.comments
                FROM Approval
                JOIN ChangeRequest
                    ON Approval.change_id = ChangeRequest.change_id
                WHERE Approval.decision = 'PENDING'
                ORDER BY Approval.approval_id
            """)

            return cursor.fetchall()

        finally:
            connection.close()
