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
app.config['MYSQL_DB'] = 'soapapp'
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

# Add VSAT Form Class
class AddVsatForm(Form):
    t_id = StringField('TerminalID', [validators.Length(min=1, max=20)])
    t_name = StringField('TerminalName', [validators.Length(min=4, max=25)])
    bh_vlan = StringField('BH_vlan', [validators.Length(min=1, max=25)])
    bh_name = StringField('BH_name', [validators.Length(min=2, max=25)])
    bh_src = StringField('BH_src', [validators.Length(min=2, max=25)])
    bh_src_ip = StringField('BH_src_ip', [validators.Length(min=7, max=25)])
    t_rt_ip = StringField('Route', [validators.Length(min=7, max=25)])
    t_rt_msk = StringField('Mask', [validators.Length(min=7, max=25)])
    t_rt_gw = StringField('GW', [validators.Length(min=7, max=25)])

# User Register
@app.route('/add_vsat', methods=['GET', 'POST'])
def add_vsat():
    form = AddVsatForm(request.form)
    if request.method == 'POST':
        if form.validate():
            t_id = form.t_id.data
            t_name = form.t_name.data
            bh_vlan = form.bh_vlan.data
            bh_name = form.bh_name.data
            bh_src = form.bh_src.data
            bh_src_ip = form.bh_src_ip.data
            t_rt_ip = form.t_rt_ip.data
            t_rt_msk = form.t_rt_msk.data
            gw = form.t_rt_gw.data

            # Create cursor
            cur = mysql.connection.cursor()

            # Execute query
            cur.execute("INSERT INTO vsats(t_id, t_name, bh_vlan, bh_name, bh_src, bh_src_ip, t_rt_ip, t_rt_msk, t_rt_msk) VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s)", (t_id, t_name, bh_vlan, bh_name, bh_src, bh_src_ip, t_rt_ip, t_rt_msk, t_rt_msk))

            # Commit to DB
            mysql.connection.commit()

            # Close connection
            cur.close()

            flash('You are now registered and can log in', 'success')

            return redirect(url_for('dashboard'))
        else: flash('Validation wrong', 'danger')
    return render_template('addvsat.html', form=form)

if __name__ == '__main__':
    app.secret_key='secret123'
    app.run(host='127.0.0.1', port=5011, debug=True)
