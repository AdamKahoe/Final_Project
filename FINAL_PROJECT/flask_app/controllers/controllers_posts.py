from flask import render_template, session,flash, redirect, request
import re
from flask_bcrypt import Bcrypt
from flask_app import app
from flask_app.models.models_user import User
from flask_app.models.models_post import Post
from flask_app.models import models_post

@app.route('/new/post')
def new_post():
    if 'user_id' not in session:
        return redirect('/logout')
    data = {
        "id":session['user_id']
    }
    return render_template('add_post.html',user=User.get_by_id(data))


@app.route('/create/post',methods=['POST'])
def create_post():
    if 'user_id' not in session:
        return redirect('/logout')
    if not models_post.Post.validate_post(request.form):
        return redirect('/new/post')
    data = {
        "title": request.form['title'],
        "content": request.form['content'],
        "user_id": session["user_id"]
    }
    models_post.Post.save(data)
    return redirect('/dashboard')

@app.route('/edit/post/<int:id>')
def edit_post(id):
    if 'user_id' not in session:
        return redirect('/logout')
    data = {
        "id":id
    }
    user_data = {
        "id":session['user_id']
    }
    return render_template("edit_post.html",edit=models_post.Post.get_one(data),user=User.get_by_id(user_data))

@app.route('/update/post/',methods=['POST'])
def update_post():
    if 'user_id' not in session:
        return redirect('/logout')
    if not models_post.Post.validate_post(request.form):
        return redirect('/new/post')
    data = {
        "title": request.form['title'],
        "content": request.form['content'],
        "id": request.form['id']
    }
    # models_post.Post.update(data)
    models_post.Post.update(request.form)
    return redirect('/dashboard')

@app.route('/delete/post/<int:id>')
def delete_post(id):
    if 'user_id' not in session:
        return redirect('/logout')
    data = {
        "id": id
    }
    models_post.Post.delete(data)
    return redirect('/home')