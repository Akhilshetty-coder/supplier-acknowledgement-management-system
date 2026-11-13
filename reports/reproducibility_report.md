# Reproducibility Report

## Environment
- Operating system: Windows-10-10.0.26300-SP0
- Python: 3.11.9
- Pandas: 3.1.1
- SQLite: 3.45.1
- Database: `database/supplier_management.db`
- Notebook: `notebooks/02_data_validation.ipynb`

## How to reproduce
1. Open the project folder in VS Code.
2. Open `notebooks/02_data_validation.ipynb`.
3. Select the project's Python virtual environment kernel.
4. Ensure the database and `data/ground_truth/ground_truth.csv` are present.
5. Run all notebook cells from top to bottom.
6. Review the results in `reports/validation_summary.csv`.

The validation queries read the database. The notebook writes the validation summary report.

## Results
- Validation checks: 10
- Passed: 10
- Failed: 0
- Summary file: `reports/validation_summary.csv`

The ground-truth check compares scenario IDs with production primary-key IDs; it does not compare every database text value.
