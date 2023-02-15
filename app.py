"""Blogly application."""

from flask import Flask, redirect, render_template, request
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User, Post, Tag, PostTag

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
    posts = Post.query.order_by(Post.id.desc()).limit(5).all()
    return render_template('index.html', posts=posts)

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
    tags = Tag.query.all()
    return render_template('post_form.html', user=user, tags=tags)

@app.route('/users/<user_id>/posts/new', methods=['POST'])
def add_post(user_id):
    title = request.form['title']
    content = request.form['content']
    tag_ids = request.form.getlist('tags')

    new_post = Post(title=title, content=content, user_id=user_id)
    db.session.add(new_post)
    db.session.commit()

    for i in tag_ids:
        tag = Tag.query.get(int(i))
        new_post.tags.append(tag)

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
    tags = Tag.query.all()
    return render_template('edit_post.html', post=post, tags=tags)

@app.route('/posts/<post_id>/edit', methods=['POST'])
def edit_post(post_id):
    post = Post.query.get(post_id)
    post.title = request.form['title']
    post.content = request.form['content']

    post.tags.clear()
    tag_ids = request.form.getlist('tags')
    for i in tag_ids:
        tag = Tag.query.get(int(i))
        post.tags.append(tag)

    db.session.add(post)
    db.session.commit()

    return redirect(f'/posts/{post_id}')

@app.route('/posts/<post_id>/delete', methods=['POST'])
def delete_post(post_id):
    post = Post.query.get(post_id)
    db.session.delete(post)
    db.session.commit()

    return redirect('/users')

@app.route('/tags')
def tags():
    tags = Tag.query.all()
    return render_template('tags.html', tags=tags)

@app.route('/tags/<tag_id>')
def show_tag(tag_id):
    tag = Tag.query.get(tag_id)
    return render_template('tag_details.html', tag=tag)

@app.route('/tags/new')
def new_tag():
    return render_template('tag_form.html')

@app.route('/tags/new', methods=['POST'])
def add_new_tag():
    name = request.form['name']
    new_tag = Tag(name=name)

    db.session.add(new_tag)
    db.session.commit()

    return redirect('/tags')

@app.route('/tags/<tag_id>/edit')
def edit_tag_form(tag_id):
    tag = Tag.query.get(tag_id)
    return render_template('edit_tag.html', tag=tag)

@app.route('/tags/<tag_id>/edit', methods=['POST'])
def edit_tag(tag_id):
    tag = Tag.query.get(tag_id)
    tag.name = request.form['name']

    db.session.add(tag)
    db.session.commit()
    
    return redirect('/tags')

@app.route('/tags/<tag_id>/delete', methods=['POST'])
def delete_tag(tag_id):
    tag = Tag.query.get(tag_id)
    db.session.delete(tag)
    db.session.commit()
    return redirect('/tags')