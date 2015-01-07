# -*- coding: utf-8 -*-
import datetime
import json

import pytest

from optimo import (
    WorkShift,
    OptimoAPI,
    Driver,
    Order,
    RoutePlan,
    OptimoError,
)
from optimo.util import OptimoEncoder, validate_url

from tests.schema.v1 import RoutePlanValidator


@pytest.fixture(scope='module')
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


def test_validate_scheme():
    with pytest.raises(OptimoError) as excinfo:
        validate_url('some.url.com')

    assert str(excinfo.value) == ("The url: 'some.url.com' does not define a "
                                  "protocol scheme")


class TestOptimoAPIConfiguration(object):
    def test_optimoapi_instatiation(self):
        optimo_apiv1 = OptimoAPI('https://foo.bar.com', 'foobarkey')
        assert optimo_apiv1.optimo_url == 'https://foo.bar.com'
        assert optimo_apiv1.access_key == 'foobarkey'
        assert optimo_apiv1.version == 'v1'

        optimo_apiv2 = OptimoAPI('https://foo.bar.com', 'foobarkey', version='v2')
        assert optimo_apiv2.version == 'v2'

    def test_optimoapi_url(self):
        with pytest.raises(OptimoError) as excinfo:
            OptimoAPI('', 'foobarkey')
        assert str(excinfo.value) == "'optimo_url' must be a url string"

        with pytest.raises(OptimoError) as excinfo:
            OptimoAPI(None, 'foobarkey')
        assert str(excinfo.value) == "'optimo_url' must be a url string"

        with pytest.raises(OptimoError) as excinfo:
            OptimoAPI(3, 'foobarkey')
        assert str(excinfo.value) == "'optimo_url' must be a url string"

        # omit the 'https'
        optimo_apiv1 = OptimoAPI('https://foo.bar.com', 'foobarkey')
        assert optimo_apiv1.optimo_url == 'https://foo.bar.com'

    def test_optimoapi_version(self):
        VERSION_ERROR_MSG = "'version' must be a string denoting the API " \
                            "version you want to use('v1', 'v2', etc"
        with pytest.raises(OptimoError) as excinfo:
            OptimoAPI('http://foo.bar.com', 'foobarkey', version=0)
        assert str(excinfo.value) == VERSION_ERROR_MSG

        with pytest.raises(OptimoError) as excinfo:
            OptimoAPI('http://foo.bar.com', 'foobarkey', version='')
        assert str(excinfo.value) == VERSION_ERROR_MSG

        with pytest.raises(OptimoError) as excinfo:
            OptimoAPI('http://foo.bar.com', 'foobarkey', version=2.0)
        assert str(excinfo.value) == VERSION_ERROR_MSG

        with pytest.raises(OptimoError) as excinfo:
            OptimoAPI('http://foo.bar.com', 'foobarkey', version='s1')
        assert str(excinfo.value) == VERSION_ERROR_MSG

        optimo_api = OptimoAPI('http://foo.bar.com', 'foobarkey', version='v1')
        assert optimo_api.version == 'v1'

    def test_optimoapi_access_key(self):
        with pytest.raises(OptimoError) as excinfo:
            OptimoAPI('http://foo.bar.com', '')
        assert str(excinfo.value) == ("'access_key' must be the string access"
                                      " key provided to you by optimoroute")

        with pytest.raises(OptimoError) as excinfo:
            OptimoAPI('http://foo.bar.com', None)
        assert str(excinfo.value) == ("'access_key' must be the string access"
                                      " key provided to you by optimoroute")

        with pytest.raises(OptimoError) as excinfo:
            OptimoAPI('http://foo.bar.com', 432)
        assert str(excinfo.value) == ("'access_key' must be the string access"
                                      " key provided to you by optimoroute")


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


def test_unsuccessful_plan(optimo_api, route_plan):
    route_plan.request_id = '666'

    with pytest.raises(OptimoError) as excinfo:
        optimo_api.plan(route_plan)


def test_wrong_routeplan_type(optimo_api):
    with pytest.raises(TypeError):
        optimo_api.plan(5)


def test_successful_stop(optimo_api):
    assert optimo_api.stop('3421') is None


def test_unsuccessful_stop(optimo_api):
    with pytest.raises(OptimoError) as excinfo:
        optimo_api.stop('0000')

    assert "Request with the requestId specified" in str(excinfo.value)
    assert "was not found" in str(excinfo.value)
