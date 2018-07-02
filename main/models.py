from django.db import models


class Lifemark(models.Model):
    title = models.TextField(default='')
