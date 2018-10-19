from datetime import datetime
from django.urls import reverse, resolve
from django.test import TestCase
from main.models import Lifemark
from bs4 import BeautifulSoup
from ..views import (LifemarkSearchListView,
                     CreateLifemarkView,
                     UpdateLifemarkView,
                     DeleteLifemarkView,
                     show_map)
from main.forms import LifemarkForm
from .base import LifemarkTestCase
from ..templatetags.imgur_filters import to_imgur_thumbnail


class HomeTest(LifemarkTestCase):
    def setUp(self):
        self.login('augie', '1234')
        self.url = reverse('home')
        self.res = self.client.get(self.url)

    def test_url_existance(self):
        view = resolve(self.url)
        self.assertEqual(view.func.view_class, LifemarkSearchListView)

    def test_status_code(self):
        self.assertEquals(self.res.status_code, 200)

    def test_uses_template(self):
        res = self.client.get(self.url)
        self.assertTemplateUsed(res, 'home.html')

    def test_returns_expecting_html(self):
        res = self.client.get(self.url)

        html = res.content.decode('utf8')
        self.assertTrue(html.replace('\n', '').startswith('<!DOCTYPE html><html>'))
        self.assertIn('<title>Lifemarks</title>', html)
        self.assertTrue(html.strip().endswith('</html>'))

        self.assertTemplateUsed(res, 'home.html')

    def test_initial_home_has_no_lifemarks(self):
        self.client.get(self.url)
        self.assertEqual(Lifemark.objects.count(), 0)

    def test_home_page_displays_all_lifemarks(self):
        Lifemark.objects.create(title='first item')
        Lifemark.objects.create(title='second item')

        res = self.client.get(self.url)

        self.assertIn('first item', res.content.decode())
        self.assertIn('second item', res.content.decode())

    def test_uses_form(self):
        res = self.client.get(self.url)
        self.assertIsInstance(res.context['form'], LifemarkForm)

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

    def test_pagination(self):
        for i in range(11):
            Lifemark.objects.create(title=f'existing item {i + 1}')

        res = self.client.get(reverse('home'))
        lifemarks = res.context['lifemarks']
        page_obj = res.context['page_obj']
        self.assertTrue(res.context['is_paginated'])
        self.assertEqual(len(lifemarks), 10)
        self.assertTrue(page_obj.has_next)
        self.assertEqual(lifemarks[0].title, 'existing item 11')


class CreateLifemarkTest(LifemarkTestCase):
    def setUp(self):
        self.login('augie', '1234')
        self.url = reverse('new')

    def test_url_existance(self):
        view = resolve(self.url)
        self.assertEqual(view.func.view_class, CreateLifemarkView)

    def test_create_new_with_post(self):
        self.client.post(self.url, data={'title': 'new item'})

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

    def test_redirects_after_new(self):
        res = self.client.post(self.url, data={'title': 'new item'})
        self.assertEqual(res.status_code, 302)
        self.assertEqual(res['location'], reverse('home'))

    def test_create_new_full_fields(self):
        res = self.client.post('/new', data={
            'title': 'new item',
            'link': 'http://aaa.com',
            'category': 'web',
            'state': 'todo',
            'due_datehour': '2018-01-01 01',
            'rating': 'xxxxx',
            'tags': 'aaa bbb',
            'desc': 'aaaabbbbccccdddd',
            'image_url': 'http://aaa.com/img/sample.jpeg',
            'geo_lat': '38.5',
            'geo_lon': '49.78',
            'u_geo_lat': '38.5',
            'u_geo_lon': '49.78',
        })

        self.assertEqual(res.status_code, 302)
        self.assertEqual(res['location'], reverse('home'))

        self.assertEqual(Lifemark.objects.count(), 1)
        saved = Lifemark.objects.get(title='new item')
        self.assertEqual(saved.title, 'new item')
        self.assertEqual(saved.link, 'http://aaa.com')
        self.assertEqual(saved.category, 'web')
        self.assertEqual(saved.state, 'todo')
        self.assertEqual(saved.due_datehour, '2018-01-01 01')
        self.assertEqual(saved.rating, 'xxxxx')
        self.assertEqual(saved.tags, 'aaa bbb')
        self.assertEqual(saved.desc, 'aaaabbbbccccdddd')
        self.assertEqual(saved.image_url, 'http://aaa.com/img/sample.jpeg')
        self.assertEqual(float(saved.c_geo_lat), 38.5)
        self.assertEqual(float(saved.c_geo_lon), 49.78)

    def test_invalid_do_not_saved_on_db(self):
        self.client.post(self.url)
        self.assertEqual(Lifemark.objects.count(), 0)


