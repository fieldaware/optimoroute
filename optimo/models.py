# -*- coding: utf-8 -*-
import abc
import datetime
from numbers import Number
from decimal import Decimal

from .errors import OptimoValidationError


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

    def validate_type(self, attr, expected):
        """Validates that ``attr`` is of the ``expected`` type

        :param attr: name of the model attribute to check
        :param expected: expected type of ``attr``
        :return: None if is valid, or it will raise a TypeError
        """
        type_error_msg = "'{}.{}' must be of type {!r}, not {!r}"
        value = getattr(self, attr)

        if not isinstance(value, expected):
            cls_name = self.__class__.__name__
            raise TypeError(
                type_error_msg.format(cls_name, attr, expected, type(value))
            )


ITERABLES = (list, tuple)


class SchedulingInfo(BaseModel):
    """Scheduling information if order is already scheduled

    :param scheduled_at: ``datetime.datetime`` instance of when driver is expected
        at the location
    :param scheduled_driver: ``str`` driver id or :class:`optimo.models.Driver <Driver> object`
    :param locked: ``bool`` that indicates if the order can be moved (to a
        different time or assigned to a different driver) or is fixed.
    """
    def __init__(self, scheduled_at, scheduled_driver, locked=False):
        self.scheduled_at = scheduled_at
        self.scheduled_driver = scheduled_driver
        self.locked = locked

    def validate(self):
        self.validate_type('scheduled_at', datetime.datetime)
        self.validate_type('scheduled_driver', (basestring, Driver))
        self.validate_type('locked', bool)

    def as_optimo_schema(self):
        self.validate()
        d = {
            'scheduledAt': self.scheduled_at,
            'locked': self.locked,
        }
        if isinstance(self.scheduled_driver, Driver):
            d['scheduledDriver'] = self.scheduled_driver.id
        else:
            d['scheduledDriver'] = self.scheduled_driver
        return d


class TimeWindow(BaseModel):
    """Time window that defines the earliest time alowed to begin the service
    and the dealine to end the service.

    :param start_time: ``datetime.datetime`` instance of when to begin the service
    :param end_time: ``datetime.datetime`` instance of the service's deadline
    """
    def __init__(self, start_time, end_time):
        self.start_time = start_time
        self.end_time = end_time

    def validate(self):
        self.validate_type('start_time', datetime.datetime)
        self.validate_type('end_time', datetime.datetime)

    def as_optimo_schema(self):
        self.validate()
        return {
            'timeFrom': self.start_time,
            'timeTo': self.end_time,
        }


class Order(BaseModel):
    """Order that needs to be planned by optimoroute service.

    :param id: ``str`` unique order identifier
    :param lat: ``numbers.Number`` GPS latitude of the delivery/service location
    :param lng: ``numbers.Number`` GPS longitude of the delivery/service location
    :param duration: ``int`` number of minutes required to unload the goods or
        perform a task at the given location.
    :param time_window: :class: `optimo.models.TimeWindow` instance for this order
    :param priority: ``str`` order priority value which can be one of ('L', 'M', 'H', 'C')
    :param skills: ``list`` of strings of driver skills used to differentiate
        some drivers from others.
    :param assigned_to: ``str`` driver id this order must be assigned to.
    :param scheduling_info: :class:`optimo.models.SchedulingInfo <SchedulingInfo>` object
        if order is already scheduled.
    """
    def __init__(self, id, lat, lng, duration, time_window=None, priority='M',
                 skills=None, assigned_to=None, scheduling_info=None):
        self.id = id
        self.lat = lat
        self.lng = lng
        self.duration = duration
        # described as 'tw' in the JSON schema
        self.time_window = time_window
        # (M)edium is the default for the OptimoRoute service
        self.priority = priority
        self.skills = skills if skills is not None else []
        self.assigned_to = assigned_to
        self.scheduling_info = scheduling_info

    def validate(self):
        cls_name = self.__class__.__name__
        self.validate_type('id', str)
        if not self.id:
            raise ValueError("'{}.id' cannot be empty".format(cls_name))

        self.validate_type('lat', Number)
        self.validate_type('lng', Number)

        self.validate_type('duration', (int, long))
        if self.duration < 0:
            raise ValueError("'{}.duration' cannot be negative".format(cls_name))

        if self.time_window is not None:
            self.validate_type('time_window', TimeWindow)

        self.validate_type('priority', basestring)
        if self.priority not in ('L', 'M', 'H', 'C'):
            raise ValueError(
                "'{}.priority' must be one of ('L', 'M', 'H', 'C')"
                .format(cls_name)
            )

        self.validate_type('skills', ITERABLES)
        for skill in self.skills:
            if not isinstance(skill, basestring):
                raise TypeError(
                    "'{}.skills' must contain elements of type str"
                    .format(cls_name)
                )

        if self.assigned_to is not None:
            self.validate_type('assigned_to', (basestring, Driver))

        if self.scheduling_info is not None:
            self.validate_type('scheduling_info', SchedulingInfo)

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
            if isinstance(self.assigned_to, Driver):
                d['assignedTo'] = self.assigned_to.id
            else:
                d['assignedTo'] = self.assigned_to

        if self.scheduling_info:
            d['schedulingInfo'] = self.scheduling_info

        return d


