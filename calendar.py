from flask import Flask, render_template
from flask_wtf import FlaskForm

app = Flask(__name__)
app.config['SECRET_KEY']='nah'


posts = [ 
    {
        'appt': 'Renewal',
        'day': 15,
        'month': 4,
        'year': 2019,
        'hour': 8,
        'min': 20,
        'className': 'important'
    },
    {
        'appt': 'Application',
        'day': 16,
        'month': 4,
        'year': 2019,
        'hour': 10,
        'min': 30,
        'className': 'chill'
    },
    {
        'appt': 'Exam',
        'day': 16,
        'month': 4,
        'year': 2019,
        'hour': 13,
        'min': 45,
        'className': 'chill'
    }
]


@app.route('/')
def index():
    return render_template( 'user_dash.html', user_name='Jane Doe', posts=posts) 

@app.route('/home')
def home():
    return render_template('testing.html', user_name='fuckhead')

if __name__ == '__main__':
    app.run(debug=True)