class UpdateLifemarkTest(LifemarkTestCase):
    def setUp(self):
        self.login('augie', '1234')

    def test_url_existance(self):
        view = resolve('/update/0/')
        self.assertEqual(view.func.view_class, UpdateLifemarkView)

    def test_update_with_post(self):
        lifemark = Lifemark.objects.create(title='initial title')
        pk = lifemark.pk
        self.assertEqual(lifemark.title, 'initial title')

        self.client.post(reverse('update', kwargs={'pk': pk}), data={'id': pk, 'title': 'modified title'})

        updated = Lifemark.objects.get(id=pk)
        self.assertEqual(updated.title, 'modified title')

    def test_redirects_after_update(self):
        lifemark = Lifemark.objects.create(title='initial title')
        res = self.client.post(f'/update/{lifemark.id}/', data={'title': 'modified title'})

        self.assertEqual(res.status_code, 302)
        self.assertEqual(res['location'], reverse('home'))

    def test_update_with_all_fields(self):
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
            image_url='http://sample.com/init.jpg',
            c_geo_lat=67.89,
            c_geo_lon=56.78
        )
        pk = lifemark.id

        res = self.client.post(reverse('update', kwargs={'pk': pk}), data={
            'id': pk,
            'title': 'mod title',
            'link': 'mod link',
            'category': 'mod',
            'state': 'complete',
            'due_datehour': '2018-02-01 28',
            'rating': 'xxxxx',
            'tags': 'aaa bbb ccc ddd',
            'desc': 'mod description',
            'image_url': 'http://sample.com/mod.jpg',
            'geo_lat': '12.34',
            'geo_lon': '23.45',
        })

        self.assertEqual(res.status_code, 302)
        self.assertEqual(res['location'], reverse('home'))

        updated = Lifemark.objects.get(id=pk)

        self.assertEqual(updated.title, 'mod title')
        self.assertEqual(updated.link, 'mod link')
        self.assertEqual(updated.category, 'mod')
        self.assertEqual(updated.state, 'complete')
        self.assertEqual(updated.due_datehour, '2018-02-01 28')
        self.assertEqual(updated.rating, 'xxxxx')
        self.assertEqual(updated.tags, 'aaa bbb ccc ddd')
        self.assertEqual(updated.desc, 'mod description')
        self.assertEqual(updated.image_url, 'http://sample.com/mod.jpg')
        self.assertEqual(float(updated.c_geo_lat), 67.89)  # creat location doesn't change
        self.assertEqual(float(updated.c_geo_lon), 56.78)
        self.assertEqual(float(updated.u_geo_lat), 12.34)  # update location is set
        self.assertEqual(float(updated.u_geo_lon), 23.45)


class DeleteLifemarkTest(LifemarkTestCase):
    def setUp(self):
        self.login('augie', '1234')

    def test_url_existance(self):
        view = resolve('/delete/0/')
        self.assertEqual(view.func.view_class, DeleteLifemarkView)

    def test_delete_with_post(self):
        lifemark_1st = Lifemark.objects.create(title='existing item1')
        lifemark_2nd = Lifemark.objects.create(title='existing item2')
        self.assertEquals(Lifemark.objects.count(), 2)

        self.client.post(reverse('delete', kwargs={'pk': lifemark_1st.id}))
        self.assertEquals(Lifemark.objects.count(), 1)
        self.assertEquals(Lifemark.objects.all()[0].title, 'existing item2')

        self.client.post(reverse('delete', kwargs={'pk': lifemark_2nd.id}))
        self.assertEquals(Lifemark.objects.count(), 0)

    def test_redirects_after_delete(self):
        lifemark = Lifemark.objects.create(title='existing item')
        res = self.client.post(reverse('delete', kwargs={'pk': lifemark.id}))

        self.assertEqual(res.status_code, 302)
        self.assertEqual(res['location'], reverse('home'))


