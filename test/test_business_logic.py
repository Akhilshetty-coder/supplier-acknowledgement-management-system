
from business_logic.acknowledgement_service import AcknowledgementService
from business_logic.purchase_order_service import PurchaseOrderService
from business_logic.approval_service import ApprovalService
from business_logic.delivery_service import DeliveryService
from business_logic.inventory_service import InventoryService
from business_logic.production_service import ProductionService
from business_logic.notification_service import NotificationService
from business_logic.audit_service import AuditService
from business_logic.exception_service import ExceptionService

print("\n===== BUSINESS LOGIC TESTING =====")

# Database test IDs from the synthetic dataset
VALID_PO_LINE_1 = "POL-000001-01"
VALID_PO_LINE_2 = "POL-000001-02"
INVALID_PO_LINE = "POL999"


# 1. Acknowledgement Service
ack = AcknowledgementService()
print("\n1. Acknowledgement:")
print(ack.validate_acknowledgement(80, 100))


# 2. Purchase Order Service
po = PurchaseOrderService()
print("\n2. Purchase Order:")
print(po.validate_quantity_change(100))
print(po.validate_delivery_date("2026-12-15"))


# 3. Approval Service
approval = ApprovalService()
print("\n3. Approval:")
print(approval.check_approval_required(100, 120))
print(approval.validate_approval_status("APPROVED"))


# 4. Delivery Service
delivery = DeliveryService()
print("\n4. Delivery:")
print(delivery.check_delivery_delay(
    "2026-12-10", "2026-12-15"
))


# 5. Inventory Service
inventory = InventoryService()
print("\n5. Inventory:")
print(inventory.calculate_inventory_impact(50, 100, 80))


# 6. Production Service
production = ProductionService()
print("\n6. Production:")
print(production.check_production_impact(100, 70, 5))


# 7. Notification Service
notification = NotificationService()
print("\n7. Notification:")
print(notification.generate_notification(
    "DELIVERY_DELAY",
    "Supplier delivery delayed by 5 days."
))


# 8. Audit Service
audit = AuditService()
print("\n8. Audit:")
print(audit.create_audit_record(
    "Planner",
    "APPROVED",
    "Purchase order PO101 approved."
))


# 9. Acknowledgement Database Integration
print("\n9. Acknowledgement Database Integration:")

print("\nTest 1 - Valid quantity:")
print(ack.validate_database_acknowledgement(
    VALID_PO_LINE_1, 182
))

print("\nTest 2 - Excess quantity:")
print(ack.validate_database_acknowledgement(
    VALID_PO_LINE_1, 205
))

print("\nTest 3 - Invalid purchase order line:")
print(ack.validate_database_acknowledgement(
    INVALID_PO_LINE, 50
))


# 10. Purchase Order Database Integration
print("\n10. Purchase Order Database Integration:")

print("\nTest 1 - Existing PO line:")
print(po.get_purchase_order_details(VALID_PO_LINE_1))

print("\nTest 2 - Another existing PO line:")
print(po.get_purchase_order_details(VALID_PO_LINE_2))

print("\nTest 3 - Invalid PO line:")
print(po.get_purchase_order_details(INVALID_PO_LINE))


# 11. Approval Database Integration
print("\n11. Approval Database Integration:")

pending_approvals = approval.get_pending_approvals()

print("\nPending Approval Records:")
for record in pending_approvals:
    print(record)

print("\nTotal pending approvals:", len(pending_approvals))


# 12. Delivery Database Integration
print("\n12. Delivery Database Integration:")

print("\nTest 1 - First PO line:")
print(delivery.get_promised_delivery_dates(VALID_PO_LINE_1))

print("\nTest 2 - Second PO line:")
print(delivery.get_promised_delivery_dates(VALID_PO_LINE_2))

print("\nTest 3 - Invalid PO line:")
print(delivery.get_promised_delivery_dates(INVALID_PO_LINE))


# 13. Inventory Database Integration
print("\n13. Inventory Database Integration:")

print("\nTest 1 - First PO line:")
print(inventory.get_inventory_plans(VALID_PO_LINE_1))

print("\nTest 2 - Second PO line:")
print(inventory.get_inventory_plans(VALID_PO_LINE_2))

print("\nTest 3 - Invalid PO line:")
print(inventory.get_inventory_plans(INVALID_PO_LINE))


# 14. Production Database Integration
print("\n14. Production Database Integration:")

