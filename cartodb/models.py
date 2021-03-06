from django.db import models
import urllib2
import urllib
# Create your models here.

class cartodb:
  api_key = 'a02e34100685bd3fb2edc93fe0f58fdbc7d50715'
  domain_name = 'xabel'

  def __init__(self, domain_name):
    self.domain_name = domain_name

  def urlRoot(self):
    return 'http://' + self.domain_name + '.cartodb.com/api/v2/sql?api_key='+ self.api_key+'&q='

  def parseSQL(self):
    self.params.reverse()
    db = self.params.pop()
    sql = ''
    if db['type'] == 'SELECT':
      sql = self.parseSELECT(db["value"])
    elif db['type'] == 'INSERT':
      sql = self.parseINSERT(db["value"])

    self.params = []
    return sql

  def parseINSERT(self, db_name):
    sql = 'INSERT INTO ' + db_name
    while len(self.params) > 0:
      fields = self.params.pop()
      col_names = []
      col_values = []
      for key in fields['column']:
        col_names.append(key)
        col_values.append(fields['column'][key])
      sql = sql + ' ("' + '","'.join(col_names) + '")'
      sql = sql + ' VALUES '
      sql = sql + ' (\'' + '\',\''.join(col_values) + '\')'
      sql = sql + ';'
    return sql

  def parseSELECT(self, db_name):

    sql = 'SELECT * FROM ' + db_name
    sql_params = []
    while len(self.params) > 0:
      sql_params.append(self.extractParam())
    if len(sql_params) > 0:
      sql = sql + ' WHERE ' + ' AND '.join(sql_params)
    return sql

  def extractParam(self):
    if len(self.params) > 0:
      param1 = self.params.pop()
      if param1["name"] == 'field':
        value = self.params.pop()
        if value["name"] != "comp":
          return ''
          # should throw and exception
        else:
          if value["type"] == 'is':
            return param1["value"] + " ilike '%" + value["value"] + "%'"
    return ''


  def at(self, db_name):
    self.params = [{"name":"db_name", "type": "SELECT", "value": db_name}]
    return self

  def to(self, db_name):
    self.params = [{"name":"db_name", "type": "INSERT", "value": db_name}]
    return self

  def add(self, col):
    self.params.append({"name":"column", "column": col})
    return self

  def open(self):
    return self._get(self.parseSQL())

  def field(self, value):
    self.params.append({"name":"field", "value":value})
    return self

  def has(self, value):
    self.params.append({"name":"comp", "type": "is", "value": value})
    return self

  def bigger(self, value):
    self.params.append({"name":"comp", "type": "big", "value": value})
    return self

  def _get(self, sql):
    print self.urlRoot() + sql
    fetcher = urllib2.urlopen(self.urlRoot() + urllib.quote_plus(sql))
    result = fetcher.read()
    return result
