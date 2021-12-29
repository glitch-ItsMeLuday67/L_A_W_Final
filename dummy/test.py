import sqlite3

conn = sqlite3.connect("database/users.db")
cur = conn.cursor()

cur.execute("SELECT * FROM registration_db;")
records = cur.fetchall()
print(records)