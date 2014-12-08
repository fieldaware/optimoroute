# -*- coding: utf-8 -*-
import datetime
from numbers import Number

from optimoroute.api.model import BaseModel


class SchedulingInfo(BaseModel):
    def __init__(self, scheduled_at, scheduled_driver, locked=False):
        self.scheduled_at = scheduled_at
        self.scheduled_driver = scheduled_driver
        self.locked = locked

    def validate(self):
        cls_name = self.__class__.__name__
        if not isinstance(self.scheduled_at, datetime.datetime):
            raise TypeError(
                "'{}.scheduled_at' must be of type datetime.datetime"
                .format(cls_name)
            )

        if not isinstance(self.scheduled_driver, basestring):
            raise TypeError(
                "'{}.scheduled_driver' must be of type str".format(cls_name)
            )

        if not isinstance(self.locked, bool):
            raise TypeError("'{}.locked' must be of type bool".format(cls_name))

    def as_optimo_schema(self):
        self.validate()
        return {
            'scheduledAt': self.scheduled_at,
            'scheduledDriver': self.scheduled_driver,
            'locked': self.locked
        }


class TimeWindow(BaseModel):
    def __init__(self, time_from, time_to):
        self.time_from = time_from
        self.time_to = time_to

    def validate(self):
        cls_name = self.__class__.__name__
        if not isinstance(self.time_from, datetime.datetime):
            raise TypeError(
                "'{}.time_from' must be of type datetime.datetime"
                .format(cls_name)
            )

        if not isinstance(self.time_to, datetime.datetime):
            raise TypeError(
                "'{}.time_to' must be of type datetime.datetime"
                .format(cls_name)
            )

    def as_optimo_schema(self):
        self.validate()
        return {
            'timeFrom': self.time_from,
            'timeTo': self.time_to
        }


class Order(BaseModel):
    def __init__(self, id, lat, lng, duration):
        self.id = id
        self.lat = lat
        self.lng = lng
        self.duration = duration
        # described as 'tw' in the JSON schema
        self.time_window = None
        # (M)edium is the default for the OptimoRoute service
        self.priority = 'M'
        self.skills = []
        self.assigned_to = None
        self.scheduling_info = None

    def validate(self):
        cls_name = self.__class__.__name__
        if not isinstance(self.id, basestring):
            raise TypeError("'{}.id' must be of type str".format(cls_name))
        if not self.id:
            raise ValueError("'{}.id' cannot be empty".format(cls_name))

        if not isinstance(self.lat, Number):
            raise TypeError("'{}.lat' must be a number".format(cls_name))
        if not isinstance(self.lng, Number):
            raise TypeError("'{}.lng' must be a number".format(cls_name))

        if not isinstance(self.duration, (int, long)):
            raise TypeError("'{}.duration' must be of type int".format(cls_name))
        if self.duration < 0:
            raise ValueError("'{}.duration' cannot be negative".format(cls_name))

        if self.time_window is not None:
            if not isinstance(self.time_window, TimeWindow):
                raise TypeError(
                    "'{}.time_window' must be of type {!r}"
                    .format(cls_name, TimeWindow)
                )

        if not isinstance(self.priority, basestring):
            raise TypeError(
                "'{}.priority' must be of type str".format(cls_name)
            )
        if self.priority not in ('L', 'M', 'H', 'C'):
            raise ValueError(
                "'{}'.priority must be one of ('L', 'M', 'H', 'C')"
                .format(cls_name)
            )

    def as_optimo_schema(self):
        self.validate()
        d = {
            'id': self.id,
            'lat': self.lat,
            'lon': self.lng,
            'duration': self.duration,
            'priority': self.priority,
        }

        if self.time_window:
            d['tw'] = self.time_window

        if self.skills:
            d['skills'] = self.skills

        if self.assigned_to:
            d['assignedTo'] = self.assigned_to

        if self.scheduling_info:
            d['schedulingInfo'] = self.scheduling_info

        return d


class Break(BaseModel):

    def __init__(self, start_from, start_to, duration):
        self.start_from = start_from
        self.start_to = start_to
        self.duration = duration

    def validate(self):
        cls_name = self.__class__.__name__
        if not isinstance(self.start_from, datetime.datetime):
            raise TypeError("'{}.start_from' must be a datetime.datetime "
                            "instance".format(cls_name))
        if not isinstance(self.start_to, datetime.datetime):
            raise TypeError("'{}.start_to' must be a datetime.datetime "
                            "instance".format(cls_name))

        if not isinstance(self.duration, (int, long)):
            raise TypeError("'{}.duration' must be an integer")

    def as_optimo_schema(self):
        self.validate()
        return {
            'breakStartFrom': self.start_from,
            'breakStartTo': self.start_to,
            'breakDuration': self.duration
        }


class WorkShift(BaseModel):

    def __init__(self, work_from, work_to):
        self.work_from = work_from
        self.work_to = work_to
        self.allowed_overtime = None
        self.break_ = None

    def validate(self):
        cls_name = self.__class__.__name__
        if not isinstance(self.work_from, datetime.datetime):
            raise TypeError("'{}.work_from' must be a datetime.datetime "
                            "instance".format(cls_name))
        if not isinstance(self.work_to, datetime.datetime):
            raise TypeError("'{}.work_to' must be a datetime.datetime "
                            "instance".format(cls_name))

        if self.allowed_overtime is not None:
            if not isinstance(self.allowed_overtime, (int, long)):
                raise TypeError("'{}.allowed_overtime' must an integer".format(cls_name))

        if self.break_ is not None:
            if not isinstance(self.break_, Break):
                raise TypeError("{}.break_ must of type Break".format(cls_name))
            self.break_.validate()

    def as_optimo_schema(self):
        self.validate()
        d = {
            'workTimeFrom': self.work_from,
            'workTimeTo': self.work_to,
        }

        if self.allowed_overtime:
            d['allowedOvertime'] = self.allowed_overtime

        if self.break_:
            d['break'] = self.break_

        return d