class Break(BaseModel):
    """Break information for the driver

    :param earliest_start: ``datetime.datetime`` instance of the earliest time to start the break
    :param latest_start: ``datetime.datetime`` instance of the latest time to start the break
    :param duration: ``int`` number of minutes of the break's duration
    """
    def __init__(self, earliest_start, latest_start, duration):
        self.earliest_start = earliest_start
        self.latest_start = latest_start
        self.duration = duration

    def validate(self):
        self.validate_type('earliest_start', datetime.datetime)
        self.validate_type('latest_start', datetime.datetime)
        self.validate_type('duration', (int, long))

    def as_optimo_schema(self):
        self.validate()
        return {
            'breakStartFrom': self.earliest_start,
            'breakStartTo': self.latest_start,
            'breakDuration': self.duration,
        }


class WorkShift(BaseModel):
    """Work shift information for a driver

    :param start_work: ``datetime.datetime`` instance of when work starts
    :param end_work: ``datetime.datetime`` instance of when work ends
    :param allowed_overtime: ``int`` number of minutes denoting the allowed overtime
    :param break_: :class:`optimo.models.Break <Break>` object containing break information
    :param unavailable_times: ``list`` of :class:`optimo.models.TimeWindow` objects that
        describe when a technician is not available.
    """
    def __init__(self, start_work, end_work, allowed_overtime=None, break_=None,
                 unavailable_times=None):
        self.start_work = start_work
        self.end_work = end_work
        self.allowed_overtime = allowed_overtime
        self.break_ = break_
        self.unavailable_times = (unavailable_times if unavailable_times
                                  is not None else [])

    def validate(self):
        cls_name = self.__class__.__name__
        self.validate_type('start_work', datetime.datetime)
        self.validate_type('end_work', datetime.datetime)

        if self.allowed_overtime is not None:
            self.validate_type('allowed_overtime', (int, long))

        if self.break_ is not None:
            self.validate_type('break_', Break)

        self.validate_type('unavailable_times', ITERABLES)
        for time_window in self.unavailable_times:
            if not isinstance(time_window, TimeWindow):
                raise TypeError(
                    "'{}.unavailable_times' must contain elements of type "
                    "{}".format(cls_name, 'TimeWindow')
                )

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


