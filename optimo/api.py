# -*- coding: utf-8 -*-
import json

from optimo.base import CoreOptimoAPI
from .util import OptimoEncoder
from .models import RoutePlan


class OptimoError(Exception):
    """Raised when an operation was not successful"""


def parse_response(raw_response):
    data = json.loads(raw_response['content'])
    status_code = raw_response['status_code']
    return data, status_code


class OptimoAPI(object):
    def __init__(self, optimo_url, access_key, version='v1'):
        self.core_api = CoreOptimoAPI(optimo_url, version, access_key)
        self.optimo_url = optimo_url
        self.version = version
        self.access_key = access_key

    def plan(self, route_plan, encoder=OptimoEncoder):
        if not isinstance(route_plan, RoutePlan):
            raise TypeError("Must be of type {!r}".format(RoutePlan))

        route_plan.validate()
        raw_response = self.core_api.plan_routes(route_plan, encoder=encoder)
        data, status_code = parse_response(raw_response)
        if data['success'] is True:
            return
        else:
            raise OptimoError(data['message'])

    def stop(self, request_id):
        payload = {'requestId': request_id}
        raw_response = self.core_api.stop_planning(payload)
        data, status_code = parse_response(raw_response)
        if data['success'] is True:
            return
        else:
            raise OptimoError(data['message'])

    def get(self, request_id):
        raw_response = self.core_api.get_result(request_id)
        data, status_code = parse_response(raw_response)
        if data['success'] is True:
            return data
        elif data['code'] == 'ERR_PLANNING_IN_PROGRESS':
            # Just return None. No reason to panic.
            return
        else:
            raise OptimoError(data['message'])
