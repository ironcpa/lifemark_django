from django.test import TestCase
from django.urls import reverse
from main.models import Lifemark
from main.forms import LifemarkForm
from datetime import datetime


class BasicPageTest(TestCase):
    def test_uses_home_template(self):
        response = self.client.get(reverse('home'))
        self.assertTemplateUsed(response, 'home.html')

    def test_home_page_returns_expected_html(self):
        response = self.client.get(reverse('home'))

        html = response.content.decode('utf8')
        self.assertTrue(html.replace('\n', '').startswith('<!DOCTYPE html><html>'))
        self.assertIn('<title>Lifemarks</title>', html)
        self.assertTrue(html.strip().endswith('</html>'))

        self.assertTemplateUsed(response, 'home.html')

    def test_can_save_a_POST_request(self):
        self.client.post('/new', data={'title': 'new item'})

        self.assertEqual(Lifemark.objects.count(), 1)
        new_item = Lifemark.objects.first()
        self.assertEqual(new_item.title, 'new item')
        filtered = Lifemark.objects.filter(
            cdate__lte=datetime.now(),
            udate__lte=datetime.now(),
        )
        self.assertEqual(filtered.count(), 1)
        self.assertEqual(filtered.first().title, 'new item')
        self.assertEqual(filtered.first(), new_item)

    def test_redirects_after_POST(self):
        response = self.client.post('/new', data={'title': 'new item'})
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response['location'], reverse('home'))

    def test_initial_home_has_no_lifemarks(self):
        self.client.get(reverse('home'))
        self.assertEqual(Lifemark.objects.count(), 0)

    def test_home_page_displays_all_lifemarks(self):
        Lifemark.objects.create(title='first item')
        Lifemark.objects.create(title='second item')

        res = self.client.get(reverse('home'))

        self.assertIn('first item', res.content.decode())
        self.assertIn('second item', res.content.decode())

    def test_main_page_uses_lifemark_form(self):
        res = self.client.get(reverse('home'))
        self.assertIsInstance(res.context['form'], LifemarkForm)

    def test_can_update_POST_request(self):
        lifemark = Lifemark.objects.create(title='initial title')
        self.assertEqual(lifemark.title, 'initial title')

        self.client.post(reverse('update', kwargs={'pk': 1}), data={'id': 1, 'title': 'modified title'})

        updated = Lifemark.objects.get(id=1)
        self.assertEqual(updated.title, 'modified title')

    def test_redirects_after_update_POST(self):
        lifemark = Lifemark.objects.create(title='initial title')
        # res = self.client.post(f'/update', data={'id': lifemark.id, 'title': 'modified title'})
        res = self.client.post(f'/update/{lifemark.id}/', data={'title': 'modified title'})

        self.assertEqual(res.status_code, 302)
        self.assertEqual(res['location'], reverse('home'))

    def test_delete(self):
        lifemark_1st = Lifemark.objects.create(title='existing item1')
        lifemark_2nd = Lifemark.objects.create(title='existing item2')
        self.assertEquals(Lifemark.objects.count(), 2)

        self.client.post(reverse('delete', kwargs={'pk': lifemark_1st.id}))
        self.assertEquals(Lifemark.objects.count(), 1)
        self.assertEquals(Lifemark.objects.all()[0].title, 'existing item2')

        self.client.post(reverse('delete', kwargs={'pk': lifemark_2nd.id}))
        self.assertEquals(Lifemark.objects.count(), 0)

    def test_redirect_to_home_after_delete(self):
        lifemark = Lifemark.objects.create(title='existing item')
        res = self.client.post(reverse('delete', kwargs={'pk': lifemark.id}))

        self.assertEqual(res.status_code, 302)
        self.assertEqual(res['location'], reverse('home'))

    def test_recent_list_shows_recent_10_items(self):
        for i in range(9):
            Lifemark.objects.create(title=f'existing item {i + 1}')

        res = self.client.get(reverse('home'))
        recent_items = res.context['lifemarks']
        self.assertEqual(len(recent_items), 9)
        self.assertEqual(recent_items[0].title, 'existing item 9')
        self.assertEqual(recent_items[8].title, 'existing item 1')

        Lifemark.objects.create(title=f'10th item')
        res = self.client.get(reverse('home'))
        recent_items = res.context['lifemarks']
        self.assertEqual(len(recent_items), 10)
        self.assertEqual(recent_items[0].title, '10th item')
        self.assertEqual(recent_items[9].title, 'existing item 1')

        Lifemark.objects.create(title=f'11th item')
        res = self.client.get(reverse('home'))
        recent_items = res.context['lifemarks']
        self.assertEqual(len(recent_items), 10)
        self.assertEqual(recent_items[0].title, '11th item')
        self.assertEqual(recent_items[1].title, '10th item')
        self.assertEqual(recent_items[9].title, 'existing item 2')

        recently_updated = Lifemark.objects.get(title='10th item')
        recently_updated.desc = 'updated desc'
        recently_updated.save()
        res = self.client.get(reverse('home'))
        recent_items = res.context['lifemarks']
        self.assertEqual(len(recent_items), 10)
        self.assertEqual(recent_items[0].title, '10th item')
        self.assertEqual(recent_items[1].title, '11th item')
        self.assertEqual(recent_items[9].title, 'existing item 2')


