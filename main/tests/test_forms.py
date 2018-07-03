from django.test import TestCase
from main.forms import LifemarkForm


class LifemarkFormTest(TestCase):

    def test_form_renders_correct_entries(self):
        form = LifemarkForm()
        self.assertIn('placeholder="Enter lifemark title"', form.as_p())
