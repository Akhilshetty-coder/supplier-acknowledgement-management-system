
# Supplier Acknowledgement Management System
## Business Rules Documentation

### 1. Project Objective

The objective is to build a system that manages supplier acknowledgements,
purchase order changes, promised delivery dates, approval decisions
and downstream inventory and production impacts.

### 2. Primary Actors

1. Supplier
2. Planner
3. Carrier/Warehouse Operator
4. Logistics Analyst
5. Operations Manager

### 3. Purchase Order Rules

- Every purchase order must have a unique PO ID.
- Every PO must belong to an existing supplier.
- Every PO must contain at least one PO line.
- Each PO line must contain requested quantity, unit price
  and requested delivery date.

### 4. Supplier Acknowledgement Rules

- Supplier can accept the full quantity.
- Supplier can partially accept the quantity.
- Supplier can reject the quantity.
- Supplier can propose a new price.
- Supplier can propose a new delivery date.
- Supplier can submit multiple acknowledgement revisions.

### 5. Change Detection Rules

Compare the following values:

- Requested quantity versus accepted quantity.
- Requested price versus confirmed price.
- Requested delivery date versus promised delivery date.

Create a change request whenever a relevant value changes.

### 6. Approval Rules

Quantity:
- No change: No approval.
- Change up to 2%: Planner approval.
- Change above 2%: Manager approval.

Price:
- No change: No approval.
- Price change up to 2%: Planner approval.
- Price change above 2%: Manager approval.

Delivery:
- Early or unchanged delivery: No approval.
- Delay up to 3 days: Planner approval.
- Delay above 3 days: Manager approval.

The highest required approval level applies when multiple
changes occur together.

These are configurable project assumptions.

### 7. Inventory Rules

- Only approved changes can update projected supply.
- Pending changes cannot update inventory plans.
- Rejected changes cannot update inventory plans.
- Previous approved values must be preserved.
- Inventory shortages must be identified.

### 8. Supplier Silence Rules

- Monitor acknowledgement due dates.
- Identify POs without supplier responses.
- Mark them as awaiting acknowledgement.
- Notify the responsible planner after the configured deadline.

Initial assumed response period: 3 days.

### 9. Revision Management Rules

- Each acknowledgement must have a revision number.
- Revision numbers must increase sequentially.
- Older revisions must not overwrite newer revisions.
- Preserve all acknowledgement history.

### 10. Exception Management

The system must identify:

1. Unapproved changes updating inventory.
2. Acknowledgement referring to the wrong PO line.
3. Promised delivery date before order date.
4. Older revision overwriting newer revision.

### 11. Downstream Impact Rules

- Calculate available supply.
- Compare available supply against production demand.
- Identify production shortages.
- Identify affected production orders.
- Notify affected planners.

### 12. Expected Business Outcomes

- Better supplier acknowledgement tracking.
- Faster approval decisions.
- Improved delivery visibility.
- Reduced inventory planning errors.
- Identification of production shortages.
- Complete revision and approval traceability.
