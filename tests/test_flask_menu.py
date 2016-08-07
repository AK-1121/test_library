from flask_login import LoginManager
from flask_menu import app
from library_lib import Library, Librarian
from logging import FileHandler, WARNING, Formatter
from unittest import TestCase, skip
from urllib.parse import urlparse

import os
from multiprocessing import Process


class TestsWithoutLogin(TestCase):
    def setUp(self):
        self.app = app.test_client()  # creates a test client
        self.app.testing = True
        #library = Library('Детскя библиотека №28')
        app.secret_key = 'strong SecReT Key 123123123!'
        #app.config['SESSION_TYPE'] = 'filesystem'  # http://stackoverflow.com/a/26080974
        login_manager = LoginManager()
        login_manager.init_app(app)
        login_manager.login_view = 'login'

    def test_hello_page(self):
        """
        Hello page just returns "Hello magic world!!!". It doesn`t use DB communication and other things.
        """
        resp = self.app.get('/hello')
        self.assertTrue("Hello magic world!!!" in str(resp.data))
        self.assertEqual(resp.status_code, 200)

    #@skip('Not emplemented yet.')
    def test_different_pages_without_authorization(self):
        login_required_pages = ['/add_book', '/book/3', '/show_all_books', '/show_books',
                                '/add_user', '/show_all_users', '/show_users', '/user/17',
                                '/admin/register']
        for url_link in login_required_pages:
            #print("Link: " + url_link)
            resp = self.app.get(url_link)
            self.assertEqual(resp.status_code, 302, "Current url_link: {}".format(url_link))
            self.assertEqual(urlparse(resp.location).path, '/login', "Current url_link: {}".format(url_link))

    def tearDown(self):
        pass


class TestsWithUserLogin(TestCase):
    def setUp(self):
        file_handler_log = FileHandler('tests_error.log')
        file_handler_log.setLevel(WARNING)
        file_handler_log.setFormatter(Formatter("%(name)s - %(levelname)s - %(asctime)s - %(message)s"))
        app.logger.addHandler(file_handler_log)

        #self.app.secret_key = 'strong SecReT Key 123123123!'
        app.secret_key = 'strong SecReT Key 123123123!'

        self.app = app.test_client()  # creates a test client
        self.app.testing = True
        #self.app.trace = True
        db_file_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "library.db")
        library = Library('Тестовая библиотека №28', db_file_path)
        #admin = Librarian("test_admin", "Admin Ivanov", "12345678", 2, email="admin@mail.ru", phone="+7-495-5555555")
        #print("Librarians before commit: {}".format(self.library.session.query(Librarian).filter_by(user='test_user')))
        """
        if not self.library.session.query(Librarian).filter_by(user_name='test_user').first():
            self.user = Librarian("test_user", "User Userovich", "12345678", 1, email="user@mail.ru",
                                  phone="+7-495-5555555")
            self.library.session.add(self.user)
            self.library.session.commit()
        """
        #print("Librarians after commit: {}".format(self.library.session.query(Librarian).all()))
        #def __init__(self, user_name, real_name, password, status=1, email=None, personal_info=None, phone=None,
        #         address=None):
        #self.app.config['SESSION_TYPE'] = 'filesystem'  # http://stackoverflow.com/a/26080974

        login_manager = LoginManager()
        login_manager.init_app(app)
        login_manager.login_view = 'login'

        #resp = self.app.post('/login', data=dict(user_name='test_user', password="12345678"))
        resp = self.app.post('/login', data=dict(user_name='test2', password="test222"))
        print("App: {}".format(dir(self.app)))
        #print("App Trace: {}".format(self.app.trace()))
        print("Login resp status: {} - {}".format(resp.status_code, resp.data))

    @skip("Don`t work properly.")
    def test_show_all_books(self):
        resp = self.app.get('/show_all_books')
        self.assertTrue("Список имеющихся книг" in str(resp.data))



