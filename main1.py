import eventlet
from flask import Flask, render_template, Response, request, redirect, url_for, flash
from flask_mqtt import Mqtt
from flask_socketio import SocketIO
import json, datetime, time, threading, pytz
import flask_login
import database


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
                return render_template('manager.html', usrname=usrname) 
            else:
                user = User(usrid, usrname)
                flask_login.login_user(user)
                return render_template('User-homepage.html', usrname=usrname) 
            
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



if __name__ == '__main__':    
    app.run(debug=True)