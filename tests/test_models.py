# -*- coding: utf-8 -*-
from datetime import datetime
import pytest

from optimo import WorkShift, Driver, Order, RoutePlan, Break


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

    assert brk.as_optimo_schema() == {
        'breakStartFrom': dt,
        'breakStartTo': dt,
        'breakDuration': 5
    }


def test_workshift():
    cls_name = WorkShift.__name__

    ws = WorkShift(3, 4)

    with pytest.raises(TypeError) as excinfo:
        ws.validate()

    err_msg = TYPE_ERR_MSG.format(
        cls_name,
        'start_work',
        'datetime.datetime'
    )
    assert err_msg == str(excinfo.value)

    dt = datetime(year=2014, month=12, day=5, hour=8, minute=0)
    ws = WorkShift(dt, 3)

    with pytest.raises(TypeError) as excinfo:
        ws.validate()

    err_msg = TYPE_ERR_MSG.format(
        cls_name,
        'end_work',
        'datetime.datetime'
    )
    assert err_msg == str(excinfo.value)

    ws = WorkShift(dt, dt)
    ws.allowed_overtime = 2.5
    with pytest.raises(TypeError) as excinfo:
        ws.validate()

    err_msg = TYPE_ERR_MSG.format(
        cls_name,
        'allowed_overtime',
        'int'
    )
    assert err_msg == str(excinfo.value)

    ws = WorkShift(dt, dt)
    ws.allowed_overtime = 2
    ws.break_ = 42

    with pytest.raises(TypeError) as excinfo:
        ws.validate()

    err_msg = TYPE_ERR_MSG.format(
        cls_name,
        'break_',
        'Break'
    )
    assert err_msg == str(excinfo.value)

    ws = WorkShift(dt, dt)
    ws.allowed_overtime = 2
    ws.break_ = Break(dt, dt, 5)

    assert ws.validate() is None
