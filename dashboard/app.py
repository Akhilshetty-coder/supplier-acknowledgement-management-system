
import sqlite3
from pathlib import Path
from datetime import date

import pandas as pd
import streamlit as st
import plotly.express as px


# ==========================================================
# 1. PAGE CONFIGURATION
# ==========================================================

st.set_page_config(
    page_title="Supplier Management Dashboard",
    page_icon="📦",
    layout="wide",
    initial_sidebar_state="expanded"
)

PROJECT_ROOT = Path(__file__).resolve().parent.parent
DB_PATH = PROJECT_ROOT / "database" / "supplier_management.db"


# ==========================================================
# 2. PROFESSIONAL DASHBOARD DESIGN
# ==========================================================

st.markdown("""
<style>

    .stApp {
        background-color: #f5f7fb;
    }

    /* SIDEBAR */

    [data-testid="stSidebar"] {
        background-color: #172554;
    }

    /* Default sidebar text */
    [data-testid="stSidebar"] label,
    [data-testid="stSidebar"] p,
    [data-testid="stSidebar"] h1,
    [data-testid="stSidebar"] h2,
    [data-testid="stSidebar"] h3 {
        color: #ffffff !important;
    }

    /* Navigation radio labels */
    [data-testid="stSidebar"] [role="radiogroup"] label {
        color: #ffffff !important;
    }

    /* Supplier dropdown container */
    [data-testid="stSidebar"] [data-baseweb="select"] > div {
        background-color: #ffffff !important;
        border: 1px solid #cbd5e1 !important;
        border-radius: 8px !important;
    }

    /* Supplier dropdown text */
    [data-testid="stSidebar"] [data-baseweb="select"] input {
        color: #172554 !important;
        -webkit-text-fill-color: #172554 !important;
    }

    [data-testid="stSidebar"] [data-baseweb="select"] span {
        color: #172554 !important;
    }

    [data-testid="stSidebar"] [data-baseweb="select"] svg {
        fill: #172554 !important;
    }

    /* Dropdown menu options */
    [data-baseweb="popover"] [role="option"] {
        color: #172554 !important;
        background-color: #ffffff !important;
    }

    /* Refresh button */
    [data-testid="stSidebar"] button {
        background-color: #ffffff !important;
        color: #172554 !important;
        border: 1px solid #cbd5e1 !important;
        border-radius: 8px !important;
    }

    [data-testid="stSidebar"] button p,
    [data-testid="stSidebar"] button span {
        color: #172554 !important;
    }

    [data-testid="stSidebar"] button:hover {
        background-color: #dbeafe !important;
        border-color: #93c5fd !important;
    }

    /* MAIN HEADER */

    .main-title {
        font-size: 30px;
        font-weight: 750;
        color: #172554;
        margin-bottom: 2px;
    }

    .subtitle {
        color: #64748b;
        font-size: 14px;
        margin-bottom: 25px;
    }

    .section-title {
        color: #172554;
        font-size: 20px;
        font-weight: 700;
        margin-top: 15px;
        margin-bottom: 12px;
    }

    /* KPI CARDS */

    div[data-testid="stMetric"] {
        background: #ffffff;
        border: 1px solid #e2e8f0;
        padding: 17px;
        border-radius: 12px;
        box-shadow: 0 2px 8px rgba(15, 23, 42, 0.04);
    }

    div[data-testid="stMetricLabel"] {
        color: #64748b;
    }

    div[data-testid="stMetricValue"] {
        color: #172554;
        font-weight: 750;
    }

    /* CHARTS */

    div[data-testid="stPlotlyChart"] {
        background: #ffffff;
        padding: 10px;
        border-radius: 12px;
        border: 1px solid #e2e8f0;
    }

    /* FOOTER */

    .dashboard-footer {
        text-align: center;
        color: #64748b;
        font-size: 12px;
        padding: 20px;
    }

</style>
""", unsafe_allow_html=True)


# ==========================================================
# 3. DATABASE CONNECTION
# ==========================================================

@st.cache_data(ttl=60)
def load_data(query):
    with sqlite3.connect(DB_PATH) as conn:
        return pd.read_sql_query(query, conn)


# ==========================================================
# 4. LOAD DATABASE TABLES
# ==========================================================

