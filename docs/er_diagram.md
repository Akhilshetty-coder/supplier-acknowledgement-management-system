
# Supplier Acknowledgement System
# Entity Relationship Diagram (ER Diagram)

## 1. Database Relationships

```mermaid
erDiagram

    Supplier ||--o{ PurchaseOrder : creates

    PurchaseOrder ||--o{ POLine : contains

    PurchaseOrder ||--o{ Acknowledgement : receives

    Acknowledgement ||--o{ AcknowledgementLine : contains

    POLine ||--o{ AcknowledgementLine : references

    AcknowledgementLine ||--o{ PromiseDate : has

    POLine ||--o{ ChangeRequest : has

    AcknowledgementLine ||--o{ ChangeRequest : generates

    ChangeRequest ||--o{ Approval : requires

    ChangeRequest ||--o{ InventoryPlan : updates

    POLine ||--o{ InventoryPlan : tracks

    ProductionOrder ||--o{ ProductionOrderSupplyAllocation : receives

    POLine ||--o{ ProductionOrderSupplyAllocation : supplies

    PurchaseOrder ||--o{ Notification : generates

    ChangeRequest ||--o{ Notification : generates

    ProductionOrder ||--o{ Notification : generates

    Supplier {
        TEXT supplier_id PK
        TEXT supplier_name
        TEXT email
        TEXT phone
        TEXT status
        TEXT created_at
    }

    PurchaseOrder {
        TEXT po_id PK
        TEXT supplier_id FK
        TEXT order_date
        TEXT currency
        TEXT status
    }

    POLine {
        TEXT po_line_id PK
        TEXT po_id FK
        TEXT product_name
        REAL requested_quantity
        REAL unit_price
        TEXT requested_date
    }

    Acknowledgement {
        TEXT ack_id PK
        TEXT po_id FK
        INTEGER revision_no
        TEXT received_at
        TEXT status
    }

    AcknowledgementLine {
        TEXT ack_line_id PK
        TEXT ack_id FK
        TEXT po_id FK
        TEXT po_line_id FK
        REAL accepted_quantity
        REAL rejected_quantity
        REAL proposed_unit_price
    }

    PromiseDate {
        TEXT promise_id PK
        TEXT ack_line_id FK
        TEXT promised_date
        TEXT effective_from
        TEXT effective_to
        INTEGER is_current
    }

    ChangeRequest {
        TEXT change_id PK
        TEXT po_line_id FK
        TEXT ack_line_id FK
        TEXT change_type
        TEXT old_value
        TEXT new_value
        TEXT approval_status
        TEXT created_at
    }

    Approval {
        TEXT approval_id PK
        TEXT change_id FK
        TEXT approval_level
        TEXT decision
        TEXT approver_role
        TEXT decided_at
        TEXT comments
    }

    InventoryPlan {
        TEXT inventory_plan_id PK
        TEXT po_line_id FK
        TEXT source_change_id FK
        REAL projected_quantity
        TEXT effective_from
        TEXT effective_to
        INTEGER version_no
        TEXT status
    }

    ProductionOrder {
        TEXT production_order_id PK
        TEXT product_name
        REAL required_quantity
        TEXT required_date
        TEXT status
    }

    ProductionOrderSupplyAllocation {
        TEXT allocation_id PK
        TEXT production_order_id FK
        TEXT po_line_id FK
        REAL allocated_quantity
        TEXT created_at
    }

    Notification {
        TEXT notification_id PK
        TEXT po_id FK
        TEXT change_id FK
        TEXT production_order_id FK
        TEXT recipient_role
        TEXT message
        TEXT notification_status
        TEXT created_at
    }
```

## 2. Relationship Explanation

1. Supplier to PurchaseOrder: One supplier can have multiple purchase orders.
2. PurchaseOrder to POLine: One purchase order can contain multiple products.
3. PurchaseOrder to Acknowledgement: One purchase order can receive multiple acknowledgements.
4. Acknowledgement to AcknowledgementLine: One acknowledgement can contain multiple lines.
5. AcknowledgementLine to PromiseDate: One acknowledgement line can have multiple promise-date records.
6. POLine to ChangeRequest: One purchase order line can have multiple change requests.
7. ChangeRequest to Approval: One change request can have multiple approval records.
8. ChangeRequest to InventoryPlan: A change can create multiple inventory plan versions.
9. ProductionOrder and POLine connect through ProductionOrderSupplyAllocation.
10. Notification connects purchase orders, changes and production orders with recipient roles.

## 3. Conclusion

The ER Diagram explains how all 12 database tables are connected using primary keys and foreign keys.

It provides a visual understanding of the Supplier Acknowledgement System database architecture.