class ServiceRegionPolygon(BaseModel):
    """Service Region assigned to a driver

    :param lat_lng_pairs: ``list`` of ``numbers.Number`` pairs that form a polygon area
    """
    def __init__(self, lat_lng_pairs):
        self.lat_lng_pairs = lat_lng_pairs

    def validate(self):
        cls_name = self.__class__.__name__
        self.validate_type('lat_lng_pairs', ITERABLES)

        if not self.lat_lng_pairs:
            raise ValueError("'{}.lat_lng_pairs' cannot be empty".format(cls_name))

        if not len(self.lat_lng_pairs) > 2:
            raise ValueError("'{}.lat_lng_pairs' must have at least 3 lat/lng pairs to form a "
                             "polygon".format(cls_name))

        for pair in self.lat_lng_pairs:
            if not len(pair) == 2:
                raise ValueError("A lat/lng pair must consist of exactly 2 elements(lat and lng)")

            if not all(map(lambda n: isinstance(n, Number), pair)):
                raise TypeError("Latitude and longitude elements must be of type Number")

            if not (-90 <= pair[0] <= 90):
                raise ValueError("Latitude can take values between -90 and +90")
            if not (-180 <= pair[1] <= 180):
                raise ValueError("Longitude can take values between -180 and +180")

    def as_optimo_schema(self):
        return self.lat_lng_pairs


class Driver(BaseModel):
    """Driver object that will be assigned to orders

    :param id: ``str`` unique driver identifier
    :param start_lat: ``numbers.Number`` GPS latitude of the starting location of the driver
    :param start_lng: ``numbers.Number`` GPS longitude of the starting location of the driver
    :param end_lat: ``numbers.Number`` GPS latitude of the ending location of the driver
    :param end_lng: ``numbers.Number`` GPS longitude of the ending location of the driver
    :param work_shifts: ``list`` of :class:`optimo.models.WorkShift` objects
    :param skills: ``list`` of string skill ids for the driver
    :param speed_factor: ``numbers.Number`` denoting the driving speed adjustment
    :param service_regions: ``list`` of
        :class:`optimo.models.ServiceRegionPolygon` denoting the areas the driver
        can service
    :param cost_per_hour: ``numbers.Number`` denoting the driver's cost per hour
    :param cost_per_hour_for_overtime: ``numbers.Number`` denoting the driver's
        cost of overtime per hour
    :param cost_per_km: ``numbers.Number`` Driver's cost per kilometer
    :param fixed_cost: ``numbers.Number`` Cost that is incurred every time this
        driver is used, regardless of time
    """

    def __init__(self, id, start_lat, start_lng, end_lat, end_lng, work_shifts=None, skills=None,
                 speed_factor=None, service_regions=None, cost_per_hour=None, cost_per_hour_for_overtime=None,
                 cost_per_km=None, fixed_cost=None):
        self.id = id
        self.start_lat = start_lat
        self.start_lng = start_lng
        self.end_lat = end_lat
        self.end_lng = end_lng
        self.work_shifts = work_shifts if work_shifts is not None else []
        self.skills = skills if skills is not None else []
        self.speed_factor = speed_factor
        self.service_regions = service_regions if service_regions is not None else []
        self.cost_per_hour = cost_per_hour
        self.cost_per_hour_for_overtime = cost_per_hour_for_overtime
        self.cost_per_km = cost_per_km
        self.fixed_cost = fixed_cost

    def validate(self):
        cls_name = self.__class__.__name__
        self.validate_type('id', basestring)
        if not self.id:
            raise ValueError("'{}.id' cannot be empty".format(cls_name))

        self.validate_type('start_lat', Number)
        self.validate_type('start_lng', Number)

        self.validate_type('end_lat', Number)
        self.validate_type('end_lng', Number)

        self.validate_type('work_shifts', ITERABLES)
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

        self.validate_type('skills', ITERABLES)
        for skill in self.skills:
            if not isinstance(skill, basestring):
                raise TypeError(
                    "'{}.skills' must contain elements of type str"
                    .format(cls_name)
                )

        if self.speed_factor is not None:
            self.validate_type('speed_factor', Number)

        self.validate_type('service_regions', ITERABLES)
        for region in self.service_regions:
            if not isinstance(region, ServiceRegionPolygon):
                raise TypeError(
                    "'{}.service_regions' must contain elements of type {}"
                    .format(cls_name, 'ServiceRegionPolygon')
                )

        if self.cost_per_hour is not None:
            self.validate_type('cost_per_hour', Number)

        if self.cost_per_hour_for_overtime is not None:
            self.validate_type('cost_per_hour_for_overtime', Number)

        if self.cost_per_km is not None:
            self.validate_type('cost_per_km', Number)

        if self.fixed_cost is not None:
            self.validate_type('fixed_cost', Number)

    def as_optimo_schema(self):
        self.validate()
        d = {
            'id': self.id,
            'startLat': self.start_lat,
            'startLon': self.start_lng,
            'endLat': self.end_lat,
            'endLon': self.end_lng,
            'workShifts': self.work_shifts,
            'skills': self.skills,
            'serviceRegions': self.service_regions,
        }

        if self.speed_factor:
            d['speedFactor'] = self.speed_factor
        if self.cost_per_hour:
            d['costPerHour'] = self.cost_per_hour
        if self.cost_per_hour_for_overtime:
            d['costPerHourForOvertime'] = self.cost_per_hour_for_overtime
        if self.cost_per_km:
            d['costPerKm'] = self.cost_per_km
        if self.fixed_cost:
            d['fixedCost'] = self.fixed_cost

        return d


