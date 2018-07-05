from django.db import models


class Lifemark(models.Model):
    title = models.TextField()
    link = models.TextField(default='', null=True)
    category = models.TextField(default='')
    is_complete = models.TextField(default='')
    due_date = models.TextField(default='', null=True)
    rating = models.TextField(default='', null=True)
    tags = models.TextField(default='')
    desc = models.TextField(default='')
    image_url = models.TextField(default='', null=True)

    def __str__(self):
        return f'Lifemark: "{self.title}"'


class TestModel(models.Model):
    title = models.TextField()
