
# 4. Detailed Table Documentation

## 4.1 Supplier

**Purpose:** Stores information about suppliers who provide materials or products to the company.

| Column Name | Data Type | Key | Description |
|---|---|---|---|
| supplier_id | TEXT | PK | Unique supplier identification |
| supplier_name | TEXT | - | Name of the supplier |
| email | TEXT | - | Supplier email address |
| phone | TEXT | - | Supplier contact number |
| status | TEXT | - | Current supplier status |
| created_at | TEXT | - | Record creation date and time |

## 4.2 PurchaseOrder

**Purpose:** Stores purchase orders created for suppliers.

| Column Name | Data Type | Key | Description |
|---|---|---|---|
| po_id | TEXT | PK | Unique purchase order ID |
| supplier_id | TEXT | FK | Supplier associated with the order |
| order_date | TEXT | - | Date when the order was created |
| currency | TEXT | - | Currency used for the order |
| status | TEXT | - | Current purchase order status |

## 4.3 POLine

**Purpose:** Stores individual products and their quantities within a purchase order.

| Column Name | Data Type | Key | Description |
|---|---|---|---|
| po_line_id | TEXT | PK | Unique purchase order line ID |
| po_id | TEXT | FK | Related purchase order |
| product_name | TEXT | - | Name of the ordered product |
| requested_quantity | REAL | - | Quantity requested |
| unit_price | REAL | - | Price per unit |
| requested_date | TEXT | - | Requested delivery date |

## 4.4 Acknowledgement

**Purpose:** Stores supplier responses to purchase orders.

| Column Name | Data Type | Key | Description |
|---|---|---|---|
| ack_id | TEXT | PK | Unique acknowledgement ID |
| po_id | TEXT | FK | Related purchase order |
| revision_no | INTEGER | - | Acknowledgement revision number |
| received_at | TEXT | - | Date and time acknowledgement was received |
| status | TEXT | - | Acknowledgement status |

## 4.5 AcknowledgementLine

**Purpose:** Stores supplier responses for individual purchase order lines.

| Column Name | Data Type | Key | Description |
|---|---|---|---|
| ack_line_id | TEXT | PK | Unique acknowledgement line ID |
| ack_id | TEXT | FK | Related acknowledgement |
| po_id | TEXT | FK | Related purchase order |
| po_line_id | TEXT | FK | Related purchase order line |
| accepted_quantity | REAL | - | Quantity accepted by supplier |
| rejected_quantity | REAL | - | Quantity rejected by supplier |
| proposed_unit_price | REAL | - | Price proposed by supplier |

## 4.6 PromiseDate

**Purpose:** Maintains supplier-promised delivery dates and their validity periods.

| Column Name | Data Type | Key | Description |
|---|---|---|---|
| promise_id | TEXT | PK | Unique promise record ID |
| ack_line_id | TEXT | FK | Related acknowledgement line |
| promised_date | TEXT | - | Delivery date promised by supplier |
| effective_from | TEXT | - | Date from which the promise is effective |
| effective_to | TEXT | - | Date until which the promise is effective |
| is_current | INTEGER | - | Indicates whether this is the current promise (1/0) |

## 4.7 ChangeRequest

**Purpose:** Records changes requested by suppliers or arising from acknowledgement differences.

| Column Name | Data Type | Key | Description |
|---|---|---|---|
| change_id | TEXT | PK | Unique change request ID |
| po_line_id | TEXT | FK | Related purchase order line |
| ack_line_id | TEXT | FK | Related acknowledgement line |
| change_type | TEXT | - | Type of requested change |
| old_value | TEXT | - | Previous value |
| new_value | TEXT | - | Proposed new value |
| approval_status | TEXT | - | Current approval status |
| created_at | TEXT | - | Change request creation date and time |

## 4.8 Approval

**Purpose:** Tracks approval decisions for requested changes.