class OptimizationParameters(BaseModel):
    """OptimizationParameters object, offering optimization options for a RoutePlan instance.

    :param service_outside_service_areas: ``bool`` flag indicating whether orders, that do not
        belong to a service area, can be scheduled.
    :param balancing: ``str`` route balancing setting. Can be one of ('OFF', 'ON', 'ON_FORCE').
    :param balance_by: ``str`` defines the criteria for balancing routes. Can be one
        of ('WT', 'NUM').
    :param balancing_factor: ``float`` or ``decimal.Decimal`` indicating the importance of balancing
        compared to route costs.
    """
    BALANCING_VALUES = ('OFF', 'ON', 'ON_FORCE')
    BALANCE_BY_VALUES = ('WT', 'NUM')

    def __init__(self, service_outside_service_areas=False, balancing='ON_FORCE', balance_by='WT',
                 balancing_factor=0.3):

        self.service_outside_service_areas = service_outside_service_areas
        self.balancing = balancing
        self.balance_by = balance_by
        self.balancing_factor = balancing_factor

    def as_optimo_schema(self):
        self.validate()
        return {
            'serviceOutsideServiceAreas': self.service_outside_service_areas,
            'balancing': self.balancing,
            'balanceBy': self.balance_by,
            'balancingFactor': self.balancing_factor,
        }

    def validate(self):
        cls_name = self.__class__.__name__
        self.validate_type('service_outside_service_areas', bool)

        self.validate_type('balancing', basestring)
        if self.balancing not in self.BALANCING_VALUES:
            raise ValueError(
                "'{}.balancing' must be one of {!r}".format(cls_name, self.BALANCING_VALUES)
            )

        self.validate_type('balance_by', basestring)
        if self.balance_by not in self.BALANCE_BY_VALUES:
            raise ValueError(
                "'{}.balancing' must be one of {!r}".format(cls_name, self.BALANCE_BY_VALUES)
            )

        self.validate_type('balancing_factor', (float, Decimal))
        if not (0.0 <= self.balancing_factor <= 1.0):
            raise ValueError("'{}.balancing_factor' must be in the range "
                             "'0.0 - 1.0'".format(cls_name))


