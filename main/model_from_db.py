# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from __future__ import unicode_literals

from django.db import models


class Lifemark(models.Model):
    key = models.AutoField(primary_key=True)
    title = models.CharField(max_length=100, blank=True, null=True)
    link = models.CharField(max_length=500, blank=True, null=True)
    descr = models.CharField(max_length=5000, blank=True, null=True)
    img_link = models.CharField(max_length=500, blank=True, null=True)
    category = models.CharField(max_length=20, blank=True, null=True)
    tags = models.CharField(max_length=100, blank=True, null=True)
    cdate = models.DateTimeField(blank=True, null=True)
    udate = models.DateTimeField(blank=True, null=True)
    ddate = models.DateTimeField(blank=True, null=True)
    geo_lat = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    geo_lon = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    is_complete = models.NullBooleanField()
    state = models.CharField(max_length=20, blank=True, null=True)
    u_geo_lat = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    u_geo_lon = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    due_date = models.DateTimeField(blank=True, null=True)
    rating = models.CharField(max_length=5, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'lifemark'
