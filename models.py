"""Models for Blogly."""
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import DateTime
from sqlalchemy.sql import func

db = SQLAlchemy()

def connect_db(app):
    db.app = app
    db.init_app(app)

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    first_name = db.Column(db.String(15), nullable=False)
    last_name = db.Column(db.String(15))
    image_url = db.Column(db.String, default='https://1fid.com/wp-content/uploads/2022/06/no-profile-picture-6-1024x1024.jpg')


    posts = db.relationship('Post', backref='user', cascade='all, delete-orphan')

    def __repr__(self):
        return f'User: { self.full_name() }'

    def full_name(self):
        if self.last_name:
            return f'{self.first_name} {self.last_name}'
        else:
            return f'{self.first_name}'
        


class Post(db.Model):
    __tablename__='posts'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.Text, nullable=False)
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(DateTime(timezone=True), server_default=func.now())
    updated_at = db.Column(DateTime(timezone=True), onupdate=func.now())
    user_id = db.Column(db.Integer, db.ForeignKey(User.id))

    #tag = db.relationship('Tag', backref='post')
    #user = db.relationship('User', secondary='posts_tags', backref='posts')

    def __repr__(self):
        for title in self.title:
            return f'title: {self.title}'

    def time(self):
        time = self.created_at
        return time.strftime('%d %b %Y %I:%M %p')


class Tag(db.Model):
    __tablename__='tags'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.Text, unique=True)

    posts = db.relationship('Post', secondary='posts_tags', backref='tags')

    def __repr__(self):
        return f'{self.name}'


class PostTag(db.Model):
    __tablename__='posts_tags'

    post_id = db.Column(db.Integer, db.ForeignKey('posts.id'), primary_key=True)
    tag_id = db.Column(db.Integer, db.ForeignKey('tags.id'), primary_key=True)

    def __repr__(self):
        return f'{self.post_id} {self.tag_id}'