class ViewModelIntergrationTest(TestCase):

    def test_post_saves_correct_model(self):
        res = self.client.post('/new', data={
            'title': 'new item',
            'link': 'http://aaa.com',
            'category': 'web',
            'state': 'todo',
            'due_datehour': '2018010101',
            'rating': 'xxxxx',
            'tags': 'aaa bbb',
            'desc': 'aaaabbbbccccdddd',
            'image_url': 'http://aaa.com/img/sample.jpeg'
        })

        self.assertEqual(res.status_code, 302)
        self.assertEqual(res['location'], reverse('home'))

        self.assertEqual(Lifemark.objects.count(), 1)
        saved = Lifemark.objects.get(title='new item')
        self.assertEqual(saved.title, 'new item')
        self.assertEqual(saved.link, 'http://aaa.com')
        self.assertEqual(saved.category, 'web')
        self.assertEqual(saved.state, 'todo')
        self.assertEqual(saved.due_datehour, '2018010101')
        self.assertEqual(saved.rating, 'xxxxx')
        self.assertEqual(saved.tags, 'aaa bbb')
        self.assertEqual(saved.desc, 'aaaabbbbccccdddd')
        self.assertEqual(saved.image_url, 'http://aaa.com/img/sample.jpeg')

    def test_invalid_do_not_saved_on_db(self):
        self.client.post(reverse('new'))
        self.assertEqual(Lifemark.objects.count(), 0)

    def test_post_updates_all_fields_correctly(self):
        lifemark = Lifemark.objects.create(title='initial title')
        self.assertEqual(lifemark.title, 'initial title')

        self.client.post(reverse('update', kwargs={'pk': 1}), data={'id': 1, 'title': 'modified title'})

        lifemark = Lifemark.objects.create(
            title='init title',
            link='init link',
            category='init',
            state='todo',
            due_datehour='2018010101',
            rating='x',
            tags='aaa bbb',
            desc='init description',
            image_url='http://sample.com/init.jpg'
        )
        pk = lifemark.id

        res = self.client.post(reverse('update', kwargs={'pk': pk}), data={
            'id': pk,
            'title': 'mod title',
            'link': 'mod link',
            'category': 'mod',
            'state': 'complete',
            'due_datehour': '2018020128',
            'rating': 'xxxxx',
            'tags': 'aaa bbb ccc ddd',
            'desc': 'mod description',
            'image_url': 'http://sample.com/mod.jpg',
        })

        self.assertEqual(res.status_code, 302)
        self.assertEqual(res['location'], reverse('home'))

        updated = Lifemark.objects.get(id=pk)

        self.assertEqual(updated.title, 'mod title')
        self.assertEqual(updated.link, 'mod link')
        self.assertEqual(updated.category, 'mod')
        self.assertEqual(updated.state, 'complete')
        self.assertEqual(updated.due_datehour, '2018020128')
        self.assertEqual(updated.rating, 'xxxxx')
        self.assertEqual(updated.tags, 'aaa bbb ccc ddd')
        self.assertEqual(updated.desc, 'mod description')
        self.assertEqual(updated.image_url, 'http://sample.com/mod.jpg')

    def test_can_select_saved_categories(self):
        Lifemark.objects.create(
            title='sample1',
            category='aaa'
        )

        response = self.client.get(reverse('home'))
        expected_category_select = (
            '<select id="id_category_sel" class="form-control">'
            '<option value=""></option>'
            '<option value="aaa">aaa</option>'
            '</select>'
        )
        self.assertContains(response, expected_category_select, html=True)

        Lifemark.objects.create(
            title='sample2',
            category='bbb'
        )

        response = self.client.get(reverse('home'))
        expected_category_select = (
            '<select id="id_category_sel" class="form-control">'
            '<option value=""></option>'
            '<option value="aaa">aaa</option>'
            '<option value="bbb">bbb</option>'
            '</select>'
        )
        self.assertContains(response, expected_category_select, html=True)
