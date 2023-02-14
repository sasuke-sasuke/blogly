from unittest import TestCase
from app import app
from models import db, User, Post

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///test_db'
app.config['SQLALCHEMY_ECHO'] = False

app.config['TESTING'] = True
app.config['DEBUG_TB_HOSTS'] = ['dont-show-debug-toolbar']

db.drop_all()
db.create_all()


class UserViewsTestCase(TestCase):

    def setUp(self):
        User.query.delete()

        user = User(first_name='Colts', last_name='Chicken', image_url='https://cdn.mos.cms.futurecdn.net/BX7vjSt8KMtcBHyisvcSPK.jpg')
        post = Post(title='Test Title', content='Ladies leave yo man at home.', user_id=user.id)
        db.session.add(user)
        db.session.commit()
        db.session.add(post)
        db.session.commit()

        self.user_fname = user.first_name
        self.full_name = user.full_name()
        self.user_id = user.id
        self.post_id = post.id
        self.post_title = post.title
        self.post_content = post.content

    def tearDown(self):
        db.session.rollback()

    def test_users(self):
        with app.test_client() as client:
            resp = client.get('/users')
            html = resp.get_data(as_text=True)

            self.assertEquals(resp.status_code, 200)
            self.assertIn('<h1>Users</h1>', html)

    def test_new_user_form(self):
        with app.test_client() as client:
            resp = client.get('/users/new')
            html = resp.get_data(as_text=True)

            self.assertEquals(resp.status_code, 200)
            self.assertIn('<h1>Create a User</h1>', html)

    def test_profile(self):
        with app.test_client() as client:
            resp = client.get(f'/users/{self.user_id}')
            html = resp.get_data(as_text=True)

            self.assertEquals(resp.status_code, 200)
            self.assertIn(self.user_fname, html)


    def test_post_new_user(self):
        with app.test_client() as client:
            data = {'first-name':'Tom', 'last-name':'Test', 'image-url':'https://miro.medium.com/max/1400/0*i1XbVjul86E_CSyf.jpg'}
            resp = client.post('/users/new', data=data, follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEquals(resp.status_code, 200)
            self.assertIn('<h1>Users</h1>', html)

    def test_show_post_form(self):
        with app.test_client() as client:
            resp = client.get(f'/users/{self.user_id}/posts/new')
            html = resp.get_data(as_text=True)

            self.assertEquals(resp.status_code, 200)
            self.assertIn(f'<h1>Add Post for { self.full_name }</h1>', html)

    # def test_edit_post(self):
    #     with app.test_client() as client:
    #         self.post_title = 'New Test Title'
    #         self.post_content = 'New test content'

    #         data = {'title': self.post_title, 'content': self.post_content, 'user_id': self.user_id}
    #         resp = client.post(f'/posts/{ self.post_id }/edit', data=data, follow_redirects=True)

    #         self.assertEquals(resp.status_code, 200)
    #         self.assertIn('<h1>New Test Title</h1>', html)