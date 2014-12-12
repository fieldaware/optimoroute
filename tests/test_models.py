# -*- coding: utf-8 -*-
import json
import pytest
from datetime import datetime

from optimo import (
    WorkShift,
    Driver,
    Order,
    RoutePlan,
    Break,
    SchedulingInfo,
    TimeWindow,
    UnavailableTime,
)
from optimo.util import OptimoEncoder

from tests.schema.v1 import (
    BreakValidator,
    DriverValidator,
    OrderValidator,
    RoutePlanValidator,
    UnavailableTimeValidator,
    WorkShiftValidator,
    SchedulingInfoValidator,
    TimeWindowValidator,
)


jsonify = lambda o: json.dumps(o, cls=OptimoEncoder)
dictify = lambda o: json.loads(jsonify(o))

TYPE_ERR_MSG = "'{}.{}' must be of type {}"


def test_break():
    dt = datetime(year=2014, month=12, day=5, hour=8, minute=0)
    cls_name = Break.__name__

    brk = Break(3, 4, 5)
    with pytest.raises(TypeError) as excinfo:
        brk.validate()
    err_msg = TYPE_ERR_MSG.format(cls_name, 'start_break', 'datetime.datetime')
    assert err_msg == str(excinfo.value)

    brk = Break(dt, 4, 5)
    with pytest.raises(TypeError) as excinfo:
        brk.validate()
    err_msg = TYPE_ERR_MSG.format(cls_name, 'end_break', 'datetime.datetime')
    assert err_msg == str(excinfo.value)

    brk = Break(dt, dt, 5.5)
    with pytest.raises(TypeError) as excinfo:
        brk.validate()
    err_msg = TYPE_ERR_MSG.format(cls_name, 'duration', 'int')
    assert err_msg == str(excinfo.value)

    brk = Break(dt, dt, 5)
    assert brk.validate() is None

    assert jsonify(brk) == '{"breakStartTo": "2014-12-05T08:00", ' \
                           '"breakStartFrom": "2014-12-05T08:00", ' \
                           '"breakDuration": 5}'

    assert BreakValidator.validate(dictify(brk)) is None


def test_workshift():
    cls_name = WorkShift.__name__

    ws = WorkShift(3, 4)
    with pytest.raises(TypeError) as excinfo:
        ws.validate()
    err_msg = TYPE_ERR_MSG.format(cls_name, 'start_work', 'datetime.datetime')
    assert err_msg == str(excinfo.value)

    dt = datetime(year=2014, month=12, day=5, hour=8, minute=0)
    ws = WorkShift(dt, 3)
    with pytest.raises(TypeError) as excinfo:
        ws.validate()
    err_msg = TYPE_ERR_MSG.format(cls_name, 'end_work', 'datetime.datetime')
    assert err_msg == str(excinfo.value)

    ws = WorkShift(dt, dt)
    ws.allowed_overtime = 2.5
    with pytest.raises(TypeError) as excinfo:
        ws.validate()
    err_msg = TYPE_ERR_MSG.format(cls_name, 'allowed_overtime', 'int')
    assert err_msg == str(excinfo.value)

    ws = WorkShift(dt, dt)
    ws.allowed_overtime = 2
    ws.break_ = 42
    with pytest.raises(TypeError) as excinfo:
        ws.validate()
    err_msg = TYPE_ERR_MSG.format(cls_name, 'break_', 'Break')
    assert err_msg == str(excinfo.value)

    ws = WorkShift(dt, dt)
    ws.allowed_overtime = 2
    ws.break_ = Break(dt, dt, 5)
    ws.unavailable_times = 3
    with pytest.raises(TypeError) as excinfo:
        ws.validate()
    err_msg = TYPE_ERR_MSG.format(cls_name, 'unavailable_times', 'list')
    assert err_msg == str(excinfo.value)

    ws = WorkShift(dt, dt)
    ws.allowed_overtime = 2
    ws.break_ = Break(dt, dt, 5)
    ws.unavailable_times = [3]
    with pytest.raises(TypeError) as excinfo:
        ws.validate()
    err_msg = "'{}.unavailable_times' must contain elements of type " \
              "UnavailableTime".format(cls_name)
    assert err_msg == str(excinfo.value)

    ws = WorkShift(dt, dt)
    ws.allowed_overtime = 2
    ws.break_ = Break(dt, dt, 5)
    ws.unavailable_times = [UnavailableTime(dt, dt)]
    assert ws.validate() is None
    assert jsonify(ws) == '{"workTimeFrom": "2014-12-05T08:00", ' \
                          '"break": {"breakStartTo": "2014-12-05T08:00", ' \
                          '"breakStartFrom": "2014-12-05T08:00", ' \
                          '"breakDuration": 5}, "unavailableTimes": ' \
                          '[{"timeFrom": "2014-12-05T08:00", "timeTo": ' \
                          '"2014-12-05T08:00"}], "workTimeTo": ' \
                          '"2014-12-05T08:00", "allowedOvertime": 2}'

    assert WorkShiftValidator.validate(dictify(ws)) is None


