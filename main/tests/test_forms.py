from django.test import TestCase
from main.forms import LifemarkForm
from main.models import Lifemark


class LifemarkFormTest(TestCase):

    def test_form_renders_correct_entries(self):
        form = LifemarkForm()
        form_text = form.as_p()

        self.assertIn('name="title"', form_text)
        self.assertIn('placeholder="Enter lifemark title"', form_text)

        self.assertIn('name="link"', form_text)
        self.assertIn('name="category"', form_text)
        self.assertIn('name="state"', form_text)
        self.assertIn('name="due_datehour"', form_text)
        self.assertIn('name="due_datehour"', form_text)
        self.assertIn('name="rating"', form_text)
        self.assertIn('name="tags"', form_text)
        self.assertIn('name="desc"', form_text)
        self.assertIn('name="image_url"', form_text)
        self.assertIn('name="geo_lat"', form_text)
        self.assertIn('name="geo_lon"', form_text)

    def test_form_failed_validation_for_full_entries(self):
        form = LifemarkForm(data={'title': ''})

        self.assertFalse(form.is_valid())
        self.assertEqual(
            form.errors['title'],
            ["You need a valid title"]
        )

    def test_form_successful_validation_for_full_entires(self):
        form = LifemarkForm(data={
            'title': 'aaa',
        })

        self.assertTrue(form.is_valid())

    def test_form_saves_model(self):
        form = LifemarkForm(data={
            'title': 'aaa',
            'geo_lat': 98.76,
            'geo_lon': 87.65
        })
        lifemark = form.save()

        self.assertEqual(lifemark.title, 'aaa')
        self.assertEqual(float(lifemark.geo_lat), 98.76)
        self.assertEqual(float(lifemark.geo_lon), 87.65)
