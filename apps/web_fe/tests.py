from django.test import TestCase
from django.test.client import Client
import json
from django.contrib.auth.models import User
from web_fe.views import *
from util.utilities import print_debug


def userSetup(current_test):
    # First create a new user
    current_test.test_user = User.objects.create_user(
        'testuser', 'test@test.test', 'testpass')
    # Now login as that user
    current_test.client = Client()
    current_test.client.login(username='testuser', password='testpass')


class UserLoginTest(TestCase):

    def setUp(self):
        userSetup(self)

    def tearDown(self):
        User.objects.filter(username='testuser').delete()

    def test_valid_user_login_success(self):
        user = {
            'username': 'testuser',
            'password': 'testpass'
        }
        response = self.client.post(
            '/acme/login/', {'username': user['username'], 'password': user['password']})

        self.assertEquals(response.status_code, 302)
        self.assertTrue(response.url.split('/').pop() != 'login')

    def test_valud_user_invalid_password_login_success(self):
        user = {
            'username': 'testuser',
            'password': 'NOT_A_GOOD_PASSWORD'
        }
        response = self.client.post(
            '/acme/login/', {'username': user['username'], 'password': user['password']})

        self.assertEquals(response.status_code, 302)
        self.assertEquals(response.url.split('/').pop(), 'login')

    def test_user_login_failure(self):
        user = {
            'username': 'NOT_A_USER',
            'password': 'NOT_A_PASSWORD'
        }
        response = self.client.post(
            '/acme/login/', {'username': user['username'], 'password': user['password']})

        self.assertEquals(response.status_code, 302)
        self.assertEquals(response.url.split('/').pop(), 'login')
