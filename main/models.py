from django.db import models


class Lifemark(models.Model):
    title = models.TextField(default='')
    link = models.TextField(default='', null=True)
    category = models.TextField(default='')
    is_complete = models.TextField(default='')
    due_date = models.TextField(default='', null=True)
    rating = models.TextField(default='', null=True)
    tags = models.TextField(default='')
    desc = models.TextField(default='')
    image_url = models.TextField(default='', null=True)
