from django.test import TestCase
from django.core.exceptions import ValidationError
from main.models import Lifemark


class LifemarkModelTest(TestCase):

    def test_saving_and_retrieving_lifemarks(self):
        first_lifemark = Lifemark()
        first_lifemark.title = 'first item'
        first_lifemark.due_datehour = '2018123456'
        first_lifemark.save()

        second_lifemark = Lifemark()
        second_lifemark.title = 'second item'
        second_lifemark.save()

        all_saved = Lifemark.objects.all()
        self.assertEqual(all_saved.count(), 2)

        saved_first_lifemark = all_saved[0]
        saved_second_lifemark = all_saved[1]
        self.assertEqual(saved_first_lifemark.title, 'first item')
        self.assertEqual(saved_first_lifemark.due_datehour, '2018123456')
        self.assertEqual(saved_second_lifemark.title, 'second item')

    def test_lifemark_validation(self):
        lifemark = Lifemark()
        with self.assertRaises(ValidationError):
            lifemark.full_clean()
            lifemark.save()

        self.assertEqual(Lifemark.objects.count(), 0)

        lifemark.title = 'aaa'
        try:
            lifemark.full_clean()
            lifemark.save()
        except ValidationError:
            pass
        self.assertEqual(Lifemark.objects.count(), 1)

    def test_lifemark_search_w_keyword(self):
        Lifemark.objects.create(title='aaa')
        Lifemark.objects.create(title='xxxaaa')
        Lifemark.objects.create(title='xxxaaayyy')
        Lifemark.objects.create(title='other')
        Lifemark.objects.create(title='other', desc='xxxaaayyy')

        lifemarks = Lifemark.objects.get_all_matches_on_any_fields(
            ('title',),
            '',
            '',
            'aaa'
        )
        self.assertEquals(len(lifemarks), 3)

        lifemarks = Lifemark.objects.get_all_matches_on_any_fields(
            ('title', 'desc'),
            '',
            '',
            'aaa'
        )
        self.assertEquals(len(lifemarks), 4)

    def test_lifemark_search_w_multi_keywords(self):
        Lifemark.objects.create(title='aaabbb')
        Lifemark.objects.create(title='aaa')
        Lifemark.objects.create(title='aaabbb')
        Lifemark.objects.create(title='other')
        Lifemark.objects.create(title='other', desc='aaabbb')
        Lifemark.objects.create(title='other', desc='xxxaaayyy')
        Lifemark.objects.create(title='other', desc='xxxbbbyyy')
        Lifemark.objects.create(title='other', desc='xxxaaabbbyyy')
        Lifemark.objects.create(title='other', desc='other')

        lifemarks = Lifemark.objects.get_any_matches_on_any_fields(
            ('title',),
            '',
            '',
            'aaa bbb'
        )
        self.assertEquals(len(lifemarks), 3)

        lifemarks = Lifemark.objects.get_all_matches_on_any_fields(
            ('title',),
            '',
            '',
            'aaa bbb'
        )
        self.assertEquals(len(lifemarks), 2)

        lifemarks = Lifemark.objects.get_any_matches_on_any_fields(
            ('title', 'desc'),
            '',
            '',
            'aaa bbb'
        )
        self.assertEquals(len(lifemarks), 7)

        lifemarks = Lifemark.objects.get_all_matches_on_any_fields(
            ('title', 'desc'),
            '',
            '',
            'aaa bbb'
        )
        self.assertEquals(len(lifemarks), 4)

    def test_lifemark_searh_w_category(self):
        Lifemark.objects.create(title='aaa')
        Lifemark.objects.create(title='aaa')
        Lifemark.objects.create(title='aaa', category='xxx')
        Lifemark.objects.create(title='aaa', category='yyy')
        Lifemark.objects.create(title='bbb', category='xxx')
        Lifemark.objects.create(title='bbb', category='xxx', desc='aaa')

        lifemarks = Lifemark.objects.get_all_matches_on_any_fields(
            ('title', 'category', 'desc'),
            'xxx',
            '',
            ''
        )
        self.assertEqual(len(lifemarks), 3)

        lifemarks = Lifemark.objects.get_all_matches_on_any_fields(
            ('title', 'category', 'desc'),
            'xxx',
            '',
            'aaa'
        )
        self.assertEqual(len(lifemarks), 2)

    def test_lifemark_searh_w_state(self):
        Lifemark.objects.create(title='aaa')
        Lifemark.objects.create(title='aaa')
        Lifemark.objects.create(title='aaa', state='todo')
        Lifemark.objects.create(title='bbb', state='todo')
        Lifemark.objects.create(title='bbb', state='complete')
        Lifemark.objects.create(title='bbb', state='working')
        Lifemark.objects.create(title='bbb', state='todo', desc='aaa')

        lifemarks = Lifemark.objects.get_all_matches_on_any_fields(
            ('title', 'desc'),
            '',
            'todo',
            ''
        )
        self.assertEqual(len(lifemarks), 3)

        lifemarks = Lifemark.objects.get_all_matches_on_any_fields(
            ('title', 'desc'),
            '',
            'todo',
            'aaa'
        )
        self.assertEqual(len(lifemarks), 2)

    def test_get_dued_lifemarks(self):
        Lifemark.objects.create(title='test1', state='todo', due_datehour='2018-01-01 00')
        Lifemark.objects.create(title='test2', state='todo', due_datehour='2018-01-01 10')
        Lifemark.objects.create(title='test3', state='todo', due_datehour='2018-01-02 00')
        Lifemark.objects.create(title='test4', state='todo', due_datehour='2018-01-02 10')
        Lifemark.objects.create(title='test5', state='todo', due_datehour='2018-01-03 00')
        Lifemark.objects.create(title='test6', state='todo', due_datehour='2018-01-03 10')
        Lifemark.objects.create(title='test7', due_datehour='2018-01-02 10')

        curr_datehour = '2018-01-01 00'
        lifemarks = Lifemark.objects.get_dued_lifemarks(curr_datehour)
        self.assertEqual(lifemarks.count(), 3)
        self.assertIn(Lifemark.objects.get(title='test1'), lifemarks)
        self.assertIn(Lifemark.objects.get(title='test2'), lifemarks)
        self.assertIn(Lifemark.objects.get(title='test3'), lifemarks)

    def test_get_hourly_dued_lifemarks(self):
        Lifemark.objects.create(title='test1', state='todo', due_datehour='2018-01-01 00')
        Lifemark.objects.create(title='test2', state='todo', due_datehour='2018-01-01 01')
        Lifemark.objects.create(title='test3', state='todo', due_datehour='2018-01-01 02')
        Lifemark.objects.create(title='test4', state='todo', due_datehour='2018-01-01 03')
        Lifemark.objects.create(title='test5', state='todo', due_datehour='2018-01-01 04')

        curr_datehour = '2018-01-01 01'
        lifemarks = Lifemark.objects.get_hourly_dued_lifemarks(curr_datehour)
        self.assertEquals(lifemarks.count(), 2)
        self.assertIn(Lifemark.objects.get(title='test2'), lifemarks)
        self.assertIn(Lifemark.objects.get(title='test3'), lifemarks)
