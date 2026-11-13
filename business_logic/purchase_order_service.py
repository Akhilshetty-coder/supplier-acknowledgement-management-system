
from datetime import datetime
from database.db_connection import get_connection


class PurchaseOrderService:
    """
    Handles purchase order change validations.
    """

    def validate_quantity_change(self, new_quantity):

        if new_quantity <= 0:
            return False, "Purchase order quantity must be greater than zero."

        return True, "Quantity change is valid."

    def validate_delivery_date(self, new_delivery_date):

        try:
            datetime.strptime(new_delivery_date, "%Y-%m-%d")
        except ValueError:
            return False, "Invalid delivery date format. Use YYYY-MM-DD."

        return True, "Delivery date is valid."

    def get_purchase_order_details(self, po_line_id):

        connection = get_connection()
        cursor = connection.cursor()

        try:
            cursor.execute("""
                SELECT
                    po_line_id,
                    po_id,
                    product_name,
                    requested_quantity,
                    unit_price,
                    requested_date
                FROM POLine
                WHERE po_line_id = ?
            """, (po_line_id,))

            result = cursor.fetchone()

            if result is None:
                return None

            return result

        finally:
            connection.close()