def test_scheduling_info():
    dt = datetime(year=2014, month=12, day=5, hour=8, minute=0)
    cls_name = SchedulingInfo.__name__

    si = SchedulingInfo(1, 1)
    with pytest.raises(TypeError) as excinfo:
        si.validate()
    err_msg = TYPE_ERR_MSG.format(cls_name, 'scheduled_at', 'datetime.datetime')
    assert err_msg == str(excinfo.value)

    si = SchedulingInfo(dt, 1)
    with pytest.raises(TypeError) as excinfo:
        si.validate()
    err_msg = TYPE_ERR_MSG.format(cls_name, 'scheduled_driver', 'str')
    assert err_msg == str(excinfo.value)

    si = SchedulingInfo(dt, 'bobos', locked=4)
    with pytest.raises(TypeError) as excinfo:
        si.validate()
    err_msg = TYPE_ERR_MSG.format(cls_name, 'locked', 'bool')
    assert err_msg == str(excinfo.value)

    si = SchedulingInfo(dt, 'bobos')
    assert si.validate() is None
    assert jsonify(si) == '{"scheduledAt": "2014-12-05T08:00", ' \
                          '"scheduledDriver": "bobos", "locked": false}'

    assert SchedulingInfoValidator.validate(dictify(si)) is None


def test_time_window():
    cls_name = TimeWindow.__name__
    dt = datetime(year=2014, month=12, day=5, hour=8, minute=0)

    tw = TimeWindow(2, 3)
    with pytest.raises(TypeError) as excinfo:
        tw.validate()
    err_msg = TYPE_ERR_MSG.format(cls_name, 'start_time', 'datetime.datetime')
    assert err_msg == str(excinfo.value)

    tw = TimeWindow(dt, 3)
    with pytest.raises(TypeError) as excinfo:
        tw.validate()
    err_msg = TYPE_ERR_MSG.format(cls_name, 'end_time', 'datetime.datetime')
    assert err_msg == str(excinfo.value)

    tw = TimeWindow(dt, dt)
    assert tw.validate() is None
    assert jsonify(tw) == '{"timeFrom": "2014-12-05T08:00", ' \
                          '"timeTo": "2014-12-05T08:00"}'

    assert TimeWindowValidator.validate(dictify(tw)) is None


