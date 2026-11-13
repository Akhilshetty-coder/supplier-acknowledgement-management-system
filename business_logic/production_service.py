

from database.db_connection import get_connection


class ProductionService:
    """
    Handles production schedule impact calculations.
    """

    def check_production_impact(
        self,
        required_quantity,
        available_quantity,
        delay_days
    ):

        # Calculate the shortage quantity
        shortage = required_quantity - available_quantity

        # Check whether production has enough materials
        if shortage > 0:
            if delay_days > 0:
                return {
                    "impact": True,
                    "shortage": shortage,
                    "delay_days": delay_days,
                    "status": "Production at risk due to material shortage and delivery delay."
                }

            return {
                "impact": True,
                "shortage": shortage,
                "delay_days": delay_days,
                "status": "Production at risk due to material shortage."
            }

        # Check whether delivery delay affects production
        if delay_days > 0:
            return {
                "impact": True,
                "shortage": 0,
                "delay_days": delay_days,
                "status": "Production schedule may be delayed."
            }

        return {
            "impact": False,
            "shortage": 0,
            "delay_days": 0,
            "status": "No production impact."
        }

    def get_production_details(self, po_line_id):

        connection = get_connection()
        cursor = connection.cursor()

        try:
            cursor.execute("""
                SELECT
                    ProductionOrder.production_order_id,
                    ProductionOrder.product_name,
                    ProductionOrder.required_quantity,
                    ProductionOrder.required_date,
                    ProductionOrder.status,
                    ProductionOrderSupplyAllocation.allocated_quantity
                FROM ProductionOrder
                JOIN ProductionOrderSupplyAllocation
                    ON ProductionOrder.production_order_id =
                       ProductionOrderSupplyAllocation.production_order_id
                WHERE ProductionOrderSupplyAllocation.po_line_id = ?
                ORDER BY ProductionOrder.production_order_id
            """, (po_line_id,))

            return cursor.fetchall()

        finally:
            connection.close()