class SearchTest(LifemarkTestCase):
    def setUp(self):
        self.login('augie', '1234')
        self.url = reverse('search')

    def test_uses_expecting_view(self):
        view = resolve(self.url)
        self.assertEquals(view.func.view_class, LifemarkSearchListView)

    def test_uses_template(self):
        res = self.client.get(self.url)
        self.assertTemplateUsed(res, 'home.html')

    def test_keyword_search(self):
        Lifemark.objects.create(title='title:aaa')
        Lifemark.objects.create(title='bbb', link='aaa')
        Lifemark.objects.create(title='ddd', tags='aaa')
        Lifemark.objects.create(title='ddd', tags='eee', desc='desc_aaa')

        res = self.client.get('/search?q=aaa')
        lifemarks = list(res.context['lifemarks'])

        self.assertEqual(len(lifemarks), 4)
        # check order
        self.assertEquals('desc_aaa', lifemarks[0].desc)
        self.assertEquals('title:aaa', lifemarks[-1].title)

    def test_search_result_pagination(self):
        for i in range(22):
            Lifemark.objects.create(title=f'auto gen {i}')

        res = self.client.get(self.url + '?q=auto')
        page_obj = res.context['page_obj']

        self.assertEquals(len(page_obj), 10)
        self.assertEquals(page_obj.number, 1)

        res = self.client.get(self.url + '?q=auto&page=2')
        page_obj = res.context['page_obj']

        self.assertEquals(len(page_obj), 10)
        self.assertEquals(page_obj.number, 2)

        res = self.client.get(self.url + '?q=auto&page=3')
        page_obj = res.context['page_obj']

        self.assertEquals(len(page_obj), 2)
        self.assertEquals(page_obj.number, 3)

    def test_search_shows_keyword_lines(self):
        Lifemark.objects.create(title='keyword aaa')
        Lifemark.objects.create(title='bbb', tags='keyword')
        Lifemark.objects.create(title='ccc keyword', desc='ccc\nccc keyword ccc\nccc')
        Lifemark.objects.create(title='ddd', tags='xxx yyy')
        Lifemark.objects.create(title='eee', desc='xxxxx\nyyyyy')

        res = self.client.get(self.url + '?q=keyword')
        lifemarks = list(res.context['lifemarks'])
        lifemark_line_data = res.context['lifemark_line_data']
        match_line_count = sum([len(v.lines) for k, v in lifemark_line_data.items()])
        first_row_title = list(lifemark_line_data.values())[0].lifemark.title

        self.assertEqual(len(lifemarks), 3)
        self.assertEqual(len(lifemark_line_data), 3)
        self.assertEqual(match_line_count, 4)
        self.assertEqual(first_row_title, 'ccc keyword')

        check_lifemark_id = Lifemark.objects.get(title='keyword aaa').id

        bs = BeautifulSoup(res.content.decode('utf8'), 'html.parser')
        list_table = bs.find('table', {'id': 'id_recent_list'})
        tr = list_table.find('tr', {'onclick': f'goto_detail({check_lifemark_id}, 0)'})

        expecting_keyword_line = '\n'.join([
            f'<tr onclick="goto_detail({check_lifemark_id}, 0)">',
            '<td></td>',
            '<td>title</td>',
            '<td>0</td>',
            '<td>keyword aaa</td>'  # ignore tailing tags for buttons
        ])
        self.assertTrue(expecting_keyword_line in str(tr))

    def test_search_todo_category(self):
        Lifemark.objects.create(title='aaa')
        Lifemark.objects.create(title='bbb', category='xxx')
        Lifemark.objects.create(title='ccc', category='todo')
        Lifemark.objects.create(title='ddd', category='todo')
        Lifemark.objects.create(title='eee', category='todo')
        Lifemark.objects.create(title='eee', category='yyy')

        res = self.client.get(self.url + '?c=todo')

        lifemarks = list(res.context['lifemarks'])

        self.assertEqual(len(lifemarks), 3)

    def test_search_todo_category_w_keyword(self):
        Lifemark.objects.create(title='aaa')
        Lifemark.objects.create(title='bbb', category='xxx')
        Lifemark.objects.create(title='ccc', category='todo', desc='keyword')
        Lifemark.objects.create(title='ddd', category='todo', desc='keyword')
        Lifemark.objects.create(title='eee', category='todo')
        Lifemark.objects.create(title='eee', category='todo', desc='seoaifj')
        Lifemark.objects.create(title='eee', category='yyy')

        res = self.client.get(self.url + '?q=keyword&c=todo')

        lifemarks = list(res.context['lifemarks'])

        self.assertEqual(len(lifemarks), 2)

    def test_search_ref_category(self):
        Lifemark.objects.create(title='aaa')
        Lifemark.objects.create(title='bbb', category='xxx')
        Lifemark.objects.create(title='ccc', category='ref')
        Lifemark.objects.create(title='ddd', category='ref')
        Lifemark.objects.create(title='eee', category='ref')
        Lifemark.objects.create(title='eee', category='yyy')

        res = self.client.get(self.url + '?c=ref')

        lifemarks = list(res.context['lifemarks'])

        self.assertEqual(len(lifemarks), 3)

    def test_search_multi_keywords(self):
        Lifemark.objects.create(title='aaa1')
        Lifemark.objects.create(title='aaa2', desc='bbb')
        Lifemark.objects.create(title='aaa3', desc='bbb ccc')

        keywords = 'aaa bbb ccc'
        res = self.client.get(self.url + '?q=' + keywords)

        lifemarks = list(res.context['lifemarks'])

        self.assertEqual(len(lifemarks), 1)
        self.assertEqual(lifemarks[0].title, 'aaa3')

    def test_search_todo_state(self):
        Lifemark.objects.create(title='aaa')
        Lifemark.objects.create(title='bbb', state='working')
        Lifemark.objects.create(title='ccc', state='todo')
        Lifemark.objects.create(title='ddd', state='todo')
        Lifemark.objects.create(title='eee', state='todo')
        Lifemark.objects.create(title='eee', state='complete')

        res = self.client.get(self.url + '?s=todo')

        lifemarks = list(res.context['lifemarks'])

        self.assertEqual(len(lifemarks), 3)

    def test_search_todo_state_w_keyword(self):
        Lifemark.objects.create(title='aaa')
        Lifemark.objects.create(title='bbb', state='working')
        Lifemark.objects.create(title='ccc', state='todo', desc='keyword')
        Lifemark.objects.create(title='ddd', state='todo', desc='keyword')
        Lifemark.objects.create(title='eee', state='todo')
        Lifemark.objects.create(title='eee', state='todo', desc='seoaifj')
        Lifemark.objects.create(title='eee', state='complete')

        res = self.client.get(self.url + '?q=keyword&s=todo')

        lifemarks = list(res.context['lifemarks'])

        self.assertEqual(len(lifemarks), 2)

    def test_search_working_state(self):
        Lifemark.objects.create(title='aaa')
        Lifemark.objects.create(title='bbb', state='todo')
        Lifemark.objects.create(title='ccc', state='working')
        Lifemark.objects.create(title='ddd', state='working')
        Lifemark.objects.create(title='eee', state='working')
        Lifemark.objects.create(title='eee', state='complete')

        res = self.client.get(self.url + '?s=working')

        lifemarks = list(res.context['lifemarks'])

        self.assertEqual(len(lifemarks), 3)

    def test_search_working_state_w_keyword(self):
        Lifemark.objects.create(title='aaa')
        Lifemark.objects.create(title='bbb', state='todo')
        Lifemark.objects.create(title='ccc', state='working', desc='keyword')
        Lifemark.objects.create(title='ddd', state='working', desc='keyword')
        Lifemark.objects.create(title='eee', state='working')
        Lifemark.objects.create(title='eee', state='working', desc='seoaifj')
        Lifemark.objects.create(title='eee', state='complete')

        res = self.client.get(self.url + '?q=keyword&s=working')

        lifemarks = list(res.context['lifemarks'])

        self.assertEqual(len(lifemarks), 2)


