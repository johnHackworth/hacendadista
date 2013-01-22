from django.db import models
import urllib2

# Create your models here.

class idealista:
  api_key = '2a4b958a8173cd12f9428a16c82a083c'
  radius = '1000'
  def url(self, center):
    return "http://www.idealista.com/labs/propertyMap.htm?action=json&operation=A&distance=" + self.radius +"&center=" + center + "&k=" + self.api_key

  def get(self, center):
    fetcher = urllib2.urlopen(self.url(center))
    result = fetcher.read()
    return result
