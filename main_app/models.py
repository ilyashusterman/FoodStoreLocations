import jsonpickle
import json
from django.db import models


class Chains(models.Model):
    name = models.CharField(max_length=100)


class Branches(models.Model):
    name = models.CharField(max_length=100)
    chain = models.ForeignKey(Chains)
    longitude = models.FloatField(max_length=100)
    latitude = models.FloatField(max_length=100)

    def __str__(self):
        return jsonpickle.encode({'name': self.name,
                                  'chain_name': self.chain_id,
                                  'longitude': self.longitude,
                                  'latitude': self.latitude
                                  })