from django.db import models
from django.db.models import Q


class LifemarkManager(models.Manager):
    def get_any_matches_on_any_fields(self, fields, category, keywords_str):
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

    def get_all_matches_on_any_fields(self, fields, category, keywords_str):
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
            for keyword in keywords:
                q_keyword = Q()
                for field in fields:
                    q_keyword = q_keyword | Q(**{f'{field}__contains': keyword})
                q_objects = q_objects & q_keyword

        return qs.filter(q_objects)

    def get_dued_lifemarks(self, datehour):
        """
        'dued' means expiration date tomorrow
        compare to curr datehour + 1day
        """
        qs = self.filter(state='todo')
        return qs.extra(where=[f"to_timestamp(due_datehour, 'YYYY-MM-DD HH24') <= to_timestamp('{datehour}', 'YYYY-MM-DD HH24') + interval '1 day'"])

    def get_hourly_dued_lifemarks(self, datehour):
        """
        'hourly dued' means expiration 1hour later
        compare to curr datehour + 1hour
        ignore 00hour items: ruled by view logic
        """
        qs = self.filter(state='todo')
        return qs.extra(where=[f"extract(hour from to_timestamp(due_datehour, 'YYYY-MM-DD HH24')) != 0 and to_timestamp(due_datehour, 'YYYY-MM-DD HH24') <= to_timestamp('{datehour}', 'YYYY-MM-DD HH24') + interval '1 hour'"])


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
