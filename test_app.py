from unittest import TestCase
from app import app
from models import db, User

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
        db.session.add(user)
        db.session.commit()

        self.user_fname = user.first_name
        self.user_id = user.id

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
