from django.db import models
from datetime import datetime, timedelta
import pytz

class House(models.Model):
  street = models.CharField(max_length=255, default='')
  lastFetched = models.DateTimeField(default=(datetime.now(pytz.utc)- timedelta(2)))
