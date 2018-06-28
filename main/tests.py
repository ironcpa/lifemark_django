from django.test import TestCase
from django.urls import resolve
from main.views import home_page


class BasicPageTest(TestCase):

    def test_root_url_resolves_to_home_page_view(self):
        found = resolve('/')
        print('==================')
        print(found)
        self.assertEqual(found.func, home_page)
