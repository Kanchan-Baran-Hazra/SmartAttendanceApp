# from flask_sqlalchemy import SQLAlchemy
# from datetime import datetime

# # Initialize SQLAlchemy
# db=SQLAlchemy()

# class Institute(db.Model):
#     institute_id=db.Column(db.Integer,primary_key=True)
#     admin_name=db.Column(db.String(50),nullable=False)
#     email=db.Column(db.String(50),nullable=False)
#     password=db.Column(db.Text,nullable=False)
#     max_student=db.Column(db.Integer,nullable=True)
#     departments=db.Column(db.Text,nullable=False)
#     address=db.Column(db.Text,nullable=True,default='Asia/India')
#     contract_No=db.Column(db.Integer,nullable=False)
#     ins_Type=db.Column(db.String(20),nullable=False)
#     status = db.Column(db.String(20), default='active')
#     reg_date=db.Column(db.DateTime,default=datetime.now)
#     last_login = db.Column(db.DateTime)
#     ins_logo=db.Column(db.String(200),nullable=True,default='images.jpeg')

# class Student_Reg(db.Model):
#     student_id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String(50), nullable=False)
#     email = db.Column(db.String(50), nullable=False, unique=True)
#     password = db.Column(db.Text, nullable=False)
#     roll_no = db.Column(db.String(20), nullable=False)
#     institute_id = db.Column(db.Integer, nullable=False)
#     phone_number = db.Column(db.String(15), nullable=False)
#     gender = db.Column(db.String(20))
#     is_active = db.Column(db.Boolean, default=True)
#     address = db.Column(db.Text, nullable=True)
#     registration_date = db.Column(db.DateTime, default=datetime.now)
#     is_verified = db.Column(db.Boolean, default=False)
#     profile_picture = db.Column(db.String(200), nullable=True, default='images.jpeg')

# class Attend_record(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     student_id = db.Column(db.Integer,nullable=False)
#     subject_id = db.Column(db.Integer,nullable=False)
#     date = db.Column(db.Date, nullable=False)
#     time_marked = db.Column(db.DateTime, default=datetime.now)
    
#     status = db.Column(db.String(20), default='Present')  # Present, Absent, Late
#     method = db.Column(db.String(50))  # Face, QR, Manual
#     marked_by = db.Column(db.Integer)  # Optional
    
#     verified = db.Column(db.Boolean, default=False)
#     remarks = db.Column(db.String(200))


# from datetime import date

# today = date.today()
# print(date.today().strftime('%a'))  # Output: 'Tue' (for example)
#        # Output: 2025-07-30

# from datetime import datetime
# import pytz

# india = pytz.timezone('Asia/Kolkata')
# print(datetime.now(india),datetime.now())  # returns IST (Indian Standard Time)



from datetime import date

def get_day():
    return date.today().strftime('%a')


print(get_day())
