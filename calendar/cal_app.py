from flask import Flask, render_template
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms import SelectField

app = Flask(__name__)
app.config['SECRET_KEY']='test03'


#python cal_app.py
#------ Array holding appointments
posts = [ 
   
    {
        'appt': 'Application',
        'day': 16,
        'month': 4,
        'year': 2019,
        'hour': 10,
        'min': 30,
        'period':30
    },
    {
        'appt': 'Exam',
        'day': 16,
        'month': 4,
        'year': 2019,
        'hour': 13,
        'min': 45,
        'period':60
    },
    {
        'appt': 'renewal',
        'day': 17,
        'month': 5,
        'year': 2019,
        'hour': 9,
        'min': 45,
        'period':30
    },
    {
        'appt': 'American Visa Application',
        'day': 21,
        'month': 7,
        'year': 2019,
        'hour': 8,
        'min': 00,
        'period':30
    }
]

#------ Forms
class MinistryPickForm(FlaskForm):
    ministry=SelectField('ministry', choices=[] )
    department=SelectField('department', choices=[])
    location=SelectField('location', choices=[])

@app.route('/')
def home():
    return render_template('welcome.html')

@app.route('/user-dash')
def dash():
    form=MinistryPickForm()
    return render_template( 'user_dash.html', posts=posts, form=form) 

if __name__ == '__main__':
    app.run(debug=True)