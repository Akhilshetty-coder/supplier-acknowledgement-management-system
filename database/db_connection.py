
import sqlite3
import os

# Get the current database folder path
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Database file path
DB_PATH = os.path.join(BASE_DIR, "supplier_management.db")


# Function to connect to the database
def get_connection():

    connection = sqlite3.connect(DB_PATH)

    # Enable foreign key validation
    connection.execute("PRAGMA foreign_keys = ON")

    return connection
