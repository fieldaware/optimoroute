# -*- coding: utf-8 -*-
import json
import datetime

from decimal import Decimal

from models import BaseModel


class CoreOptimoEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, datetime.datetime):
            return o.strftime('%Y-%m-%dT%H:%M')
        if isinstance(o, Decimal):
            return float(o)
        return super(CoreOptimoEncoder, self).default(o)


class OptimoEncoder(CoreOptimoEncoder):
    def default(self, o):
        if isinstance(o, BaseModel):
            return o.as_optimo_schema()
        return super(OptimoEncoder, self).default(o)