def test_order():
    cls_name = Order.__name__

    order = Order(3, 5, 6, 7)
    with pytest.raises(TypeError) as excinfo:
        order.validate()
    err_msg = TYPE_ERR_MSG.format(cls_name, 'id', 'str')
    assert err_msg == str(excinfo.value)

    order = Order('', '5', '6', '7')
    with pytest.raises(ValueError) as excinfo:
        order.validate()
    err_msg = "'{}.{}' cannot be empty".format(cls_name, 'id')
    assert err_msg == str(excinfo.value)

    order = Order('3', '5', '6', '7')
    with pytest.raises(TypeError) as excinfo:
        order.validate()
    err_msg = TYPE_ERR_MSG.format(cls_name, 'lat', 'Number')
    assert err_msg == str(excinfo.value)

    order = Order('3', 5, '6', '7')
    with pytest.raises(TypeError) as excinfo:
        order.validate()
    err_msg = TYPE_ERR_MSG.format(cls_name, 'lng', 'Number')
    assert err_msg == str(excinfo.value)

    order = Order('3', 5, 6, '7')
    with pytest.raises(TypeError) as excinfo:
        order.validate()
    err_msg = TYPE_ERR_MSG.format(cls_name, 'duration', 'int')
    assert err_msg == str(excinfo.value)

    order = Order('3', 5, 6, -1)
    with pytest.raises(ValueError) as excinfo:
        order.validate()
    err_msg = "'{}.duration' cannot be negative".format(cls_name)
    assert err_msg == str(excinfo.value)

    order = Order('3', 5.2, 6.1, 7)
    order.time_window = 'Foo'
    with pytest.raises(TypeError) as excinfo:
        order.validate()
    err_msg = TYPE_ERR_MSG.format(cls_name, 'time_window', 'TimeWindow')
    assert err_msg == str(excinfo.value)

    dt = datetime(year=2014, month=12, day=5, hour=8, minute=0)
    order = Order('3', 5.2, 6.1, 7)
    order.time_window = TimeWindow(dt, dt)
    order.priority = 3
    with pytest.raises(TypeError) as excinfo:
        order.validate()
    err_msg = TYPE_ERR_MSG.format(cls_name, 'priority', 'str')
    assert err_msg == str(excinfo.value)

    order = Order('3', 5.2, 6.1, 7)
    order.time_window = TimeWindow(dt, dt)
    order.priority = 'F'
    with pytest.raises(ValueError) as excinfo:
        order.validate()
    err_msg = "'{}.{}' must be one of {}".format(cls_name, 'priority',
                                                 "('L', 'M', 'H', 'C')")
    assert err_msg == str(excinfo.value)

    order = Order('3', 5.2, 6.1, 7)
    order.time_window = TimeWindow(dt, dt)
    order.skills = 'handy'
    with pytest.raises(TypeError) as excinfo:
        order.validate()
    err_msg = TYPE_ERR_MSG.format(cls_name, 'skills', 'list')
    assert err_msg == str(excinfo.value)

    order = Order('3', 5.2, 6.1, 7)
    order.time_window = TimeWindow(dt, dt)
    order.skills = ['handy', 3]
    with pytest.raises(TypeError) as excinfo:
        order.validate()
    err_msg = "'{}.skills' must contain elements of type str".format(cls_name)
    assert err_msg == str(excinfo.value)

    order = Order('3', 5.2, 6.1, 7)
    order.time_window = TimeWindow(dt, dt)
    order.skills = ['handy', 'quiet']
    order.assigned_to = 4
    with pytest.raises(TypeError) as excinfo:
        order.validate()
    err_msg = TYPE_ERR_MSG.format(cls_name, 'assigned_to', 'str')
    assert err_msg == str(excinfo.value)

    order = Order('3', 5.2, 6.1, 7)
    order.time_window = TimeWindow(dt, dt)
    order.skills = ['handy', 'quiet']
    order.assigned_to = 'Tom & Jerry'
    order.scheduling_info = 45
    with pytest.raises(TypeError) as excinfo:
        order.validate()
    err_msg = TYPE_ERR_MSG.format(cls_name, 'scheduling_info', 'SchedulingInfo')
    assert err_msg == str(excinfo.value)

    order = Order('3', 5.2, 6.1, 7)
    order.time_window = TimeWindow(dt, dt)
    order.skills = ['handy', 'quiet']
    order.assigned_to = 'Tom & Jerry'
    order.scheduling_info = SchedulingInfo(dt, 'rantanplan')
    assert order.validate() is None
    assert jsonify(order) == '{"assignedTo": "Tom & Jerry", "skills": ' \
                             '["handy", "quiet"], "tw": {"timeFrom": ' \
                             '"2014-12-05T08:00", "timeTo": ' \
                             '"2014-12-05T08:00"}, "lon": 6.1, "priority": ' \
                             '"M", "duration": 7, "lat": 5.2, ' \
                             '"schedulingInfo": {"scheduledAt": ' \
                             '"2014-12-05T08:00", "scheduledDriver": ' \
                             '"rantanplan", "locked": false}, "id": "3"}'
    assert OrderValidator.validate(dictify(order)) is None


