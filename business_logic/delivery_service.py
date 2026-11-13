
from datetime import datetime
from database.db_connection import get_connection


class DeliveryService:
    """
    Handles supplier delivery date calculations.
    """

    def check_delivery_delay(self, original_date, new_date):

        original = datetime.strptime(original_date, "%Y-%m-%d")
        updated = datetime.strptime(new_date, "%Y-%m-%d")

        delay_days = (updated - original).days

        if delay_days > 0:
            return True, f"Delivery delayed by {delay_days} days."

        elif delay_days < 0:
            return False, f"Delivery is {abs(delay_days)} days earlier."

        else:
            return False, "Delivery date remains unchanged."

    def validate_delivery_date(self, delivery_date):

        try:
            datetime.strptime(delivery_date, "%Y-%m-%d")
            return True, "Delivery date is valid."

        except ValueError:
            return False, "Invalid date. Use YYYY-MM-DD."

    def get_promised_delivery_dates(self, po_line_id):

        connection = get_connection()
        cursor = connection.cursor()

        try:
            cursor.execute("""
                SELECT
                    PromiseDate.promise_id,
                    PromiseDate.promised_date,
                    PromiseDate.is_current,
                    AcknowledgementLine.po_line_id
                FROM PromiseDate
                JOIN AcknowledgementLine
                    ON PromiseDate.ack_line_id =
                       AcknowledgementLine.ack_line_id
                WHERE AcknowledgementLine.po_line_id = ?
                ORDER BY PromiseDate.promise_id
            """, (po_line_id,))

            return cursor.fetchall()

        finally:
            connection.close()
