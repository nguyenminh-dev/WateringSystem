import sqlite3
import hashlib
import datetime
import sys
import os

DATABASE = 'db.sqlite3'

def hashPassword(password):
    hashpassword = hashlib.md5(password.encode('utf8')).hexdigest()
    return hashpassword

def connectDatabase(database):
    con = None
    try:
        con = sqlite3.connect(database)
    except sqlite3.Error as e:
        print ("Error %s:" % e.args[0])
        sys.exit(1)
    return con

def createUser(username, email, phonenumber, password, Role):
    cipherpassword = hashPassword(password)
    con = connectDatabase(DATABASE)
    cur = con.cursor()
    cur.execute("INSERT INTO Users(UserName, Email, PhoneNumber, Password, Role) VALUES (?, ?, ?, ?, ?)", (username, email, phonenumber, cipherpassword, Role))
    con.commit()
    con.close()
    return True

def getPasswordByUserName(username):
    con = connectDatabase(DATABASE)
    cur = con.cursor()
    cur.execute("Select Password FROM Users WHERE UserName=?", [username])
    rows = cur.fetchall()
    if rows:
        con.commit()
        con.close()
        return rows[0][0]
    else:
        return None

def loginUser(username, password):
    if hashPassword(password) == getPasswordByUserName(username):
        return True
    else:
        return False

def getNameById(userId):
    con = connectDatabase(DATABASE)
    cur = con.cursor()
    cur.execute("SELECT UserName from Users WHERE rowid=?", [userId])
    rows = cur.fetchall()
    con.commit()
    con.close()
    if rows:
        return rows[0][0]
    else:
        return None

def getIdNameByUserName(username, password):
    if loginUser(username, password):
        con = connectDatabase(DATABASE)
        cur = con.cursor()
        cur.execute("SELECT rowid, UserName, Role FROM Users WHERE UserName=?", [username])
        rows = cur.fetchall()
        con.commit()
        con.close()
        return rows[0][0], rows[0][1], rows[0][2]
    else:
        return None

def getModes():
    con = connectDatabase(DATABASE)
    cur = con.cursor()
    cur.execute("SELECT * FROM Modes")
    rows = cur.fetchall()
    con.commit()
    con.close()
    if rows:
        return rows
    else: return 0

def addModes(mode, soil, temp, humid, status, spraymode, amountwater, time, createtime):
    con = connectDatabase(DATABASE)
    cur = con.cursor()
    cur.execute("INSERT INTO Modes(Mode, Soil, Temp, Humid, Status, SprayMode, AmountWater, Time, CreateTime) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)", (mode, soil, temp, humid, status, spraymode, amountwater, time, createtime))
    con.commit()
    con.close()
    return True

def updateModes(rowid, mode, soil, temp, humid, status, spraymode, amountwater, time, createtime):
    con = connectDatabase(DATABASE)
    cur = con.cursor()
    cur.execute("UPDATE Modes SET Mode= ?, Soil= ?, Temp=?, Humid=?, Status=?, SprayMode=?, AmountWater=?, Time=?, CreateTime=? WHERE rowid=?" , (mode, soil, temp, humid, status, spraymode, amountwater, time, createtime, rowid))
    con.commit()
    con.close()
    return True

def deleteModes(mode):
    con = connectDatabase(DATABASE)
    cur = con.cursor()
    cur.execute("DELETE FROM Modes WHERE Mode = ?", [mode])
    con.commit()
    con.close()
    return True

def getIdbyName(ModeName):
    con = connectDatabase(DATABASE)
    cur = con.cursor()
    cur.execute("SELECT rowid from Modes WHERE Mode=?", [ModeName])
    rows = cur.fetchall()
    con.commit()
    con.close()
    if rows:
        return rows[0][0]
    else:
        return None