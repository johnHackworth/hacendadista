from django.db import models
from datetime import datetime, timedelta
import pytz

class PointOfInterest(models.Model):
  cartodb_id = models.IntegerField()
  street = models.CharField(max_length=255, default='', null=True)
  pc = models.CharField(max_length=10, default='', null=True)
  the_geom = models.CharField(max_length=255, default='', null=True)
  the_geom_webmercator = models.CharField(max_length=255, default='', null=True)
  tlf = models.CharField(max_length=12, default='', null=True)
  created_at = models.CharField(max_length=28, default='', null=True)
  updated_at = models.CharField(max_length=28, default='', null=True)
  cartodb_georef_status = models.BooleanField(default=False)
  lastFetched = models.DateTimeField(default=(datetime.now(pytz.utc)- timedelta(2)), null=True)