class LifemarkContentDetailTest(LifemarkTestCase):
    def setUp(self):
        self.login('augie', '1234')
        self.url = reverse('home')

    def test_show_link_as_anchor(self):
        link = 'http://sample.link.com'
        Lifemark.objects.create(
            title='test',
            link=link
        )
        res = self.client.get(self.url)

        expecting_anchor = f'<a href="{link}" target="_blank">test</a>'
        self.assertContains(res, expecting_anchor, html=True)

    def test_show_image_url_as_thumbnail(self):
        image_url = 'http://sample.com/sample_image.jpg'
        Lifemark.objects.create(
            title='test',
            image_url=image_url
        )
        res = self.client.get(self.url)

        thumbnail_image_url = to_imgur_thumbnail(image_url)
        expecting_img_tag = f'<a href="{image_url}" target="_blank"><img src="{thumbnail_image_url}" /></a>'
        self.assertContains(res, expecting_img_tag, html=True)


class UtilityTest(LifemarkTestCase):
    def setUp(self):
        self.login('augie', '1234')

    def test_home_shows_existing_categories(self):
        Lifemark.objects.create(
            title='sample1',
            category='aaa'
        )

        res = self.client.get(reverse('home'))
        expected_category_select = (
            '<select id="id_category_sel" class="form-control">'
            '<option value=""></option>'
            '<option value="aaa">aaa</option>'
            '</select>'
        )
        self.assertContains(res, expected_category_select, html=True)

        Lifemark.objects.create(
            title='sample2',
            category='bbb'
        )

        res = self.client.get(reverse('home'))
        expected_category_select = (
            '<select id="id_category_sel" class="form-control">'
            '<option value=""></option>'
            '<option value="aaa">aaa</option>'
            '<option value="bbb">bbb</option>'
            '</select>'
        )
        self.assertContains(res, expected_category_select, html=True)


