import sqlite3
import hashlib
import datetime
from sqlite3.dbapi2 import Date
import sys
import os

DATABASE = 'db.sqlite3'

con = sqlite3.connect('db.sqlite3')

cur = con.cursor()

# cur.execute("""
# CREATE TABLE Users(
#     UserName TEXT NOT NULL UNIQUE, 
#     Email TEXT, 
#     PhoneNumber TEXT, 
#     Password TEXT,
#     Role TEXT
# )
# """)

# cur.execute("""
# CREATE TABLE Modes(
#     Mode TEXT NOT NULL UNIQUE, 
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
# cur.execute("INSERT INTO Modes(Mode, Soil, Temp, Humid, Status, SprayMode, AmountWater, Time, CreateTime) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)", ('Cây cà chua', 50, 100, 150, 1, 'Phun sương', 10, 90, '2021-11-28'))
# cur.execute("INSERT INTO Modes(Mode, Soil, Temp, Humid, Status, SprayMode, AmountWater, Time, CreateTime) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)", ('Cây rau cải', 50, 100, 150, 1, 'Phun sương', 10, 90, '2021-11-28'))
# cur.execute("INSERT INTO Modes(Mode, Soil, Temp, Humid, Status, SprayMode, AmountWater, Time, CreateTime) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)", ('Cây vải', 50, 100, 150, 1, 'Phun sương', 10, 90, '2021-11-28'))

# cur.execute('SELECT * FROM Users')

# result = cur.fetchall()
# for row in result:
#     print (row)
# print(result)
cur.execute('SELECT * FROM Modes')

result = cur.fetchall()
for row in result:
    print (row)
print(result)
con.commit()
con.close()