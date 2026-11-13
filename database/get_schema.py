
import sqlite3
from pathlib import Path
from io import StringIO
from contextlib import redirect_stdout

# Project paths
BASE_DIR = Path(__file__).resolve().parent
DB_PATH = BASE_DIR / "supplier_management.db"
OUTPUT_PATH = BASE_DIR.parent / "docs" / "schema_output.txt"

# Connect to the existing database without creating a new one
conn = sqlite3.connect(
    f"file:{DB_PATH.as_posix()}?mode=rw",
    uri=True
)

cursor = conn.cursor()
report_buffer = StringIO()

try:
    with redirect_stdout(report_buffer):
        cursor.execute("""
            SELECT name
            FROM sqlite_master
            WHERE type = 'table'
            AND name NOT LIKE 'sqlite_%'
            ORDER BY name
        """)

        tables = cursor.fetchall()

        print("========== DATABASE SCHEMA ==========")
        print("Database:", DB_PATH.name)
        print("Total Tables:", len(tables))

        for table in tables:
            table_name = table[0]

            print("\nTABLE NAME:", table_name)
            print("-" * 60)

            cursor.execute(f'PRAGMA table_info("{table_name}")')
            columns = cursor.fetchall()

            print("\nCOLUMNS:")

            for column in columns:
                print(
                    f"Name: {column[1]} | "
                    f"Type: {column[2]} | "
                    f"Not Null: {column[3]} | "
                    f"Primary Key: {column[5]}"
                )

            cursor.execute(f'PRAGMA foreign_key_list("{table_name}")')
            foreign_keys = cursor.fetchall()

            print("\nFOREIGN KEYS:")

            if foreign_keys:
                for fk in foreign_keys:
                    print(
                        f"Column: {fk[3]} | "
                        f"References: {fk[2]} | "
                        f"Referenced Column: {fk[4]}"
                    )
            else:
                print("No foreign keys")

        print("\n========== SCHEMA EXTRACTION COMPLETED ==========")

finally:
    conn.close()

# Save the schema report using UTF-8 encoding
report = report_buffer.getvalue().rstrip() + "\n"
OUTPUT_PATH.write_text(report, encoding="utf-8")

print(report)
print("Schema report saved to:", OUTPUT_PATH)
