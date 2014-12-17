# -*- coding: utf-8 -*-
import datetime
import json
from decimal import Decimal

from optimo.util import CoreOptimoEncoder


def test_coreoptimoencoder():
    dt = datetime.datetime(year=2014, month=12, day=5, hour=8, minute=0)
    dec = Decimal('4.5')

    d = {'datetime': dt, 'a_decimal': dec, 'integer': 5}
    assert json.dumps(d, cls=CoreOptimoEncoder) == \
        '{"a_decimal": 4.5, "integer": 5, "datetime": "2014-12-05T08:00"}'
