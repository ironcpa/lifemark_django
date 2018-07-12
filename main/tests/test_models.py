from django.test import TestCase
from django.core.exceptions import ValidationError
from main.models import Lifemark


class LifemarkModelTest(TestCase):

    def test_saving_and_retrieving_lifemarks(self):
        first_lifemark = Lifemark()
        first_lifemark.title = 'first item'
        first_lifemark.save()

        second_lifemark = Lifemark()
        second_lifemark.title = 'second item'
        second_lifemark.save()

        all_saved = Lifemark.objects.all()
        self.assertEqual(all_saved.count(), 2)

        saved_first_lifemark = all_saved[0]
        saved_second_lifemark = all_saved[1]
        self.assertEqual(saved_first_lifemark.title, 'first item')
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