def test_unavailable_time():
    cls_name = UnavailableTime.__name__

    ut = UnavailableTime(1, 2)
    with pytest.raises(TypeError) as excinfo:
        ut.validate()
    err_msg = TYPE_ERR_MSG.format(cls_name, 'start_time', 'datetime.datetime')
    assert err_msg == str(excinfo.value)

    dt = datetime(year=2014, month=12, day=5, hour=8, minute=0)

    ut = UnavailableTime(dt, 2)
    with pytest.raises(TypeError) as excinfo:
        ut.validate()
    err_msg = TYPE_ERR_MSG.format(cls_name, 'end_time', 'datetime.datetime')
    assert err_msg == str(excinfo.value)

    ut = UnavailableTime(dt, dt)
    assert ut.validate() is None
    assert jsonify(ut) == '{"timeFrom": "2014-12-05T08:00", ' \
                          '"timeTo": "2014-12-05T08:00"}'
    assert UnavailableTimeValidator.validate(dictify(ut)) is None


def test_driver():
    cls_name = Driver.__name__

    drv = Driver(3, '3', '4', '4', '5')
    with pytest.raises(TypeError) as excinfo:
        drv.validate()
    err_msg = TYPE_ERR_MSG.format(cls_name, 'id', 'str')
    assert err_msg == str(excinfo.value)

    drv = Driver('', '3', '4', '4', '5')
    with pytest.raises(ValueError) as excinfo:
        drv.validate()
    err_msg = "'{}.id' cannot be empty".format(cls_name)
    assert err_msg == str(excinfo.value)

    drv = Driver('3', '3', '4', '4', '5')
    with pytest.raises(TypeError) as excinfo:
        drv.validate()
    err_msg = TYPE_ERR_MSG.format(cls_name, 'start_lat', 'Number')
    assert err_msg == str(excinfo.value)

    drv = Driver('3', 3, '4', '4', '5')
    with pytest.raises(TypeError) as excinfo:
        drv.validate()
    err_msg = TYPE_ERR_MSG.format(cls_name, 'start_lng', 'Number')
    assert err_msg == str(excinfo.value)

    drv = Driver('3', 3, 4, '4', '5')
    with pytest.raises(TypeError) as excinfo:
        drv.validate()
    err_msg = TYPE_ERR_MSG.format(cls_name, 'end_lat', 'Number')
    assert err_msg == str(excinfo.value)

    drv = Driver('3', 3, 4, 4, '5')
    with pytest.raises(TypeError) as excinfo:
        drv.validate()
    err_msg = TYPE_ERR_MSG.format(cls_name, 'end_lng', 'Number')
    assert err_msg == str(excinfo.value)

    drv = Driver('3', 3, 4, 4, 5)
    drv.work_shifts = 4
    with pytest.raises(TypeError) as excinfo:
        drv.validate()
    err_msg = TYPE_ERR_MSG.format(cls_name, 'work_shifts', 'list')
    assert err_msg == str(excinfo.value)

    dt = datetime(year=2014, month=12, day=5, hour=8, minute=0)

    drv = Driver('3', 3, 4, 4, 5)
    drv.work_shifts = []
    with pytest.raises(ValueError) as excinfo:
        drv.validate()
    err_msg = "'{}.work_shifts' must contain at least 1 element".\
        format(cls_name)
    assert err_msg == str(excinfo.value)

    drv = Driver('3', 3, 4, 4, 5)
    drv.work_shifts = [3]
    with pytest.raises(TypeError) as excinfo:
        drv.validate()
    err_msg = "'{}.work_shifts' must contain elements of type WorkShift".\
        format(cls_name)
    assert err_msg == str(excinfo.value)

    drv = Driver('3', 3, 4, 4, 5)
    drv.work_shifts = [WorkShift(dt, dt)]
    drv.skills = 3
    with pytest.raises(TypeError) as excinfo:
        drv.validate()
    err_msg = TYPE_ERR_MSG.format(cls_name, 'skills', 'list')
    assert err_msg == str(excinfo.value)

    drv = Driver('3', 3, 4, 4, 5)
    drv.work_shifts = [WorkShift(dt, dt)]
    drv.skills = [2]
    with pytest.raises(TypeError) as excinfo:
        drv.validate()
    err_msg = "'{}.skills' must contain elements of type str".format(cls_name)
    assert err_msg == str(excinfo.value)

    drv = Driver('3', 3, 4, 4, 5)
    drv.work_shifts = [WorkShift(dt, dt)]
    drv.skills = ['calm', 'angry']
    assert drv.validate() is None
    assert jsonify(drv) == '{"endLon": 5, "skills": ["calm", "angry"], ' \
                           '"endLat": 4, "startLat": 3, "workShifts": ' \
                           '[{"workTimeFrom": "2014-12-05T08:00", ' \
                           '"workTimeTo": "2014-12-05T08:00"}], ' \
                           '"startLon": 4, "id": "3"}'
    assert DriverValidator.validate(dictify(drv)) is None


