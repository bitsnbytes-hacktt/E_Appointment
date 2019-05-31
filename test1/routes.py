#----- Imports ----- 
from functools import wraps
from flask import render_template , redirect, url_for, flash,jsonify,request
from test1 import app, db, mail
from test1.forms import PublicUserRegisterationForm, PublicUserLoginForm, AdminUserLoginForm, AdminUserDeleteForm, MinistryPickForm, RequestResetForm, ResetPasswordForm
from flask_login import login_user,logout_user,current_user,login_required
from test1.models import User, Role, Ministry, Location, Department, Setting, Appointment,Service_Time
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask_mail import Message

#
#
#

#----- Custom Decorators -----
def protect_user(func):
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
    return decorated_view

#
#
#

#----- Functions -----

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


#----------------------- Welcome page ----------------------------------- 
@app.route("/welcome")
def welcome():
    return render_template('welcome.html')


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

    return render_template( 'user_dash.html' , posts=posts , fname=current_user.fname , lname=current_user.lname , form=form) 

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

# **************************************************
@app.route("/query_test", methods=['GET', 'POST'])
def query_test():
    d_id_data = 1
    l_id_data = 1
    date_data = '01/05/2019'

    q1 = Setting.query.filter_by(department_id=d_id_data , location_id=l_id_data).first()
    cap_data = q1.limit

    q2 = Service_Time.query.filter_by(department_id=d_id_data , location_id=l_id_data).all()

    display_list = []

    for x in q2:
        temp_time = x.start_time.split(":")
        q_time = int(temp_time[0])

        time_count = Appointment.query.filter_by(time=q_time , date=date_data , department_id=d_id_data , location_id=l_id_data).count()

        if time_count <= cap_data:
            display_list.append(x.start_time)
    
    timeArray=[]
    for y in display_list:
        timeObj={}
        timeObj['id']= y
        timeObj['name']= y
        timeArray.append(timeObj)

    return jsonify({'times': timeArray})
# **************************************************



@app.route("/appointment/make" , methods=['GET','POST'])
@login_required
def appointment_make():
    form = MinistryPickForm()

    return  "User:" + str(current_user.id) + " Min:" + form.ministry.data + " Dep:" + form.department.data + " Loc:" + form.location.data + " Date:" + form.date.data

    #new_appt = Appointment(user_id=current_user.id , department_id=form.department.data , date=form.date.data)
    #db.session.add(new_appt)
    #db.session.commit()


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


#------------------------ User register/login/logout ---------------------------------- 
@app.route("/user_register" , methods=['GET','POST'])
def user_register():
    form = PublicUserRegisterationForm()

    if form.validate_on_submit():
        new_public_user = User(fname=form.fname.data , lname=form.lname.data , email=form.email.data , password=form.password.data)
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
        input_public_user = User.query.filter_by(email=form.email.data , password=form.password.data).first()

        input_role = Role.query.filter_by(user_id=input_public_user.id).first()

        if input_role.admin == False:
            login_user(input_public_user, remember=False)
            return redirect(url_for('user_dash'))
        else:
            login_user(input_public_user, remember=False)
            return redirect(url_for('admin_dash'))

    return render_template('public_user_login.html' , form=form)

@app.route("/user_dash/logout" , methods=['GET','POST'])
@login_required
def user__logout():
    logout_user()
    return redirect(url_for('welcome'))




















# ---------------------------------------------------------------------------------
# ----------------------------------- OLD STUFF !!! -------------------------------

@app.route("/user_home" , methods=['GET','POST'])
@login_required
@protect_user
def user_home():
    return render_template('user_home.html' , name=current_user.fname)


#----------------------- Admin User ----------------------------------- 
@app.route("/admin_login" , methods=['GET','POST'])
def admin_login():
    form = AdminUserLoginForm()

    if form.validate_on_submit():
        input_admin_user = User.query.filter_by(email=form.email.data , password=form.password.data).first()

        if input_admin_user:
            if input_admin_user.email == "admin@ttappointment.com" and input_admin_user.password == "admin":
                login_user(input_admin_user, remember=False)
                return redirect(url_for('head_admin_home'))
            else:
                if input_admin_user.email == form.email.data and input_admin_user.password == form.password.data:
                    login_user(input_admin_user, remember=False)
                    return redirect(url_for('admin_home'))

    return render_template('admin_user_login.html' , form=form)

@app.route("/admin_home" , methods=['GET','POST'])
@login_required
@protect_admin
def admin_home():
    return render_template('admin_home.html' , name=current_user.fname)

@app.route("/admin_home/logout" , methods=['GET','POST'])
@login_required
@protect_admin
def admin_home_logout():
    logout_user()
    return redirect(url_for('welcome'))

#--------------------- Head Admin User ------------------------------------- 
@app.route("/head_admin_home")
@login_required
@protect_head_admin
def head_admin_home():
    return render_template('head_admin_home.html' , name=current_user.name)

@app.route("/head_admin_home/create" , methods=['GET','POST'])
@login_required
@protect_head_admin
def head_admin_home_create():
    form = AdminUserCreateForm()

    if form.validate_on_submit():
        new_admin_user = User(name=form.name.data , email=form.email.data , password=form.password.data)
        db.session.add(new_admin_user)
        db.session.commit()

        new_role = Role(name='Admin' , admin=True , theuser=new_admin_user)
        db.session.add(new_role)
        db.session.commit()

        return redirect(url_for('head_admin_home'))

    return render_template('head_admin_home_create.html' , name=current_user.name , form=form)

@app.route("/head_admin_home/view")
@login_required
@protect_head_admin
def head_admin_home_view():
    all_admins = Role.query.filter_by(admin=True)
    return render_template('head_admin_home_view.html' , name=current_user.name , admins=all_admins)

@app.route("/head_admin_home/delete" , methods=['GET','POST'])
@login_required
@protect_head_admin
def head_admin_home_delete():
    form = AdminUserDeleteForm()

    if form.validate_on_submit():
        delete_admin_user = User.query.filter_by(email=form.email.data).first()

        if delete_admin_user:
            db.session.delete(delete_admin_user)
            db.session.commit()
            return redirect(url_for('head_admin_home'))

    return render_template('head_admin_home_delete.html' , name=current_user.name , form=form)

@app.route("/head_admin_home/logout")
@login_required
@protect_head_admin
def head_admin_home_logout():
    logout_user()
    return redirect(url_for('welcome'))



@app.route("/appointment", methods=['GET', 'POST'])
def testing_1():
    form= MinistryPickForm()
    form.ministry.choices=[(ministry.id, ministry.name) for ministry in Ministry.query.all()]
    form.department.choices=[(department.id, department.name) for department in Department.query.filter_by(ministry_id=1).all()]
    form.location.choices=[(location.id, location.name) for location in Location.query.filter(Location.department_location.any(id=1)).all()]
    return render_template('appointment.html', form=form)





        
    

  








    


