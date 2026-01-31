import sqlite3
import os

db_path = os.path.join('instance', 'project.db')
if not os.path.exists(db_path):
    print(f"Database not found at {db_path}")
else:
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = [t[0] for t in cursor.fetchall()]
        print(f"Tables: {', '.join(tables)}")
        
        for table in tables:
            print(f"\nContents of table '{table}':")
            cursor.execute(f"SELECT * FROM {table} LIMIT 5;")
            cols = [description[0] for description in cursor.description]
            print(" | ".join(cols))
            rows = cursor.fetchall()
            for row in rows:
                print(" | ".join(map(str, row)))
    except Exception as e:
        print(f"Error: {e}")
    finally:
        conn.close()