class LoginRequriedTests(LifemarkTestCase):
    def setUp(self):
        self.login_url = reverse('login')

    def test_home(self):
        target_url = reverse('home')
        res = self.client.get(target_url)
        self.assertRedirects(res, f'{self.login_url}?next={target_url}')

    def test_search(self):
        target_url = reverse('search')
        res = self.client.get(target_url)
        self.assertRedirects(res, f'{self.login_url}?next={target_url}')


class FunctionTest(TestCase):
    def test_get_keyword_lines(self):
        Lifemark.objects.create(title='aaa keyword')
        Lifemark.objects.create(title='bbb',
                                tags='xxx keyword')
        Lifemark.objects.create(title='ccc',
                                tags='xxx yyy',
                                desc='blahblah\r\nkeyword blah\r\nblah')
        Lifemark.objects.create(title='ddd')
        Lifemark.objects.create(title='eee')
        Lifemark.objects.create(title='fff')

        lifemarks = Lifemark.objects.all()

        viewclass = LifemarkSearchListView()
        keywords_str = 'keyword'
        search_fieldnames = ['title', 'tags', 'desc']
        line_datas = viewclass.get_keywords_lines(lifemarks, keywords_str, search_fieldnames)
        # line results includes all query result
        self.assertEqual(len(line_datas), 6)
        keyword_lines = sum([len(v.lines) for k, v in line_datas.items()])
        self.assertEqual(keyword_lines, 3)

    def test_get_keyword_lines_w_multi_keywords(self):
        Lifemark.objects.create(title='aaa keyword')
        Lifemark.objects.create(title='bbb',
                                tags='xxx keyword')
        Lifemark.objects.create(title='ccc',
                                tags='xxx yyy',
                                desc='blahblah\r\nkeyword blah\r\nblah')
        Lifemark.objects.create(title='ddd',
                                tags='xxx yyy otherkw',
                                desc='....')
        Lifemark.objects.create(title='eee',
                                desc='awfawfewaf\r\nkeyword\r\nafaw\r\nfaw otherkw xefw')
        Lifemark.objects.create(title='fff')
        Lifemark.objects.create(title='ggg')

        lifemarks = Lifemark.objects.all()

        viewclass = LifemarkSearchListView()
        keywords_str = 'keyword otherkw'
        search_fieldnames = ['title', 'tags', 'desc']
        line_datas = viewclass.get_keywords_lines(lifemarks, keywords_str, search_fieldnames)
        self.assertEqual(len(line_datas), 7)
        expecting_lines = sum([len(v.lines) for k, v in line_datas.items()])
        self.assertEqual(expecting_lines, 6)


class ShowMapTests(LifemarkTestCase):
    def setUp(self):
        self.url = reverse('show_map')
        self.res = self.client.get(self.url + '?lat=0&lon0')

    def test_url_existance(self):
        view = resolve(self.url)
        self.assertEqual(view.func, show_map)

    def test_status_code(self):
        self.assertEquals(self.res.status_code, 200)

    def test_uses_template(self):
        res = self.client.get(self.url)
        self.assertTemplateUsed(res, 'show_map.html')

    def test_page_contents(self):
        expecting_map_js_func = 'function initMap()'

        html = self.res.content.decode('utf8')
        self.assertTrue(expecting_map_js_func in html)
