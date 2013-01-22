from models import PointOfInterest
from vendors.pyCartoDb.cartodb import Cartodb
from vendors.pyCartoDb.cartodb_object import CartoDb_object

class PoI_service():
  user_name = 'xabel'
  db_name = 'mercadona'

  def __init__(self):
    self.cartodb = Cartodb(self.user_name)

  def fetch_points(self):
    return self.cartodb.at(self.db_name).open()

  def sync(self):
    carto_pois = self.fetch_points()
    for carto_poi in carto_pois:
      if len(PointOfInterest.objects.filter(cartodb_id=carto_poi.get('cartodb_id'))) == 0:
        if carto_poi.get('cartodb_georef_status') is None:
          carto_poi.set('cartodb_georef_status', False)
        new_point = PointOfInterest(**carto_poi.attributes)
        new_point.save()

    for django_poi in PointOfInterest.objects.all():
      if not self.has_cartodb_id(carto_pois, django_poi.cartodb_id):
        django_poi.delete()

  def has_cartodb_id(self, carto_pois, cartodb_id):
    for carto_poi in carto_pois:
      if carto_poi.get('cartodb_id') == cartodb_id:
        return True
    return False
