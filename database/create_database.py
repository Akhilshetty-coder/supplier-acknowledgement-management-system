
import sqlite3
import os

# Get the current project directory
BASE_DIR = os.path.dirname(
    os.path.dirname(os.path.abspath(__file__))
)

# Database file location
DB_PATH = os.path.join(
    BASE_DIR,
    "database",
    "supplier_management.db"
)

# SQL schema file location
SCHEMA_PATH = os.path.join(
    BASE_DIR,
    "database",
    "schema.sql"
)

# Connect to SQLite database
connection = sqlite3.connect(DB_PATH)

# Enable foreign key validation
connection.execute("PRAGMA foreign_keys = ON")

# Read SQL schema
with open(SCHEMA_PATH, "r") as file:
    schema = file.read()

# Execute all table creation queries
connection.executescript(schema)

# Save changes
connection.commit()

# Display created tables
cursor = connection.cursor()

cursor.execute("""
    SELECT name
    FROM sqlite_master
    WHERE type = 'table'
    ORDER BY name
""")

tables = cursor.fetchall()

print("Database created successfully!")

print("\nTables created:")

for table in tables:
    print("-", table[0])

# Close database connection
connection.close()