try:

    suppliers = load_data("SELECT * FROM Supplier")

    purchase_orders = load_data("SELECT * FROM PurchaseOrder")

    polines = load_data("SELECT * FROM POLine")

    acknowledgements = load_data("SELECT * FROM Acknowledgement")

    change_requests = load_data("SELECT * FROM ChangeRequest")

    approvals = load_data("SELECT * FROM Approval")

    production_orders = load_data("SELECT * FROM ProductionOrder")

    notifications = load_data("SELECT * FROM Notification")

    promise_details = load_data("""
        SELECT
            pd.promise_id,
            po.po_id,
            s.supplier_name,
            pl.product_name,
            pl.requested_date,
            pd.promised_date,
            al.accepted_quantity,
            al.rejected_quantity,
            CASE
                WHEN pd.is_current = 1 THEN 'CURRENT'
                ELSE 'HISTORICAL'
            END AS promise_status

        FROM PromiseDate pd

        JOIN AcknowledgementLine al
            ON pd.ack_line_id = al.ack_line_id

        JOIN POLine pl
            ON al.po_line_id = pl.po_line_id

        JOIN PurchaseOrder po
            ON pl.po_id = po.po_id

        JOIN Supplier s
            ON po.supplier_id = s.supplier_id

        WHERE pd.is_current = 1

        ORDER BY pd.promised_date
    """)

except Exception as error:

    st.error(f"Database loading failed: {error}")
    st.stop()


# ==========================================================
# 5. SIDEBAR NAVIGATION
# ==========================================================

with st.sidebar:

    st.markdown("## 📦 Supplier Control")

    st.caption("Acknowledgement Management System")

    st.divider()

    page = st.radio(
        "NAVIGATION",
        [
            "Overview",
            "Purchase Orders",
            "Supplier Deliveries",
            "Operations"
        ]
    )

    st.divider()

    supplier_options = ["All Suppliers"] + (
        suppliers["supplier_name"].dropna().tolist()
        if not suppliers.empty else []
    )

    selected_supplier = st.selectbox(
        "Filter by Supplier",
        supplier_options
    )

    st.divider()

    if st.button(
        "🔄 Refresh Dashboard",
        use_container_width=True
    ):

        st.cache_data.clear()
        st.rerun()

    st.caption("Data source: SQLite database")


# ==========================================================
# 6. FILTER DATA
# ==========================================================

if selected_supplier == "All Suppliers":

    filtered_suppliers = suppliers.copy()

    filtered_pos = purchase_orders.copy()

else:

    filtered_suppliers = suppliers[
        suppliers["supplier_name"] == selected_supplier
    ].copy()

    selected_supplier_ids = filtered_suppliers[
        "supplier_id"
    ].tolist()

    filtered_pos = purchase_orders[
        purchase_orders["supplier_id"].isin(
            selected_supplier_ids
        )
    ].copy()


selected_po_ids = filtered_pos["po_id"].tolist()


filtered_acknowledgements = acknowledgements[
    acknowledgements["po_id"].isin(selected_po_ids)
].copy()


filtered_polines = polines[
    polines["po_id"].isin(selected_po_ids)
].copy()


filtered_change_requests = change_requests[
    change_requests["po_line_id"].isin(
        filtered_polines["po_line_id"]
    )
].copy()


selected_change_ids = filtered_change_requests[
    "change_id"
].tolist()


filtered_approvals = approvals[
    approvals["change_id"].isin(selected_change_ids)
].copy()


filtered_notifications = notifications[
    notifications["po_id"].isin(selected_po_ids)
].copy()


filtered_promise_details = promise_details[
    promise_details["po_id"].isin(selected_po_ids)
].copy()


# Filter production orders if the table contains po_id.
# Otherwise, show all production orders.

if "po_id" in production_orders.columns:

    filtered_production_orders = production_orders[
        production_orders["po_id"].isin(selected_po_ids)
    ].copy()

else:

    filtered_production_orders = production_orders.copy()


# ==========================================================
# 7. DASHBOARD HEADER
# ==========================================================

header_col1, header_col2 = st.columns([5, 1])

with header_col1:

    st.markdown(
        '<div class="main-title">'
        'Supplier Acknowledgement Management'
        '</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="subtitle">'
        'Enterprise Supplier Operations Control Center'
        '</div>',
        unsafe_allow_html=True
    )

