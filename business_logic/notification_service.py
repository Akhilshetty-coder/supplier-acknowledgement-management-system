
from database.db_connection import get_connection


class NotificationService:
    """
    Handles system notification messages.
    """

    def generate_notification(self, event_type, message):

        notifications = {
            "ACKNOWLEDGEMENT": "New supplier acknowledgement received.",
            "DELIVERY_DELAY": "Supplier delivery date has been delayed.",
            "APPROVAL_REQUIRED": "Purchase order change requires approval.",
            "APPROVED": "Purchase order change has been approved.",
            "REJECTED": "Purchase order change has been rejected."
        }

        # Check whether the event type is valid
        if event_type not in notifications:
            return {
                "success": False,
                "message": "Invalid notification event."
            }

        return {
            "success": True,
            "event": event_type,
            "notification": notifications[event_type],
            "details": message
        }

    def get_notifications(self, recipient_role):

        connection = get_connection()
        cursor = connection.cursor()

        try:
            cursor.execute("""
                SELECT
                    notification_id,
                    po_id,
                    change_id,
                    production_order_id,
                    recipient_role,
                    message,
                    notification_status
                FROM Notification
                WHERE recipient_role = ?
                ORDER BY notification_id
            """, (recipient_role,))

            return cursor.fetchall()

        finally:
            connection.close()
