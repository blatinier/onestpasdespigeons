from django.contrib import auth
from django.contrib.auth.models import User
from django.test import Client, TestCase
from weights.models import Measure, PigeonUser, Product


class AuthTestCase(TestCase):
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
        resp = self.client.get("/register/")
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
        resp = self.client.post("/register/", user_data, follow=True)
        self.assertEqual(resp.redirect_chain, [("/my_measures", 302)])
        self.assertIn(b"My measures", resp.content)
        self.assertTrue(auth.get_user(self.client).is_authenticated())

        # Logout
        resp = self.client.get("/logout/", follow=True)
        self.assertEqual(resp.redirect_chain, [("/", 302)])
        self.assertFalse(auth.get_user(self.client).is_authenticated())

        # Login
        login_data = {"username": "azec",
                      "password": "plokijuh"}
        resp = self.client.post("/login/", login_data, follow=True)
        self.assertEqual(resp.redirect_chain, [("/my_measures", 302)])
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
        pass  # TODO

    def test_fail_register(self):
        """
        Test failed register and check for error messages:
        - A user with that username already exists.
        - List TODO"""
        pass  # TODO