| Column Name | Data Type | Key | Description |
|---|---|---|---|
| approval_id | TEXT | PK | Unique approval ID |
| change_id | TEXT | FK | Related change request |
| approval_level | TEXT | - | Level of approval required |
| decision | TEXT | - | Approval or rejection decision |
| approver_role | TEXT | - | Role of the person approving |
| decided_at | TEXT | - | Date and time of decision |
| comments | TEXT | - | Additional approval comments |

## 4.9 InventoryPlan

**Purpose:** Maintains projected inventory quantities based on purchase order changes.

| Column Name | Data Type | Key | Description |
|---|---|---|---|
| inventory_plan_id | TEXT | PK | Unique inventory plan ID |
| po_line_id | TEXT | FK | Related purchase order line |
| source_change_id | TEXT | FK | Change request that caused the update |
| projected_quantity | REAL | - | Expected inventory quantity |
| effective_from | TEXT | - | Start date of the inventory plan |
| effective_to | TEXT | - | End date of the inventory plan |
| version_no | INTEGER | - | Inventory plan version number |
| status | TEXT | - | Current inventory plan status |

## 4.10 ProductionOrder

**Purpose:** Stores production requirements and required completion dates.

| Column Name | Data Type | Key | Description |
|---|---|---|---|
| production_order_id | TEXT | PK | Unique production order ID |
| product_name | TEXT | - | Product to be manufactured |
| required_quantity | REAL | - | Quantity required for production |
| required_date | TEXT | - | Date by which production is required |
| status | TEXT | - | Current production order status |

## 4.11 ProductionOrderSupplyAllocation

**Purpose:** Connects purchase order supplies with production orders.

| Column Name | Data Type | Key | Description |
|---|---|---|---|
| allocation_id | TEXT | PK | Unique allocation ID |
| production_order_id | TEXT | FK | Related production order |
| po_line_id | TEXT | FK | Related purchase order line |
| allocated_quantity | REAL | - | Quantity allocated to production |
| created_at | TEXT | - | Allocation creation date and time |

## 4.12 Notification

**Purpose:** Stores notifications generated for different business events.

| Column Name | Data Type | Key | Description |
|---|---|---|---|
| notification_id | TEXT | PK | Unique notification ID |
| po_id | TEXT | FK | Related purchase order |
| change_id | TEXT | FK | Related change request |
| production_order_id | TEXT | FK | Related production order |
| recipient_role | TEXT | - | Role receiving the notification |
| message | TEXT | - | Notification message |
| notification_status | TEXT | - | Current notification status |
| created_at | TEXT | - | Notification creation date and time |

# 5. Key Definitions

- PK (Primary Key): Uniquely identifies each record in a table.
- FK (Foreign Key): Connects one table with another table.
- TEXT: Stores text, identifiers, dates or timestamps.
- INTEGER: Stores whole numbers.
- REAL: Stores numeric values, including decimal values.

# 6. Database Relationships

The main relationships are:

1. Supplier → PurchaseOrder
2. PurchaseOrder → POLine
3. PurchaseOrder → Acknowledgement
4. Acknowledgement → AcknowledgementLine
5. AcknowledgementLine → PromiseDate
6. POLine → ChangeRequest
7. AcknowledgementLine → ChangeRequest
8. ChangeRequest → Approval
9. ChangeRequest → InventoryPlan
10. POLine → InventoryPlan
11. ProductionOrder → ProductionOrderSupplyAllocation
12. POLine → ProductionOrderSupplyAllocation
13. PurchaseOrder → Notification
14. ChangeRequest → Notification
15. ProductionOrder → Notification

# 7. Conclusion

The Supplier Acknowledgement System database contains 12 tables that manage suppliers, purchase orders, supplier acknowledgements, promised delivery dates, change requests, approvals, inventory planning, production orders, supply allocation and notifications.

The database provides a structured way to manage supplier commitments and understand how changes in delivery dates or quantities can affect inventory and production schedules.
