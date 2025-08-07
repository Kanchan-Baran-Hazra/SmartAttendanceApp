from flask import Flask,render_template,redirect,flash,url_for,request,jsonify,session
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import IntegrityError
from flask_mail import Mail,Message
from datetime import datetime,timedelta,date
import random
import time
import math
import pytz
from werkzeug.security import generate_password_hash, check_password_hash
import matplotlib.pyplot as plt
from collections import defaultdict
from sqlalchemy import extract
import os
from werkzeug.utils import secure_filename

app=Flask(__name__)
app.secret_key='abc123'

# conector data_base
app.config['SQLALCHEMY_DATABASE_URI']=r'sqlite:///mydatabase.db'
app.config['SQLALCHEMY_PATH_MODIFICATION']=False

# set email path
app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT']=587
app.config['MAIL_USE_TLS']=True
app.config['MAIL_USERNAME']='royaleclasic1@gmail.com'
app.config['MAIL_PASSWORD']='sushqkxfrnfnqqrh'
app.config['MAIL_DEFAULT_SENDER']='royaleclasic1@gmail.com'

# connector with app
db=SQLAlchemy(app)

# connector with mail
mail=Mail(app)

# session.permanent = False
# app.permanent_session_lifetime =timedelta(minutes=5)

app.config['UPLOAD_FOLDER']='static/uploads'

os.makedirs('static/uploads',exist_ok=True)

# for location
def is_within_radius(lat1, lon1, lat2, lon2, radius_meters=100):
    R = 6371000  # Earth radius in meters

    φ1 = math.radians(lat1)
    φ2 = math.radians(lat2)
    Δφ = math.radians(lat2 - lat1)
    Δλ = math.radians(lon2 - lon1)

    a = math.sin(Δφ / 2) ** 2 + math.cos(φ1) * math.cos(φ2) * math.sin(Δλ / 2) ** 2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

    distance = R * c  # in meters
    return distance <= radius_meters, round(distance, 2)

def get_day():
    return date.today().strftime('%a')


def get_month_part(dt):
    day = dt.day
    if 1 <= day <= 7:
        return '1–7'
    elif 8 <= day <= 15:
        return '8–15'
    elif 16 <= day <= 23:
        return '16–23'
    else:
        return '24–end'

# maneger model
class Maneger_Reg(db.Model):
    institute_id = db.Column(db.Integer, primary_key=True)  # auto
    name = db.Column(db.String(50), nullable=False)   # user input
    email = db.Column(db.String(50), nullable=False,unique=True)        # user input
    password = db.Column(db.Text, nullable=False)           # user input
    max_student = db.Column(db.Integer)                     # can change
    contract_No = db.Column(db.String(15), nullable=False)  # phone number as string
    ins_Name = db.Column(db.String(50), nullable=False)     # user input
    status = db.Column(db.Boolean, default=True)     # auto
    last_login = db.Column(db.DateTime, default=datetime.now)  # auto
    reg_date = db.Column(db.DateTime, default=datetime.now)  # auto
    ins_logo = db.Column(db.String(200), nullable=True, default='images.jpeg')  # default logo

class Student_Reg(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.String(50), nullable=False)
    name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(50), nullable=False, unique=True)
    password = db.Column(db.Text, nullable=False)
    class_id = db.Column(db.String(50), nullable=False)
    phone_number = db.Column(db.String(15), nullable=False)
    status = db.Column(db.Boolean, default=True)
    last_login = db.Column(db.DateTime, default=datetime.now)
    address = db.Column(db.Text, nullable=False)
    registration_date = db.Column(db.DateTime, default=datetime.now)
    is_verified = db.Column(db.Boolean, default=False)
    profile_picture = db.Column(db.String(200), nullable=True, default='images.jpeg')

class M_tasks(db.Model):
    id=db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('maneger__reg.institute_id'))
    task_name=db.Column(db.String(50), nullable=False)
    task_code=db.Column(db.String(50), nullable=False,unique=True)

class S_task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('student__reg.id'))  # ✔ correct FK
    teacher_name = db.Column(db.String(50), nullable=False)
    teacher_email = db.Column(db.String(50), nullable=False)
    task_name = db.Column(db.String(50), nullable=False)
    task_code = db.Column(db.String(50), nullable=False)
    is_suspant=db.Column(db.Boolean, default=False)

