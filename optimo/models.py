# -*- coding: utf-8 -*-
import abc
import datetime
from numbers import Number


class BaseModel(object):
    """Abstract base class that all OptimoRoute entities must subclass"""
    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def validate(self):
        """It must replicate the validation according to the JSON schema
        provided by OptimoRoute.

        Must return None or raise a validation error
        """

    @abc.abstractmethod
    def as_optimo_schema(self):
        """Must return a dict with the key names as expected from OptimoRoute's
        JSON schema.
        """


ITERABLES = (list, tuple)
TYPE_ERROR_MSG = "'{}.{}' must be of type {!r}, not {!r}"


class SchedulingInfo(BaseModel):
    def __init__(self, scheduled_at, scheduled_driver, locked=False):
        self.scheduled_at = scheduled_at
        self.scheduled_driver = scheduled_driver
        self.locked = locked

    def validate(self):
        cls_name = self.__class__.__name__
        if not isinstance(self.scheduled_at, datetime.datetime):
            raise TypeError(
                TYPE_ERROR_MSG.format(
                    cls_name,
                    'scheduled_at',
                    datetime.datetime,
                    type(self.scheduled_at)
                )
            )

        if not isinstance(self.scheduled_driver, basestring):
            raise TypeError(
                TYPE_ERROR_MSG.format(
                    cls_name,
                    'scheduled_driver',
                    str,
                    type(self.scheduled_driver)
                )
            )

        if not isinstance(self.locked, bool):
            raise TypeError(
                TYPE_ERROR_MSG.format(
                    cls_name,
                    'locked',
                    bool,
                    type(self.locked)
                )
            )

    def as_optimo_schema(self):
        self.validate()
        return {
            'scheduledAt': self.scheduled_at,
            'scheduledDriver': self.scheduled_driver,
            'locked': self.locked
        }


