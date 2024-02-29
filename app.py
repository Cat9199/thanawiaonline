# Project: ScholarSync Back-end
# Author: Abdelrahman Nasr
# GitHub Username: Cat9199
# Total Coding Time: 530 hours
# Project Start Date: 29th October 2023, 4:53 PM
# Project End Date: TBD

# ========================== Import lib ==========================

from flask import Flask, redirect, url_for, jsonify , session, request, render_template, Response
from google.auth.transport import requests
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from sqlalchemy.sql import func
from models.fpass import send_reset_password_email
from datetime import datetime as dt, date , timedelta
from flask_cors import CORS
import datetime
import secrets
import requests
import base64
import os
import io
import requests
import json


# ========================== Config ==========================
global APP_URL
APP_URL = 'https://scholarsync.e3lanotopia.software/'
app = Flask(__name__)
app.secret_key = 'E3lanoTopia3024SchoolarSyncApi-1.0' 
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(days=30)
CLIENT_ID = "275922294832-2ek3htov4h98h4r0l5edpnaqcbchhp1e.apps.googleusercontent.com"
CLIENT_SECRET = "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"
REDIRECT_URI = "https://thanawionline.e3lanotopia.software/callback"
SCOPES = ['openid', 'email', 'profile']
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'database.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
api_key  = 'acc_5096faf3f7807f9'
api_secret  = 'bf48a14618503e7bed7304ad193a3010'
migrate = Migrate(app, db)
CORS(app, resources={r"/*": {"origins": "*"}})
# ========================== Models =========================

class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    password =  db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(80), unique=True, nullable=False)
    age = db.Column(db.Integer, nullable=True)
    profile_img = db.Column(db.String(255), nullable=True)
    birthdate = db.Column(db.String(255), nullable=True)
    phone_number = db.Column(db.String(15), nullable=True)
    father_number = db.Column(db.String(15), nullable=True)
    city = db.Column(db.String(50), nullable=True)
    Is_google = db.Column(db.Integer)
    academic_year = db.Column(db.String(10), nullable=True)
    academic_section = db.Column(db.String(20), nullable=True)
    Wallet = db.Column(db.Integer)
    gender = db.Column(db.String(10), nullable=True)
    created_at = db.Column(db.DateTime(timezone=True), server_default=func.now())
    def serialize(self):
        return {
            'id': self.id,
            'name': self.name,
            'email': self.email,
            'age': self.age,
            'profile_img': self.profile_img,
            'birthdate': self.birthdate,
            'phone_number': self.phone_number,
            'father_number': self.father_number,
            'city': self.city,
            'academic_year': self.academic_year,
            'academic_section': self.academic_section,
            'Wallet': self.Wallet,
            'created_at': self.created_at,
            'gender': self.gender
        }
    
