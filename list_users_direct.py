import sqlite3
import os

db_path = os.path.join('instance', 'project.db')
if not os.path.exists(db_path):
    print(f"Database not found at {db_path}")
else:
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT name, email, role FROM user")
        rows = cursor.fetchall()
        print("-" * 50)
        print(f"{'Name':<20} | {'Email':<30} | {'Role':<15}")
        print("-" * 50)
        for row in rows:
            print(f"{row[0]:<20} | {row[1]:<30} | {row[2]:<15}")
        print("-" * 50)
    except Exception as e:
        print(f"Error: {e}")
    finally:
        conn.close()
