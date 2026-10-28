import sqlite3
import os

db_path = r"c:\Users\Admin\Desktop\ai rules and skills\extracted_apk\com_fakechat_unpacked\assets\fakeitemzalo.sqlite"
if os.path.exists(db_path):
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()
    cur.execute("SELECT name FROM sqlite_master WHERE type='table'")
    tables = cur.fetchall()
    print("Tables in fakeitemzalo:", tables)
    for t in tables:
        name = t[0]
        print(f"\n--- Table {name} ---")
        cur.execute(f"PRAGMA table_info({name})")
        for col in cur.fetchall():
            print("  Col:", col[1], col[2])
        cur.execute(f"SELECT * FROM {name} LIMIT 3")
        for row in cur.fetchall():
            print("  Row:", row)

