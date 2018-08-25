from django.test import TestCase
from main.models import Lifemark
from main.templatetags.nbsp_filter import nbsp
from main.templatetags.imgur_filters import to_imgur_thumbnail
from main.templatetags.lifemark_filters import td_class
from main.templatetags.lifemark_filters import LIFEMARK_TD_CLASS_REF, LIFEMARK_TD_CLASS_TODO, LIFEMARK_TD_CLASS_WORKING, LIFEMARK_TD_CLASS_COMPLETE


class NbspFilterTest(TestCase):
    def test_nbsp(self):
        text = '  a   b    '
        self.assertEquals(
            '&nbsp;&nbsp;a&nbsp;&nbsp;&nbsp;b&nbsp;&nbsp;&nbsp;&nbsp;',
            nbsp(text)
        )


class ImgurFilterTest(TestCase):
    def test_to_imgur_thumbnail(self):
        org_img_url = 'abcde.jpg'
        self.assertEqual(
            'abcdes.jpg',
            to_imgur_thumbnail(org_img_url)
        )


class LifemarkFilterTest(TestCase):
    def test_to_class(self):
        lifemark = Lifemark.objects.create(title='test', category='ref', state='todo')
        self.assertEqual(td_class(lifemark), LIFEMARK_TD_CLASS_REF)

        lifemark = Lifemark.objects.create(title='test', category='', state='todo')
        self.assertEqual(td_class(lifemark), LIFEMARK_TD_CLASS_TODO)

        lifemark = Lifemark.objects.create(title='test', state='todo')
        self.assertEqual(td_class(lifemark), LIFEMARK_TD_CLASS_TODO)

        lifemark = Lifemark.objects.create(title='test', state='working')
        self.assertEqual(td_class(lifemark), LIFEMARK_TD_CLASS_WORKING)

        lifemark = Lifemark.objects.create(title='test', state='complete')
        self.assertEqual(td_class(lifemark), LIFEMARK_TD_CLASS_COMPLETE)
