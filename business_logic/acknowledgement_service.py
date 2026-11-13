
from database.db_connection import get_connection


class AcknowledgementService:
    """
    Handles supplier acknowledgement business operations.
    """

    def validate_acknowledgement(self, acknowledged_quantity, ordered_quantity):

        # Check whether acknowledged quantity is valid
        if acknowledged_quantity <= 0:
            return False, "Acknowledged quantity must be greater than zero."

        # Check whether acknowledged quantity exceeds ordered quantity
        if acknowledged_quantity > ordered_quantity:
            return False, "Acknowledged quantity cannot exceed ordered quantity."

        return True, "Acknowledgement is valid."

    def get_ordered_quantity(self, po_line_id):

        # Connect to SQLite database
        connection = get_connection()
        cursor = connection.cursor()

        try:
            cursor.execute("""
                SELECT requested_quantity
                FROM POLine
                WHERE po_line_id = ?
            """, (po_line_id,))

            result = cursor.fetchone()

            if result is None:
                return None

            return result[0]

        finally:
            connection.close()

    def validate_database_acknowledgement(
        self, po_line_id, acknowledged_quantity
    ):

        # Get ordered quantity from database
        ordered_quantity = self.get_ordered_quantity(po_line_id)

        if ordered_quantity is None:
            return False, "Purchase order line not found."

        # Validate supplier acknowledgement
        return self.validate_acknowledgement(
            acknowledged_quantity,
            ordered_quantity
        )