@pytest.fixture
def orders():
    dt = datetime(year=2014, month=12, day=5, hour=8, minute=0)

    order1 = Order('3', 5.2, 6.1, 7)
    order1.time_window = TimeWindow(dt, dt)
    order1.skills = ['handy', 'quiet']
    order1.assigned_to = 'Tom & Jerry'
    order1.scheduling_info = SchedulingInfo(dt, 'rantanplan')

    order2 = Order('4', 5.2, 6.1, 7)
    order2.time_window = TimeWindow(dt, dt)
    order2.skills = ['barista', 'terrorista']
    order2.assigned_to = 'Sam & Max'
    order2.scheduling_info = SchedulingInfo(dt, 'rantanplan')
    return order1, order2


@pytest.fixture
def drivers():
    dt = datetime(year=2014, month=12, day=5, hour=8, minute=0)

    drv1 = Driver('3', 3, 4, 4, 5)
    drv1.work_shifts = [WorkShift(dt, dt)]
    drv1.skills = ['calm', 'angry']

    drv2 = Driver('4', 3, 4, 4, 5)
    drv2.work_shifts = [WorkShift(dt, dt)]
    drv2.skills = ['pirate', 'ninja']
    return drv1, drv2


def test_routeplan(orders, drivers):
    cls_name = RoutePlan.__name__

    routeplan = RoutePlan(1234, 4, 4)
    with pytest.raises(TypeError) as excinfo:
        routeplan.validate()
    err_msg = TYPE_ERR_MSG.format(cls_name, 'request_id', 'str')
    assert err_msg == str(excinfo.value)

    routeplan = RoutePlan('', 4, 4)
    with pytest.raises(ValueError) as excinfo:
        routeplan.validate()
    err_msg = "'{}.request_id' cannot be an empty string".format(cls_name)
    assert err_msg == str(excinfo.value)

    routeplan = RoutePlan('1234', 4, 4)
    with pytest.raises(TypeError) as excinfo:
        routeplan.validate()
    err_msg = TYPE_ERR_MSG.format(cls_name, 'callback_url', 'str')
    assert err_msg == str(excinfo.value)

    routeplan = RoutePlan('1234', 'someurl', 4)
    with pytest.raises(TypeError) as excinfo:
        routeplan.validate()
    err_msg = TYPE_ERR_MSG.format(cls_name, 'status_callback_url', 'str')
    assert err_msg == str(excinfo.value)

    routeplan = RoutePlan('1234', 'someurl', 'somestatusurl')
    routeplan.orders = 4
    with pytest.raises(TypeError) as excinfo:
        routeplan.validate()
    err_msg = TYPE_ERR_MSG.format(cls_name, 'orders', 'list')
    assert err_msg == str(excinfo.value)

    routeplan = RoutePlan('1234', 'someurl', 'somestatusurl')
    routeplan.orders = []
    with pytest.raises(ValueError) as excinfo:
        routeplan.validate()
    err_msg = "'{}.orders' must have at least 1 element".format(cls_name)
    assert err_msg == str(excinfo.value)

    routeplan = RoutePlan('1234', 'someurl', 'somestatusurl')
    routeplan.orders = [3]
    with pytest.raises(TypeError) as excinfo:
        routeplan.validate()
    err_msg = "'{}.orders' must contain elements of type Order".format(cls_name)
    assert err_msg == str(excinfo.value)

    routeplan = RoutePlan('1234', 'someurl', 'somestatusurl')
    routeplan.orders = list(orders)
    routeplan.drivers = 3
    with pytest.raises(TypeError) as excinfo:
        routeplan.validate()
    err_msg = TYPE_ERR_MSG.format(cls_name, 'drivers', 'list')
    assert err_msg == str(excinfo.value)

    routeplan = RoutePlan('1234', 'someurl', 'somestatusurl')
    routeplan.orders = list(orders)
    routeplan.drivers = []
    with pytest.raises(ValueError) as excinfo:
        routeplan.validate()
    err_msg = "'{}.drivers' must have at least 1 element".format(cls_name)
    assert err_msg == str(excinfo.value)

    routeplan = RoutePlan('1234', 'someurl', 'somestatusurl')
    routeplan.orders = list(orders)
    routeplan.drivers = [3]
    with pytest.raises(TypeError) as excinfo:
        routeplan.validate()
    err_msg = "'{}.drivers' must contain elements of type Driver".\
        format(cls_name)
    assert err_msg == str(excinfo.value)

    routeplan = RoutePlan('1234', 'someurl', 'somestatusurl')
    routeplan.orders = list(orders)
    routeplan.drivers = list(drivers)
    routeplan.no_load_capacities = 'HA'
    with pytest.raises(TypeError) as excinfo:
        routeplan.validate()
    err_msg = TYPE_ERR_MSG.format(cls_name, 'no_load_capacities', 'int')
    assert err_msg == str(excinfo.value)

    routeplan = RoutePlan('1234', 'someurl', 'somestatusurl')
    routeplan.orders = list(orders)
    routeplan.drivers = list(drivers)
    routeplan.no_load_capacities = 5
    with pytest.raises(ValueError) as excinfo:
        routeplan.validate()
    err_msg = "'{}.no_load_capacities' must be between 0-4".format(cls_name)
    assert err_msg == str(excinfo.value)

    routeplan = RoutePlan('1234', 'someurl', 'somestatusurl')
    routeplan.orders = list(orders)
    routeplan.drivers = list(drivers)
    routeplan.no_load_capacities = 3
    assert routeplan.validate() is None
    assert jsonify(routeplan) == \
        '{"noLoadCapacities": 3, "statusCallback": "somestatusurl", ' \
        '"drivers": [{"endLon": 5, "skills": ["calm", "angry"], "endLat": 4, ' \
        '"startLat": 3, "workShifts": [{"workTimeFrom": "2014-12-05T08:00", ' \
        '"workTimeTo": "2014-12-05T08:00"}], "startLon": 4, "id": "3"}, ' \
        '{"endLon": 5, "skills": ["pirate", "ninja"], "endLat": 4, ' \
        '"startLat": 3, "workShifts": [{"workTimeFrom": "2014-12-05T08:00", ' \
        '"workTimeTo": "2014-12-05T08:00"}], "startLon": 4, "id": "4"}], ' \
        '"callback": "someurl", "requestId": "1234", "orders": ' \
        '[{"assignedTo": "Tom & Jerry", "skills": ["handy", "quiet"], "tw": ' \
        '{"timeFrom": "2014-12-05T08:00", "timeTo": "2014-12-05T08:00"}, ' \
        '"lon": 6.1, "priority": "M", "duration": 7, "lat": 5.2, ' \
        '"schedulingInfo": {"scheduledAt": "2014-12-05T08:00", ' \
        '"scheduledDriver": "rantanplan", "locked": false}, "id": "3"}, ' \
        '{"assignedTo": "Sam & Max", "skills": ["barista", "terrorista"], ' \
        '"tw": {"timeFrom": "2014-12-05T08:00", "timeTo": ' \
        '"2014-12-05T08:00"}, "lon": 6.1, "priority": "M", "duration": 7, ' \
        '"lat": 5.2, "schedulingInfo": {"scheduledAt": "2014-12-05T08:00", ' \
        '"scheduledDriver": "rantanplan", "locked": false}, "id": "4"}]}'
    assert RoutePlanValidator.validate(dictify(routeplan)) is None