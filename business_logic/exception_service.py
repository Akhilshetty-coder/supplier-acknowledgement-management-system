import pandas as pd
import os
from datetime import datetime


class ExceptionService:
    """
    Detects exceptions in supplier acknowledgement operations.
    """

    # 1. Check whether a change is approved
    def check_approval_exception(self, approval_status):

        if approval_status != "APPROVED":
            return {
                "anomaly": True,
                "message": "Unapproved change detected."
            }

        return {
            "anomaly": False,
            "message": "Change is approved."
        }

    # 2. Check whether purchase order line exists
    def check_po_line_exception(self, po_line_id):

        from database.db_connection import get_connection

        connection = get_connection()
        cursor = connection.cursor()

        try:
            cursor.execute("""
                SELECT po_line_id
                FROM POLine
                WHERE po_line_id = ?
            """, (po_line_id,))

            result = cursor.fetchone()

            if result is None:
                return {
                    "anomaly": True,
                    "message": "Invalid purchase order line."
                }

            return {
                "anomaly": False,
                "message": "Purchase order line exists."
            }

        finally:
            connection.close()

    # 3. Check promised delivery date
    def check_promise_date_exception(
        self,
        order_date,
        promised_date
    ):

        try:
            order = datetime.strptime(order_date, "%Y-%m-%d")
            promised = datetime.strptime(promised_date, "%Y-%m-%d")

        except ValueError:
            return {
                "anomaly": True,
                "message": "Invalid date format."
            }

        if promised < order:
            return {
                "anomaly": True,
                "message": "Promised date is before order date."
            }

        return {
            "anomaly": False,
            "message": "Promised date is valid."
        }

    # 4. Check acknowledgement revision
    def check_revision_exception(
        self,
        current_revision,
        new_revision
    ):

        if new_revision <= current_revision:
            return {
                "anomaly": True,
                "message": "Older or duplicate acknowledgement revision."
            }

        return {
            "anomaly": False,
            "message": "Acknowledgement revision is valid."
        }


    # 5. Compare actual results with ground truth
    def compare_ground_truth(self, actual_results):

        import pandas as pd
        import os

        base_dir = os.path.dirname(
            os.path.dirname(os.path.abspath(__file__))
        )

        file_path = os.path.join(
            base_dir,
            "data",
            "ground_truth",
            "ground_truth.csv"
        )

        expected_data = pd.read_csv(file_path)

        if len(actual_results) != len(expected_data):
            raise ValueError(
                "Actual results count does not match ground truth."
            )

        comparison = []

        for index, row in expected_data.iterrows():

            expected = row["expected_result"]
            actual = actual_results[index]

            comparison.append({
                "anomaly_id": row["anomaly_id"],
                "scenario": row["scenario"],
                "expected": expected,
                "actual": actual,
                "match": expected == actual
            })

        return comparison

    # 6. Save exception comparison report
    def save_exception_report(self, comparison_results):

        import pandas as pd
        import os

        base_dir = os.path.dirname(
            os.path.dirname(os.path.abspath(__file__))
        )

        report_dir = os.path.join(
            base_dir,
            "reports"
        )

        os.makedirs(report_dir, exist_ok=True)

        report_path = os.path.join(
            report_dir,
            "exception_report.csv"
        )

        report_data = pd.DataFrame(comparison_results)

        report_data.to_csv(
            report_path,
            index=False
        )

        return report_path
