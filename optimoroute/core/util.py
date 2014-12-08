# -*- coding: utf-8 -*-
import datetime
from decimal import Decimal
import json


class CoreOptimoEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, datetime.datetime):
            return o.strftime('%Y-%m-%dT%H:%M')
        if isinstance(o, Decimal):
            return float(o)
        return super(CoreOptimoEncoder, self).default(o)
