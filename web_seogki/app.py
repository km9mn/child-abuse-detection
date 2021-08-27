from flask import Flask, url_for, redirect, render_template, request
import re
import time
import bcrypt
import datetime
import pandas as pd
from flask import Flask, render_template, request, redirect, Response
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager, UserMixin, login_user, logout_user
from flask_login import current_user
from flask_sqlalchemy import SQLAlchemy
from flask import flash
from model import *

app = Flask(__name__,static_folder='static',template_folder='templates')
app.secret_key = 'super secret key'
app.config['SESSION_TYPE'] = 'filesystem'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False 
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///child_abuse_detection_database.db'
#app.config['MAX_CONTENT_LENGTH'] = 15 * 640 * 640
db = SQLAlchemy(app)
migrate = Migrate()

def hash_password(password):
    password.encode('utf-8')
    hashed_pw = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    return hashed_pw

def check_email(email):
    result = User.query.filter_by(email=email).all()
    print(result)
    return True if result else False

def convert_datetime(unixtime):
    """Convert unixtime to datetime"""
    date = datetime.datetime.fromtimestamp(unixtime).strftime('%Y-%m-%d %H:%M:%S')
    return date # format : str

def convert_unixtime(date_time):
    """Convert datetime to unixtime"""
    unixtime = datetime.datetime.strptime(date_time,'%Y-%m-%d %H:%M:%S').timestamp()
    return unixtime
           
def check_login(email, pw):
    result = User.query.filter_by(email=email, pw=pw).all()
    print(result)
    return False if result else True

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/main',methods=['GET','POST'])
def maain():
    if request.method == 'GET':
        return render_template('main.html')
    else:
        email = request.form['email'] 
        password = hash_password(request.form['password'])
        if check_login(email,password):
            return render_template('main.html')
        else:
            flash("please put correct email or password")
            return render_template('index.html')

@app.route('/logout')
def logout():
    return render_template('index.html')

@app.route('/register',methods=['GET','POST'])
def register():
    if request.method == 'GET':
        return render_template('register.html')
    else:
        name = request.form.get('name')
        password = hash_password(request.form.get('password'))
        email = request.form.get('email')
        officenum = request.form.get('officenum')
        location1 = request.form.get('locate1')
        location2 = request.form.get('locate2')
        department = request.form.get('dept')
        ph1 = request.form.get('ph_num1')
        ph2 = request.form.get('ph_num2')
        ph3 = request.form.get('ph_num3')
        if check_email(email):
            flash('email already exists')
            return render_template('register.html')
        elif not (name and password and email and officenum and location1 and location2 and department and ph1 and ph2 and ph3):
            flash('fill all the area')
            return render_template('register.html')
        else:
            location_id = Location.query.filter(Location.name==location1+' '+location2).one().id
            user = User(
                email=email,
                pw=password,
                office_num=officenum,
                department=department,
                name=name,
                ph_num1=ph1,
                ph_num2=ph2,
                ph_num3=ph3,
                loc_id = location_id)
            db.session.add(user)
            db.session.commit()
            flash('register finished')
            return render_template('index.html')

@app.route('/list')
def listing():
    return render_template('list.html')

@app.route('/main')
def mainpage():
    return render_template('main.html')

video_data = [
    {
        'index':"1",
        'place':"우리집1-주소는이러쿵저러쿰",
        'time': time.time(),
        'accuracy':"80%",
        'video_info':'testing',
        'video_path':"/static/violence/test3.mp4"
    },
{
        'index':"2",
        'place':"우리집2-주소는이러쿵저러쿰",
        'time': time.time(),
        'accuracy':"180%",
        'video_info':'testing123213',
        'video_path':"/static/violence/test4.mp4"
    },
    {
        'index':"3",
        'place':"우리집3-주소는이러쿵저러쿰",
        'time': time.time(),
        'accuracy':"820%",
        'video_info':'testing please',
        'video_path':"/static/violence/test5.mp4"
    },
    {
        'index':"4",
        'place':"우리집4-주소는이러쿵저러쿰",
        'time': time.time(),
        'accuracy':"803%",
        'video_info':'testin1231221331123123g',
        'video_path':"/static/violence/test6.mp4"
    }
]
video_data2 = [
    {
        'index':"3",
        'place':"우리집3-주소는이러쿵저러쿰",
        'time': time.time(),
        'accuracy':"820%",
        'video_info':'testing please',
        'video_path':"/static/violence/test5.mp4"
    },
    {
        'index':"4",
        'place':"우리집4-주소는이러쿵저러쿰",
        'time': time.time(),
        'accuracy':"803%",
        'video_info':'testin1231221331123123g',
        'video_path':"/static/violence/test6.mp4"
    },
    {
        'index':"1",
        'place':"우리집1-주소는이러쿵저러쿰",
        'time': time.time(),
        'accuracy':"80%",
        'video_info':'testing',
        'video_path':"/static/violence/test3.mp4"
    },
    {
        'index':"2",
        'place':"우리집2-주소는이러쿵저러쿰",
        'time': time.time(),
        'accuracy':"180%",
        'video_info':'testing123213',
        'video_path':"/static/violence/test4.mp4"
    }
]
@app.route('/video')
def video():
    test = """
    Located in sdafpk
    Model ACcuracy : 50%
    Stuff like that
    """
    return render_template('video.html', video_table_data=video_data, data_length=len(video_data), video_info=test, video_table_data_t=video_data2)

@app.route('/report/<video_id>')
def report_police(video_id):
    # report 처리
    return 'report ' + str(video_id)
    return render_template('list.html')

@app.route('/safe/<video_id>')
def safe_video(video_id):
    # safe 처리
    return 'safe ' + str(video_id)
    return render_template('list.html')
    
if __name__ == '__main__':
      app.run(debug=True)