class TimeWindow(BaseModel):
    def __init__(self, start_time, end_time):
        self.start_time = start_time
        self.end_time = end_time

    def validate(self):
        cls_name = self.__class__.__name__
        if not isinstance(self.start_time, datetime.datetime):
            raise TypeError(
                TYPE_ERROR_MSG.format(
                    cls_name,
                    'start_time',
                    datetime.datetime,
                    type(self.start_time)
                )
            )

        if not isinstance(self.end_time, datetime.datetime):
            raise TypeError(
                TYPE_ERROR_MSG.format(
                    cls_name,
                    'end_time',
                    datetime.datetime,
                    type(self.end_time)
                )
            )

    def as_optimo_schema(self):
        self.validate()
        return {
            'timeFrom': self.start_time,
            'timeTo': self.end_time
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
            raise TypeError(
                TYPE_ERROR_MSG.format(cls_name, 'id', str, type(self.id))
            )
        if not self.id:
            raise ValueError("'{}.id' cannot be empty".format(cls_name))

        if not isinstance(self.lat, Number):
            raise TypeError(
                TYPE_ERROR_MSG.format(cls_name, 'lat', Number, type(self.lat))
            )
        if not isinstance(self.lng, Number):
            raise TypeError(
                TYPE_ERROR_MSG.format(cls_name, 'lng', Number, type(self.lng))
            )

        if not isinstance(self.duration, (int, long)):
            raise TypeError(
                TYPE_ERROR_MSG.format(
                    cls_name,
                    'duration',
                    int,
                    type(self.duration)
                )
            )
        if self.duration < 0:
            raise ValueError("'{}.duration' cannot be negative".format(cls_name))

        if self.time_window is not None:
            if not isinstance(self.time_window, TimeWindow):
                raise TypeError(
                    TYPE_ERROR_MSG.format(
                        cls_name,
                        'time_window',
                        TimeWindow,
                        type(self.time_window)
                    )
                )

        if not isinstance(self.priority, basestring):
            raise TypeError(
                TYPE_ERROR_MSG.format(
                    cls_name,
                    'priority',
                    str,
                    type(self.priority)
                )
            )
        if self.priority not in ('L', 'M', 'H', 'C'):
            raise ValueError(
                "'{}.priority' must be one of ('L', 'M', 'H', 'C')"
                .format(cls_name)
            )

        if not isinstance(self.skills, ITERABLES):
            raise TypeError(
                TYPE_ERROR_MSG.format(
                    cls_name, 'skills', list, type(self.skills)
                )
            )
        else:
            for skill in self.skills:
                if not isinstance(skill, basestring):
                    raise TypeError(
                        "'{}.skills' must contain elements of type str"
                        .format(cls_name)
                    )

        if self.assigned_to is not None:
            if not isinstance(self.assigned_to, basestring):
                raise TypeError(
                    TYPE_ERROR_MSG.format(
                        cls_name, 'assigned_to', str, type(self.assigned_to)
                    )
                )

        if self.scheduling_info is not None:
            if not isinstance(self.scheduling_info, SchedulingInfo):
                raise TypeError(
                    TYPE_ERROR_MSG.format(
                        cls_name,
                        'scheduling_info',
                        SchedulingInfo,
                        type(self.scheduling_info)
                    )
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

    def __init__(self, start_break, end_break, duration):
        self.start_break = start_break
        self.end_break = end_break
        self.duration = duration

    def validate(self):
        cls_name = self.__class__.__name__
        if not isinstance(self.start_break, datetime.datetime):
            raise TypeError(
                TYPE_ERROR_MSG.format(
                    cls_name,
                    'start_break',
                    datetime.datetime,
                    type(self.start_break)
                )
            )
        if not isinstance(self.end_break, datetime.datetime):
            raise TypeError(
                TYPE_ERROR_MSG.format(
                    cls_name,
                    'end_break',
                    datetime.datetime,
                    type(self.end_break)
                )
            )

        if not isinstance(self.duration, (int, long)):
            raise TypeError(
                TYPE_ERROR_MSG.format(
                    cls_name,
                    'duration',
                    int,
                    type(self.duration)
                )
            )

    def as_optimo_schema(self):
        self.validate()
        return {
            'breakStartFrom': self.start_break,
            'breakStartTo': self.end_break,
            'breakDuration': self.duration
        }


class WorkShift(BaseModel):

    def __init__(self, start_work, end_work, allowed_overtime=None, break_=None,
                 unavailable_times=None):
        self.start_work = start_work
        self.end_work = end_work
        self.allowed_overtime = allowed_overtime
        self.break_ = break_
        self.unavailable_times = unavailable_times or []

    def validate(self):
        cls_name = self.__class__.__name__
        if not isinstance(self.start_work, datetime.datetime):
            raise TypeError(
                TYPE_ERROR_MSG.format(
                    cls_name,
                    'start_work',
                    datetime.datetime,
                    type(self.start_work)
                )
            )
        if not isinstance(self.end_work, datetime.datetime):
            raise TypeError(
                TYPE_ERROR_MSG.format(
                    cls_name,
                    'end_work',
                    datetime.datetime,
                    type(self.end_work)
                )
            )

        if self.allowed_overtime is not None:
            if not isinstance(self.allowed_overtime, (int, long)):
                raise TypeError(
                    TYPE_ERROR_MSG.format(
                        cls_name,
                        'allowed_overtime',
                        int,
                        type(self.allowed_overtime)
                    )
                )

        if self.break_ is not None:
            if not isinstance(self.break_, Break):
                raise TypeError(
                    TYPE_ERROR_MSG.format(
                        cls_name,
                        'break_',
                        Break,
                        type(self.break_)
                    )
                )
            self.break_.validate()

        if not isinstance(self.unavailable_times, ITERABLES):
            raise TypeError(
                TYPE_ERROR_MSG.format(
                    cls_name,
                    'unavailable_times',
                    list,
                    type(self.unavailable_times)
                )
            )
        else:
            for ut in self.unavailable_times:
                if not isinstance(ut, UnavailableTime):
                    raise TypeError(
                        "'{}.unavailable_times' must contain elements of type "
                        "{}".format(cls_name, 'UnavailableTime')
                    )
                ut.validate()

    def as_optimo_schema(self):
        self.validate()
        d = {
            'workTimeFrom': self.start_work,
            'workTimeTo': self.end_work,
        }

        if self.allowed_overtime:
            d['allowedOvertime'] = self.allowed_overtime

        if self.break_:
            d['break'] = self.break_

        if self.unavailable_times:
            d['unavailableTimes'] = self.unavailable_times

        return d


class UnavailableTime(BaseModel):

    def __init__(self, start_time, end_time):
        self.start_time = start_time
        self.end_time = end_time

    def validate(self):
        cls_name = self.__class__.__name__
        if not isinstance(self.start_time, datetime.datetime):
            raise TypeError(
                TYPE_ERROR_MSG.format(
                    cls_name,
                    'start_time',
                    datetime.datetime,
                    type(self.start_time)
                )
            )
        if not isinstance(self.end_time, datetime.datetime):
            raise TypeError(
                TYPE_ERROR_MSG.format(
                    cls_name,
                    'end_time',
                    datetime.datetime,
                    type(self.end_time)
                )
            )

    def as_optimo_schema(self):
        self.validate()
        return {
            'timeFrom': self.start_time,
            'timeTo': self.end_time,
        }


class Driver(BaseModel):

    def __init__(self, id, start_lat, start_lng, end_lat, end_lng,
                 work_shifts=None, skills=None):
        # TODO: support speed_factor
        self.id = id
        self.start_lat = start_lat
        self.start_lng = start_lng
        self.end_lat = end_lat
        self.end_lng = end_lng
        self.work_shifts = work_shifts or []
        self.skills = skills or []

    def validate(self):
        cls_name = self.__class__.__name__
        if not isinstance(self.id, basestring):
            raise TypeError(
                TYPE_ERROR_MSG.format(cls_name, 'id', str, type(self.id))
            )
        else:
            if not self.id:
                raise ValueError("'{}.id' cannot be empty".format(cls_name))

        if not isinstance(self.start_lat, Number):
            raise TypeError(
                TYPE_ERROR_MSG.format(
                    cls_name,
                    'start_lat',
                    Number,
                    type(self.start_lat)
                )
            )
        if not isinstance(self.start_lng, Number):
            raise TypeError(
                TYPE_ERROR_MSG.format(
                    cls_name,
                    'start_lng',
                    Number,
                    type(self.start_lng)
                )
            )

        if not isinstance(self.end_lat, Number):
            raise TypeError(
                TYPE_ERROR_MSG.format(
                    cls_name,
                    'end_lat',
                    Number,
                    type(self.end_lat)
                )
            )
        if not isinstance(self.end_lng, Number):
            raise TypeError(
                TYPE_ERROR_MSG.format(
                    cls_name,
                    'end_lng',
                    Number,
                    type(self.end_lng)
                )
            )

        if not isinstance(self.work_shifts, ITERABLES):
            raise TypeError(
                TYPE_ERROR_MSG.format(
                    cls_name,
                    'work_shifts',
                    list,
                    type(self.work_shifts)
                )
            )
        else:
            if not self.work_shifts:
                raise ValueError(
                    "'{}.work_shifts' must contain at least 1 "
                    "element".format(cls_name)
                )
            for ws in self.work_shifts:
                if not isinstance(ws, WorkShift):
                    raise TypeError(
                        "'{}.work_shifts' must contain elements of type {}"
                        .format(cls_name, 'WorkShift')
                    )
                ws.validate()

        if not isinstance(self.skills, ITERABLES):
            raise TypeError(
                TYPE_ERROR_MSG.format(
                    cls_name,
                    'skills',
                    list,
                    type(self.skills)
                )
            )
        else:
            for skill in self.skills:
                if not isinstance(skill, basestring):
                    raise TypeError(
                        "'{}.skills' must contain elements of type str"
                        .format(cls_name)
                    )

    def as_optimo_schema(self):
        self.validate()
        d = {
            'id': self.id,
            'startLat': self.start_lat,
            'startLon': self.start_lng,
            'endLat': self.end_lat,
            'endLon': self.end_lng,
            'workShifts': self.work_shifts,
            'skills': self.skills
        }
        return d


class RoutePlan(BaseModel):
    NO_LOAD_CAPACITIES_MIN = 0
    NO_LOAD_CAPACITIES_MAX = 4

    def __init__(self, request_id, callback_url, status_callback_url,
                 orders=None, drivers=None):
        # TODO: support for serviceRegions and optimizationParamaters
        self.request_id = request_id
        self.callback_url = callback_url
        self.status_callback_url = status_callback_url
        self.orders = orders or []
        self.drivers = drivers or []
        self.no_load_capacities = None

    def validate(self):
        cls_name = self.__class__.__name__
        if not isinstance(self.request_id, basestring):
            raise TypeError(
                TYPE_ERROR_MSG.format(
                    cls_name,
                    'request_id',
                    str,
                    type(self.request_id)
                )
            )
        if not self.request_id:
            raise ValueError("'{}.request_id' cannot be an empty string".format(cls_name))

        if not isinstance(self.callback_url, basestring):
            raise TypeError(
                TYPE_ERROR_MSG.format(
                    cls_name,
                    'callback_url',
                    str,
                    type(self.callback_url)
                )
            )

        if not isinstance(self.status_callback_url, basestring):
            raise TypeError(
                TYPE_ERROR_MSG.format(
                    cls_name,
                    'status_callback_url',
                    str,
                    type(self.status_callback_url)
                )
            )

        if not isinstance(self.orders, ITERABLES):
            raise TypeError(
                TYPE_ERROR_MSG.format(
                    cls_name,
                    'orders',
                    list,
                    type(self.orders)
                )
            )
        if not self.orders:
            raise ValueError("'{}.orders' must have at least 1 element".format(cls_name))
        else:
            for order in self.orders:
                if not isinstance(order, Order):
                    raise TypeError("'{}.orders' must contain elements of "
                                    "type {}".format(cls_name, 'Order'))
                order.validate()

        if not isinstance(self.drivers, ITERABLES):
            raise TypeError(
                TYPE_ERROR_MSG.format(
                    cls_name,
                    'drivers',
                    list,
                    type(self.drivers)
                )
            )
        if not self.drivers:
            raise ValueError("'{}.drivers' must have at least 1 element".format(cls_name))
        else:
            for drv in self.drivers:
                if not isinstance(drv, Driver):
                    raise TypeError("'{}.drivers' must contain elements of type"
                                    " {}".format(cls_name, 'Driver'))
                drv.validate()

        if self.no_load_capacities is not None:
            if not isinstance(self.no_load_capacities, (int, long)):
                raise TypeError(
                    TYPE_ERROR_MSG.format(
                        cls_name,
                        'no_load_capacities',
                        int,
                        type(self.no_load_capacities)
                    )
                )
            else:
                if (self.no_load_capacities < self.NO_LOAD_CAPACITIES_MIN or
                        self.no_load_capacities > self.NO_LOAD_CAPACITIES_MAX):
                    raise ValueError(
                        "'{}.no_load_capacities' must be between 0-4".
                        format(cls_name)
                    )

    def as_optimo_schema(self):
        self.validate()
        d = {
            'requestId': self.request_id,
            'callback': self.callback_url,
            'statusCallback': self.status_callback_url,
            'orders': self.orders,
            'drivers': self.drivers,
        }
        if self.no_load_capacities:
            d['noLoadCapacities'] = self.no_load_capacities
        return d
