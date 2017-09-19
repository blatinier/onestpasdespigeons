from django.contrib import auth
from django.contrib.auth.models import User
from django.test import Client, TestCase


class AuthTestCase(TestCase):
    fixtures = ['user.json']

    def setUp(self):
        self.client = Client()

    def test_regular_register_logout_login(self):
        """
        Test the following steps:
        - Register
        - Logout
        - Login
        """
        # Go to register page:
        resp = self.client.get("/en/register/")
        self.assertEqual(resp.status_code, 200)
        self.assertIn(b"Register", resp.content)

        # Register user
        user_data = {"user-username": "azec",
                     "user-first_name": "qsd",
                     "user-last_name": "wxc",
                     "user-email": "pipo@lala.com",
                     "user-password1": "plokijuh",
                     "user-password2": "plokijuh",
                     "profile-language": "en",
                     "profile-country": "us"}
        resp = self.client.post("/en/register/", user_data, follow=True)
        self.assertEqual(resp.redirect_chain, [("/en/my_measures", 302)])
        self.assertIn(b"My measures", resp.content)
        self.assertTrue(auth.get_user(self.client).is_authenticated())

        # Logout
        resp = self.client.get("/en/logout/", follow=True)
        self.assertEqual(resp.redirect_chain, [("/", 302), ("/en/", 302)])
        self.assertFalse(auth.get_user(self.client).is_authenticated())

        # Login
        login_data = {"username": "azec",
                      "password": "plokijuh"}
        resp = self.client.post("/en/login/", login_data, follow=True)
        self.assertEqual(resp.redirect_chain, [("/my_measures", 302), ("/en/my_measures", 302)])
        self.assertIn(b"My measures", resp.content)
        self.assertTrue(auth.get_user(self.client).is_authenticated())

    def test_fail_login(self):
        """
        Test login failures and check for error messages:
        - Wrong password
        - Non existant user
        - No password
        - No user
        """
        # Logout before test just in case
        resp = self.client.get("/en/logout/", follow=True)

        # wrong pwd
        login_data = {"username": "azec",
                      "password": "pipo"}
        resp = self.client.post("/en/login/", login_data)
        self.assertIn(b"The login/password combination failed. Try again.", resp.content)
        self.assertFalse(auth.get_user(self.client).is_authenticated())

        # user non existant
        login_data = {"username": "az",
                      "password": "pipo"}
        resp = self.client.post("/en/login/", login_data)
        self.assertIn(b"The login/password combination failed. Try again.", resp.content)
        self.assertFalse(auth.get_user(self.client).is_authenticated())

        # no user
        login_data = {"username": "",
                      "password": "pipo"}
        resp = self.client.post("/en/login/", login_data)
        self.assertIn(b"The login/password combination failed. Try again.", resp.content)
        self.assertFalse(auth.get_user(self.client).is_authenticated())

        # no pwd
        login_data = {"username": "az",
                      "password": ""}
        resp = self.client.post("/en/login/", login_data)
        self.assertIn(b"The login/password combination failed. Try again.", resp.content)
        self.assertFalse(auth.get_user(self.client).is_authenticated())

    def test_fail_register(self):
        """
        Test failed register and check for error messages:
        - A user with that username already exists.
        - Password too short.
        - Password too common (eg: aaaaaaaa)
        - Password confirmation do not match"""

        # Username already exists
        user_data = {"user-username": "test_user_1",
                     "user-password1": "plokijuh",
                     "user-password2": "plokijuh"}
        resp = self.client.post("/en/register/", user_data, follow=True)
        self.assertIn(b"A user with that username already exists.", resp.content)
        self.assertFalse(auth.get_user(self.client).is_authenticated())

        # Password too short
        user_data = {"user-username": "abcdefgh",
                     "user-password1": "plo",
                     "user-password2": "plo"}
        resp = self.client.post("/en/register/", user_data, follow=True)
        self.assertIn(b"This password is too short. It must contain at least 8 characters.", resp.content)
        self.assertFalse(auth.get_user(self.client).is_authenticated())

        # Password too common
        user_data = {"user-username": "abcdefgh",
                     "user-password1": "aaaaaaaa",
                     "user-password2": "aaaaaaaa"}
        resp = self.client.post("/en/register/", user_data, follow=True)
        self.assertIn(b"This password is too common.", resp.content)
        self.assertFalse(auth.get_user(self.client).is_authenticated())

        # Password confirmation do not match
        user_data = {"user-username": "abcdefgh",
                     "user-password1": "poiuytreza",
                     "user-password2": "plokijuhygtf"}
        resp = self.client.post("/en/register/", user_data, follow=True)
        self.assertIn(b"The two password fields didn&#39;t match.", resp.content)
        self.assertFalse(auth.get_user(self.client).is_authenticated())

    def test_delete_account(self):
        # Register user
        user_data = {"user-username": "azec",
                     "user-first_name": "qsd",
                     "user-last_name": "wxc",
                     "user-email": "pipo@lala.com",
                     "user-password1": "plokijuh",
                     "user-password2": "plokijuh",
                     "profile-language": "en",
                     "profile-country": "us"}
        self.client.post("/en/register/", user_data, follow=True)
        self.assertTrue(auth.get_user(self.client).is_authenticated())
        self.assertTrue(auth.get_user(self.client).is_active)
        # Deactivate account
        resp = self.client.get("/en/delete_account", follow=True)
        self.assertFalse(auth.get_user(self.client).is_authenticated())
        self.assertFalse(auth.get_user(self.client).is_active)
        self.assertEqual(resp.redirect_chain, [("/en/", 302)])
        self.assertIn(b"Account deactivated", resp.content)

    def test_register_page_locked_for_logged_users(self):
        self.client.force_login(User.objects.get(username="test_user_1"))
        resp = self.client.get("/en/register/", follow=True)
        self.assertEqual(resp.redirect_chain, [("/en/my_measures", 302)])
        self.assertIn(b'You already have an account.', resp.content)
