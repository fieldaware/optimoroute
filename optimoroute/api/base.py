# -*- coding: utf-8 -*-
import json
from optimoroute.core.base import CoreOptimoAPI
from optimoroute.api.util import OptimoEncoder
from optimoroute.api.entities import RoutePlan


class OptimoResponse(object):
    def __init__(self, data=None, headers=None, status_code=None):
        self.data = data
        self.headers = headers
        self.status_code = status_code

    @property
    def is_success(self):
        return self.data['success']

    @property
    def error_message(self):
        return self.data['message'] if not self.is_success else None


def build_response(raw_response):
    data = json.loads(raw_response['content'])
    headers = raw_response['headers']
    status_code = raw_response['status_code']
    return OptimoResponse(data=data, headers=headers, status_code=status_code)


class OptimoAPI(object):
    def __init__(self, optimo_url, version, access_key):
        self.core_api = CoreOptimoAPI(optimo_url, version, access_key)
        self.optimo_url = optimo_url
        self.version = version
        self.access_key = access_key

    def plan(self, route_plan, encoder=OptimoEncoder):
        if not isinstance(route_plan, RoutePlan):
            raise TypeError("Must be of type {!r}".format(RoutePlan))

        route_plan.validate()
        raw_response = self.core_api.plan_routes(route_plan, encoder=encoder)
        return build_response(raw_response)

    def stop(self, request_id):
        payload = {'requestId': request_id}
        raw_response = self.core_api.stop_planning(payload)
        return build_response(raw_response)

    def get(self, request_id):
        raw_response = self.core_api.get_result(request_id)
        return build_response(raw_response)
