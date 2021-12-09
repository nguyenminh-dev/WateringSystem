import eventlet
from flask import Flask, render_template, Response, request, redirect, url_for, flash
from flask_mqtt import Mqtt
from flask_socketio import SocketIO
import json, datetime, time, threading, pytz
import flask_login
import database
import connectBBC1
import getDataRelay
from Adafruit_IO import Client
from flask_wtf import FlaskForm
from wtforms import SubmitField
from flask_bootstrap import Bootstrap
import random
from datetime import date

ADAFRUIT_IO_USERNAME = ""
ADAFRUIT_IO_KEY = ""
# ADAFRUIT_IO_USERNAME = "CSE_BBC"
# ADAFRUIT_IO_KEY = "aio_eIzx84QrfGct3jkJM5aW02aKAIbB"
aio=Client(ADAFRUIT_IO_USERNAME, ADAFRUIT_IO_KEY)
app = Flask(__name__)
app.secret_key = 'hcmutk18'

login_manager = flask_login.LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"
login_manager.login_message = "User needs to be logged in to view this page"
login_manager.login_message_category = "error"

class User(flask_login.UserMixin):
    def __init__(self, userid, username):
        self.id = userid
        self.name = username
save_data = dict(tuoinuoc=0)
@login_manager.user_loader
def load_user(userId):
    userName = database.getNameById(userId)
    return User(userId, userName)

@app.route('/')
def index():
    if hasattr(flask_login.current_user, 'name'):
        return render_template('index.html', name=flask_login.current_user.name)       
    else:        
        return render_template('index.html')

