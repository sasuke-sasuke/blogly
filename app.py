"""Blogly application."""

from flask import Flask, redirect, render_template, request
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User, Post

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

app.config['SECRET_KEY'] = 'mychickensteve'
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
debug = DebugToolbarExtension(app)

connect_db(app)
app.app_context().push()


@app.route('/')
def home_page():
    return redirect('/users')

@app.route('/users')
def users():
    users = User.query.all()
    return render_template('users.html', users=users)

@app.route('/users/new')
def new_user_form():
    return render_template('form.html')

@app.route('/users/new', methods=['POST'])
def post_new_user():
    fname = request.form['first-name']
    lname = request.form['last-name']
    image = request.form['image-url']
    if len(image) <= 0:
        image = None

    new_user = User(first_name=fname, last_name=lname, image_url=image)
    db.session.add(new_user)
    db.session.commit()

    return redirect('/users')

@app.route('/users/<user_id>')
def profile(user_id):
    user = User.query.get(user_id)
    return render_template('profile.html', user=user)

@app.route('/users/<user_id>/edit')
def edit_profile(user_id):
    user = User.query.get(user_id)
    return render_template('edit_user.html', user=user)

@app.route('/users/<user_id>/edit', methods=['POST'])
def update_user(user_id):
    user = User.query.get(user_id)
    user.first_name = request.form['first-name']
    user.last_name = request.form['last-name']
    user.image_url = request.form['image-url']

    db.session.add(user)
    ad.session.commit()

    return redirect('/users')

@app.route('/users/<user_id>/delete', methods=['POST'])
def delete_user(user_id):
    user = User.query.get(user_id)

    db.session.delete(user)
    db.session.commit()
    return redirect('/users')


@app.route('/users/<user_id>/posts/new')
def show_post_form(user_id):
    user = User.query.get(user_id)
    return render_template('post_form.html', user=user)

@app.route('/users/<user_id>/posts/new', methods=['POST'])
def add_post(user_id):
    title = request.form['title']
    content = request.form['content']

    new_post = Post(title=title, content=content, user_id=user_id)
    db.session.add(new_post)
    db.session.commit()

    return redirect(f'/users/{user_id}')

@app.route('/posts/<post_id>')
def show_post_details(post_id):
    post = Post.query.get(post_id)
    return render_template('post_details.html', post=post)

@app.route('/posts/<post_id>/edit')
def show_edit_post_form(post_id):
    post = Post.query.get(post_id)
    return render_template('edit_post.html', post=post)

@app.route('/posts/<post_id>/edit', methods=['POST'])
def edit_post(post_id):
    post = Post.query.get(post_id)
    post.title = request.form['title']
    post.content = request.form['content']

    db.session.add(post)
    db.session.commit()

    return redirect(f'/posts/{post_id}')

@app.route('/posts/<post_id>/delete', methods=['POST'])
def delete_post(post_id):
    post = Post.query.get(post_id)
    db.session.delete(post)
    db.session.commit()

    return redirect('/users')




