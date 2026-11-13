

from database.db_connection import get_connection


class InventoryService:
    """
    Handles inventory impact calculations.
    """

    def calculate_inventory_impact(
        self,
        current_stock,
        ordered_quantity,
        new_quantity
    ):

        # Calculate the quantity difference
        quantity_difference = new_quantity - ordered_quantity

        # Calculate expected stock after supplier changes
        expected_stock = current_stock + quantity_difference

        if quantity_difference < 0:
            message = "Inventory supply has decreased."

        elif quantity_difference > 0:
            message = "Inventory supply has increased."

        else:
            message = "No inventory impact."

        return {
            "quantity_difference": quantity_difference,
            "expected_stock": expected_stock,
            "message": message
        }

    def get_inventory_plans(self, po_line_id):

        connection = get_connection()
        cursor = connection.cursor()

        try:
            cursor.execute("""
                SELECT
                    inventory_plan_id,
                    po_line_id,
                    source_change_id,
                    projected_quantity,
                    version_no,
                    status
                FROM InventoryPlan
                WHERE po_line_id = ?
                ORDER BY version_no
            """, (po_line_id,))

            return cursor.fetchall()

        finally:
            connection.close()