@app.route('/logout')
def logout():
    flask_login.logout_user()
    return redirect(url_for('index'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if database.getPasswordByUserName(username) == None or database.loginUser(username, password) == False:
            flash('Wrong email or password. Please try again!', category='error')
            return render_template('login.html')
        else: 
            usrid, usrname, role = database.getIdNameByUserName(username, password)
            flash('Login successful!', category='success')
            if(role == 'Admin'):
                user = User(usrid, usrname)
                flask_login.login_user(user)
                return redirect(url_for('adminhomepage'))
            else:
                user = User(usrid, usrname)
                flask_login.login_user(user)
                return redirect(url_for('userhomepage')) 
            
    return render_template('login.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    error = None
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        phonenumber = request.form['phonenumber']
        password = request.form['password']
        role = 'User'
        if database.getPasswordByUserName(username) != None:
            flash('Account already exists. Please try another Username!', category='error')
        else:            
            database.createUser(username, email, phonenumber, password, role)
            flash('Register successful!', category='susscess')
    return render_template('signup.html', error=error)

@app.route('/area')
@flask_login.login_required
def area():
    user = flask_login.current_user   
    return render_template('area.html', usrname=user.name)

@app.route('/userhomepage')
@flask_login.login_required
def userhomepage():
    user = flask_login.current_user   
    return render_template('User-homepage.html', usrname=user.name)

@app.route('/adminhomepage')
@flask_login.login_required
def adminhomepage():
    user = flask_login.current_user   
    return render_template('Admin-homepage.html', usrname=user.name)

@app.route('/manager', methods=['GET', 'POST', 'PUT'])
@flask_login.login_required
def manager():
    error = None
    if request.method == 'PUT':
        rowid = request.form['rowid']
        mode = request.form['username']
        soil = request.form['soil']
        temp = request.form['temp']
        humid = request.form['humid']
        status = request.form['status']
        spraymode = request.form['spraymode']
        amountwater = request.form['amountwater']
        time = request.form['time']
        createtime = request.form['createtime']
        code = request.form['code']
        if database.getIdbyName(mode) != None:
            flash('Mode already exists. Please try another name!', category='error')
        else:
            database.updateModes(rowid, mode, soil, temp, humid, status, spraymode, amountwater, time, createtime, code)
            flash('Update successful!', category='susscess')
    
    modes = database.getModes()
    user = flask_login.current_user   
    return render_template('manager.html', usrname=user.name, modes = modes)

@app.route('/manager/create', methods=['POST'])
@flask_login.login_required
def createMode():
    now = datetime.datetime.now()
    timestamp_th = now.strftime("%Y-%m-%d %H:%M:%S+07:00")
    if request.method == 'POST':
        mode = request.form['mode']
        soil = request.form['soil']
        temp = request.form['temp']
        humid = request.form['humid']
        status = 0
        spraymode = request.form['spraymode']
        amountwater = request.form['amountwater']
        time = 60
        createtime = timestamp_th
        code = randomCode()
        if database.getIdbyName(mode) != None:
            flash('Mode already exists. Please try another name!', category='error')
        else:            
            database.addModes(mode, soil, temp, humid, status, spraymode, amountwater, time, createtime, code)
            flash('Create successful!', category='susscess')    
    return redirect(url_for('manager'))

@app.route('/update/<int:code>', methods=['POST', 'GET'])
@flask_login.login_required
def updateMode(code):
    mode = database.getInfoUpdate(code)[0]
    soil = database.getInfoUpdate(code)[1]
    temp = database.getInfoUpdate(code)[2]
    humid = database.getInfoUpdate(code)[3]
    
    if request.method == 'POST':
        mode = request.form['mode']
        soil = request.form['soil']
        temp = request.form['temp']
        humid = request.form['humid']
        database.updateModes(mode, soil, temp, humid, code)
        return redirect(url_for('manager'))
    else:
        return render_template('updateMode.html', mode=mode, soil=soil, temp=temp, humid=humid, code = code)

@app.route('/delete/<int:code>')
@flask_login.login_required
def deleteMode(code):
    database.deleteModes(code)
    flash('Delete successful!', category='susscess')
    return redirect(url_for('manager'))

@app.route('/detailhand', methods=['GET', 'POST'])
@flask_login.login_required
def detailhand():
    user = flask_login.current_user   
    return render_template('detail_hand.html', usrname=user.name)

@app.route('/detailauto', methods=['GET', 'POST'])
@flask_login.login_required
def detailauto():
    modes = database.getModes()
    user = flask_login.current_user   
    return render_template('detail_auto.html', usrname=user.name, modes = modes)

@app.route('/autowatering', methods=['GET', 'POST'])
@flask_login.login_required
def autowatering():
    mode = request.form.get('comp_select')
    soil = database.getInfoByMode(mode)[1]
    temp = database.getInfoByMode(mode)[2]
    humid = database.getInfoByMode(mode)[3]
    autoWateringMode(temp,humid,soil)
    user = flask_login.current_user   
    return render_template('selectMode.html', usrname=user.name, soil=soil, mode = mode, temp = temp, humid = humid)

@app.route('/temp')
def temp():
    def generate():
        yield str(database.getLastAir()[0])
    return Response(generate(), mimetype='text')

@app.route('/humid')
def humid():
    def generate():
        yield str(database.getLastAir()[1])
    return Response(generate(), mimetype='text')

@app.route('/soil')
def soil():
    def generate():
        yield str(database.getLastSoil()[0])
    return Response(generate(), mimetype='text')

@app.route('/relay')
def relay():
    def generate():
        yield str(database.getLastPump()[0])
    return Response(generate(), mimetype='text')

def randomCode():
    a = random.randint(1, 10000)
    if database.getModeByCode(a) != None:
        return randomCode()
    return a

def autoWateringMode(temp, humid, soil):
    temp1 = database.getLastAir()[0]
    humid1 = database.getLastAir()[1]
    soil1 = database.getLastSoil()[0]
    pump = database.getLastPump()[0]
    now = datetime.datetime.now()
    timestamp_th = now.strftime("%Y-%m-%d %H:%M:%S+07:00")
    if soil1 < soil:
        if temp1 < temp and humid1 > humid and pump == 'OFF':
            data = {"id":"11","name":"RELAY","data":"1","unit":""}
            database.insertPump('ON', timestamp_th)
            connectBBC1.PublishData(data)
    elif soil1 < 50 and pump =='OFF':
            data = {"id":"11","name":"RELAY","data":"1","unit":""}
            database.insertPump('ON', timestamp_th)
            connectBBC1.PublishData(data)
    elif soil1 > 450:
        if pump == 'ON':
            data = {"id":"11","name":"RELAY","data":"0","unit":""}
            database.insertPump('OFF', timestamp_th)
            connectBBC1.PublishData(data)
    else:
        data = {"id":"11","name":"RELAY","data":"0","unit":""}
        database.insertPump('OFF', timestamp_th)
        connectBBC1.PublishData(data)

def autoWatering():
    threading.Timer(5.0, autoWatering).start()
    temp1 = database.getLastAir()[0]
    humid1 = database.getLastAir()[1]
    soil1 = database.getLastSoil()[0]
    pump = database.getLastPump()[0]
    now = datetime.datetime.now()
    timestamp_th = now.strftime("%Y-%m-%d %H:%M:%S+07:00")
    if soil1 < 10 and pump =='OFF':
        data = {"id":"11","name":"RELAY","data":"1","unit":""}
        database.insertPump('ON', timestamp_th)
        connectBBC1.PublishData(data)
    elif soil1 > 300 and pump =='ON':
        data = {"id":"11","name":"RELAY","data":"0","unit":""}
        database.insertPump('OFF', timestamp_th)
        connectBBC1.PublishData(data)

def getDataFromServer():
    threading.Timer(5.0, getDataFromServer).start()
    hcm_time_zone = pytz.timezone("Asia/Ho_Chi_Minh")
    temp_humid_server = aio.receive('bk-iot-temp-humid')
    timestamp_th = datetime.datetime.strptime(temp_humid_server[1], '%Y-%m-%dT%H:%M:%S%z')
    timestamp_th = timestamp_th.astimezone(hcm_time_zone)
    if str(timestamp_th) != database.getLastAir()[2]:
        data = temp_humid_server[3]
        data = data.replace("'", '"')
        data = json.loads(data)
        pos_minus = data['data'].find('-')
        temp = data['data'][:pos_minus]
        humid = data['data'][pos_minus + 1:]
        database.insertAir(temp, humid, timestamp_th)
    else:
        pass
    soil_server = aio.receive('bk-iot-soil')
    timestamp_s = datetime.datetime.strptime(soil_server[1], '%Y-%m-%dT%H:%M:%S%z')
    timestamp_s = timestamp_s.astimezone(hcm_time_zone)
    if str(timestamp_s) != database.getLastSoil()[1]:
        data = soil_server[3]
        data = data.replace("'", '"')
        data = json.loads(data)
        soil = data['data']
        database.insertSoil(soil, timestamp_s)
    else:
        pass
    getDataRelay.getDataRelay()


getDataFromServer()
# autoWatering()
if __name__ == '__main__':    
    app.run(debug=True)