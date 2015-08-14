# -*- coding: utf-8 -*-
from copy import deepcopy

from jsonschema.validators import Draft4Validator

from ..loader import SCHEMA_STORE

# Schemas
RoutePlanSchema = deepcopy(SCHEMA_STORE['v1'])
OrderSchema = deepcopy(RoutePlanSchema['properties']['orders']['items'])
SchedulingInfoSchema = deepcopy(OrderSchema['properties']['schedulingInfo'])
TimeWindowSchema = deepcopy(OrderSchema['properties']['tw'])
DriverSchema = deepcopy(RoutePlanSchema['properties']['drivers']['items'])
WorkShiftSchema = deepcopy(DriverSchema['properties']['workShifts']['items'])
BreakSchema = deepcopy(WorkShiftSchema['properties']['break'])
ServiceRegionPolygonSchema = deepcopy(DriverSchema['properties']['serviceRegions']['items'])

# Validators
RoutePlanValidator = Draft4Validator(RoutePlanSchema)
OrderValidator = Draft4Validator(OrderSchema)
SchedulingInfoValidator = Draft4Validator(SchedulingInfoSchema)
TimeWindowValidator = Draft4Validator(TimeWindowSchema)
DriverValidator = Draft4Validator(DriverSchema)
WorkShiftValidator = Draft4Validator(WorkShiftSchema)
BreakValidator = Draft4Validator(BreakSchema)
ServiceRegionPolygonValidator = Draft4Validator(ServiceRegionPolygonSchema)