with header_col2:

    st.caption(
        f"Date: {date.today().strftime('%d %b %Y')}"
    )


st.divider()


# ==========================================================
# 8. COMMON KPI CALCULATIONS
# ==========================================================

pending_changes = (
    filtered_change_requests["approval_status"]
    .astype(str)
    .str.upper()
    .eq("PENDING")
    .sum()
)


pending_approvals = (
    filtered_approvals["decision"]
    .astype(str)
    .str.upper()
    .eq("PENDING")
    .sum()
)


production_count = len(filtered_production_orders)


# ==========================================================
# 9. OVERVIEW PAGE
# ==========================================================

if page == "Overview":

    st.markdown(
        '<div class="section-title">'
        'Business Overview'
        '</div>',
        unsafe_allow_html=True
    )

    col1, col2, col3 = st.columns(3)

    col1.metric(
        "Total Suppliers",
        len(filtered_suppliers)
    )

    col2.metric(
        "Purchase Orders",
        len(filtered_pos)
    )

    col3.metric(
        "Acknowledgements",
        len(filtered_acknowledgements)
    )


    col4, col5, col6 = st.columns(3)

    col4.metric(
        "Pending Changes",
        int(pending_changes)
    )

    col5.metric(
        "Pending Approvals",
        int(pending_approvals)
    )

    col6.metric(
        "Production Orders",
        production_count
    )


    st.markdown(
        '<div class="section-title">'
        'Business Analytics'
        '</div>',
        unsafe_allow_html=True
    )


    chart1, chart2 = st.columns(2)


    # Purchase order chart

    with chart1:

        if not filtered_pos.empty:

            po_status = (
                filtered_pos["status"]
                .value_counts()
                .reset_index()
            )

            po_status.columns = ["Status", "Count"]

            fig = px.bar(
                po_status,
                x="Status",
                y="Count",
                color="Status",
                text="Count",
                title="Purchase Orders by Status"
            )

            fig.update_layout(
                template="plotly_white",
                showlegend=False
            )

            st.plotly_chart(
                fig,
                width="stretch"
            )

        else:

            st.info("No purchase orders available.")


    # Change request chart

    with chart2:

        if not filtered_change_requests.empty:

            approval_status = (
                filtered_change_requests["approval_status"]
                .value_counts()
                .reset_index()
            )

            approval_status.columns = ["Status", "Count"]

            fig = px.pie(
                approval_status,
                names="Status",
                values="Count",
                hole=0.45,
                title="Change Request Approval Status"
            )

            fig.update_layout(
                template="plotly_white"
            )

            st.plotly_chart(
                fig,
                width="stretch"
            )

        else:

            st.info("No change requests available.")


    # Recent purchase orders

    st.markdown(
        '<div class="section-title">'
        'Recent Purchase Orders'
        '</div>',
        unsafe_allow_html=True
    )

    if not filtered_pos.empty:

        po_details = filtered_pos.merge(
            suppliers[["supplier_id", "supplier_name"]],
            on="supplier_id",
            how="left"
        )

        display_columns = [
            column for column in [
                "po_id",
                "supplier_name",
                "order_date",
                "currency",
                "status"
            ]
            if column in po_details.columns
        ]

        st.dataframe(
            po_details[display_columns],
            width="stretch",
            hide_index=True
        )

    else:

        st.info("No purchase order records found.")


# ==========================================================
# 10. PURCHASE ORDERS PAGE
# ==========================================================

elif page == "Purchase Orders":

    st.markdown(
        '<div class="section-title">'
        'Purchase Order Management'
        '</div>',
        unsafe_allow_html=True
    )

    st.metric(
        "Total Purchase Orders",
        len(filtered_pos)
    )


    if not filtered_pos.empty:

        po_details = filtered_pos.merge(
            suppliers[["supplier_id", "supplier_name"]],
            on="supplier_id",
            how="left"
        )

        st.dataframe(
            po_details,
            width="stretch",
            hide_index=True
        )

        st.download_button(
            "Download Purchase Order Report",
            data=po_details.to_csv(
                index=False
            ).encode("utf-8"),
            file_name="purchase_order_report.csv",
            mime="text/csv"
        )

    else:

        st.info("No purchase orders available.")


    st.markdown("### Acknowledgement Records")

    if not filtered_acknowledgements.empty:

        st.dataframe(
            filtered_acknowledgements,
            width="stretch",
            hide_index=True
        )

    else:

        st.info("No acknowledgement records available.")


    st.markdown("### Purchase Order Lines")

    if not filtered_polines.empty:

        st.dataframe(
            filtered_polines,
            width="stretch",
            hide_index=True
        )

    else:

        st.info("No purchase order lines available.")


