from flask import Flask, render_template, flash, redirect, url_for, session, request, logging
#from data import Articles
from flask_mysqldb import MySQL
from wtforms import Form, StringField, TextAreaField, PasswordField, validators
from passlib.hash import sha256_crypt
from functools import wraps

app = Flask(__name__)
pass_hash='$5$rounds=535000$B/pDI473X4BVypX.$tJcgCJANcaNqQrj8e.aKhGA3r4hQId3tYFrwGCsJoI7'

# Config MySQL
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = '$SatCom$'
app.config['MYSQL_DB'] = 'tetraapp'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'
# init MYSQL
mysql = MySQL(app)


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Get Form Fields
        username_candidate = request.form['username']
        password_candidate = request.form['password']

        if username_candidate =='admin':
            # Compare Passwords
            if sha256_crypt.verify(password_candidate, pass_hash):
                # Passed
                session['logged_in'] = True
                session['username'] = username_candidate

                flash('You are now logged in', 'success')
                return redirect(url_for('dashboard'))
            else:
                error = 'Invalid login'
                return render_template('home.html', error=error)
        else:
            error = 'Username not found'
            return render_template('home.html', error=error)

    return render_template('home.html')

# About
@app.route('/about')
def about():
    return render_template('about.html')

# Check if user logged in
def is_logged_in(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args, **kwargs)
        else:
            flash('Unauthorized, Please login', 'danger')
            return redirect(url_for('index'))
    return wrap

# Logout
@app.route('/logout')
@is_logged_in
def logout():
    session.clear()
    flash('You are now logged out', 'success')
    return redirect(url_for('index'))

@app.route('/dashboard')
@is_logged_in
def dashboard():
    return render_template('dashboard.html')

@app.route('/addvsat')
@is_logged_in
def add_vsat():
    return render_template('addvsat.html')

if __name__ == '__main__':
    app.secret_key='secret123'
    app.run(host='127.0.0.1', port=5011, debug=True)
