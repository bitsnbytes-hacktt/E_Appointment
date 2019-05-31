#----- Imports ----- 
from functools import wraps
from flask import render_template , redirect, url_for, flash,jsonify,request
from test1 import app, db, mail
from test1.forms import PublicUserRegisterationForm, PublicUserLoginForm, AdminUserLoginForm, AdminUserDeleteForm, MinistryPickForm, RequestResetForm, ResetPasswordForm, MakeMinistryForm, MakeDepartmentForm, MakeAdminForm
from flask_login import login_user,logout_user,current_user,login_required
from test1.models import User, Role, Ministry, Location, Department, Setting, Appointment,Service_Time
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask_mail import Message
from werkzeug.security import generate_password_hash , check_password_hash

#
#
#

#----- Custom Decorators -----
""" def protect_user(func):
    @wraps(func)
    def decorated_view(*args, **kwargs):
        if current_user.roles[0].admin == True:
            return redirect(url_for('welcome'))
        else:
            return func(*args, **kwargs)
    return decorated_view

def protect_head_admin(func):
    @wraps(func)
    def decorated_view(*args, **kwargs):
        if current_user.roles[0].admin == True and current_user.email == "admin@ttappointment.com":
            return func(*args, **kwargs)
        else:
            return redirect(url_for('welcome'))
    return decorated_view

def protect_admin(func):
    @wraps(func)
    def decorated_view(*args, **kwargs):
        if current_user.roles[0].admin == False or current_user.email == "admin@ttappointment.com":
            return redirect(url_for('welcome'))
        else:
            return func(*args, **kwargs)
    return decorated_view """

#
#
#

#----- Email Functions -----

def send_reset_email(user):
    token = user.get_reset_token()
    msg = Message('Password Reset Request',
                    sender='admin@ttappointment.com',
                    recipients=[user.email])
    msg.body = f'''Link:
{url_for('reset_token',token=token,_external=True)}
'''
    mail.send(msg)

def send_register_email(new_user):
    msg = Message('Welcome to TTAppointments',
                    sender='admin@ttappointment.com',
                    recipients=[new_user.email])
    msg.body = f'''
Welcome, {new_user.fname} {new_user.lname}. 
Thank you for registering for TTAppointments.
'''
    mail.send(msg)

#
#
#

# -------------------------------------------------------------------------
#----------------------- Reset Password -----------------------------------
@app.route("/reset_password" , methods=['GET','POST'])
def reset_request():
    if current_user.is_authenticated:
        return redirect(url_for('welcome'))
    form = RequestResetForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        send_reset_email(user)
        return redirect(url_for('user_login'))
    return render_template('reset_request.html', form=form)

