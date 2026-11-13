
-- ==================================================
-- SUPPLIER ACKNOWLEDGEMENT MANAGEMENT SYSTEM
-- DATABASE SCHEMA
-- ==================================================

PRAGMA foreign_keys = ON;

-- 1. SUPPLIER
CREATE TABLE IF NOT EXISTS Supplier (
    supplier_id TEXT PRIMARY KEY,
    supplier_name TEXT NOT NULL,
    email TEXT UNIQUE,
    phone TEXT,
    status TEXT NOT NULL
        CHECK (status IN ('ACTIVE', 'INACTIVE', 'BLOCKED')),
    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
);

-- 2. PURCHASE ORDER
CREATE TABLE IF NOT EXISTS PurchaseOrder (
    po_id TEXT PRIMARY KEY,
    supplier_id TEXT NOT NULL,
    order_date TEXT NOT NULL,
    currency TEXT NOT NULL DEFAULT 'INR',
    status TEXT NOT NULL
        CHECK (status IN (
            'OPEN', 'PARTIALLY_ACKNOWLEDGED',
            'ACKNOWLEDGED', 'CLOSED', 'CANCELLED'
        )),

    FOREIGN KEY (supplier_id)
        REFERENCES Supplier(supplier_id)
);

-- 3. PURCHASE ORDER LINE
CREATE TABLE IF NOT EXISTS POLine (
    po_line_id TEXT PRIMARY KEY,
    po_id TEXT NOT NULL,
    product_name TEXT NOT NULL,
    requested_quantity REAL NOT NULL
        CHECK (requested_quantity > 0),
    unit_price REAL NOT NULL
        CHECK (unit_price >= 0),
    requested_date TEXT NOT NULL,

    UNIQUE (po_id, po_line_id),

    FOREIGN KEY (po_id)
        REFERENCES PurchaseOrder(po_id)
);

-- 4. ACKNOWLEDGEMENT (PO LEVEL)
CREATE TABLE IF NOT EXISTS Acknowledgement (
    ack_id TEXT PRIMARY KEY,
    po_id TEXT NOT NULL,
    revision_no INTEGER NOT NULL
        CHECK (revision_no > 0),
    received_at TEXT NOT NULL,
    status TEXT NOT NULL
        CHECK (status IN (
            'RECEIVED', 'CURRENT', 'SUPERSEDED', 'INVALID'
        )),

    UNIQUE (po_id, revision_no),
    UNIQUE (ack_id, po_id),

    FOREIGN KEY (po_id)
        REFERENCES PurchaseOrder(po_id)
);

-- SUPPORTING TABLE: ACKNOWLEDGEMENT LINE
CREATE TABLE IF NOT EXISTS AcknowledgementLine (
    ack_line_id TEXT PRIMARY KEY,
    ack_id TEXT NOT NULL,
    po_id TEXT NOT NULL,
    po_line_id TEXT NOT NULL,
    accepted_quantity REAL NOT NULL
        CHECK (accepted_quantity >= 0),
    rejected_quantity REAL NOT NULL
        CHECK (rejected_quantity >= 0),
    proposed_unit_price REAL
        CHECK (proposed_unit_price >= 0),

    UNIQUE (ack_id, po_line_id),

    FOREIGN KEY (ack_id, po_id)
        REFERENCES Acknowledgement(ack_id, po_id),

    FOREIGN KEY (po_id, po_line_id)
        REFERENCES POLine(po_id, po_line_id)
);

-- 5. PROMISE DATE
CREATE TABLE IF NOT EXISTS PromiseDate (
    promise_id TEXT PRIMARY KEY,
    ack_line_id TEXT NOT NULL,
    promised_date TEXT NOT NULL,
    effective_from TEXT NOT NULL,
    effective_to TEXT,
    is_current INTEGER NOT NULL DEFAULT 1
        CHECK (is_current IN (0, 1)),

    FOREIGN KEY (ack_line_id)
        REFERENCES AcknowledgementLine(ack_line_id),

    CHECK (
        effective_to IS NULL
        OR effective_to >= effective_from
    )
);

-- 6. CHANGE REQUEST
CREATE TABLE IF NOT EXISTS ChangeRequest (
    change_id TEXT PRIMARY KEY,
    po_line_id TEXT NOT NULL,
    ack_line_id TEXT NOT NULL,
    change_type TEXT NOT NULL
        CHECK (change_type IN (
            'QUANTITY', 'PRICE', 'DELIVERY_DATE'
        )),
    old_value TEXT NOT NULL,
    new_value TEXT NOT NULL,
    approval_status TEXT NOT NULL
        CHECK (approval_status IN (
            'NOT_REQUIRED', 'PENDING',
            'APPROVED', 'REJECTED'
        )),
    created_at TEXT NOT NULL,

    FOREIGN KEY (po_line_id)
        REFERENCES POLine(po_line_id),

    FOREIGN KEY (ack_line_id)
        REFERENCES AcknowledgementLine(ack_line_id)
);

