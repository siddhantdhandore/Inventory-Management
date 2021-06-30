import sqlite3
conn =sqlite3.connect('newdatabase.db')
cur = conn.cursor()

x=cur.execute("select * from products;")
print(x.fetchall())
conn.close()
