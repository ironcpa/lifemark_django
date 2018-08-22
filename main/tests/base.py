from django.contrib.auth.models import User
from django.test import TestCase


class LifemarkTestCase(TestCase):
    def login(self, username, password):
        if not username:
            username = 'test'
        if not password:
            password = '1234'
        User.objects.create_user(
            username=username,
            password=password,
            email='test@sample.com'
        )
        self.client.login(username=username, password=password)
