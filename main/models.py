from django.db import models


class Lifemark(models.Model):
    title = models.TextField()
    link = models.TextField(blank=True, default='')
    category = models.TextField(blank=True, default='')
    is_complete = models.TextField(blank=True, default='')
    due_datehour = models.TextField(blank=True, default='')
    rating = models.TextField(blank=True, default='')
    tags = models.TextField(blank=True, default='')
    desc = models.TextField(blank=True, default='')
    image_url = models.TextField(blank=True, default='')
    # cdate = models.DateTimeField(null=False)
    # udate = models.DateTimeField(null=False)

    def __str__(self):
        return f'Lifemark: "{self.title}"'


class TestModel(models.Model):
    title = models.TextField(default=None, null=True)
    category = models.TextField(default='', null=True)
    state = models.TextField(null=True)