-- 7. APPROVAL
CREATE TABLE IF NOT EXISTS Approval (
    approval_id TEXT PRIMARY KEY,
    change_id TEXT NOT NULL,
    approval_level TEXT NOT NULL
        CHECK (approval_level IN ('PLANNER', 'MANAGER')),
    decision TEXT NOT NULL
        CHECK (decision IN ('PENDING', 'APPROVED', 'REJECTED')),
    approver_role TEXT,
    decided_at TEXT,
    comments TEXT,

    FOREIGN KEY (change_id)
        REFERENCES ChangeRequest(change_id)
);

-- 8. INVENTORY PLAN
-- Each row is a version or historical projection.
CREATE TABLE IF NOT EXISTS InventoryPlan (
    inventory_plan_id TEXT PRIMARY KEY,
    po_line_id TEXT NOT NULL,
    source_change_id TEXT,
    projected_quantity REAL NOT NULL
        CHECK (projected_quantity >= 0),
    effective_from TEXT NOT NULL,
    effective_to TEXT,
    version_no INTEGER NOT NULL
        CHECK (version_no > 0),
    status TEXT NOT NULL
        CHECK (status IN ('CURRENT', 'SUPERSEDED')),

    UNIQUE (po_line_id, version_no),

    FOREIGN KEY (po_line_id)
        REFERENCES POLine(po_line_id),

    FOREIGN KEY (source_change_id)
        REFERENCES ChangeRequest(change_id),

    CHECK (
        effective_to IS NULL
        OR effective_to >= effective_from
    )
);

-- 9. PRODUCTION ORDER
CREATE TABLE IF NOT EXISTS ProductionOrder (
    production_order_id TEXT PRIMARY KEY,
    product_name TEXT NOT NULL,
    required_quantity REAL NOT NULL
        CHECK (required_quantity > 0),
    required_date TEXT NOT NULL,
    status TEXT NOT NULL
        CHECK (status IN (
            'PLANNED', 'IN_PROGRESS',
            'COMPLETED', 'DELAYED', 'CANCELLED'
        ))
);

-- SUPPORTING TABLE: MANY-TO-MANY BRIDGE
CREATE TABLE IF NOT EXISTS ProductionOrderSupplyAllocation (
    allocation_id TEXT PRIMARY KEY,
    production_order_id TEXT NOT NULL,
    po_line_id TEXT NOT NULL,
    allocated_quantity REAL NOT NULL
        CHECK (allocated_quantity > 0),
    created_at TEXT NOT NULL,

    FOREIGN KEY (production_order_id)
        REFERENCES ProductionOrder(production_order_id),

    FOREIGN KEY (po_line_id)
        REFERENCES POLine(po_line_id)
);

-- 10. NOTIFICATION
CREATE TABLE IF NOT EXISTS Notification (
    notification_id TEXT PRIMARY KEY,
    po_id TEXT,
    change_id TEXT,
    production_order_id TEXT,
    recipient_role TEXT NOT NULL,
    message TEXT NOT NULL,
    notification_status TEXT NOT NULL
        CHECK (notification_status IN (
            'PENDING', 'SENT', 'READ', 'FAILED'
        )),
    created_at TEXT NOT NULL,

    FOREIGN KEY (po_id)
        REFERENCES PurchaseOrder(po_id),

    FOREIGN KEY (change_id)
        REFERENCES ChangeRequest(change_id),

    FOREIGN KEY (production_order_id)
        REFERENCES ProductionOrder(production_order_id)
);

-- INDEXES FOR COMMON SEARCHES
CREATE INDEX IF NOT EXISTS idx_po_supplier
ON PurchaseOrder(supplier_id);

CREATE INDEX IF NOT EXISTS idx_polines_po
ON POLine(po_id);

CREATE INDEX IF NOT EXISTS idx_ack_po
ON Acknowledgement(po_id);

CREATE INDEX IF NOT EXISTS idx_changes_status
ON ChangeRequest(approval_status);

CREATE INDEX IF NOT EXISTS idx_inventory_line
ON InventoryPlan(po_line_id);

CREATE INDEX IF NOT EXISTS idx_notification_status
ON Notification(notification_status);


-- 11. AUDIT LOG
CREATE TABLE IF NOT EXISTS AuditLog (
    audit_id INTEGER PRIMARY KEY AUTOINCREMENT,
    user TEXT NOT NULL,
    action TEXT NOT NULL,
    description TEXT NOT NULL,
    timestamp TEXT NOT NULL
);
