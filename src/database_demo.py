import sqlite3
from pathlib import Path

DB_PATH = Path("data/sales.db")
SCHEMA_PATH = Path("sql/schema.sql")

def main():
    #Create/connect to database
    conn = sqlite3.connect(DB_PATH)


    #Create cursor object
    cursor = conn.cursor()


    #Create table
    with open(SCHEMA_PATH, "r") as f:
        schema_sql = f.read()

    cursor.executescript(schema_sql)


    # Insert sample data
    sample_data = [
        ("Notebook", 25),
        ("Sticker", 40),
        ("Mug", 15)
    ]


    cursor.executemany("""
    INSERT INTO sales (product_name, quantity)
    VALUES (?, ?)
    """, sample_data)


    # Commit changes
    conn.commit()


    #Query data
    cursor.execute("SELECT * FROM sales")


    rows = cursor.fetchall()


    print("\nSales Table:")
    for row in rows:
        print(row)


    #Close connection
    conn.close()


if __name__ == "__main__":
    main()