class Notification(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user = db.Column(db.String(100))
    notificashen = db.Column(db.String(255), nullable=False)
    is_read = db.Column(db.Boolean, default=False)
    type = db.Column(db.String(50))
    url = db.Column(db.String(255))
    created_at = db.Column(db.DateTime(timezone=True), server_default=func.now())
    

class FPT(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    userid = db.Column(db.Integer)
    token = db.Column(db.String(20)) 
    

class LogInAction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user = db.Column(db.String(100))
    browser = db.Column(db.String(50))
    browser_version = db.Column(db.String(20))
    platform = db.Column(db.String(50))
    engine = db.Column(db.String(50))
    os = db.Column(db.String(50))
    os_version = db.Column(db.String(20))
    device = db.Column(db.String(50))
    language = db.Column(db.String(20))
    user_agent_string = db.Column(db.String(255))
    remote_address = db.Column(db.String(15))
    is_mobile = db.Column(db.Boolean)
    is_tablet = db.Column(db.Boolean)
    is_desktop = db.Column(db.Boolean)
    is_bot = db.Column(db.Boolean)
    screen_resolution = db.Column(db.String(20))
    color_depth = db.Column(db.String(10))
    timezone = db.Column(db.String(50))
    accepts_cookies = db.Column(db.Boolean)
    created_at = db.Column(db.DateTime(timezone=True), server_default=func.now())

class Wallet_log(db.Model):
    id= db.Column(db.Integer, primary_key=True)
    user = db.Column(db.String(100))
    Amount =  db.Column(db.Integer)
    Prodect_id =  db.Column(db.Integer) 
    Prodect_name =  db.Column(db.String(100))
    created_at = db.Column(db.DateTime(timezone=True), server_default=func.now())  
class Pay_code(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user = db.Column(db.String(100))
    code = db.Column(db.String(25))
    price = db.Column(db.Integer)
    is_used = db.Column(db.Boolean, default=False)
    log_barcode = db.Column(db.String(255))
    created_at = db.Column(db.DateTime(timezone=True), server_default=func.now())
    
class Course(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text, nullable=True)
    academic_year = db.Column(db.Integer, nullable=False)
    academic_section = db.Column(db.String(50), nullable=False)
    price = db.Column(db.Float, nullable=False)
    is_free = db.Column(db.Boolean, default=False)
    banner_url = db.Column(db.String(255))
    category = db.Column(db.String(50))
    added_by = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime(timezone=True), server_default=func.now())
    def serialize(self):
        return {
            'id': self.id,
            'name': self.name,
            'academic_year': self.academic_year,
            'academic_section': self.academic_section,
            'price': self.price,
            'is_free': self.is_free,
            'banner_url': self.banner_url,
            'description': self.description,
            'category': self.category,
            'added_by': self.added_by,
            'created_at': self.created_at
        }
class Pay_log(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user = db.Column(db.String(100))
    name =  db.Column(db.String(100))
    
class Img(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(100), nullable=False)
    img = db.Column(db.LargeBinary)   
class Lesson(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    course_id = db.Column(db.Integer, nullable=False)
    iframeCode = db.Column(db.Text, nullable=True)
    lessonTime = db.Column(db.Integer, nullable=True)
    Ltype = db.Column(db.String(50), nullable=False)
    play_count = db.Column(db.Integer, default=3)
    created_at = db.Column(db.DateTime(timezone=True), server_default=func.now())
    def serialize(self):
        return {
            'id': self.id,
            'name': self.name,
            'course_id': self.course_id,
            'iframeCode': self.iframeCode,
            'Ltype': self.Ltype,
            'play_count': self.play_count,
            'created_at': self.created_at
        }
class Enroll(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user = db.Column(db.String(100))
    course = db.Column(db.Integer)
    created_at = db.Column(db.DateTime(timezone=True), server_default=func.now())
    def serialize(self):
        return {
            'id': self.id,
            'user': self.user,
            'course': self.course,
            'created_at': self.created_at
        }

class Admin(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    password =  db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(80), unique=True, nullable=False)
    roule = db.Column(db.String(50), nullable=False)
    created_at = db.Column(db.DateTime(timezone=True), server_default=func.now())
    

# ========================== Functions ==========================
def addPayLog(user,amount,prodect_id,prodect_name):
    new_log = Wallet_log(
        user=user,
        Amount=amount,
        Prodect_id=prodect_id,
        Prodect_name=prodect_name
    )
    db.session.add(new_log)
    db.session.commit()

def generate_pay_code():
    code = secrets.randbelow(99999999999999)
    return code

def get_user_info(access_token):
    user_info_url = "https://www.googleapis.com/oauth2/v1/userinfo"
    response = requests.get(user_info_url, headers={'Authorization': f'Bearer {access_token}'})
    user_info = response.json()
    user_data = {
        'name': user_info.get('name'),
        'email': user_info.get('email'),
        'profile_picture': user_info.get('picture'),
    }
    return user_data
def calculate_age(birthdate):
    birthdate = dt.strptime(birthdate, "%Y-%m-%d")
    current_date = dt.now()
    age = current_date.year - birthdate.year - ((current_date.month, current_date.day) < (birthdate.month, birthdate.day))
    return age
def generate_google_auth_url():
    return f"https://accounts.google.com/o/oauth2/auth?response_type=code&client_id={CLIENT_ID}&redirect_uri={REDIRECT_URI}&scope={'+'.join(SCOPES)}"

def exchange_code_for_token(code):
    token_url = "https://oauth2.googleapis.com/token"
    params = {
        'code': code,
        'client_id': CLIENT_ID,
        'client_secret': CLIENT_SECRET,
        'redirect_uri': REDIRECT_URI,
        'grant_type': 'authorization_code',
    }
    response = requests.post(token_url, data=params)
    token_info = response.json()
    return token_info['access_token']

def generate_random_token(length=20):
    token = secrets.token_hex(length // 2)
    return token

def parse_user_agent(user_agent_string):
    parts = user_agent_string.split(' ')

    if len(parts) >= 6 and '/' in parts[5]:
        browser = parts[5].split('/')[0]
        browser_version = parts[5].split('/')[1]
    else:
        browser = browser_version = ""

    platform = parts[1]
    engine = parts[3]
    os = parts[2]
    os_version = parts[4]
    device = " ".join(parts[6:8]) if len(parts) >= 8 else ""
    language = parts[-1].split(';')[0] if parts[-1].startswith('lang=') else ""

    is_mobile = 'Mobile' in user_agent_string
    is_tablet = 'Tablet' in user_agent_string
    is_desktop = not (is_mobile or is_tablet)
    is_bot = 'bot' in user_agent_string.lower()
    screen_resolution = request.headers.get('Screen-Resolution', '')
    color_depth = request.headers.get('Color-Depth', '')
    timezone = request.headers.get('Timezone', '')
    accepts_cookies = 'Cookie' in request.headers.get('Accept', '')

    return {
        'browser': browser,
        'browser_version': browser_version,
        'platform': platform,
        'engine': engine,
        'os': os,
        'os_version': os_version,
        'device': device,
        'language': language,
        'is_mobile': is_mobile,
        'is_tablet': is_tablet,
        'is_desktop': is_desktop,
        'is_bot': is_bot,
        'screen_resolution': screen_resolution,
        'color_depth': color_depth,
        'timezone': timezone,
        'accepts_cookies': accepts_cookies
    }


def addNotificashen(user,notificashen,type,url):
    newNotificashen = Notification(
        user=user,
        notificashen=notificashen,
        type=type,
        url=url
    )
    db.session.add(newNotificashen)
    db.session.commit()

# IsEnrolled Function 
def IsEnrolled(course_id):
    user = session.get('user')
    if user:
        user = Users.query.filter_by(email=user).first()
        enroll = Enroll.query.filter_by(user=user.email,course=course_id).first()
        if enroll:
            return True
        else:
            return False


def addLogin(user):
    user_agent_string = request.headers.get('User-Agent')
    remote_address = request.remote_addr
    split_info = parse_user_agent(user_agent_string)

    user_agent_data = LogInAction(
        user=user,
        browser=split_info['browser'],
        browser_version=split_info['browser_version'],
        platform=split_info['platform'],
        engine=split_info['engine'],
        os=split_info['os'],
        os_version=split_info['os_version'],
        device=split_info['device'],
        language=split_info['language'],
        user_agent_string=user_agent_string,
        remote_address=remote_address,
        is_mobile=split_info['is_mobile'],
        is_tablet=split_info['is_tablet'],
        is_desktop=split_info['is_desktop'],
        is_bot=split_info['is_bot'],
        screen_resolution=split_info['screen_resolution'],
        color_depth=split_info['color_depth'],
        timezone=split_info['timezone'],
        accepts_cookies=split_info['accepts_cookies']
    )

    db.session.add(user_agent_data)
    db.session.commit()
    
# Add Lesson to database Function
def addLesson(name,course_id,iframeCode,Ltype):
    newLesson = Lesson(
        name=name,
        course_id=course_id,
        iframeCode=iframeCode,
        Ltype=Ltype
    )
    db.session.add(newLesson)
    db.session.commit()

@app.route('/logingoogle')
def logingoogle():
    return redirect(generate_google_auth_url())
    
# ========================== Main Routes ==========================   
@app.before_request
def detect_device():
    user_agent = request.headers.get('User-Agent')
    session['is_mobile'] = 'Mobile' in user_agent
    session['is_webview'] = 'wv' in user_agent.lower()
    print(session['is_mobile'], session['is_webview'])
    
@app.route('/')
def home():
    username = session.get('user')
    if username:
        return redirect('/dashboard')
    else : 
        if session['is_mobile']:
            return render_template('app/landing.html')
        else:
            return  redirect('/login')
        


# ========================== Login and Sign Up ==========================

@app.route('/login',methods = ['POST','GET'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user = Users.query.filter_by(email=email).first()
        if user :
            if user.password == password:
                session.permanent = True
                session['user'] = email
                addLogin(email)
                return redirect('/dashboard')
            else :
                return 'sorry'
    username = session.get('user')
    if username:
        return redirect('/dashboard')
    else :              
        if session['is_mobile']:
            return render_template('app/login.html')
        else:
            return render_template('web/login.html')
     

@app.route('/sign_up')
def sign_up():
    username = session.get('user')
    if username:
        return redirect('/dashboard')
    else :
        if session['is_mobile']:
            return render_template("app/signup.html")
        else :
            return render_template("web/signup.html")
    
@app.route('/signup', methods=['POST'])
def signup():
    username = request.form.get('username')
    email = request.form.get('email')
    password = request.form.get('password')
    city = request.form.get('city')
    date_of_birth = request.form.get('dateInput')
    phone = request.form.get('phone')
    phone_parent = request.form.get('phone-parent')
    section = request.form.get('section')
    gender = request.form.get('gender')
    age=calculate_age(date_of_birth)
    academic_year = None
    if section == '1sec':
          section = "الصف الاول الثانوي"
          academic_year = 1
    elif section == '2sic':
          section = "الصف الثاني الثانوي علمي"
          academic_year = 2
    elif section == '2art':
          section = "الصف الثاني الثانوي ادبي"
          academic_year = 2
    elif section == '3art':
            section = "الصف الثالث الثانوي ادبي"
            academic_year = 3
    elif section == '3sic':
            section = "الصف الثالث الثانوي علم علوم"
            academic_year = 3
    elif section == '3math':
            section = "الصف الثالث الثانوي علم رياضة"
            academic_year = 3
    else:
        pass
    if gender == 'boy':
        userimg = f"https://avatar.iran.liara.run/public/boy?username={username}"
    else :
        userimg = f"https://avatar.iran.liara.run/public/girl?username={username}"
    new_user = Users(
        name=username,
        email=email,
        password=password,
        city=city,
        age=age,
        phone_number=phone,
        father_number = phone_parent,
        birthdate=date_of_birth,
        academic_year = academic_year ,
        academic_section=section, 
        profile_img = userimg
    )
    db.session.add(new_user)
    db.session.commit()
    session.permanent = True
    addLogin(new_user.email)
    session['user'] = new_user.email
    return redirect('/dashboard')

@app.route('/callback')
def callback():
    code = request.args.get('code')
    token = exchange_code_for_token(code)
    user_info = get_user_info(token)
    session['user_info'] = user_info
    session['user_email'] = user_info.get('email') 
    user = Users.query.filter_by(email=user_info["email"]).first()
    if user:
        session.permanent = True
        addLogin(user_info["email"])
        session['user'] = user_info["email"]
        return redirect('/dashboard')
    else:
        user = Users(name=user_info.get('name'), email=user_info.get('email'),password='GoogleLoginPasswored', profile_img=user_info["profile_picture"])
        db.session.add(user)
        db.session.commit()
        id = user.id
        return redirect(f'/googlesc/{id}')

@app.route("/googlesc/<int:id>",methods=['POST','GET'])
def googlesc(id):
    if request.method == 'POST':
        city = request.form.get('city')
        date_of_birth = request.form.get('dateInput')
        phone = request.form.get('phone')
        phone_parent = request.form.get('phone-parent')
        section = request.form.get('section')
        age=calculate_age(date_of_birth)
        academic_year = None
        if section == '1sec':
            section = "الصف الاول الثانوي"
            academic_year = 1
        elif section == '2sic':
            section = "الصف الثاني الثانوي علمي"
            academic_year = 2
        elif section == '2art':
            section = "الصف الثاني الثانوي ادبي"
            academic_year = 2
        elif section == '3art':
                section = "الصف الثالث الثانوي ادبي"
                academic_year = 3
        elif section == '3sic':
                section = "الصف الثالث الثانوي علم علوم"
                academic_year = 3
        elif section == '3math':
                section = "الصف الثالث الثانوي علم رياضة"
                academic_year = 3
        else:
            pass
        GoodleAc = Users.query.get(id)
        GoodleAc.city = city
        GoodleAc.birthdate = date_of_birth
        GoodleAc.phone_number = phone
        GoodleAc.father_number = phone_parent
        GoodleAc.academic_section = section
        GoodleAc.age = age
        GoodleAc.academic_year = academic_year
        db.session.commit()
        session.permanent = True
        addLogin(GoodleAc.email)
        session['user'] = GoodleAc.email
        return redirect('/dashboard')
    if session['is_mobile']:
        return render_template("app/googlesc.html",id=id)
    else : 
        return render_template("web/googlesc.html",id=id) 

@app.route("/forgetpasswored",methods=['POST','GET'])
def forgetpasswored():
    if request.method == 'POST':
        email = request.form['email']
        ID = Users.query.filter_by(email=email).first()
        if ID:
            ID = ID.id
            Token = generate_random_token()
            token = FPT(
                userid = ID,
                token=Token
            )  
            db.session.add(token)
            db.session.commit()
            send_reset_password_email(user_id=Token,email=email)
            return 'mail sended'
        else :
            return 'email Not Found'
    if session['is_mobile']:
        return render_template("app/forgetpasswored.html")
    else : 
        return render_template("web/forgetpasswored.html")
    
@app.route("/reset_password/<hashid>", methods=['POST','GET'])
def reset_password(hashid):
    token = FPT.query.filter_by(token=hashid).first()
    user = Users.query.get_or_404(token.userid)
    if request.method == 'POST':
        password = request.form['password']
        user.password = password
        db.session.commit()
        return 'passwored chang'
    if session['is_mobile']:
        return render_template("app/reset_password.html",id = hashid)
    else :
        return render_template("web/reset_password.html",id = hashid)

@app.route("/logout")
def logout():
    username = session.get('user')
    if username:
        session['user'] = None
        return redirect('/')
    else:
        return redirect('/')
# ========================== User Dashboard ==========================

@app.route("/dashboard")
def dashboard():
    username = session.get('user')
    
    if username:
        user = Users.query.filter_by(email=username).first()

        enrollments = Enroll.query.filter_by(user=user.email).all()
        enrollment_ids = [enrollment.course for enrollment in enrollments]

        courses = Course.query.filter(Course.id.in_(enrollment_ids)).all()

        course_data = {course.id: course.serialize() for course in courses}
        if session['is_mobile']:
            return render_template('app/dashboard/main.html', user=user, course_data=course_data.values())
        else:
            return render_template('web/dashboard/main.html', user=user, course_data=course_data.values())
    else:
        return redirect('/login')

@app.route('/all-courses')
def all_courses():
    username = session.get('user')
    if username:
        user = Users.query.filter_by(email=username).first()
        courses = Course.query.filter_by(academic_year=user.academic_year).all()
        categories_set = set(course.category for course in courses if course.category)
        unique_categories = list(categories_set)
        if session['is_mobile']:
            return render_template('app/dashboard/all-courses.html',user=user,courses=courses,uni=unique_categories)
        else:    
            return render_template('web/dashboard/all-courses.html',user=user,courses=courses,uni=unique_categories)
    else :
        return redirect('/login')
    
@app.route('/my-courses')
def my_courses():
    username = session.get('user')
    if username:
        user = Users.query.filter_by(email=username).first()
        enrollments = Enroll.query.filter_by(user=user.email).all()
        enrollment_ids = [enrollment.course for enrollment in enrollments]
        courses = Course.query.filter(Course.id.in_(enrollment_ids)).all()
        course_data = {course.id: course.serialize() for course in courses}
        categories_set = set(course['category'] for course in course_data.values() if course['category'])
        unique_categories = list(categories_set)
        if session['is_mobile']:
            return render_template('app/dashboard/my-courses.html', user=user, courses=courses, uni=unique_categories)
        else:
            return render_template('web/dashboard/my-courses.html', user=user, courses=courses, uni=unique_categories)
        

    else :
        return redirect('/login')
    


@app.route("/q-bank")
def q_bank():
    username = session.get('user')
    if username:
        user = Users.query.filter_by(email=username).first()
        if session['is_mobile']:
            return render_template('app/dashboard/qbank.html',user=user)
        else :
            return render_template('web/dashboard/qbank.html',user=user)
    else :
        return redirect('/login')

@app.route("/revegens")
def revegens():
    username = session.get('user')
    if username:
        user = Users.query.filter_by(email=username).first()
        if session['is_mobile']:
            return render_template('app/dashboard/revegens.html',user=user)
        else:
            return render_template('web/dashboard/revegens.html',user=user)
    else :
        return redirect('/login')

@app.route("/notification")
def notification():
    username = session.get('user')
    if username:
        user = Users.query.filter_by(email=username).first()
        notification = Notification.query.filter_by(user=user.id).all()
        # make the last notification the first one
        notification.reverse()
        return render_template('web/dashboard/notification.html',user=user,notification=notification)
    else :
        return redirect('/login')

@app.route("/priveci-police")
def priveci():
    username = session.get('user')
    if username:
        user = Users.query.filter_by(email=username).first()
        return render_template('web/dashboard/pv.html',user=user)
    else :
        return redirect('/login')
@app.route("/help")
def help():
    username = session.get('user')
    if username:
        user = Users.query.filter_by(email=username).first()
        return render_template('web/dashboard/help.html',user=user)
    else :
        return redirect('/login') 
@app.route("/settings")
def settings():
    username = session.get('user')
    if username:
        user = Users.query.filter_by(email=username).first()
        if session['is_mobile']:
            return render_template('app/dashboard/setting.html',user=user)
        else :
            return render_template('web/dashboard/setting.html',user=user)
    else :
        return redirect('/login')
# corese info page
@app.route("/course/<int:id>")
def course(id):
    username = session.get('user')
    if username:
        Course_info = Course.query.get(id)
        Lessons = Lesson.query.filter_by(course_id=id).all()
        user = Users.query.filter_by(email=username).first()
        enroll = Enroll.query.filter_by(user=user.email,course=id).first()

        states = False
        if enroll:
            states = True
        firesLessonInCouresId = Lesson.query.filter_by(course_id=id).first()
        if session['is_mobile']:
            return render_template('app/dashboard/corese-info.html',user=user,Course_info=Course_info,Lessons=Lessons,states=states,lid = firesLessonInCouresId)
        else:
            return render_template('web/dashboard/corese-info.html',user=user,Course_info=Course_info,Lessons=Lessons,states=states,lid = firesLessonInCouresId)
    else :
        return redirect('/login')
@app.route("/lesson/<int:id>")
def lesson(id):
    username = session.get('user')
    if username:
        user = Users.query.filter_by(email=username).first()
        lesson = Lesson.query.get(id)
        lesson.play_count += 1
        db.session.commit()
        return render_template('web/dashboard/lesson.html',user=user,lesson=lesson)
    else :
        return redirect('/login')
# ========================== Admin Dashboard ==========================
# make a /add_course page
@app.route("/add_course", methods=['POST', 'GET'])
def add_course():
    username = session.get('user')
    
    if username:
        user = Users.query.filter_by(email=username).first()

        if request.method == 'POST':
            name = request.form.get('name')
            academic_year = request.form.get('academicYear')
            academic_section = request.form.get('academicSection')
            price = request.form.get('price')
            is_free = request.form.get('isFree', False) 
            banner_url = request.form.get('bannerUrl')
            category = request.form.get('category')
            added_by = user.email

            new_course = Course(
                name=name,
                academic_year=academic_year,
                academic_section=academic_section,
                price=price,
                is_free=is_free,
                banner_url=banner_url,
                category=category,
                added_by=added_by
            )

            db.session.add(new_course)
            db.session.commit()

            return redirect('/dashboard')

        return render_template('admin/add_course.html', user=user)
    else:
        return redirect('/login')

# add lessons to course route 
@app.route("/add_lesson", methods=['POST', 'GET'])
def add_lesson():
    username = session.get('user')
    if username:
        user = Users.query.filter_by(email=username).first()
        if request.method == 'POST':
            name = request.form.get('name')
            iframeCode = request.form.get('iframeCode')
            Ltype = request.form.get('Ltype')
            lessonTime = request.form.get('lessonTime')
            course_id = request.form.get('course_id')
            lesson = Lesson(
                name=name,
                course_id=course_id,
                iframeCode=iframeCode,
                Ltype=Ltype,
                lessonTime=lessonTime
            )
            db.session.add(lesson)
            db.session.commit()

            # Fetch the course using the course_id
            course = Course.query.get(course_id)

            return redirect(f'/add_lesson')

        # Fetch all courses for rendering the template
        all_courses = Course.query.all()

        return render_template('admin/add_lesson.html', user=user, all_courses=all_courses)
    else:
        return redirect('/login')

# enrol cores to email from admin
@app.route("/enroll_coreas", methods=['POST','GET'])
def Enroll_cour():
        if request.method == 'POST':
            email = request.form.get('email')
            course_id = request.form.get('course_id')
            enroll = Enroll(
                user=email,
                course=course_id
            )
            db.session.add(enroll)
            db.session.commit()
            return redirect('/enroll_coreas')
        users = Users.query.all()
        all_courses = Course.query.all()
        return render_template('admin/enroll_coreas.html', users=users,all_courses=all_courses)

@app.route("/playvideo/<int:id>")
def playvideo(id):
    username = session.get('user')
    if username:
        user = Users.query.filter_by(email=username).first()
        lesson = Lesson.query.get(id)
        next_lesson = Lesson.query.filter_by(course_id=lesson.course_id).filter(Lesson.id > lesson.id).first()
        back_lesson = Lesson.query.filter_by(course_id=lesson.course_id).filter(Lesson.id < lesson.id).first()
        if lesson.Ltype == 'section':

            next_lesson = Lesson.query.filter_by(course_id=lesson.course_id).filter(Lesson.id > lesson.id).first()
            return redirect(f'/playvideo/{next_lesson.id}')
        else:
            pass
        all_lessons = Lesson.query.filter_by(course_id=lesson.course_id).all()
        enroll = Enroll.query.filter_by(user=user.email,course=lesson.course_id).first()
        if enroll:
            lesson.play_count += 1
            db.session.commit()
            if session['is_mobile']:
                return render_template('app/dashboard/playvideo.html',user=user,lesson=lesson,course=all_lessons,next_lesson=next_lesson,back_lesson=back_lesson)
            else :
                return render_template('web/dashboard/playvideo.html',user=user,lesson=lesson,course=all_lessons,next_lesson=next_lesson,back_lesson=back_lesson)
        else:
            return redirect(f'/payc/{lesson.course_id}')
    else :
        return redirect('/login')

@app.route("/payc/<int:id>")
def payc(id):
    username = session.get('user')
    if username:
        user = Users.query.filter_by(email=username).first()
        course = Course.query.get(id)
        if session['is_mobile']:
            return render_template('app/dashboard/checkout.html',user=user,course=course)
        else :
            return render_template('web/dashboard/checkout.html',user=user,course=course)
    else :
        return redirect('/login')
# api form for pay coreas take a username and code and coreas id and enroall coures 
@app.route("/enrollCoreas/<int:id>", methods=['POST'])
def enrollCoreas(id):
    username = session.get('user')
    if username:
        user = Users.query.filter_by(email=username).first()
        code = request.form.get('code')
        course = Course.query.get(id)
        pay_code = Pay_code.query.filter_by(code=code).first()
        if pay_code:
            if pay_code.is_used == 0 :
                if course.price <= pay_code.price:
                    pay_code.is_used = 1
                    enroll = Enroll(
                        user=user.email,
                        course=course.id
                    )
                    db.session.add(enroll)
                    db.session.commit()
                    return redirect('/course/'+str(id))
                else :
                    if session['is_mobile']:
                        return render_template('app/dashboard/checkout.html',user=user,course=course,error='قيمة الكود لا تكفي للدفع')
                    else :
                        return render_template('web/dashboard/checkout.html',user=user,course=course,error='قيمة الكود لا تكفي للدفع')
            else:
                if session['is_mobile']:
                    return render_template('app/dashboard/checkout.html',user=user,course=course,error='الكود مستخدم')
                else :
                    return render_template('web/dashboard/checkout.html',user=user,course=course,error='الكود مستخدم')
        else:
            if session['is_mobile']:
                return render_template('app/dashboard/checkout.html',user=user,course=course,error='الكود غير موجود')
            else :
                
                return render_template('web/dashboard/checkout.html',user=user,course=course,error='الكود غير موجود')
    else:
        return redirect('/login')
# askAi route
@app.route("/askAi")
def askAi():
    username = session.get('user')
    if username:
        user = Users.query.filter_by(email=username).first()
        return render_template('web/dashboard/askAi.html',user=user)
    else :
        return redirect('/login')
# ========================== API ==========================
@app.route("/api/count_unread_notificashen/<int:id>")
def count_unread_notificashen(id):
    count = Notification.query.filter_by(user=id, is_read=False).count()
    return jsonify({"count": count})

# api for check if code found or not and if found is used or not and make it used
@app.route("/api/check_code/<code>")
def check_code(code):
    user = session.get('user')
    User = Users.query.filter_by(email=user).first()
    code = Pay_code.query.filter_by(code=code).first()
    if code:
        if code.is_used == False:
            if User.Wallet == None:
                User.Wallet = 0
            User.Wallet= int(User.Wallet) + int(code.price)
            code.is_used = True
            db.session.commit()
            
            return jsonify({"success": True, "price": code.price})
        else:
            return jsonify({"success": False, "message": "Code is used"})
    else:
        return jsonify({"success": False, "message": "Code not found"})
# add code to db 
@app.route("/api/add_code", methods=['POST'])
def add_code():
    code = request.form.get('code')
    price = request.form.get('price')
    new_code = Pay_code(
        code=code,
        price=price
    )
    db.session.add(new_code)
    db.session.commit()
    return jsonify({"success": True, "message": "Code added"})

@app.route('/Save_img',methods=['POST'])
def Save_img():
    try :
        photo_data = request.files['photoData']
        image_data = photo_data.read()
        code = generate_random_token(length=10)
        NewImg = Img(
            code = code,
            img= image_data
        )
        db.session.add(NewImg)
        db.session.commit()
        return jsonify({'success': True, 'url': f'/img/{code}'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
@app.route('/img/<code>/')
def renderimg(code):
    img = Img.query.filter_by(code=code).first()

    if img:
        return Response(img.img, mimetype='image/jpeg')
    else:
        return Response("Image not found", status=404, mimetype='text/plain')

@app.route("/api/addNotificashen/<int:id>/<notificashen>/<type>/<url>")
def addNotificashen_api(id,notificashen,type,url):
    addNotificashen(id,notificashen,type,url)
    return jsonify({'success': True}), 200
@app.route("/api/notification/read/<int:id>")
def notification_read(id):
    notification = Notification.query.filter_by(user=id, is_read=False).all()
    for noti in notification:
        noti.is_read = True
    db.session.commit()
    return jsonify({'success': True}), 200

# Add Lesson to db api route using function
@app.route("/api/add_lesson", methods=['POST'])
def add_lesson_func():
    name = request.form.get('name')
    course_id = request.form.get('courseId')
    iframeCode = request.form.get('iframeCode')
    Ltype = request.form.get('Ltype')
    addLesson(name,course_id,iframeCode,Ltype)
    return jsonify({'success': True}), 200 
# api to get all coreace info by id
@app.route("/api/course/<int:id>")
def course_api(id):
    Course_info = Course.query.get(id)
    Lessons = Lesson.query.filter_by(course_id=id).all()
    # reatern the number of sections and videos and exames as a number and do not return the data

    return jsonify({"course": Course_info.serialize(), "lessons": [lesson.serialize() for lesson in Lessons]})
# ========================== techer Dashboard =====================
@app.route("/api/th/get_all_users")
def get_all_users():
    users = Users.query.all()
    return jsonify({"users": [user.serialize() for user in users]})
@app.route("/api/th/get_users/<int:year>/<section>/<location>")
def get_users(year,section,location):
    users = Users.query.filter_by(academic_year=year,academic_section=section,city=location).all()
    return jsonify({"users": [user.serialize() for user in users]})
# get all courses
@app.route("/api/th/get_all_courses")
def get_all_courses():
    courses = Course.query.all()
    return jsonify({"courses": [course.serialize() for course in courses]})
# search for student by name or email or phone number or father number or city or academic year or academic section and search will be similar not exact
@app.route("/api/th/search/<search>")
def search(search):
    users = Users.query.filter(Users.name.like('%'+search+'%') | Users.email.like('%'+search+'%') | Users.phone_number.like('%'+search+'%') | Users.father_number.like('%'+search+'%') | Users.city.like('%'+search+'%') | Users.academic_year.like('%'+search+'%') | Users.academic_section.like('%'+search+'%')).all()
    return jsonify({"users": [user.serialize() for user in users]})
# make a api route for get user info by id
@app.route("/api/th/get_user/<int:id>")
def get_user(id):
    user = Users.query.get(id)
    return jsonify({"user": user.serialize()})
# api fro know the user enrolment coreses
@app.route("/api/th/get_user_courses/<email>")
def get_user_courses(email):
    user = Users.query.filter_by(email=email).first()
    Enrolc = Enroll.query.filter_by(user=user.email).all() 
    # retern all coreses data
    return jsonify({"courses": [enroll.serialize() for enroll in Enrolc]})
# route for th to init codes with value and the num of codes and it retern codes and a url for csv file with codes and it post not git method
@app.route("/api/th/init_codes", methods=['POST'])
def init_codes():
    value = request.form.get('value')
    num = request.form.get('num')
    codes = []
    log_barcode = generate_random_token(length=30)
    for i in range(int(num)):
        code = generate_pay_code()
        new_code = Pay_code(
            code=code,
            price=value,
            log_barcode=log_barcode
        )
        db.session.add(new_code)
        codes.append(code)
    db.session.commit()
    return jsonify({"codes": codes, "url": f"/api/th/get_codes_csv/{log_barcode}"})
# get code csv file by log_barcode
@app.route("/api/th/get_codes_csv/<log_barcode>")
def get_codes_csv(log_barcode):
    codes = Pay_code.query.filter_by(log_barcode=log_barcode).all()
    csv = "code,price\n"
    for code in codes:
        csv += f"{code.code},{code.price}\n"
    return Response(csv, mimetype='text/csv', headers={"Content-Disposition": f"attachment; filename={log_barcode}.csv"})
# aqi for reatern the count of users 
@app.route("/api/th/get_users_count")
def get_users_count():
    users = Users.query.all()
    return jsonify({"count": len(users)})
# api for retern the count of lessons videos
@app.route("/api/th/get_lessons_count")
def get_lessons_count():
    lessons = Lesson.query.filter_by(Ltype='video').all()
    return jsonify({"count": len(lessons)})
# api for git all lessons exames
@app.route("/api/th/get_exames_count")
def get_exames_count():
    lessons = Lesson.query.filter_by(Ltype='exame').all()
    return jsonify({"count": len(lessons)})
# api for count Viwes of videos from enrollmients times for 
@app.route("/api/th/get_videos_views")
def get_videos_views():
    enroll = Enroll.query.all()
    return jsonify({"count":len(enroll)})

# get all data for spesefic user by email enrolmint and exams and user data and used codes
@app.route("/api/th/get_user_data/<email>")
def get_user_data(email):
    user = Users.query.filter_by(email=email).first()
    Enrolc = Enroll.query.filter_by(user=user.email).all()
    codes = Pay_code.query.filter_by(user=user.email).all()
    return jsonify({"user": user.serialize(), "enrolc": [enroll.serialize() for enroll in Enrolc], "codes": [code.serialize() for code in codes]})

@app.route("/api/th/login", methods=['POST'])
def ThLogin():
    username = request.form.get('username')
    password = request.form.get('password')
    if username == 'thadmin@gmail.com' and password == 'E3lanoTopia@Software.2025':
        return jsonify({"States": True})
    else:
        return jsonify({"States": False})
# api to ratern th notificashen count
@app.route("/api/th/count_unread_notificashen")
def count_unread_notificashen_th():
    count = Notification.query.filter_by(is_read=False).count()
    return jsonify({"count": count})
# api for reatern all notificashen
@app.route("/api/th/get_all_notificashen")
def get_all_notificashen():
    notification = Notification.query.all()
    return jsonify({"notification": [noti.serialize() for noti in notification]})


# ========================== Error Pages ==========================
@app.errorhandler(404)
def page_not_found(e):
    return render_template('web/error/404.html'), 404
# 5xx errors
@app.errorhandler(500)
def internal_server_error(e):
    return render_template('web/error/500.html'), 500
# ======================== Servir Site ==========================
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 3030))
    app.run(debug=True, host='0.0.0.0', port=port)
