# OptimoRoute Python library

This is a python library for [OptimoRoute][optimoroute.com]'s web service.

---

**Note**: This is not yet intended for production usage. It is currently in Pre-Alpha development status. Use at your own risk.
 
---

# Requirements

* Python (has only been tested with python 2.7.*)
* An access key provided to you by [OptimoRoute][optimoroute.com]

# Installation

Installation using `pip`:

    pip install optimoroute

# Usage

```python
import datetime
from decimal import Decimal
from optimoroute.api import OptimoAPI


d1 = datetime.datetime(year=2014, month=12, day=5, hour=8, minute=0)
d2 = datetime.datetime(year=2014, month=12, day=5, hour=14, minute=0)
ws = WorkShift(work_from=d1, work_to=d2)

drv = Driver(
    id='123', 
    start_lat=Decimal('53.350046'), 
    start_lng=Decimal('-6.274655'), 
    end_lat=Decimal('53.341191'), 
    end_lng=Decimal('-6.260402')
)
drv.work_shifts.append(ws)

order1 = Order(
    id='123', 
    lat=Decimal('53.343204'), 
    lng=Decimal('-6.269798'), 
    duration=20
)

order2 = Order(
    id='456', 
    lat=Decimal('53.341820'), 
    lng=Decimal('-6.264991'), 
    duration=25
)

# The 'request_id' is the one we'll use later to check the results of the 
# plan optimization.
routeplan = RoutePlan(
    request_id='1234',
    callback_url='https://callback.com/1234',
    status_callback_url='https://status.callback.com/1234'
)
routeplan.drivers.append(drv)
routeplan.orders.append(order1)
routeplan.orders.append(order2)

optimo_api = OptimoAPI('https://api.optimoroute.com', 'v1', 'some_access_key')

# Start the plan optimization.
resp = optimo_api.plan(routeplan)
# We can check if the request was successful
resp.is_success

# Get the result of the optimization. We use the 'request_id' we provided to
# optimoroute previously.
resp = optimo_api.get('1234')

# If the optimization has finished we can see the result.
resp.data
# output
{
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

# We can stop an already running optimization
resp = optimo_api.stop('1234')
resp.is_success
```


# Todo

* Provide 100% test coverage
* Add docstrings to every function/class.


[optimoroute.com]: http://optimoroute.com
