import sqlite3 
conn=sqlite3.connect('Employee.db')
cur=conn.cursor()
# cur.execute("""CREATE TABLE Employee_db
# (Emp_ID INTEGER PRIMARY KEY AUTOINCREMENT,
# Emp_Name TEXT,
# Contact TEXT UNIQUE ,
# Department TEXT,
# Salary INTEGER);""")
# print("Table Created")

# cur.execute("""INSERT INTO Employee_db
# (Emp_Name, Contact, Department, Salary)
# values('Regina K', '080-251477', 'Sales', 20000);""")

# cur.execute("""INSERT INTO Employee_db
# (Emp_Name, Contact, Department, Salary)
# values('Alex', '9898911111', 'Testing', 25000);""")

# cur.execute("""INSERT INTO Employee_db
# (Emp_Name, Contact, Department, Salary)
# values('Anika', '+91-9422783131', 'Test', 20000);""")

# cur.execute("""INSERT INTO Employee_db
# (Emp_Name, Contact, Department, Salary)
# values('Peter', '8881217777', 'Development', 40000);""")

# cur.execute("""INSERT INTO Employee_db
# (Emp_Name, Contact, Department, Salary)
# values('Jenny', '8797224151', 'Sales', 35000);""")
# print("values inserted")
records = cur.execute("SELECT Emp_Name, Department FROM Employee_db;").fetchall()
print(records)
conn.commit()
conn.close()