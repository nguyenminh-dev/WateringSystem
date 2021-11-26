import sqlite3
import hashlib
import datetime
import sys
import os

con = sqlite3.connect('db.sqlite3')

cur = con.cursor()

# cur.execute("CREATE TABLE Users(Id INTEGER PRIMARY KEY AUTOINCREMENT, UserName TEXT, Email TEXT, PhoneNumber TEXT, Password TEXT)")

# cur.execute("CREATE TABLE Modes(Id INTEGER PRIMARY KEY AUTOINCREMENT, Mode TEXT, Soil REAL, Temp REAL, Humid REAL, Status BOOL, SprayMode TEXT, AmountWater REAL,Time REAL, CreateTime DATE)")

cur.execute("INSERT INTO Users VALUES(1,'admin','admin@gmail.com','1234','Admin@123')")
cur.execute("INSERT INTO Users VALUES(2,'admin1','admin@gmail.com','1234','Admin@123')")

cur.execute('SELECT * FROM Users')

result = cur.fetchall()
for row in result:
    print (row)
print(result)