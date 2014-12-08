# -*- coding: utf-8 -*-
from optimoroute.core.util import CoreOptimoEncoder
from optimoroute.api.entities import BaseModel


class OptimoEncoder(CoreOptimoEncoder):
    def default(self, o):
        if isinstance(o, BaseModel):
            return o.as_optimo_schema()
        return super(OptimoEncoder, self).default(o)