print("\nTest 1 - First PO line:")
print(production.get_production_details(VALID_PO_LINE_1))

print("\nTest 2 - Second PO line:")
print(production.get_production_details(VALID_PO_LINE_2))

print("\nTest 3 - Invalid PO line:")
print(production.get_production_details(INVALID_PO_LINE))


# 15. Notification Database Integration
print("\n15. Notification Database Integration:")

print("\nTest 1 - Planner Notifications:")
planner_notifications = notification.get_notifications("Planner")

for record in planner_notifications:
    print(record)

print("Total Planner Notifications:", len(planner_notifications))

print("\nTest 2 - Manager Notifications:")
manager_notifications = notification.get_notifications("Manager")

for record in manager_notifications:
    print(record)

print("Total Manager Notifications:", len(manager_notifications))

print("\nTest 3 - Invalid Recipient:")
print(notification.get_notifications("Unknown"))


# 16. Audit Database Integration
print("\n16. Audit Database Integration:")

print("\nTest 1 - Save Audit Record:")
print(audit.save_audit_record(
    "Planner",
    "APPROVED",
    "Purchase order PO001 approved."
))

print("\nTest 2 - Save Another Audit Record:")
print(audit.save_audit_record(
    "Manager",
    "REJECTED",
    "Purchase order PO002 rejected."
))

print("\nTest 3 - Retrieve Audit History:")
audit_history = audit.get_audit_history()

for record in audit_history:
    print(record)

print("\nTotal Audit Records:", len(audit_history))


# 17. Exception Detection Testing
exception = ExceptionService()

print("\n17. Exception Detection Testing:")

print("\nTest 1 - Unapproved Quantity Change:")
print(exception.check_approval_exception("PENDING"))

print("\nTest 2 - Invalid Purchase Order Line:")
print(exception.check_po_line_exception(INVALID_PO_LINE))

print("\nTest 3 - Promised Date Before Order Date:")
print(exception.check_promise_date_exception(
    "2026-11-20",
    "2026-11-15"
))

print("\nTest 4 - Older Acknowledgement Revision:")
print(exception.check_revision_exception(2, 1))

print("\nTest 5 - Valid Approval:")
print(exception.check_approval_exception("APPROVED"))

print("\nTest 6 - Valid Purchase Order Line:")
print(exception.check_po_line_exception(VALID_PO_LINE_1))

print("\nTest 7 - Valid Promised Date:")
print(exception.check_promise_date_exception(
    "2026-11-20",
    "2026-11-25"
))

print("\nTest 8 - Valid Acknowledgement Revision:")
print(exception.check_revision_exception(1, 2))


# 18. Ground Truth Comparison Testing
print("\n18. Ground Truth Comparison Testing:")

# AN001: Unapproved quantity change
result_1 = exception.check_approval_exception("PENDING")

# AN002: Invalid purchase order line
result_2 = exception.check_po_line_exception(INVALID_PO_LINE)

# AN003: Promised date before order date
result_3 = exception.check_promise_date_exception(
    "2026-11-20",
    "2026-11-15"
)

# AN004: Older acknowledgement revision
result_4 = exception.check_revision_exception(2, 1)

# AN005: Valid supplier acknowledgement
result_5 = ack.validate_database_acknowledgement(
    VALID_PO_LINE_1,
    182
)

# AN006: Valid approved quantity change
result_6 = exception.check_approval_exception("APPROVED")


# Convert detection results into labels
actual_results = [
    "ANOMALY" if result_1["anomaly"] else "NORMAL",
    "ANOMALY" if result_2["anomaly"] else "NORMAL",
    "ANOMALY" if result_3["anomaly"] else "NORMAL",
    "ANOMALY" if result_4["anomaly"] else "NORMAL",
    "NORMAL" if result_5[0] else "ANOMALY",
    "ANOMALY" if result_6["anomaly"] else "NORMAL"
]


# Compare with ground truth
comparison_results = exception.compare_ground_truth(
    actual_results
)

print("\nGround Truth Comparison:")

for result in comparison_results:
    print(result)

total_matches = sum(
    1 for result in comparison_results if result["match"]
)

print("\nTotal Matching Results:", total_matches)
print("Total Ground Truth Records:", len(comparison_results))


# Save exception report
print("\nSaving Exception Report:")

report_path = exception.save_exception_report(
    comparison_results
)

print("Exception report saved successfully!")
print("Report location:", report_path)


print("\n===== ALL TESTS EXECUTED =====")
