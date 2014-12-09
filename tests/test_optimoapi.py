# -*- coding: utf-8 -*-
import datetime
import json

import pytest

from tests.schema.v1 import RoutePlanValidator
from optimo import (
    WorkShift,
    OptimoAPI,
    Driver,
    Order,
    RoutePlan,
    OptimoError
)
from optimo.util import OptimoEncoder


@pytest.fixture
def optimo_api():
    return OptimoAPI('https://foo.bar.com', 'foobarkey')


@pytest.fixture
def route_plan():
    from decimal import Decimal

    d1 = datetime.datetime(year=2014, month=12, day=5, hour=8, minute=0)
    d2 = datetime.datetime(year=2014, month=12, day=5, hour=14, minute=0)
    ws = WorkShift(d1, d2)

    drv = Driver('123', Decimal('53.350046'), Decimal('-6.274655'), Decimal('53.341191'), Decimal('-6.260402'))
    drv.work_shifts.append(ws)

    order1 = Order('123', Decimal('53.343204'), Decimal('-6.269798'), 20)
    order2 = Order('456', Decimal('53.341820'), Decimal('-6.264991'), 25)

    routeplan = RoutePlan(
        request_id='4321',
        callback_url='https://callback.com/1234',
        status_callback_url='https://status.callback.com/1234'
    )
    routeplan.drivers.append(drv)
    routeplan.orders.append(order1)
    routeplan.orders.append(order2)
    return routeplan


def test_optimoapi_instantiation():
    optimo_apiv1 = OptimoAPI('https://foo.bar.com', 'foobarkey')
    assert optimo_apiv1.optimo_url == 'https://foo.bar.com'
    assert optimo_apiv1.access_key == 'foobarkey'
    assert optimo_apiv1.version == 'v1'

    optimo_apiv2 = OptimoAPI('https://foo.bar.com', 'foobarkey', version='v2')
    assert optimo_apiv2.version == 'v2'


def test_successful_get(optimo_api):
    data = optimo_api.get('1234')
    assert data == {
        u'creationTime': u'2014-12-04T17:01:52',
        u'requestId': u'1234',
        u'result': {
            u'routes': [
                {
                    u'driverId': u'123',
                    u'orders': [
                        {u'id': u'123', u'scheduledAt': u'2014-12-05T08:04'},
                        {u'id': u'456', u'scheduledAt': u'2014-12-05T08:27'}
                    ]
                }
            ],
            u'unservedOrders': []
        },
        u'success': True
    }


def test_unsuccessful_get(optimo_api):
    with pytest.raises(OptimoError) as excinfo:
        optimo_api.get('0000')

    assert "Request with the requestId specified" in str(excinfo.value)
    assert "was not found" in str(excinfo.value)


def test_unsuccessful_get_planning_in_progress(optimo_api):
    # When in progress we just return None instead of the results.
    assert optimo_api.get('0110') is None


def test_successful_plan(optimo_api, route_plan):
    assert route_plan.validate() is None
    # we need to do this because only the OptimoEncoder serializes correctly
    # to plain python dict.
    route_plan_dict = json.loads(json.dumps(route_plan, cls=OptimoEncoder))
    # check if OptimoRoute's JSON schema feels the same about its validity.
    assert RoutePlanValidator.validate(route_plan_dict) is None

    assert optimo_api.plan(route_plan) is None


def test_successful_stop(optimo_api):
    assert optimo_api.stop('3421') is None


def test_unsuccessful_stop(optimo_api):
    with pytest.raises(OptimoError) as excinfo:
        optimo_api.stop('0000')

    assert "Request with the requestId specified" in str(excinfo.value)
    assert "was not found" in str(excinfo.value)
