from functools import wraps
from flask import Flask , render_template , redirect, url_for





app= Flask(__name__)

@app.route('/dashboard')
def dashboard():
       return render_template('new.html')



if __name__ =="__main__":
    app.run(debug=True)
