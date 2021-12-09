import sqlite3
import hashlib
import datetime
from sqlite3.dbapi2 import Date
import datetime

DATABASE = 'db.sqlite3'

con = sqlite3.connect('db.sqlite3')

cur = con.cursor()

cur.execute("""
CREATE TABLE Users(
    UserName TEXT NOT NULL UNIQUE, 
    Email TEXT, 
    PhoneNumber TEXT, 
    Password TEXT,
    Role TEXT
)
""")

cur.execute("""
CREATE TABLE Modes(
    Mode TEXT NOT NULL UNIQUE, 
    Soil REAL, 
    Temp REAL, 
    Humid REAL, 
    Status BOOL, 
    SprayMode TEXT, 
    AmountWater REAL,
    Time REAL, 
    CreateTime DATE,
    Code INT NOT NULL UNIQUE
)
""")

cur.execute("""
CREATE TABLE Soils(
    Soil REAL,
    Timestamp DATE
)
""")

cur.execute("""
CREATE TABLE Airs(
    Temp REAL,
    Humid REAL,
    Timestamp DATE
)
""")

cur.execute("""
CREATE TABLE Pumps(
    Status TEXT,
    Timestamp DATE
)
""")

now = datetime.datetime.now()
timestamp_th = now.strftime("%Y-%m-%d %H:%M:%S+07:00")

password = 'Admin@123'
passwordhash = hashlib.md5(password.encode('utf8')).hexdigest()
cur.execute("INSERT INTO Users(UserName, Email, PhoneNumber, Password, Role) VALUES (?, ?, ?, ?, ?)", ('admin', 'admin@123', '123', passwordhash, 'Admin'))
cur.execute("INSERT INTO Modes(Mode, Soil, Temp, Humid, Status, SprayMode, AmountWater, Time, CreateTime, Code) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", ('Cây cà chua', 50, 100, 150, 0, 'Phun sương', 10, 90, timestamp_th, 1))
cur.execute("INSERT INTO Modes(Mode, Soil, Temp, Humid, Status, SprayMode, AmountWater, Time, CreateTime, Code) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", ('Cây rau cải', 50, 100, 150, 0, 'Phun sương', 10, 90, timestamp_th, 2))
cur.execute("INSERT INTO Modes(Mode, Soil, Temp, Humid, Status, SprayMode, AmountWater, Time, CreateTime, Code) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", ('Cây vải', 50, 100, 150, 0, 'Phun sương', 10, 90, timestamp_th, 3))
cur.execute("INSERT INTO Airs values (?, ?, ?)", (30,50,timestamp_th))
cur.execute("INSERT INTO Soils values (?, ?)", (60,timestamp_th))
cur.execute("INSERT INTO Pumps values (?, ?)", ('ON',timestamp_th))
# cur.execute('SELECT * FROM Users')

# result = cur.fetchall()
# for row in result:
#     print (row)
# print(result)
# cur.execute('SELECT * FROM Modes')

# result = cur.fetchall()
# for row in result:
#     print (row)
# print(result)
# cur.execute('SELECT * FROM Pumps')

# result = cur.fetchall()
# for row in result:
#     print (row)
# print(result)
# cur.execute('SELECT * FROM Soils')

# result = cur.fetchall()
# for row in result:
#     print (row)
# print(result)
con.commit()
con.close()