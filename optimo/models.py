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
    def __init__(self, start_time, end_time):
        self.start_time = start_time
        self.end_time = end_time

    def validate(self):
        cls_name = self.__class__.__name__
        if not isinstance(self.start_time, datetime.datetime):
            raise TypeError(
                "'{}.start_time' must be of type datetime.datetime"
                .format(cls_name)
            )

        if not isinstance(self.end_time, datetime.datetime):
            raise TypeError(
                "'{}.end_time' must be of type datetime.datetime"
                .format(cls_name)
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
            raise TypeError("'{}.id' must be of type str".format(cls_name))
        if not self.id:
            raise ValueError("'{}.id' cannot be empty".format(cls_name))

        if not isinstance(self.lat, Number):
            raise TypeError("'{}.lat' must be of type Number".format(cls_name))
        if not isinstance(self.lng, Number):
            raise TypeError("'{}.lng' must be of type Number".format(cls_name))

        if not isinstance(self.duration, (int, long)):
            raise TypeError("'{}.duration' must be of type int".format(cls_name))
        if self.duration < 0:
            raise ValueError("'{}.duration' cannot be negative".format(cls_name))

        if self.time_window is not None:
            if not isinstance(self.time_window, TimeWindow):
                raise TypeError(
                    "'{}.time_window' must be of type {}"
                    .format(cls_name, 'TimeWindow')
                )

        if not isinstance(self.priority, basestring):
            raise TypeError(
                "'{}.priority' must be of type str".format(cls_name)
            )
        if self.priority not in ('L', 'M', 'H', 'C'):
            raise ValueError(
                "'{}.priority' must be one of ('L', 'M', 'H', 'C')"
                .format(cls_name)
            )

        if not isinstance(self.skills, list):
            raise TypeError("'{}.skills' must be of type list".format(cls_name))
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
                    "'{}.assigned_to' must be of type str".format(cls_name)
                )

        if self.scheduling_info is not None:
            if not isinstance(self.scheduling_info, SchedulingInfo):
                raise TypeError(
                    "'{}.scheduling_info' must be of type SchedulingInfo".
                    format(cls_name)
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
            raise TypeError("'{}.start_break' must be of type datetime."
                            "datetime".format(cls_name))
        if not isinstance(self.end_break, datetime.datetime):
            raise TypeError("'{}.end_break' must be of type datetime.datetime"
                            .format(cls_name))

        if not isinstance(self.duration, (int, long)):
            raise TypeError("'{}.duration' must be of type int".format(cls_name))

    def as_optimo_schema(self):
        self.validate()
        return {
            'breakStartFrom': self.start_break,
            'breakStartTo': self.end_break,
            'breakDuration': self.duration
        }


class WorkShift(BaseModel):

    def __init__(self, start_work, end_work, unavailable_times=None):
        self.start_work = start_work
        self.end_work = end_work
        self.allowed_overtime = None
        self.break_ = None
        self.unavailable_times = unavailable_times or []

    def validate(self):
        cls_name = self.__class__.__name__
        if not isinstance(self.start_work, datetime.datetime):
            raise TypeError("'{}.start_work' must be of type datetime.datetime"
                            .format(cls_name))
        if not isinstance(self.end_work, datetime.datetime):
            raise TypeError("'{}.end_work' must be of type datetime.datetime"
                            .format(cls_name))

        if self.allowed_overtime is not None:
            if not isinstance(self.allowed_overtime, (int, long)):
                raise TypeError("'{}.allowed_overtime' must be of type int".
                                format(cls_name))

        if self.break_ is not None:
            if not isinstance(self.break_, Break):
                raise TypeError("'{}.break_' must be of type Break".format(cls_name))
            self.break_.validate()

        if not isinstance(self.unavailable_times, list):
            raise TypeError(
                "'{}.unavailable_times' must be of type list".format(cls_name)
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
            raise TypeError("'{}.start_time' must be of type datetime.datetime"
                            .format(cls_name))
        if not isinstance(self.end_time, datetime.datetime):
            raise TypeError("'{}.end_time' must be of type datetime.datetime"
                            .format(cls_name))

    def as_optimo_schema(self):
        self.validate()
        return {
            'timeFrom': self.start_time,
            'timeTo': self.end_time,
        }


class Driver(BaseModel):

    def __init__(self, id, start_lat, start_lng, end_lat, end_lng,
                 work_shifts=None, skills=None):

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
            raise TypeError("'{}.id' must be of type str".format(cls_name))
        else:
            if not self.id:
                raise ValueError("'{}.id' cannot be empty".format(cls_name))

        if not isinstance(self.start_lat, Number):
            raise TypeError(
                "'{}.start_lat' must be of type Number".format(cls_name)
            )
        if not isinstance(self.start_lng, Number):
            raise TypeError(
                "'{}.start_lng' must be of type Number".format(cls_name)
            )

        if not isinstance(self.end_lat, Number):
            raise TypeError(
                "'{}.end_lat' must be of type Number".format(cls_name)
            )
        if not isinstance(self.end_lng, Number):
            raise TypeError(
                "'{}.end_lng' must be of type Number".format(cls_name)
            )

        if not isinstance(self.work_shifts, list):
            raise TypeError(
                "'{}.work_shifts' must be of type list".format(cls_name)
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

        if not isinstance(self.skills, list):
            raise TypeError(
                "'{}.skills' must be of type list".format(cls_name)
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
            raise TypeError("'{}.request_id' must be of type str".
                            format(cls_name))
        if not self.request_id:
            raise ValueError("'{}.request_id' cannot be an empty string".format(cls_name))

        if not isinstance(self.callback_url, basestring):
            raise TypeError("'{}.callback_url' must be of type str".
                            format(cls_name))

        if not isinstance(self.status_callback_url, basestring):
            raise TypeError("'{}.status_callback_url' must be of type str".
                            format(cls_name))

        if not isinstance(self.orders, list):
            raise TypeError("'{}.orders' must be of type list".format(cls_name))
        if not self.orders:
            raise ValueError("'{}.orders' must have at least 1 element".format(cls_name))
        else:
            for order in self.orders:
                if not isinstance(order, Order):
                    raise TypeError("'{}.orders' must contain elements of "
                                    "type {}".format(cls_name, 'Order'))
                order.validate()

        if not isinstance(self.drivers, list):
            raise TypeError("'{}.drivers' must be of type list".format(cls_name))
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
                raise TypeError("'{}.no_load_capacities' must be of type int".
                                format(cls_name))
            else:
                if self.no_load_capacities < 0 or self.no_load_capacities > 4:
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
