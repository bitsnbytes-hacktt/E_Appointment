from flask import Flask, render_template
from flask_wtf import FlaskForm

app = Flask(__name__)
app.config['SECRET_KEY']='test03'


posts = [ 
    {
        'appt': 'Renewal',
        'day': 15,
        'month': 4,
        'year': 2019,
        'hour': 8,
        'min': 20,
        'period':30
    },
    {
        'appt': 'Application',
        'day': 16,
        'month': 4,
        'year': 2019,
        'hour': 10,
        'min': 30,
        'period':45
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


@app.route('/')
def index():
    return render_template( 'user_dash.html', user_name='Jane Doe', posts=posts) 

if __name__ == '__main__':
    app.run(debug=True)