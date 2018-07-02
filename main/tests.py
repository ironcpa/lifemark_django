from django.test import TestCase
from django.urls import resolve
from django.http import HttpRequest
from django.template.loader import render_to_string
from main.views import home_page
from main.models import Lifemark


class BasicPageTest(TestCase):

    def test_uses_home_template(self):
        response = self.client.get('/')
        self.assertTemplateUsed(response, 'home.html')

    def test_home_page_returns_expected_html(self):
        response = self.client.get('/')

        html = response.content.decode('utf8')
        self.assertTrue(html.startswith('<html>'))
        self.assertIn('<title>Lifemark</title>', html)
        self.assertTrue(html.strip().endswith('</html>'))

        self.assertTemplateUsed(response, 'home.html')

    def test_can_save_a_POST_request(self):
        response = self.client.post('/', data={'add_title': 'new item'})
        self.assertIn('new item', response.content.decode())
        self.assertTemplateUsed(response, 'home.html')


class LifemarkModelTest(TestCase):

    def test_saving_and_retrieving_lifemarks(self):
        first_lifemark = Lifemark()
        first_lifemark.title = 'first item'
        first_lifemark.save()

        second_lifemark = Lifemark()
        second_lifemark.title = 'second item'
        second_lifemark.save()

        all_saved = Lifemark.objects.all()
        self.assertEqual(all_saved.count(), 2)

        saved_first_lifemark = all_saved[0]
        saved_second_lifemark = all_saved[1]
        self.assertEqual(saved_first_lifemark.title, 'first item')
        self.assertEqual(saved_second_lifemark.title, 'second item')
