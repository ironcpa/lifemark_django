from django.test import TestCase
from main.templatetags.nbsp_filter import nbsp


class NbspFilterTest(TestCase):
    def test_nbsp(self):
        text = '  a   b    '
        self.assertEquals(
            '&nbsp;&nbsp;a&nbsp;&nbsp;&nbsp;b&nbsp;&nbsp;&nbsp;&nbsp;',
            nbsp(text)
        )