class Messages(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    manager_id = db.Column(db.Integer, db.ForeignKey('maneger__reg.institute_id'))
    email = db.Column(db.String(50), nullable=False)
    category=db.Column(db.String(50), nullable=False)
    title = db.Column(db.String(100))
    content = db.Column(db.Text)
    date_time = db.Column(db.String(10), default=get_day)
    timestamp = db.Column(db.DateTime, default=datetime.now)

class Allow_attend(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email=db.Column(db.String(50), nullable=False)
    max_student=db.Column(db.Integer, nullable=False)
    lat=db.Column(db.Float, nullable=False)
    lon=db.Column(db.Float, nullable=False)
    time_start=db.Column(db.DateTime, default=datetime.now)
    sub_code=db.Column(db.String(50), nullable=False)

class Attend_book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    sub_code = db.Column(db.String(20), nullable=False)
    stu_id = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(50), nullable=False)
    attend_time = db.Column(db.DateTime, default=datetime.now)
    is_present=db.Column(db.Boolean,default=True)




@app.route('/',methods=['GET','POST'])
def initial():
    session.permanent = False
    return render_template('index.html')

@app.route('/logina',methods=['GET','POST'])
def logina():
    session.clear()
    if session.get('is_active'):
        session.pop('is_active', None)
        session['is_active1']=False
        session['is_active']=True
        return redirect(url_for('home'))
    elif session.get('is_active1'):
            session.pop('is_active1', None)
            session['is_active']=False
            session['is_active1']=True
            return redirect(url_for('student_home'))
    return render_template('logina.html')

@app.route('/register_manager',methods=['GET','POST'])
def register_manager():
    if request.method=='POST':
        session['f_name']=request.form.get('f_name')
        session['l_name']=request.form.get('l_name')
        session['inst_name']=request.form.get('inst_name')
        session['email']=request.form.get('email')
        session['password']=generate_password_hash(request.form.get('password'))
        session['phone']=request.form.get('phone')
        max_student=request.form.get('max_student')
        if max_student !='':
            session['max_student']=max_student
        session["gen_time"]=time.time()
        otp=str(random.randint(1000,9999))
        session['otp']=otp
        try:
            # Render HTML email body from template
            email_body = render_template("email.html", otp=otp, current_year=datetime.now().year)

            # Create email message object
            msg = Message(
                subject=f"Hello {session.get('f_name')}",
                recipients=[session.get('email')],  # must be a list!
                html=email_body
            )
            mail.send(msg)  # Send email using Flask-Mail
            return redirect(url_for("otp_ver"))  # use function name, not path
        except:
            flash("Network error..!","error")
    return render_template('/manager/login1.html')

@app.route('/otp_ver',methods=['GET','POST'])
def otp_ver():
    if session.get("resend"):
        flash("OTP sesended..","sucess")
    if request.method=='POST':
        otp=request.form.get('otp')
        if time.time()-session.get('gen_time')>300:
            flash("OTP expired.",'error')
        elif otp!=session.get('otp'):
            flash('Invalid OTP.!!','error')
        else:
            name = f"{session.get('f_name', '')} {session.get('l_name', '')}".strip()
            # print(name)
            max_student = int(session.get('max_student')) if session.get('max_student') not in (None, "", " ") else 100
            # print(max_student)
            new_mang=Maneger_Reg(name=name,email=session.get('email'),password=session.get('password'),contract_No=session.get('phone'),ins_Name=session.get('inst_name'),max_student=max_student)
            db.session.add(new_mang)
            try:
                db.session.commit()
                session['is_active']=True
                return redirect(url_for('home'))
            except:
                db.session.rollback()
                flash("Already have an account.","error")
    return render_template('/manager/OTPverification.html')

@app.route('/home',methods=['GET','POST'])
def home():
    # print(session.get('email'))
    session['manager']=True
    user=Maneger_Reg.query.filter_by(email=session.get('email')).first()
    classes=M_tasks.query.filter_by(user_id=user.institute_id).all()
    return render_template('/manager/homem.html',classes=classes,img=user.ins_logo)

@app.route('/button_click', methods=['POST'])
def button_click():
    data = request.get_json()
    btn_number = data.get('button_number')
    btn_number1 = data.get('code')
    grtStudenr=S_task.query.filter_by(user_id=btn_number,task_code=btn_number1).first()
    if grtStudenr.is_suspant==0:
        grtStudenr.is_suspant=1
    else:
        grtStudenr.is_suspant=0
    db.session.commit()
    # print(f"Button {btn_number}/ {btn_number1}was clicked.")
    return jsonify({"message": f"Server received button {btn_number} click."})

@app.route('/task/red_irct',methods=['GET','POST'])
def red_irect():
    if request.method=='POST':
        data = request.get_json()
        lat = data.get('latitude')
        lon = data.get('longitude')
        task_id=data.get('task_id')
        # print(type(lat),type(lon))
        man_info=Maneger_Reg.query.filter_by(email=session.get('email')).first()
        new_att=Allow_attend(email=man_info.email,max_student=man_info.max_student,lat=lat,lon=lon,sub_code=task_id)
        db.session.add(new_att)
        try:
            db.session.commit()
            return jsonify({"status": "success", "lat": lat, "lon": lon})
        except:
            db.session.rollback()
            return jsonify({"status": "failed", "lat": lat, "lon": lon})
    task_id = request.args.get('task_id')
    task_name = request.args.get('task_name')
    task_code = request.args.get('task_code')
    # print(task_code,task_id,task_name)
    name_mr=Maneger_Reg.query.filter_by(institute_id=task_id).first().name
    # print(name_mr)
    students_lis=S_task.query.filter_by(teacher_name=name_mr,task_code=task_code).all()
    student_info=[]
    for i in students_lis:
        student=Student_Reg.query.filter_by(id=i.user_id).first()
        alll_att=Allow_attend.query.filter_by(sub_code=i.task_code).count()
        ac_att=Attend_book.query.filter_by(sub_code=i.task_code,stu_id=i.user_id).count()
        if alll_att!=0:
            persentAge=(ac_att*100)/alll_att
        else:
            persentAge=0
        # print(task_id)
        student_info.append({'id':student.student_id,'name':student.name,'email':student.email,'student_id':i.user_id,'code':i.task_code,'sush':i.is_suspant,'task_id':i.task_code,'persentAge':persentAge})
        # print(i.task_code)
    return render_template('/manager/startAttendance.html',student_info=student_info)

@app.route('/manager_suspand/<int:student_id>')
def manager_suspand(student_id):
    sus_row = S_task.query.filter_by(user_id=student_id).first()
    print(sus_row.is_suspant)
    if sus_row.is_suspant:
        sus_row.is_suspant=False
    else:
        sus_row.is_suspant=True
    db.session.commit()
    return redirect(url_for('red_irect'))


@app.route('/cusstomers',methods=['GET','POST'])
def cusstomers():
    return render_template('/manager/customers.html')

@app.route('/addclass',methods=['GET','POST'])
def addclass():
    if request.method=='POST':
        data=request.get_json()
        if data:
            sub_name = data.get('name')
            sub_code = data.get('sub_code')
            user=Maneger_Reg.query.filter_by(email=session.get('email')).first()
            new_sub=M_tasks(task_name=sub_name,task_code=sub_code,user_id=user.institute_id)
            db.session.add(new_sub)
            try:
                db.session.commit()
            except:
                # flash("Already have an section",'error')
                return jsonify({"message":"error"})
            return jsonify({"message":'sucess'})
    return render_template('/manager/addClass.html')

@app.route('/customer',methods=['GET','POST'])
def customer():
    return render_template('/manager/seeAllstudent.html')

@app.route('/add_message',methods=['GET','POST'])
def add_message():
    # print(session.get('email'))
    if request.method=='POST':
        # print("Kanchan")
        data = request.get_json()
        title = data.get('title')
        content = data.get('content')
        email=session.get('email')
        category=data.get('category')
        manager_id = Maneger_Reg.query.filter_by(email=email).first().institute_id

        if not title or not content:
            return jsonify({'message': 'Title and content are required.'}), 400

        message = Messages(title=title, content=content, manager_id=manager_id,email=session.get('email'),category=category)
        db.session.add(message)
        try:
            db.session.commit()
            return jsonify({'message': 'Message sent successfully!'}), 200
        except:
            return jsonify({'message': 'Somthing wrong!'})
    man_id=Maneger_Reg.query.filter_by(email=session.get('email')).first().institute_id
    all_list=M_tasks.query.filter_by(user_id=man_id).all()
    sub_list=['Formal Info','All']
    for i in all_list:
        sub_list.append(i.task_name)
    return render_template('/manager/addMessage.html',sub_list=sub_list)

@app.route('/profile',methods=['GET','POST'])
def profile():
    if session.get('manager')==True:
        user1=Maneger_Reg.query.filter_by(email=session.get('email','')).first()
        name=user1.name
        email=user1.email
        jDate=user1.reg_date
        user='Institute Manager'
        image=user1.ins_logo
        is_mang=False
    else:
        user1=Student_Reg.query.filter_by(email=session.get('email','')).first()
        name=user1.name
        email=user1.email
        jDate=user1.registration_date
        user='Student ID'
        image=user1.profile_picture
        is_mang=True
    return render_template('profilem.html',name=name,email=email,jDate=jDate,user=user,image=image,is_mang=is_mang)

@app.route('/editProfm',methods=['GET','POST'])
def editProfm():
    stud=Maneger_Reg.query.filter_by(email=session.get('email')).first()
    if request.method=='POST':
        name=request.form.get('name')
        email=request.form.get('email')
        password=request.form.get('password')
        phone=request.form.get('phone')
        image=request.files["profile_pic"]

        if name:
            stud.name=name
            session["name"]=name
        if email:
            stud.email=email
            session["email"]=email
        if phone:
            stud.contract_No=phone
            session["contract_No"]=phone
        if password:
            stud.password=password
            session["password"]=password
        if image and image.filename !='':
            filename=secure_filename(image.filename)
            image.save(os.path.join(app.config['UPLOAD_FOLDER'],filename))
            stud.ins_logo=filename
            session["profile_picture"]=filename
        db.session.commit()
        return redirect(url_for("profile"))
    return render_template('/manager/editprofm.html',stud=stud)

@app.route("/resend_otp")
def resend_otp():
    session["resend"]=1
    session["gen_time"]=time.time()
    otp=str(random.randint(1000,9999))
    session["otp"]=otp
    try:
        msg=Message(
            subject=f'Hello {session.get("name")}',
            recipients=[session.get("email")]
        )
        msg.body=f'We recived a request to reset your password for your ToDo Blaze account.\n\nYour reset password OTP is {otp}.\n\nThis OTP is valid for 10 minutes.If you do not request this, just ignore this message.\n\n\nThanks,\nThe ToDo Blaze team'
        mail.send(msg)
        if session.get('manager')==False:
            return redirect(url_for("otp_ver_stu"))
        else:
            return redirect(url_for('otp_ver'))
    except IntegrityError:
        flash("Network Error..!!","error")
        if session.get('manager')==False:
            return redirect(url_for("otp_ver_stu"))
        else:
            return redirect(url_for("otp_ver"))



# student register
@app.route('/register_student',methods=['GET','POST'])
def register_student():
    if request.method=='POST':
        session['name']=request.form.get('name')
        session['student_id']=request.form.get('student_id')
        session['class_id']=request.form.get('class_id')
        session['email']=request.form.get('email')
        session['contact']=request.form.get('contact')
        session['location']=request.form.get('location')
        session['password']=request.form.get('password')

        session["gen_time"]=time.time()
        otp=str(random.randint(1000,9999))
        session['otp']=otp
        try:
            # Render HTML email body from template
            email_body = render_template("email.html", otp=otp, current_year=datetime.now().year)

            # Create email message object
            msg = Message(
                subject=f"Hello {session.get('name')}",
                recipients=[session.get('email')],  # must be a list!
                html=email_body
            )
            mail.send(msg)  # Send email using Flask-Mail
            return redirect(url_for("otp_ver_stu"))  # use function name, not path
        except:
            flash("Network error..!","error")
    return render_template('/student/register.html')

@app.route('/otp_ver_stu',methods=['GET','POST'])
def otp_ver_stu():
    if session.get("resend"):
        flash("OTP sesended..","sucess")
    if request.method=='POST':
        otp=request.form.get('otp')
        if time.time()-session.get('gen_time')>600:
            flash("OTP expired.",'error')
        elif otp!=session.get('otp'):
            flash('Invalid OTP.!!','error')
        else:
            new_std=Student_Reg(student_id=session.get('student_id'),name=session.get('name'),email=session.get('email'),password=session.get('password'),class_id=session.get('class_id'),phone_number=session.get('contact'),address=session.get('location'))
            db.session.add(new_std)
            try:
                db.session.commit()
                session['is_active1']=True
                return redirect(url_for('student_home'))
            except:
                db.session.rollback()
                flash("Already have an account.","error")
    return render_template('/student/sOTP_ver.html')

@app.route('/student_home',methods=['GET','POST'])
def student_home():
    session['manager']=False
    get_stuudentimg = Student_Reg.query.filter_by(email=session.get('email')).first().profile_picture
    get_stuudentId = Student_Reg.query.filter_by(email=session.get('email')).first().id
    get_email = S_task.query.filter_by(user_id=get_stuudentId).all()
    listof_allInfo = []

    if len(get_email) > 0:
        for i in get_email:
            get_info = Messages.query.filter_by(email=i.teacher_email).all()
            for j in get_info:
                created_time = j.timestamp
                now = datetime.utcnow()

                diff = now - created_time
                print(diff)
                total_minutes = int(diff.total_seconds() // 60)

                new_msg = total_minutes <= 5  # ✅ FIXED HERE

                my_dict = {
                    'titel': j.title,
                    'catagory': j.category,
                    'content': j.content,
                    'date_time': j.date_time,
                    'is_new': new_msg
                }
                listof_allInfo.append(my_dict)
                listof_allInfo.reverse()

    return render_template('/student/Home.html', all_info=listof_allInfo,img=get_stuudentimg)


@app.route('/student_dast')
def student_dast():
    # print(session.get('email'))
    user_id=Student_Reg.query.filter_by(email=session.get('email')).first().id
    user_tasks=S_task.query.filter_by(user_id=user_id).all()

    session['manager']=False
    get_stuudentId = Student_Reg.query.filter_by(email=session.get('email')).first().id
    get_email = S_task.query.filter_by(user_id=get_stuudentId).all()
    listof_allInfo = []

    if len(get_email) > 0:
        for i in get_email:
            get_info = Messages.query.filter_by(email=i.teacher_email).all()
            for j in get_info:
                created_time = j.timestamp
                now = datetime.utcnow()

                diff = now - created_time
                print(diff)
                total_minutes = int(diff.total_seconds() // 60)

                new_msg = total_minutes <= 5  # ✅ FIXED HERE

                my_dict = {
                    'titel': j.title,
                    'catagory': j.category,
                    'content': j.content,
                    'date_time': j.date_time,
                    'is_new': new_msg
                }
                listof_allInfo.append(my_dict)
                listof_allInfo.reverse()
                # print(len(listof_allInfo))
    return render_template('/student/dastBoard.html',user_tasks=user_tasks,all_info=listof_allInfo)

@app.route('/teachers',methods=['GET','POST'])
def teachers():
    # print(session.get('email'))
    stdent_id=Student_Reg.query.filter_by(email=session.get('email')).first().id
    all_sub=S_task.query.filter_by(user_id=stdent_id).all()
    return render_template('/student/seeAllteachers.html',all_sub=all_sub)

@app.route('/joinclass',methods=['GET','POST'])
def joinclass():
    if request.method=='POST':
        user_id=Student_Reg.query.filter_by(email=session.get('email')).first().id
        class_code=request.form.get('class_code')
        class_info=M_tasks.query.filter_by(task_code=class_code).first()
        if class_info:
            teacher_name=Maneger_Reg.query.filter_by(institute_id=class_info.user_id).first()
            new_class=S_task(user_id=user_id,teacher_name=teacher_name.name,task_name=class_info.task_name,task_code=class_info.task_code,teacher_email=teacher_name.email)
            db.session.add(new_class)
            try:
                db.session.commit()
                flash("You have successfully joined the class!", "success")
                return redirect(url_for('student_home'))
            except:
                db.session.rollback()
                flash("Already have this code..!!",'error')
        else:
            flash("No subject found..!!",'error')
    return render_template('/student/joinclass.html')

@app.route('/login',methods=['GET','POST'])
def login():
    # if session.get('is_active'):
    #     session.pop('is_active', None)
    #     session['is_active1']=False
    #     session['is_active']=True
    #     return redirect(url_for('home'))
    # if session.get('is_active1'):
    #     session.pop('is_active1', None)
    #     session['is_active']=False
    #     session['is_active1']=True
    #     return redirect(url_for('student_home'))
    if request.method=='POST':
        email=request.form.get('email')
        session['email']=email
        password=request.form.get('password')
        user1=Maneger_Reg.query.filter_by(email=email).first()
        user2=Student_Reg.query.filter_by(email=email).first()
        if user1 and user2 and check_password_hash(user1.password,user2.password):
            if check_password_hash(user1.password,password):
                session['name1']=user1.name
                session['name2']=user2.name
                return redirect(url_for('continues'))
            else:
                flash('Invalid password..!!','error')

        if user1:
            if check_password_hash(user1.password,password):
                session.pop('is_active', None)
                session['is_active']=True
                return redirect(url_for('home'))
            else:
                flash("Invalid password..!!","error")
        if user2:
            if user2.password==password:
                session.pop('is_active1', None)
                session['is_active1']=True
                return redirect(url_for('student_home'))
            else:
                flash("Invalid password..!!","error")
        elif not user1 and not user2:
            flash("No user found.!!",'error')
        # elif password!=user1.password or password!=user2.password:
        #     flash("Invalid password..!!","error")
        else:
            flash("Network error..!!","error")
    return render_template('login.html')

@app.route('/continues',methods=['GET','POST'])
def continues():
    return render_template('continues.html',name1=session.get('name1'),name2=session.get('name2'))

@app.route('/forgot_password',methods=['GET','POST'])
def forgot_password():
    if request.method=='POST':
        email=request.form.get('email')
        otp = str(random.randint(1000, 9999))
        session['otp'] = otp
        session['email'] = email
        session['otp_time'] = time.time()
        user1=Student_Reg.query.filter_by(email=email).first()
        user2=Maneger_Reg.query.filter_by(email=email).first()
        if user1 is None and user2 is None:
            flash("No user found..!!",'error')
            return redirect(url_for('login'))
        try:
            msg = Message('Your OTP for forgate',
                          recipients=[session.get('email')])
            msg.body = f'Your OTP is: {otp}. It will expire in 2 minutes.'
            mail.send(msg)
            flash('OTP sended','sucess')
            return redirect(url_for('optVerforReset'))
        except:
            flash("OTP not sent..!",'error')
            return redirect(url_for('forgot_password'))
    return render_template('forgateP.html')

@app.route('/optVerforReset',methods=['GET','POST'])
def optVerforReset():
    if request.method=='POST':
        otp=request.form.get('otp')

        if time.time()-session['otp_time'] >1000:
            flash("OTP time is expired..!!",'error')
            return redirect(url_for('forgot_password'))
        elif otp!=session.get('otp'):
            flash("Invalid OTP..!!",'error')
            return redirect(url_for('optVerforReset'))
        else:
            return redirect(url_for('reset_pass'))
    return render_template('resetOTP.html')

@app.route('/reset_pass',methods=['GET','POST'])
def reset_pass():
    if request.method=='POST':
        new_password=request.form.get('new_password')
        confirm_password=request.form.get('confirm_password')
        if new_password!=confirm_password:
            flash("Conform password is invalid..!!",'error')
            return redirect(url_for('reset_pass'))
        else:
            user1=Student_Reg.query.filter_by(email=session.get('email')).first()
            user2=Maneger_Reg.query.filter_by(email=session.get('email')).first()
            if user1 is not None and user2 is not None:
                user1.password=confirm_password
                user2.password=generate_password_hash(request.form.get('confirm_password'))
            elif user1 is not None:
                user1.password=confirm_password
            else:
                user2.password=generate_password_hash(request.form.get('confirm_password'))
            db.session.commit()
            return redirect(url_for('login'))
    return render_template('resetPass.html')

@app.route('/contact',methods=['GET','POST'])
def contact():
    if request.method=='POST':
        name=request.form.get('name')
        email=request.form.get('email')
        message=request.form.get('message')
        try:
            msg=Message(
                subject=f'Message from SMART ATTENDANCE APP',
                sender=('name','email'),
                recipients=['royaleclasic1@gmail.com']
            )
            msg.body=message
            mail.send(msg)
            flash('Message recived,thanks for your contribute.','sucess')
            return redirect(url_for("initial"))
        except:
            flash("Network Error..!!","error")
            return redirect(url_for("initial"))
    return render_template('contact.html',name1=session.get('name1'),name2=session.get('name2'))

@app.route('/singout',methods=['GET','POST'])
def singout():
    session.clear()
    return render_template('index.html')

@app.route('/send_loc',methods=['POST'])
def send_loc():
    data = request.get_json()
    lat = data.get('latitude')
    lon = data.get('longitude')
    
    session['lat']=lat
    session['lon']=lon
    
    # You can save to DB here if needed
    return jsonify({'status': 'success', 'message': 'Location saved'})

@app.route('/give_attendance',methods=['GET','POST'])
def give_attendance():
    stid=Student_Reg.query.filter_by(email=session.get('email')).first()
    subjects = S_task.query.filter_by(user_id=stid.id, is_suspant=False).all()
    arr = []
    if subjects:
        subjects.reverse()
        for i in subjects:
            sub_dict = {
                'id': i.task_code,
                'prof': i.teacher_email
            }
            arr.append(sub_dict)
    else:
        flash('No Subjects found..!!', 'error')
        return redirect(url_for('student_home'))

    if len(arr)>0:
        for j in arr:
            att_at=Allow_attend.query.filter_by(sub_code=j['id'],email=j['prof']).all()
            att_at.reverse()
            for k in att_at:
                REFERENCE_LAT=k.lat
                REFERENCE_LON=k.lon
                print(session.get('lat'),session.get('lon'))
                delta =datetime.now() - k.time_start
                if delta <= timedelta(minutes=5):
                    if session.get('lat') and session.get('lon'):
                        user_lat = float(session.get('lat'))
                        user_lon = float(session.get('lon'))
                        is_inside, distance = is_within_radius(user_lat, user_lon, REFERENCE_LAT, REFERENCE_LON)
                        if is_inside:
                            print(k.sub_code)
                            session['sub_code']=k.sub_code
                            session['att_done']=True
                            return redirect(url_for('att_method'))
                        

                    #     else:
                    #         flash("You must with in range of area",'error')
                    #         return redirect(url_for('student_home'))
                    # else:
                    #     flash("Location not fetched..!!",'error')
                    #     return redirect(url_for('student_home'))
                # else:
                #     flash("Time is over..!!",'error')
                #     return redirect(url_for('student_home'))
        if not session.get('att_done'):
            session.pop('att_done', None)
            flash("No attendance sheet found..!!",'error')
            return redirect(url_for('student_home'))
    else:
        flash('No Subjects found..!!','error')
        return redirect(url_for('student_home'))

@app.route('/att_method')
def att_method():
    return render_template('/student/askForAttMethod.html')

@app.route('/otp_foratt')
def otp_foratt():
    otp = str(random.randint(100000, 999999))
    session['otp'] = otp
    # session['email'] = email
    session['otp_time'] = time.time()
    try:
        msg = Message('Your OTP for Attendance',
                      sender='your_email@gmail.com',
                      recipients=[session.get('email')])
        msg.body = f'Your OTP is: {otp}. It will expire in 2 minutes.'
        mail.send(msg)
        flash('OTP sended','sucess')
        return redirect(url_for('vrifi_att'))
    except:
        flash("OTP not sent..!",'error')
        return redirect(url_for('att_method'))
    
@app.template_filter("within_5_minutes")
def within_5_minutes_filter(dt1, dt2):
    return abs(dt1 - dt2) <= timedelta(minutes=5)

@app.route('/vrifi_att',methods=['GET','POST'])
def vrifi_att():
    if session.get("resend"):
        flash("OTP sesended..","sucess")
    if request.method=='POST':
        user_otp = request.form['otp']
        actual_otp = session.get('otp')
        sent_time = session.get('otp_time')

        if not sent_time or time.time() - sent_time > 120:
            flash('OTP expired. Please try again.', 'danger')
            return redirect(url_for('att_method'))

        if user_otp == actual_otp:
            email=session.get('email')
            stu_id=Student_Reg.query.filter_by(email=email).first().id
            new_attend=Attend_book(stu_id=stu_id,email=email,sub_code=session.get('sub_code'))
            db.session.add(new_attend)
            try:
                db.session.commit()
                flash('✅ Attendance Marked Successfully!', 'success')
                return redirect(url_for('student_home'))
            except:
                db.session.rollback()
                flash("Network error..!",'error')
                return redirect(url_for('student_home'))
        else:
            flash('❌ Incorrect OTP. Try again.', 'danger')
            return redirect(url_for('vrifi_att'))
    return render_template('/student/attVerifi.html')

@app.route('/task-clicked', methods=['POST'])
def task_clicked():
    data = request.get_json()
    task_code = data.get('task_code')

    # Validate or log task_code
    # print(f"✅ Received Task Code: {task_code}")

    # Respond with success
    return jsonify({'status': 'success'})

@app.route('/view_result/<task_code>',methods=['GET','POST'])
def view_result(task_code):
    dID=Student_Reg.query.filter_by(email=session.get('email')).first().student_id
    acdata=Allow_attend.query.filter_by(sub_code=task_code).all()
    data=Attend_book.query.filter_by(sub_code=task_code,email=session.get('email')).all()
    data.reverse()

    # for right bar
    attendance_list = Attend_book.query.filter(
    extract('month', Attend_book.attend_time) == datetime.now().month,
    extract('year', Attend_book.attend_time) == datetime.now().year
    ).all()

    grouped_counts = defaultdict(int)

    for record in attendance_list:
        part = get_month_part(record.attend_time)
        grouped_counts[part] += 1

    # Create ordered count list
    count_list = [grouped_counts[part] for part in ['1–7', '8–15', '16–23', '24–end']]
    # print(count_list)
    
    return render_template('/student/studentView.html',data=data,acdata=acdata,dID=dID,email=session.get('email'),length=len(data),count_list=count_list)

@app.route('/editProf',methods=['GET','POST'])
def editProf():
    stud=Student_Reg.query.filter_by(email=session.get('email')).first()
    if request.method=='POST':
        name=request.form.get('name')
        student_id=request.form.get('student_id')
        email=request.form.get('email')
        password=request.form.get('password')
        phone=request.form.get('phone')
        image=request.files["profile_pic"]

        if name:
            stud.name=name
            session["name"]=name
        if student_id:
            stud.student_id=student_id
            session["student_id"]=student_id
        if email:
            stud.email=email
            session["email"]=email
        if password:
            stud.password=password
            session["password"]=password
        if image and image.filename !='':
            filename=secure_filename(image.filename)
            image.save(os.path.join(app.config['UPLOAD_FOLDER'],filename))
            stud.profile_picture=filename
            session["profile_picture"]=filename
        db.session.commit()
        return redirect(url_for("profile"))
    return render_template('/student/editProf.html',stud=stud)

@app.route("/resend_otp_foratt")
def resend_otp_foratt():
    session["resend"]=1
    session["otp_time"]=time.time()
    otp=str(random.randint(1000,9999))
    session["otp"]=otp
    try:
        msg=Message(
            subject=f'Hello {session.get("name")}',
            recipients=[session.get("email")]
        )
        msg.body=f'We recived a request to reset your password for your attendance.\n\nYour reset password OTP is {otp}.\n\nThis OTP is valid for 5 minutes.If you do not request this, just ignore this message.\n\n\nThanks,\nThe ToDo Blaze team'
        mail.send(msg)
        return redirect(url_for("vrifi_att"))
    except IntegrityError:
        flash("Network Error..!!","error")
        return redirect(url_for("vrifi_att"))




# external things
@app.route('/hero1_box1')
def hero1_box1():
    return render_template('aboutSecurity.html')

@app.route('/hero1_box2')
def hero1_box2():
    return render_template('aboutNetwork.html')

@app.route('/hero1_box3')
def hero1_box3():
    return render_template('aboutMultiuser.html')

@app.route('/box2_col1')
def box2_col1():
    return render_template('aboutMultiins.html')

@app.route('/box2_col2')
def box2_col2():
    return render_template('aboutLocation.html')

@app.route('/box2_col3')
def box2_col3():
    return render_template('aboutvisual.html')

@app.route('/box3_col1')
def box3_col1():
    return render_template('aboutNetwork.html')

@app.route('/box3_col2')
def box3_col2():
    return render_template('aboutSuport.html')

@app.route('/read_about')
def read_about():
    return render_template('readmorabout.html')

@app.route('/policy')
def policy():
    return render_template('aboutPolicy.html')

@app.route('/subscribe', methods=['POST'])  # ❗ Use POST for get_json
def subscribe():
    data = request.get_json()
    if not data or 'email' not in data:
        return jsonify({"message": "No email provided"}), 400

    email = data.get('email')

    try:
        msg = Message(
            subject='New Subscriber - SMART ATTENDANCE APP',
            sender=('SMART ATTENDANCE APP', app.config['MAIL_USERNAME']),  # ✅ Custom sender
            recipients=['royaleclasic1@gmail.com']  # ✅ Where you want to receive the notification
        )
        msg.body = f'A new user subscribed with email: {email}\n🎉 Welcome to SMART ATTENDANCE APP!'
        mail.send(msg)
        return jsonify({"message": "success"}), 200

    except Exception as e:
        print(f"Mail error: {e}")
        return jsonify({"message": "error"}), 500

@app.route('/sucess_sub')
def sucess_sub():
    return render_template('aboutSubscribe.html')

if __name__=='__main__':
    with app.app_context():
        db.create_all()
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port)