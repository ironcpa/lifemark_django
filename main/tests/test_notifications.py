from django.test import TestCase
from main.models import Lifemark
from main.notifications import create_dued_lifemarks


class NotificationTest(TestCase):
    def test_create_hourly_dued_lifemarks(self):
        Lifemark.objects.create(title='hourly dued1', state='todo', due_datehour='2018-01-01 23')
        Lifemark.objects.create(title='complete', state='complete', due_datehour='2018-01-02 00')
        Lifemark.objects.create(title='daily dued', state='todo', due_datehour='2018-01-02 00')  # ignored for hourly
        Lifemark.objects.create(title='hourly dued2', state='todo', due_datehour='2018-01-02 01')
        Lifemark.objects.create(title='not yet dued', state='todo', due_datehour='2018-01-02 02')

        # 1시간 이후 마감상태일 정보를 가져온다.
        created = create_dued_lifemarks('2018-01-02 00')

        self.assertEqual(Lifemark.objects.all().count(), 6)
        self.assertEqual(created.title, 'items due tomorrow')
        self.assertEqual(created.category, 'noti')
        self.assertTrue(created.link.startswith('lifemarks?'))
        self.assertTrue(created.desc.strip().endswith('is dued!'))
        dued_item_count = len(created.desc.strip().split('\n'))
        self.assertEqual(dued_item_count, 2)
        self.assertIn(':hourly dued1(todo) is dued!', created.desc)
        self.assertIn(':hourly dued2(todo) is dued!', created.desc)

    def test_create_daily_dued_lifemarks(self):
        Lifemark.objects.create(title='complete', state='complate', due_datehour='2018-01-02 00')
        Lifemark.objects.create(title='dued todo1', state='todo', due_datehour='2018-01-02 00')
        Lifemark.objects.create(title='hourly dued todo', state='todo', due_datehour='2018-01-02 01')
        Lifemark.objects.create(title='dued todo2', state='todo', due_datehour='2018-01-03 00')
        Lifemark.objects.create(title='not yet dued', state='todo', due_datehour='2018-01-04 00')

        # 1일 이후 마감상태일 정보를 가져온다.
        created = create_dued_lifemarks('2018-01-02 00', True)

        self.assertEqual(Lifemark.objects.all().count(), 6)
        self.assertEqual(created.title, 'items due tomorrow')
        self.assertEqual(created.category, 'noti')
        self.assertTrue(created.link.startswith('lifemarks?'))
        self.assertTrue(created.desc.strip().endswith('is dued!'))
        dued_item_count = len(created.desc.strip().split('\n'))
        self.assertEqual(dued_item_count, 3)
        self.assertIn(':dued todo1(todo) is dued!', created.desc)
        self.assertIn(':hourly dued todo(todo) is dued!', created.desc)
        self.assertIn(':dued todo2(todo) is dued!', created.desc)
