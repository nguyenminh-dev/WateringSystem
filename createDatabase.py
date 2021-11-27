import sqlite3
import hashlib
import datetime
import sys
import os

DATABASE = 'db.sqlite3'

con = sqlite3.connect('db.sqlite3')

cur = con.cursor()

# cur.execute("""
# CREATE TABLE Users(
#     UserName TEXT, 
#     Email TEXT, 
#     PhoneNumber TEXT, 
#     Password TEXT,
#     Role TEXT
# )
# """)

# cur.execute("""
# CREATE TABLE Modes(
#     Mode TEXT, 
#     Soil REAL, 
#     Temp REAL, 
#     Humid REAL, 
#     Status BOOL, 
#     SprayMode TEXT, 
#     AmountWater REAL,
#     Time REAL, 
#     CreateTime DATE
# )
# """)
# password = 'admin'
# passwordhash = hashlib.md5(password.encode('utf8')).hexdigest()
# cur.execute("INSERT INTO Users(UserName, Email, PhoneNumber, Password, Role) VALUES (?, ?, ?, ?, ?)", ('admin', 'admin@123', '123', passwordhash, 'Admin'))
cur.execute('SELECT * FROM Users')

result = cur.fetchall()
for row in result:
    print (row)
print(result)

con.commit()
con.close()