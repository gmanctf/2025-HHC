import os
import json
import sqlite3

# Path to the folder containing the request files
FOLDER = "./idor"
DBFILE = "receipts.db"

# Connect to SQLite
conn = sqlite3.connect(DBFILE)
cur = conn.cursor()

# Create tables if they don't exist
cur.execute("""CREATE TABLE IF NOT EXISTS receipts (
    id INTEGER PRIMARY KEY,
    customer TEXT,
    date TEXT,
    table_number INTEGER,
    total REAL,
    paid BOOLEAN,
    note TEXT
)""")

cur.execute("""CREATE TABLE IF NOT EXISTS items (
    receipt_id INTEGER,
    name TEXT,
    price REAL
)""")

def extract_json(filepath):
    with open(filepath, "r") as f:
        content = f.read()
    # JSON starts at the first '{'
    start = content.find("{")
    if start == -1:
        return None
    return json.loads(content[start:])

# Iterate over all files in the folder
for filename in os.listdir(FOLDER):
    filepath = os.path.join(FOLDER, filename)
    if not os.path.isfile(filepath):
        continue

    data = extract_json(filepath)
    if not data:
        print(f"Skipping {filename}, no JSON found")
        continue

    # Insert into receipts table
    cur.execute("""INSERT OR IGNORE INTO receipts
        (id, customer, date, table_number, total, paid, note)
        VALUES (?, ?, ?, ?, ?, ?, ?)""",
        (data["id"], data["customer"], data["date"], data["table"],
         data["total"], data["paid"], data["note"]))

    # Insert items
    for item in data["items"]:
        cur.execute("""INSERT INTO items (receipt_id, name, price)
                       VALUES (?, ?, ?)""",
                    (data["id"], item["name"], item["price"]))

    print(f"Imported {filename}")

conn.commit()
conn.close()
