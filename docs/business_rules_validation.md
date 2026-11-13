
# Supplier Acknowledgement System
# Business Rules Validation Checklist

## 1. Purchase Order Validation

| Rule | Database Table | Status |
|---|---|---|
| Unique PO ID | PurchaseOrder | Pending |
| Existing supplier required | PurchaseOrder | Pending |
| At least one PO line | POLine | Pending |
| Quantity must be valid | POLine | Pending |
| Unit price must be valid | POLine | Pending |
| Requested date required | POLine | Pending |

## 2. Supplier Acknowledgement Validation

| Rule | Database Table | Status |
|---|---|---|
| Full quantity acceptance | AcknowledgementLine | Pending |
| Partial quantity acceptance | AcknowledgementLine | Pending |
| Quantity rejection | AcknowledgementLine | Pending |
| Proposed price tracking | AcknowledgementLine | Pending |
| Promise date tracking | PromiseDate | Pending |
| Multiple revisions | Acknowledgement | Pending |

## 3. Change Detection Validation

| Rule | Database Table | Status |
|---|---|---|
| Quantity difference detection | ChangeRequest | Pending |
| Price difference detection | ChangeRequest | Pending |
| Delivery date difference detection | ChangeRequest | Pending |
| Old and new value tracking | ChangeRequest | Pending |

## 4. Approval Validation

| Rule | Database Table | Status |
|---|---|---|
| No change requires no approval | Approval | Pending |
| Change up to 2% requires planner approval | Approval | Pending |
| Change above 2% requires manager approval | Approval | Pending |
| Delivery delay up to 3 days requires planner approval | Approval | Pending |
| Delivery delay above 3 days requires manager approval | Approval | Pending |
| Highest approval level applies | Approval | Pending |

## 5. Inventory Validation

| Rule | Database Table | Status |
|---|---|---|
| Approved changes update inventory | InventoryPlan | Pending |
| Pending changes cannot update inventory | InventoryPlan | Pending |
| Rejected changes cannot update inventory | InventoryPlan | Pending |
| Previous values must be preserved | InventoryPlan | Pending |
| Inventory shortage identification | InventoryPlan | Pending |

## 6. Supplier Silence Validation

| Rule | Database Table | Status |
|---|---|---|
| Calculate acknowledgement due date | PurchaseOrder | Pending |
| Identify missing acknowledgements | Acknowledgement | Pending |
| Three-day response deadline | PurchaseOrder | Pending |
| Notify responsible planner | Notification | Pending |

## 7. Revision Validation

| Rule | Database Table | Status |
|---|---|---|
| Revision number required | Acknowledgement | Pending |
| Sequential revision numbers | Acknowledgement | Pending |
| Older revision cannot overwrite newer revision | Acknowledgement | Pending |
| Preserve revision history | Acknowledgement | Pending |

## 8. Production Impact Validation

| Rule | Database Table | Status |
|---|---|---|
| Calculate available supply | InventoryPlan | Pending |
| Compare supply with production demand | ProductionOrder | Pending |
| Identify production shortages | ProductionOrder | Pending |
| Track supply allocation | ProductionOrderSupplyAllocation | Pending |
| Notify affected planners | Notification | Pending |

## 9. Final Validation

All business rules must be tested before project completion.

Current Status: Pending