class RoutePlan(BaseModel):
    """Route plan object containing the necessary information to perform a plan
    optimization request.

    :param request_id: ``str`` unique identifier for the request
    :param callback_url: ``str`` callback url that will be called when optimization
        is complete. ``request_id`` parameter will be passed to the callback
    :param status_callback_url: ``str`` callback url that will be called to report
        the planning status. ``request_id`` parameter will be passed to the callback
    :param orders: ``list`` of :class:`optimo.models.Order` objects
    :param drivers: ``list`` of :class:`optimo.models.Driver` objects
    :param no_load_capacities: ``int`` number of vehicle load capacity constraints
        that will be used.
    :param optimization_parameters: ``dict`` of optimization parameters
    """
    NO_LOAD_CAPACITIES_MIN = 0
    NO_LOAD_CAPACITIES_MAX = 4

    def __init__(self, request_id, callback_url, status_callback_url, orders=None, drivers=None,
                 no_load_capacities=0, optimization_parameters=None):

        self.request_id = request_id
        self.callback_url = callback_url
        self.status_callback_url = status_callback_url
        self.orders = orders if orders is not None else []
        self.drivers = drivers if drivers is not None else []
        self.no_load_capacities = no_load_capacities
        self.optimization_parameters = (optimization_parameters if optimization_parameters
                                        is not None else OptimizationParameters())

    def validate(self):
        from .util import validate_url

        cls_name = self.__class__.__name__
        self.validate_type('request_id', basestring)
        if not self.request_id:
            raise ValueError("'{}.request_id' cannot be an empty string".format(cls_name))

        self.validate_type('callback_url', basestring)
        validate_url(self.callback_url)

        self.validate_type('status_callback_url', basestring)
        validate_url(self.status_callback_url)

        self.validate_type('orders', ITERABLES)
        if not self.orders:
            raise ValueError("'{}.orders' must have at least 1 element".format(cls_name))
        else:
            for order in self.orders:
                if not isinstance(order, Order):
                    raise TypeError("'{}.orders' must contain elements of "
                                    "type {}".format(cls_name, 'Order'))

        self.validate_type('drivers', ITERABLES)
        if not self.drivers:
            raise ValueError("'{}.drivers' must have at least 1 element".format(cls_name))
        else:
            for drv in self.drivers:
                if not isinstance(drv, Driver):
                    raise TypeError("'{}.drivers' must contain elements of type"
                                    " {}".format(cls_name, 'Driver'))

        if self.no_load_capacities is not None:
            self.validate_type('no_load_capacities', (int, long))
            if (self.no_load_capacities < self.NO_LOAD_CAPACITIES_MIN or
                    self.no_load_capacities > self.NO_LOAD_CAPACITIES_MAX):
                raise ValueError(
                    "'{}.no_load_capacities' must be between 0-4".
                    format(cls_name)
                )

        # ascertain that all driver id references of
        # SchedulingInfo.scheduled_driver and Order.assigned_to
        # correspond to actual driver objects inside 'drivers'.
        driver_ids = [drv.id for drv in self.drivers]
        for order in self.orders:
            if order.scheduling_info:
                si_schema = order.scheduling_info.as_optimo_schema()
                si_driver_id = si_schema['scheduledDriver']
                if si_driver_id not in driver_ids:
                    raise OptimoValidationError(
                        "SchedulingInfo defines driver with id: '{}' that is "
                        "not present in 'drivers' list".format(si_driver_id)
                    )
            if order.assigned_to:
                order_schema = order.as_optimo_schema()
                order_driver_id = order_schema['assignedTo']
                if order_driver_id not in driver_ids:
                    raise OptimoValidationError(
                        "The order with id: '{}' is assigned to driver with id:"
                        " '{}' that is not present in 'drivers' list"
                        .format(order.id, order_driver_id)
                    )

        self.validate_type('optimization_parameters', OptimizationParameters)

    def as_optimo_schema(self):
        self.validate()
        d = {
            'requestId': self.request_id,
            'callback': self.callback_url,
            'statusCallback': self.status_callback_url,
            'orders': self.orders,
            'drivers': self.drivers,
            'optimizationParameters': self.optimization_parameters,
        }
        if self.no_load_capacities:
            d['noLoadCapacities'] = self.no_load_capacities
        return d