# ==========================================================
# 11. SUPPLIER DELIVERIES PAGE
# ==========================================================

elif page == "Supplier Deliveries":

    st.markdown(
        '<div class="section-title">'
        'Supplier Delivery Tracking'
        '</div>',
        unsafe_allow_html=True
    )

    if not filtered_promise_details.empty:

        today = pd.Timestamp(date.today())

        promise_dates = pd.to_datetime(
            filtered_promise_details["promised_date"],
            errors="coerce"
        )

        filtered_promise_details[
            "delivery_tracking_status"
        ] = promise_dates.apply(
            lambda d: (
                "Unknown" if pd.isna(d)
                else "Overdue" if d < today
                else "Due Today" if d == today
                else "Upcoming"
            )
        )


        overdue = (
            filtered_promise_details[
                "delivery_tracking_status"
            ] == "Overdue"
        ).sum()


        due_today = (
            filtered_promise_details[
                "delivery_tracking_status"
            ] == "Due Today"
        ).sum()


        upcoming = (
            filtered_promise_details[
                "delivery_tracking_status"
            ] == "Upcoming"
        ).sum()


        col1, col2, col3 = st.columns(3)

        col1.metric(
            "Overdue Deliveries",
            int(overdue)
        )

        col2.metric(
            "Due Today",
            int(due_today)
        )

        col3.metric(
            "Upcoming Deliveries",
            int(upcoming)
        )


        st.dataframe(
            filtered_promise_details,
            width="stretch",
            hide_index=True
        )


        st.download_button(
            "Download Delivery Report",
            data=filtered_promise_details.to_csv(
                index=False
            ).encode("utf-8"),
            file_name="supplier_delivery_report.csv",
            mime="text/csv"
        )


    else:

        st.info("No promised delivery records available.")


    st.caption(
        "Tracking is based on promised dates. "
        "It does not confirm actual physical delivery."
    )


# ==========================================================
# 12. OPERATIONS PAGE
# ==========================================================

elif page == "Operations":

    st.markdown(
        '<div class="section-title">'
        'Operations and Exceptions'
        '</div>',
        unsafe_allow_html=True
    )


    st.markdown("### Pending Change Requests")

    if not filtered_change_requests.empty:

        pending_data = filtered_change_requests[
            filtered_change_requests["approval_status"]
            .astype(str)
            .str.upper()
            .eq("PENDING")
        ]

        st.dataframe(
            pending_data,
            width="stretch",
            hide_index=True
        )

    else:

        st.info("No change requests available.")


    st.markdown("### Approval Tracking")

    if not filtered_approvals.empty:

        st.dataframe(
            filtered_approvals,
            width="stretch",
            hide_index=True
        )

    else:

        st.info("No approval records available.")


    st.markdown("### Notifications")

    if not filtered_notifications.empty:

        notification_summary = (
            filtered_notifications[
                "notification_status"
            ]
            .value_counts()
            .reset_index()
        )

        notification_summary.columns = [
            "Status",
            "Count"
        ]

        st.dataframe(
            notification_summary,
            width="stretch",
            hide_index=True
        )

        with st.expander("View notification details"):

            st.dataframe(
                filtered_notifications,
                width="stretch",
                hide_index=True
            )

    else:

        st.info("No notification records available.")


    st.markdown("### Production Orders")

    if not filtered_production_orders.empty:

        st.dataframe(
            filtered_production_orders,
            width="stretch",
            hide_index=True
        )

    else:

        st.info("No production orders available.")


# ==========================================================
# 13. FOOTER
# ==========================================================

st.divider()

st.markdown("""
<div class="dashboard-footer">
    Supplier Acknowledgement Management System<br>
    Built with Python, Streamlit, SQLite and Plotly<br>
    Internal Project Dashboard | Data sourced from SQLite
</div>
""", unsafe_allow_html=True)