@app.route("/reset_password/<token>" , methods=['GET','POST'])
def reset_token(token):
    if current_user.is_authenticated:
        return redirect(url_for('welcome'))
    user = User.verify_reset_token(token)
    if user is None:
        return redirect(url_for('reset_request'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        new_password = form.password.data
        user.password = new_password
        db.session.commit()
        return redirect(url_for('user_login'))
    return render_template('reset_token.html',form=form)




# -----------------------------------------------------------------------
#----------------------- Welcome page ----------------------------------- 
@app.route("/welcome")
def welcome():
    return render_template('welcome.html')




# -------------------------------------------------------------------------
#----------------------- User home page ----------------------------------- 
posts = [
    {
        'appt': 'Passport',
        'day': 30,
        'month': 4,
        'year': 2019,
        'hour': 8,
        'min': 0,
        'period': 65

    },
    {
        'appt': 'ID',
        'day': 25,
        'month': 4,
        'year': 2019,
        'hour': 8,
        'min': 0,
        'period': 45
    },
    {
        'appt': 'Permit',
        'day': 15,
        'month': 4,
        'year': 2019,
        'hour': 8,
        'min': 0,
        'period': 45
    }
]

@app.route('/user_dash')
@login_required
def user_dash():
    form= MinistryPickForm()
    form.ministry.choices=[(ministry.id, ministry.name) for ministry in Ministry.query.all()]
    form.department.choices=[(department.id, department.name) for department in Department.query.filter_by(ministry_id=1).all()]
    form.location.choices=[(location.id, location.name) for location in Location.query.filter(Location.department_location.any(id=1)).all()]

    user_appts = Appointment.query.filter_by(user_id=current_user.id).all()
    user_appts_list = []
    for app in user_appts:
        date_temp = app.date.split("/")
        time_temp = app.time.split(":")
        calObj = {}
        calObj['appt'] = app.department.name
        calObj['day'] = int(date_temp[0])
        calObj['month'] = (int(date_temp[1]) - 1)
        calObj['year'] = int(date_temp[2])
        calObj['hour'] = int(time_temp[0])
        calObj['min'] = int(time_temp[1])
        calObj['period'] = 0
        user_appts_list.append(calObj)

    return render_template( 'user_dash.html' , posts=user_appts_list , fname=current_user.fname , lname=current_user.lname , form=form) 

@app.route("/appointment/<ministry_id>")
@login_required
def testing_2(ministry_id):   
    departments=Department.query.filter_by(ministry_id=ministry_id).all()

    departmentArray=[]

    for department in departments:
        departmentObj={}
        departmentObj['id']= department.id
        departmentObj['name']= department.name
        departmentArray.append(departmentObj)

    return jsonify({'departments': departmentArray})

@app.route("/appointment/<ministry>/<departments>")
@login_required
def testing_3(ministry, departments):    
    locations=Location.query.filter(Location.department_location.any(id=departments))

    locationArray=[]
    
    for location in locations:
        locationObj={}
        locationObj['id']= location.id
        locationObj['name']= location.name
        locationArray.append(locationObj)

    return jsonify({'locations': locationArray})

@app.route("/appointment/<departmentid>/<locationid>/<date_data>")
def query_test(departmentid,locationid,date_data):
    d_id_data = departmentid
    l_id_data = locationid
    
    input_date = date_data.split("-")
    new_date = str(input_date[2]) + '/' + str(input_date[1]) + '/' + str(input_date[0])

    q1 = Setting.query.filter_by(department_id=d_id_data , location_id=l_id_data).first()
    cap_data = q1.limit

    q2 = Service_Time.query.filter_by(department_id=d_id_data , location_id=l_id_data).all()

    display_list = []
    for x in q2:
        temp_time = x.start_time.split(":")
        q_time = temp_time[0]

        time_count = Appointment.query.filter_by(time=q_time , date=new_date , department_id=d_id_data , location_id=l_id_data).count()

        if int(time_count) < int(cap_data):
            display_list.append(x.start_time)
    
    timeArray=[]
    for y in display_list:
        timeObj={}
        timeObj['id']= y
        timeObj['name']= y
        timeArray.append(timeObj)

    return jsonify({'times': timeArray})

@app.route("/appointment/make" , methods=['GET','POST'])
@login_required
def appointment_make():
    form = MinistryPickForm()

    date_data = str(form.date.data)
    input_date = date_data.split("-")
    new_date = str(input_date[2]) + '/' + str(input_date[1]) + '/' + str(input_date[0])
 
    new_appt = Appointment(user_id=current_user.id , department_id=form.department.data ,  location_id=form.location.data , date=new_date , time=form.time.data)
    db.session.add(new_appt)
    db.session.commit()

    return redirect(url_for('user_dash'))




# --------------------------------------------------------------------------
#----------------------- Admin home page ----------------------------------- 
@app.route('/admin_dash')
@login_required
def admin_dash():
    return render_template('admin_dash.html' , fname=current_user.fname , lname=current_user.lname)

@app.route("/adminSettings", methods=['GET', 'POST'])
@login_required
def admin1():
    form= MinistryPickForm()
    
    form.ministry.choices=[(ministry.id, ministry.name) for ministry in Ministry.query.all()]
    form.department.choices=[(department.id, department.name) for department in Department.query.filter_by(ministry_id=1).all()]
    form.location.choices=[(location.id, location.name) for location in Location.query.filter(Location.department_location.any(id=1)).all()]
   
    a= str(form.startTime.data)
    b= str(form.endTime.data)
    d= form.department.data
    e = str(form.periodH.data) + ":" + str(form.periodM.data)
    f = form.location.data

    if request.method == 'POST':
        #return str(a) + "  " + str(b) + "  " + str(e) 
        new_settings = Setting(start_time=a, end_time=b, time_period=e, limit=form.capacity.data, department_id=form.department.data , location_id=form.location.data)
        db.session.add(new_settings)
        db.session.commit()
        return redirect(url_for('admin2', start = a, end = b, period = e, departmentid = d , locationid = f))
        #return str(a) + "  " + str(b) 
       
    return render_template('adminSettings.html',form=form)

@app.route("/adminSettingsError/<start>/<end>/<period>/<departmentid>/<locationid>")
@login_required
def admin2(start,end,period,departmentid,locationid):
    #return start + " " + end + " " + period + " " + departmentid

    flash('Success!')
    
    # input data
    start_time = start
    end_time = end
    period_time = period

    # data conversion
    a = start_time.split(":")
    st_h = int(a[0])
    st_m = int(a[1])

    b = end_time.split(":")
    et_h = int(b[0])
    et_m = int(b[1])

    c = period_time.split(":")
    p_h = int(c[0])
    p_m = int(c[1])

    # time list
    mylist = []

    # insert start time
    mylist.append(a[0] + ":" + a[1])

    # insert other times
    while st_h < (et_h - p_h):
        t = st_m + p_m
        
        if t >= 60:
            t2 = t - 60
            t3 = 1 + p_h
            h = t3 + st_h
            m = t2
            if m < 10 :
                tstr = str(h) + ":0" + str(m)
            else:
                tstr = str(h) + ":" + str(m)
            mylist.append(tstr)
            st_h = h
            st_m = m
        else:
            h = p_h + st_h
            m = t
            if m < 10 :
                tstr = str(h) + ":0" + str(m)
            else:
                tstr = str(h) + ":" + str(m)
            mylist.append(tstr)
            st_h = h
            st_m = m
    
    for time in mylist:
        new_service = Service_Time(start_time=time, department_id=departmentid , location_id=locationid)
        db.session.add(new_service)
        
    db.session.commit()

    return 'Finish'




# ---------------------------------------------------------------------------
#-------------------------Admin Adding to Database---------------------------
@app.route("/adminaddMin", methods=['GET', 'POST'])
@login_required
def admin3():
    form= MakeMinistryForm()
    if request.method == 'POST':  
        new_ministry = Ministry(name=form.ministry.data)
        db.session.add(new_ministry)
        db.session.commit()
        return  redirect(url_for('admin_dash',form=form))
    return  render_template('addMinistry.html',form=form)

@app.route("/adminaddlocation", methods=['GET', 'POST'])
@login_required
def admin4():
    form= MakeMinistryForm()
    if request.method == 'POST':  
        new_location =Location(name=form.location.data)
        db.session.add(new_location)
        db.session.commit()
        return redirect(url_for('admin_dash'))
    return  render_template('addlocation.html',form=form)

@app.route("/adminadddepartment", methods=['GET', 'POST'])
@login_required
def admin5():
    form= MakeDepartmentForm()
    form.ministry.choices=[(ministry.id, ministry.name) for ministry in Ministry.query.all()]
    form.location.choices=[(location.id, location.name) for location in Location.query.all()]
    if request.method == 'POST':  
        new_department =Department(name=form.department.data,  ministry_id=form.ministry.data)
        db.session.add(new_department)
        db.session.commit()
        locations=Location.query.filter_by(id=form.location.data).first()

        new_department.department_location.append(locations)
        db.session.add(new_department)
        db.session.commit()
        return redirect(url_for('admin_dash'))
    return  render_template('addDepartment.html',form=form)




# -------------------------------------------------------------------------------------
#------------------------ User register/login/logout ---------------------------------- 
@app.route("/user_register" , methods=['GET','POST'])
def user_register():
    form = PublicUserRegisterationForm()

    if form.validate_on_submit():
        hashed_password = generate_password_hash(form.password.data, method='sha256')
        new_public_user = User(fname=form.fname.data , lname=form.lname.data , email=form.email.data , password=hashed_password)
        db.session.add(new_public_user)
        db.session.commit()

        new_role = Role(name='Public' , admin=False , theuser=new_public_user)
        db.session.add(new_role)
        db.session.commit()

        send_register_email(new_public_user)

        return redirect(url_for('welcome'))
    else:
        return render_template('public_user_register.html' , form=form)

@app.route("/user_login" , methods=['GET','POST'])
def user_login():
    form = PublicUserLoginForm()

    if form.validate_on_submit():
        if form.email.data == 'admin@ttappointment.com' and form.password.data == 'admin':
            return redirect(url_for('head_admin_dash'))
        else:
            input_public_user = User.query.filter_by(email=form.email.data).first()
            if input_public_user:
                if check_password_hash(input_public_user.password,form.password.data):
                    input_role = Role.query.filter_by(user_id=input_public_user.id).first()
                    if input_role.admin == False:
                        login_user(input_public_user, remember=False)
                        return redirect(url_for('user_dash'))
                    else:
                        login_user(input_public_user, remember=False)
                        return redirect(url_for('admin_dash'))
            else:
                flash('Invalid login!')

    return render_template('public_user_login.html' , form=form)

@app.route("/user_dash/logout" , methods=['GET','POST'])
@login_required
def user__logout():
    logout_user()
    return redirect(url_for('welcome'))



# ---------------------------------------------------------------------------
#-------------------------Head Admin Home---------------------------
@app.route("/head_admin_dash" , methods=['GET','POST'])
def head_admin_dash():
    form = MakeAdminForm()

    if form.validate_on_submit():
        q = User.query.filter_by(email=form.email.data).first()
        r = Role.query.filter_by(user_id=q.id)
        r.name = 'Administrator'
        r.admin = True
        db.session.commit()

    return render_template('head_admin_dash.html' , form=form , fname='Admin' , lname='Admin')


























        
    

  








    


