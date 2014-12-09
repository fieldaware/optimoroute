# -*- coding: utf-8 -*-
from copy import deepcopy

from jsonschema.validators import Draft4Validator

from ..loader import SCHEMA_STORE

# Schemas
RoutePlanSchema = deepcopy(SCHEMA_STORE['v1'])
OrderSchema = deepcopy(RoutePlanSchema['properties']['orders']['items'])
DriverSchema = deepcopy(RoutePlanSchema['properties']['drivers']['items'])
WorkShiftSchema = deepcopy(DriverSchema['properties']['workShifts']['items'])
BreakSchema = deepcopy(WorkShiftSchema['properties']['break'])
UnavailableTime = deepcopy(WorkShiftSchema['properties']['unavailableTimes']['items'])

# Validators
RoutePlanValidator = Draft4Validator(RoutePlanSchema)
OrderValidator = Draft4Validator(OrderSchema)
DriverValidator = Draft4Validator(DriverSchema)
WorkShiftValidator = Draft4Validator(WorkShiftSchema)
BreakValidator = Draft4Validator(BreakSchema)
UnavailableTimeValidator = Draft4Validator(UnavailableTime)
