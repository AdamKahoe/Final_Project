from flask import render_template,redirect,session,request, flash
from flask_app import app
from flask_app.models.models_user import User
from flask_app.models.models_post import Post
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register',methods=['POST'])
def register():

    if not User.validate_register(request.form):
        return redirect('/')
    data ={
        "username": request.form['username'],
        "email": request.form['email'],
        "password": bcrypt.generate_password_hash(request.form['password'])
    }
    id = User.save(data)
    session['user_id'] = id
    return redirect('/dashboard')

@app.route('/login',methods=['POST'])
def login():
    user = User.get_by_email(request.form)

    if not user:
        flash("Invalid Email","login")
        return redirect('/')
    if not bcrypt.check_password_hash(user.password, request.form['password']):
        flash("Invalid Password","login")
        return redirect('/')
    session['user_id'] = user.id
    return redirect('/dashboard')

@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect('/')
    data ={
        'id': session['user_id']
    }
    return render_template("dashboard.html",user=User.get_by_id(data),post=Post.get_all())

@app.route('/home')
def home():
    if 'user_id' not in session:
        return redirect('/')
    data ={
        'id': session['user_id']
    }
    user=User.get_by_id(data)
    posts=Post.get_all()
    print("b" * 50)
    print(user,posts)
    return render_template("home.html",user=User.get_by_id(data),posts=Post.get_all())

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')