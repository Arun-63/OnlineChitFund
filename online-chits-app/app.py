from flask import Flask, render_template, request, redirect, url_for
from flask_login import login_user, LoginManager, UserMixin, login_required, current_user
import sqlite3
import time
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime as dt


app = Flask(__name__)

app.secret_key = 'super scret' # Change this!
login_manager = LoginManager()
login_manager.init_app(app)

class User(UserMixin):
    pass

def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn
    
    


@app.route('/')
def index():
    return render_template('login.html')

@app.route('/createChit', methods=['POST'])
@login_required
def createChit():
    CFName = request.form.get('CFName')
    CFSize = request.form.get('CFSize')
    NPeople = request.form.get('NPeople')
    FromDate = request.form.get('FromDate')
    PDate = str(dt.today())
    conn = get_db_connection()
    conn.execute("INSERT INTO CHIT (name,owner,fundsize,nopeople,fdate,pdate) VALUES (?, ?, ?, ?, ?, ?)",
        (CFName,current_user.id,CFSize,NPeople,FromDate,PDate)
            )
    conn.commit()

    xyz = conn.execute("SELECT * FROM CHIT").fetchall()
    print(xyz)
    conn.close()
    return redirect(url_for('home'))

@app.route('/signup', methods=['POST'])
def signup():
    email = request.form.get('email')
    name = request.form.get('name')
    uname = request.form.get('uname')
    password = request.form.get('password')
    repassword = request.form.get('repassword')
    phone_no = request.form.get('phoneno')

    if(password != '' and password == repassword):
        #DB write
        conn = get_db_connection()
        conn.execute("INSERT INTO USER (name,uname,email,password,created,updated,phone_no) VALUES (?, ?, ?, ?, ?, ?, ?)",
            (name,uname,email,generate_password_hash(password, method='pbkdf2:sha256'),time.time(),time.time(),phone_no)
            )
        conn.commit()
        conn.close()
    # else:
    #     #error
    return redirect(url_for('home'))

    
@app.route('/login', methods=['POST'])
def login():
    email = request.form.get('email')
    password = request.form.get('password')

    conn = get_db_connection()
    user_data = conn.execute("SELECT * FROM USER WHERE email = ?",(email,)).fetchone()
    #validate password by generating HASH
    if(check_password_hash(user_data['password'], password)):
        user = User()
        user.id = user_data['email']
        login_user(user)#, remember=remember)
        return redirect(url_for('home'))

    conn.close()

@login_manager.user_loader
def load_user(user_id):
    conn = get_db_connection()
    user_data = conn.execute("SELECT * FROM USER WHERE email = ?",(user_id,)).fetchone()
    conn.close()

    user = User()
    user.id = user_data['email']
    return user

@app.route('/home')
@login_required
def home():
    return render_template('home.html', name=current_user.id)

@app.route('/mylist')
@login_required
def mylist():
    return render_template('mylist_chits.html') 

@app.route('/search')
@login_required
def search():
    return render_template('search_chits.html', name=current_user.id)

@app.route('/create')
@login_required
def create():
    return render_template('create_chits.html', name=current_user.id)

@app.route('/owner')
@login_required
def owner():
    return render_template('owner.html', name=current_user.id)
