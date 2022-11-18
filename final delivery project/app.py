from flask import Flask, render_template, request, redirect, url_for, session
from flask_mysqldb import MySQL
import MySQLdb.cursors
import re
app = Flask(__name__)
app.secret_key = 'a'
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'jobs'
mysql = MySQL(app)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/login',methods =['GET', 'POST'])
def login():
    global userid
    msg = ''
    if request.method == 'POST' :
        username = request.form['username']
        password = request.form['password']
        cursor = mysql.connection.cursor()
        cursor.execute('SELECT * FROM auth WHERE username = % s AND password = % s', (username, password ))
        account = cursor.fetchone()
        print (account)
        if account:
            session['loggedin'] = True
            session['id'] = account[0]
            userid=  account[0]
            session['username'] = account[1]
            session['email'] = account[2]
            session['qualification'] = account[4]
            msg = 'Logged in successfully !'
            return redirect('/dashboard')
    else:
        msg = 'Incorrect username / password !'
        return render_template('login.html', msg = msg)


@app.route('/register', methods =['GET', 'POST'])
def register():
    msg = ''
    if request.method == 'POST' :
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        qualification=request.form['qualification']
        cursor = mysql.connection.cursor()
        cursor.execute('SELECT * FROM auth WHERE username = % s', (username, ))
        account = cursor.fetchone()
        print(account)
        if account:
            msg = 'Account already exists !'
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            msg = 'Invalid email address !'
        elif not re.match(r'[A-Za-z0-9]+', username):
            msg = 'name must contain only characters and numbers !'
        else:
            cursor.execute('INSERT INTO auth VALUES (NULL, % s, % s, % s, % s)', (username, email,password,qualification))
            mysql.connection.commit()
    elif request.method == 'POST':
        msg = 'Please fill out the form !'
    return render_template('register.html', msg = msg)

@app.route('/dashboard')
def dash():
    cursor = mysql.connection.cursor()
    cursor.execute('SELECT * FROM jobposts')
    jobpost = cursor.fetchall()
    return render_template('dashboard.html',jobpost=jobpost)



@app.route('/apply',methods =['GET', 'POST'])
def apply():
     msg = ''
     if request.method == 'POST' :

         username = request.form['username']
         email = request.form['email']
         qualification= request.form['qualification']
         jobs = request.form['s']
         cursor = mysql.connection.cursor()
         cursor.execute('SELECT * FROM job WHERE userid = % s', (session['id'], ))
         account = cursor.fetchone()
         print(account)
         if account:
            msg = 'there is only 1 job position! for you'
            return render_template('apply.html', msg = msg)
         cursor = mysql.connection.cursor()
         cursor.execute('INSERT INTO job VALUES (% s, % s, % s, % s, % s)', (session['id'],username, email,qualification,jobs))
         mysql.connection.commit()
         msg = 'You have successfully applied for job !'
         session['loggedin'] = True
         TEXT = "Hello sandeep,a new appliaction for job position" +jobs+"is requested"
     elif request.method == 'POST':
         msg = 'Please fill out the form !'

     cursor = mysql.connection.cursor()
     cursor.execute('SELECT jobtitle FROM jobposts')
     jobtitle = cursor.fetchall()

     return render_template('apply.html', msg = msg,jobtitle=jobtitle)

@app.route('/display')
def display():
    print(session["username"],session['id'])
    cursor = mysql.connection.cursor()
    cursor.execute('SELECT * FROM job WHERE userid = % s', (str(session['id'])))
    account = cursor.fetchone()
    print("accountdislay",account)
    return render_template('display.html',account = account)

@app.route('/logout')
def logout():
   session.pop('loggedin', None)
   session.pop('id', None)
   session.pop('username', None)
   return render_template('home.html')

if __name__ == '__main__':
   app.run(host='0.0.0.0',debug = True)