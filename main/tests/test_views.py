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
        self.client.post('/new', data={'title': 'new item'})

        self.assertEqual(Lifemark.objects.count(), 1)
        new_item = Lifemark.objects.first()
        self.assertEqual(new_item.title, 'new item')

    def test_redirects_after_POST(self):
        response = self.client.post('/new', data={'title': 'new item'})
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


class ViewModelIntergrationTest(TestCase):

    def test_post_saves_correct_model(self):
        res = self.client.post('/new', data={
            'title': 'new item',
            'link': 'http://aaa.com',
            'category': 'web',
            'is_complete': 'todo',
            'due_datehour': '2018010101',
            'rating': 'xxxxx',
            'tags': 'aaa bbb',
            'desc': 'aaaabbbbccccdddd',
            'image_url': 'http://aaa.com/img/sample.jpeg'
        })

        self.assertEqual(res.status_code, 302)
        self.assertEqual(res['location'], '/')

        self.assertEqual(Lifemark.objects.count(), 1)
        saved = Lifemark.objects.get(title='new item')
        self.assertEqual(saved.title, 'new item')
        self.assertEqual(saved.link, 'http://aaa.com')
        self.assertEqual(saved.category, 'web')
        self.assertEqual(saved.is_complete, 'todo')
        self.assertEqual(saved.due_datehour, '2018010101')
        self.assertEqual(saved.rating, 'xxxxx')
        self.assertEqual(saved.tags, 'aaa bbb')
        self.assertEqual(saved.desc, 'aaaabbbbccccdddd')
        self.assertEqual(saved.image_url, 'http://aaa.com/img/sample.jpeg')

    def test_invalid_do_not_saved_on_db(self):
        self.client.post('/new')
        self.assertEqual(Lifemark.objects.count(), 0)
