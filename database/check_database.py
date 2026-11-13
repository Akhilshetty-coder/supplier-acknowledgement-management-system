
import sqlite3
import os

db_path = os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    "supplier_management.db"
)

connection = sqlite3.connect(db_path)

connection.execute("PRAGMA foreign_keys = ON")

cursor = connection.cursor()

cursor.execute("""
    SELECT name
    FROM sqlite_master
    WHERE type = 'table'
    ORDER BY name
""")

tables = cursor.fetchall()

print("DATABASE TABLE VERIFICATION")
print("============================")

for table in tables:
    print("Table:", table[0])

print("\nFOREIGN KEY CHECK")

for table in tables:
    cursor.execute(
        f'PRAGMA foreign_key_list("{table[0]}")'
    )

    for fk in cursor.fetchall():
        print(table[0], "references", fk[2])

cursor.execute("PRAGMA foreign_key_check")

errors = cursor.fetchall()

print("\nFOREIGN KEY ERRORS:", len(errors))

connection.close()
