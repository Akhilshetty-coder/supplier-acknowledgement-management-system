# Supplier Acknowledgement Management System



A Python and SQLite project for tracking supplier purchase-order acknowledgements, promised delivery dates, quantity changes, and potential supply-chain exceptions.



## 1. Business Problem



When a supplier receives a purchase order (PO), they may accept the requested quantities, reject some quantities, or propose a different delivery date. These changes can affect inventory availability and production schedules.



This project provides a data-management and monitoring prototype to help identify acknowledgement issues and review possible downstream impacts.



## 2. Main Objectives



- Store supplier, purchase order, and PO-line information.

- Record supplier acknowledgements and promised dates.

- Track quantity and delivery-date change requests.

- Apply business rules and identify potential exceptions.

- Record approval and audit information.

- Connect selected purchase-order lines to production requirements.

- Generate synthetic data for testing and analysis.

- Display project information in a Streamlit dashboard.



## 3. Technology Stack



- Python 3.11

- SQLite

- Pandas

- Streamlit

- Plotly

- Jupyter Notebook



## 4. Project Structure



```text

Supplier_Acknowledgement_System/

â”œâ”€â”€ ai_documentation/

â”œâ”€â”€ business_logic/

â”œâ”€â”€ dashboard/

â”œâ”€â”€ data/

â”‚   â””â”€â”€ synthetic/

â”œâ”€â”€ database/

â”œâ”€â”€ docs/

â”œâ”€â”€ notebooks/

â”œâ”€â”€ reports/

â”œâ”€â”€ src/

â”œâ”€â”€ test/

â”œâ”€â”€ main.py

â”œâ”€â”€ requirements.txt

â”œâ”€â”€ .gitignore

â””â”€â”€ README.md

```



## 5. Database Design



The SQLite database schema contains 14 tables:



1\. Supplier

2\. PurchaseOrder

3\. POLine

4\. Acknowledgement

5\. AcknowledgementLine

6\. PromiseDate

7\. ChangeRequest

8\. Approval

9\. InventoryPlan

10\. ProductionOrder

11\. ProductionOrderSupplyAllocation

12\. Notification

13\. AuditLog

14\. DataQualityException



Primary keys and foreign keys connect related records.



## 6. Setup



Requirements: Python 3.11 or compatible, Git, and PowerShell or another terminal.



Create and activate a virtual environment:



```powershell

python -m venv venv

.\\venv\\Scripts\\Activate.ps1

```



Install dependencies:



```powershell

python -m pip install -r requirements.txt

```



## 7. Database Setup



Create the SQLite database and tables:



```powershell

python database/create_database.py

```



Import the supplied synthetic datasets:



```powershell

python database/import_synthetic_data.py

```



Verify the database:



```powershell

python database/check_database.py

python database/verify_all_data.py

```



The database file is generated locally and excluded from Git. Run the setup and import steps to create your own local database.



## 8. Synthetic Data and Validation



Synthetic datasets are stored in `data/synthetic/`.



Run synthetic-data validation:



```powershell

python src/validate_synthetic_data.py

```



The recorded result was 39 checks passed and 0 failed.



The separate notebook `notebooks/02_data_validation.ipynb` has its own reproducibility report documenting 10 checks. These are two different validation activities.



## 9. Business Logic Tests



Run:



```powershell

python -m test.test_business_logic

```



Review the output for acknowledgement, purchase-order, approval, delivery, inventory, production, notification, audit, and exception checks.



Note: the current test script writes audit records to the local database. Repeated runs can add more audit records.



## 10. Run the Dashboard



Run from the project root:



```powershell

streamlit run dashboard/app.py

```



Open the local address displayed by Streamlit in your browser.



## 11. Documentation and Reports



- `docs/business_rules.md` â€” documented business rules.

- `docs/business_rules_validation.md` â€” business-rule validation notes.

- `docs/data_dictionary.md` â€” database table and column descriptions.

- `docs/er_diagram.md` â€” entity-relationship design.

- `reports/` â€” validation and exception reports.

- `ai_documentation/` â€” AI usage disclosure and prompt-history summaries.



## 12. Data Quality Handling



The synthetic dataset includes deliberately invalid or anomalous scenarios for testing. Invalid source records identified during import are retained in the `DataQualityException` table for investigation rather than silently discarded.



The project uses synthetic data. It does not connect to real suppliers, purchase-order platforms, email systems, or production systems.



## 13. Current Scope and Limitations



This is a screening-assignment prototype, not a production-ready supply-chain platform.



- Data is synthetic and does not represent live supplier activity.

- External supplier, ERP, warehouse, and email integrations are not implemented.

- External notification delivery is not provided.

- Approval and exception scenarios are demonstrated through the available business logic and test data. Not every possible end-to-end operational workflow has been implemented.

- Validation reports describe the checks that were actually executed; they do not prove that every possible scenario has been tested.



## 14. AI Assistance Disclosure



AI tools supported requirement understanding, planning, troubleshooting, coding explanations, testing guidance, and documentation. The developer ran commands, reviewed outputs, and checked the implementation.



The prompt-history document contains categorized summaries, not a complete verbatim transcript of every interaction. See `ai_documentation/AI_USAGE_DISCLOSURE.md` and `ai_documentation/AI_PROMPT_HISTORY.md`.



## 15. Author



Developed as an individual technical screening project.
