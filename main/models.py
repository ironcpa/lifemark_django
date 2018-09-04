from django.db import models
from django.db.models import Q


class LifemarkManager(models.Manager):
    def get_matches_on_fields(self, fields, category, keywords_str):
        if keywords_str:
            keywords = keywords_str.split(' ')
        else:
            keywords = ''

        if category:
            qs = self.filter(category=category)
        else:
            qs = self.all()

        q_objects = Q()
        if keywords:
            for field in fields:
                for keyword in keywords:
                    q_objects = q_objects | Q(**{f'{field}__contains': keyword})

        return qs.filter(q_objects)


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
    c_geo_lat = models.DecimalField(max_digits=9, decimal_places=6, blank=True, null=True)
    c_geo_lon = models.DecimalField(max_digits=9, decimal_places=6, blank=True, null=True)
    u_geo_lat = models.DecimalField(max_digits=9, decimal_places=6, blank=True, null=True)
    u_geo_lon = models.DecimalField(max_digits=9, decimal_places=6, blank=True, null=True)

    objects = LifemarkManager()

    def __str__(self):
        return f'Lifemark: "{self.id}: {self.title}"'


class TestModel(models.Model):
    title = models.TextField(default=None, null=True)
    category = models.TextField(default='', null=True)
    state = models.TextField(null=True)
    cdate = models.DateTimeField(auto_now_add=True)
