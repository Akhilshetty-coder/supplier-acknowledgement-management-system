# AI Prompt History



## Project: Supplier Acknowledgement Management System



This document records the main categories of prompts used during project development. The entries below are representative summaries, not guaranteed verbatim copies of every original prompt. The developer should add or correct entries using available conversation histories and records from other AI tools.



## 1. Business Requirement Understanding



**Prompt summary:**



Explain the supplier acknowledgement management business problem, project objectives, actors, workflow, and expected system functionality in simple language.



**Purpose:** Understand the screening assignment before starting implementation.



## 2. Project Planning



**Prompt summary:**



Break the Supplier Acknowledgement Management System into step-by-step development operations and explain how to complete each operation.



**Purpose:** Organize implementation into manageable stages.



## 3. Database Design



**Prompt summary:**



Help design the SQLite database tables, primary keys, foreign keys, relationships, and data dictionary for supplier acknowledgements and purchase order management.



**Purpose:** Understand database structure and maintain data integrity.



## 4. Business Logic



**Prompt summary:**



Explain and test business rules for supplier acknowledgements, quantity changes, delivery dates, approvals, inventory plans, notifications, and audit history.



**Purpose:** Implement and verify workflow rules.



## 5. Synthetic Data Generation



**Prompt summary:**



Generate reproducible synthetic datasets for suppliers, purchase orders, PO lines, acknowledgements, acknowledgement lines, promised dates, change requests, and inventory plans.



**Purpose:** Test the system with larger datasets.



## 6. Data Validation



**Prompt summary:**



Validate synthetic CSV datasets for duplicate identifiers, missing references, invalid statuses, quantity problems, and intentionally injected anomalies.



**Purpose:** Check dataset quality and anomaly detection.



## 7. Database Import



**Prompt summary:**



Import synthetic CSV datasets into SQLite while preserving foreign-key relationships and retaining invalid source records for investigation.



**Purpose:** Replace the small sample dataset with larger synthetic records.



## 8. Dashboard Development



**Prompt summary:**



Improve the Streamlit dashboard to display supplier, purchase order, acknowledgement, delivery, and operational information with filters and charts.



**Purpose:** Make project results easier to understand.



## 9. Troubleshooting



**Prompt summary:**



Explain Python, PowerShell, SQLite, and dashboard errors and provide steps to diagnose and fix them.



**Purpose:** Resolve development issues.



## 10. Documentation and Submission



**Prompt summary:**



Prepare project documentation, installation instructions, testing instructions, AI usage disclosure, and final GitHub submission checklist.



**Purpose:** Prepare the project for technical evaluation.



## 11. AI Tool Usage



AI tools were used as supporting resources. The developer reviewed suggestions, executed commands, checked results, and validated the implementation.



**Accuracy note:** This is a categorized prompt summary. It is not a complete verbatim transcript. Additional prompts used with ChatGPT and other AI tools should be included where available.
