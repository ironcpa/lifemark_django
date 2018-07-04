from django.test import TestCase
from main.models import Lifemark
from main.forms import LifemarkForm


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
        self.client.post('/', data={'title': 'new item'})

        self.assertEqual(Lifemark.objects.count(), 1)
        new_item = Lifemark.objects.first()
        self.assertEqual(new_item.title, 'new item')

    def test_redirects_after_POST(self):
        response = self.client.post('/', data={'title': 'new item'})
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response['location'], '/')

    def test_only_saves_lifmarks_when_necessary(self):
        self.client.get('/')
        self.assertEqual(Lifemark.objects.count(), 0)

    def test_displays_all_list_items(self):
        Lifemark.objects.create(title='first item')
        Lifemark.objects.create(title='second item')

        res = self.client.get('/')

        self.assertIn('first item', res.content.decode())
        self.assertIn('second item', res.content.decode())

    def test_main_page_uses_lifemark_form(self):
        res = self.client.get('/')
        self.assertIsInstance(res.context['form'], LifemarkForm)

    def test_validation_errors_are_sent_back_to_home_page_template(self):
        pass
