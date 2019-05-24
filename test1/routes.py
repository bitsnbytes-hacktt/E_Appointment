#----- Imports ----- 
from functools import wraps
from flask import render_template , redirect, url_for, flash, redirect,jsonify
from test1 import app, db
from test1.forms import PublicUserRegisterationForm, PublicUserLoginForm, AdminUserLoginForm, AdminUserDeleteForm, MinistryPickForm
from flask_login import LoginManager,UserMixin,login_user,logout_user,current_user,login_required
from test1.models import User, Role, Ministry, Location, Department, Setting, Appointment 


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


#----------------------- Landing page ----------------------------------- 
@app.route("/welcome")
def welcome():
    return render_template('welcome.html')

#------------------------ Public User ---------------------------------- 
@app.route("/user_register" , methods=['GET','POST'])
def user_register():
    form = PublicUserRegisterationForm()

    if form.validate_on_submit():
        new_public_user = User(name=form.name.data , email=form.email.data , password=form.password.data)
        db.session.add(new_public_user)
        db.session.commit()

        new_role = Role(name='Public' , admin=False , theuser=new_public_user)
        db.session.add(new_role)
        db.session.commit()

        return redirect(url_for('welcome'))
    else:
        return render_template('public_user_register.html' , form=form)

@app.route("/user_login" , methods=['GET','POST'])
def user_login():
    form = PublicUserLoginForm()

    if form.validate_on_submit():
        input_public_user = User.query.filter_by(email=form.email.data , password=form.password.data).first()

        if input_public_user:
            if input_public_user.password == form.password.data:
                login_user(input_public_user, remember=False)
                return redirect(url_for('user_home'))

    return render_template('public_user_login.html' , form=form)

@app.route("/user_home" , methods=['GET','POST'])
@login_required
@protect_user
def user_home():
    return render_template('user_home.html' , name=current_user.name)

@app.route("/user_home/logout" , methods=['GET','POST'])
@login_required
@protect_user
def user_home_logout():
    logout_user()
    return redirect(url_for('welcome'))

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
    return render_template('admin_home.html' , name=current_user.name)

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
    form.location.choices=[(location.id, location.name) for location in Location.query.filter(Location.department_location.any(location_id=1)).all()]
    return render_template('appointment.html', form=form)



@app.route("/appointment/<ministry_id>")


def testing_2(ministry_id):   


    departments=Department.query.filter_by(ministry_id=ministry_id).all()

    departmentArray=[]
    
    for department in departments:
        departmentObj={}
        departmentObj['id']= department.id
        departmentObj['name']= department.name
        departmentArray.append(departmentObj)

    
    return jsonify({'departments': departmentArray})


@app.route("/appointment/1/<location_id>")


def testing_3(location_id):   


    locations=Location.query.filter_by(location_id=location_id)

    locationArray=[]
    
    for location in locations:
        locationObj={}
        locationObj['id']= location.id
        locationObj['name']= location.name
        locationArray.append(locationObj)

    
    return jsonify({'locations': locationArray})