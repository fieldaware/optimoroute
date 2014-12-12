# -*- coding: utf-8 -*-
import json
import datetime

from decimal import Decimal

from models import BaseModel


class CoreOptimoEncoder(json.JSONEncoder):
    """Custom JSON encoder that knows how to serialize ``datetime.datetime``
    and ``decimal.Decimal`` objects.
    """
    def default(self, o):
        if isinstance(o, datetime.datetime):
            return o.strftime('%Y-%m-%dT%H:%M')
        if isinstance(o, Decimal):
            return float(o)


class OptimoEncoder(CoreOptimoEncoder):
    """Custom JSON encoder that knows how to serialize
    :class:`optimo.models.BaseModel <BaseModel>` objects.
    """
    def default(self, o):
        if isinstance(o, BaseModel):
            return o.as_optimo_schema()
        return super(OptimoEncoder, self).default(o)