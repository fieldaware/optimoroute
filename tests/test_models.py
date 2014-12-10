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
    TimeWindow
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
    TimeWindowValidator
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
    assert ws.validate() is None
    assert jsonify(ws) == '{"workTimeFrom": "2014-12-05T08:00", "break": ' \
                          '{"breakStartTo": "2014-12-05T08:00", ' \
                          '"breakStartFrom": "2014-12-05T08:00", ' \
                          '"breakDuration": 5}, ' \
                          '"workTimeTo": "2014-12-05T08:00", ' \
                          '"allowedOvertime": 2}'

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

    order = Order('3', 5.2, 6.1, 7)
    with pytest.raises(TypeError) as excinfo:
        order.validate()
    err_msg = TYPE_ERR_MSG.format(cls_name, 'duration', 'int')
    assert err_msg == str(excinfo.value)
