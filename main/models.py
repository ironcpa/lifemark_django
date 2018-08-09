from django.db import models
from django.db.models import Q


class LifemarkManager(models.Manager):
    def get_matches_on_fields(self, fields, keywords_str):
        if not keywords_str:
            return self.none()

        keywords = keywords_str.split(' ')

        q_objects = Q()
        for field in fields:
            for keyword in keywords:
                q_objects = q_objects | Q(**{f'{field}__contains': keyword})

        return self.filter(q_objects)


class Lifemark(models.Model):
    title = models.TextField()
    link = models.TextField(blank=True, default='')
    category = models.TextField(blank=True, default='')
    state = models.TextField(blank=True, default='')
    due_datehour = models.TextField(blank=True, default='')
    rating = models.TextField(blank=True, default='')
    tags = models.TextField(blank=True, default='')
    desc = models.TextField(blank=True, default='')
    image_url = models.TextField(blank=True, default='')
    cdate = models.DateTimeField(auto_now_add=True)
    udate = models.DateTimeField(auto_now=True)

    objects = LifemarkManager()

    def __str__(self):
        return f'Lifemark: "{self.id}: {self.title}"'


class TestModel(models.Model):
    title = models.TextField(default=None, null=True)
    category = models.TextField(default='', null=True)
    state = models.TextField(null=True)
    cdate = models.DateTimeField(auto_now_add=True)