class UnavailableTime(BaseModel):

    def __init__(self, time_from, time_to):
        self.time_from = time_from
        self.time_to = time_to

    def validate(self):
        cls_name = self.__class__.__name__
        if not isinstance(self.time_from, datetime.datetime):
            raise TypeError("'{}.time_from' must be a datetime.datetime "
                            "instance".format(cls_name))
        if not isinstance(self.time_to, datetime.datetime):
            raise TypeError("'{}.time_to' must be a datetime.datetime "
                            "instance".format(cls_name))

    def as_optimo_schema(self):
        self.validate()
        return {
            'timeFrom': self.time_from,
            'timeTo': self.time_to,
        }


class Driver(BaseModel):

    def __init__(self, id, start_lat, start_lng, end_lat, end_lng,
                 work_shifts=None):

        self.id = id
        self.start_lat = start_lat
        self.start_lng = start_lng
        self.end_lat = end_lat
        self.end_lng = end_lng
        self.work_shifts = work_shifts or []
        self.unavailable_times = []

    def validate(self):
        cls_name = self.__class__.__name__
        if not isinstance(self.id, basestring):
            raise TypeError("'id' must be of type str")
        else:
            if not self.id:
                raise ValueError("'id' cannot be empty")

        if not isinstance(self.start_lat, Number):
            raise TypeError(
                "'{}.start_lat' must be a number".format(cls_name)
            )
        if not isinstance(self.start_lng, Number):
            raise TypeError(
                "'{}.start_lng' must be a number".format(cls_name)
            )

        if not isinstance(self.end_lat, Number):
            raise TypeError(
                "'{}.end_lat' must be a number".format(cls_name)
            )
        if not isinstance(self.end_lng, Number):
            raise TypeError(
                "'{}.end_lng' must be a number".format(cls_name)
            )

        if not isinstance(self.work_shifts, list):
            raise TypeError(
                "'{}.work_shifts' must be of type list".format(cls_name)
            )
        else:
            if not self.work_shifts:
                raise ValueError(
                    "'{}.work_shifts' must have at least 1 "
                    "element".format(cls_name)
                )
            for ws in self.work_shifts:
                if not isinstance(ws, WorkShift):
                    raise ValueError("'{}.work_shifts' must contain elements of"
                                     " type {!r}".format(cls_name, WorkShift))
                ws.validate()

        if not isinstance(self.unavailable_times, list):
            raise TypeError(
                "'{}.unavailable_times' must be of type "
                "list".format(cls_name)
            )
        else:
            for ut in self.unavailable_times:
                if not isinstance(ut, UnavailableTime):
                    raise ValueError(
                        "'{}.unavailable_times' must contain elements of type "
                        "{!r}".format(cls_name, UnavailableTime)
                    )
                ut.validate()

    def as_optimo_schema(self):
        self.validate()
        d = {
            'id': self.id,
            'startLat': self.start_lat,
            'startLon': self.start_lng,
            'endLat': self.end_lat,
            'endLon': self.end_lng,
            'workShifts': self.work_shifts
        }

        if self.unavailable_times:
            d['unavailableTimes'] = self.unavailable_times
        return d


class RoutePlan(BaseModel):

    def __init__(self, request_id, callback_url, status_callback_url,
                 orders=None, drivers=None):
        self.request_id = request_id
        self.callback_url = callback_url
        self.orders = orders or []
        self.drivers = drivers or []
        self.status_callback_url = status_callback_url
        self.no_load_capacities = None
        self.optimization_parameters = None

    def validate(self):
        cls_name = self.__class__.__name__
        if not isinstance(self.request_id, basestring):
            raise TypeError("'{}.request_id' must be of type str".format(cls_name))
        if not self.request_id:
            raise ValueError("'{}.request_id' cannot be an empty string".format(cls_name))

        if not isinstance(self.orders, list):
            raise TypeError("'{}.orders' must be of type list".format(cls_name))
        if not self.orders:
            raise ValueError("'{}.orders' must have at least 1 element".format(cls_name))
        else:
            for order in self.orders:
                if not isinstance(order, Order):
                    raise TypeError("'{}.drivers' must contain elements of "
                                    "type {!r}".format(cls_name, Order))
                order.validate()

        if not isinstance(self.drivers, list):
            raise TypeError("drivers must be of type list")
        if not self.drivers:
            raise ValueError("drivers must have at least 1 element")
        else:
            for drv in self.drivers:
                if not isinstance(drv, Driver):
                    raise TypeError("'{}.drivers' must contain elements of type"
                                    " {!r}".format(cls_name, Driver))
                drv.validate()

        if self.status_callback_url is not None:
            if not isinstance(self.status_callback_url, basestring):
                raise TypeError("'status_callback_url' must be of type str")

        if self.no_load_capacities is not None:
            if not isinstance(self.no_load_capacities, (int, long)):
                raise TypeError("'no_load_capacities' must be of type integer")
            else:
                if 0 <= self.no_load_capacities <= 4:
                    raise ValueError("'no_load_capacities' must be between 0-4")

    def as_optimo_schema(self):
        self.validate()
        d = {
            'requestId': self.request_id,
            'callback': self.callback_url,
            'orders': self.orders,
            'drivers': self.drivers,
            'statusCallback': self.status_callback_url,
        }
        return d
