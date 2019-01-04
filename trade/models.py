import json
import numpy

from django.db import models

# Create your models here.


class RequestedAlgoData(models.Model):
    """
    Model for store requested algo data
    """
    name = models.CharField(max_length=255)
    ticker = models.CharField(max_length=255)
    pnl = models.TextField()
    positions = models.TextField()

    def _get_text_field_as_json(self, values):
        return json.loads(values)

    def get_pnl_as_python(self):
        return self._get_text_field_as_json(self.pnl)

    def get_positions_as_python(self):
        return self._get_text_field_as_json(self.positions)

    @property
    def avg_pnl(self):
        return numpy.mean(self.get_pnl_as_python())
