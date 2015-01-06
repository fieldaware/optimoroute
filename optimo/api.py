# -*- coding: utf-8 -*-
import json

from .errors import OptimoError
from .base import CoreOptimoAPI
from .util import OptimoEncoder, DEFAULT_API_VERSION, validate_config_params
from .models import RoutePlan


def parse_response(raw_response):
    data = json.loads(raw_response['content'])
    status_code = raw_response['status_code']
    return data, status_code


class OptimoAPI(object):
    """High-level interface for the optimoroute API.

    Uses :class:`CoreOptimoAPI` internally to perform the actual API calls.

    :param optimo_url: the url of the optimoroute's service
    :param access_key: access key for the account (provided by optimoroute)
    :param version: (optional) API version string(v1, v2, ...). Will be appended to ``optimo_url``

    Usage::

      >>> from optimo import OptimoAPI, RoutePlan
      >>> route_plan = RoutePlan(request_id='1234',...)  # Configure a RoutePlan instance
      >>> optimo_api = OptimoAPI('https://api.optimoroute.com', 'myaccesskey')
      >>> optimo_api.plan(route_plan)  # Start a plan optimization
      >>> optimo_api.get('1234')  # Get the results of a plan optimization
      >>> optimo_api.stop('1234')  # Stop a running plan optimization
    """
    def __init__(self, optimo_url, access_key, version=DEFAULT_API_VERSION):
        optimo_url, version, access_key = validate_config_params(
            optimo_url,
            version,
            access_key
        )
        self.core_api = CoreOptimoAPI(optimo_url, version, access_key)
        self.optimo_url = optimo_url
        self.version = version
        self.access_key = access_key

    def plan(self, route_plan, encoder=OptimoEncoder):
        """Starts a plan optimization

        :param route_plan: a :class:`Routeplan <RoutePlan>` object
        :param encoder: (optional) Custom JSON encoder that will be relayed to ``json.dumps()``
        :return: ``None`` if successful, otherwise it will raise an :class:`OptimoError`
                 with an appropriate error message.
        """
        if not isinstance(route_plan, RoutePlan):
            raise TypeError(
                "Must be of type {!r}, not {!r}"
                .format(RoutePlan, type(route_plan))
            )

        route_plan.validate()
        raw_response = self.core_api.plan_routes(route_plan, encoder=encoder)
        data, status_code = parse_response(raw_response)
        if not data['success']:
            raise OptimoError(data['message'])

    def stop(self, request_id):
        """Stops the plan optimization corresponding to the ``request_id``

        :param request_id: the string request id that was provided to
                           optimoroute for a specific plan optimization.
        :return: ``None`` if successful, otherwise it will raise an :class:`OptimoError`
                 with an appropriate error message.
        """
        payload = {'requestId': request_id}
        raw_response = self.core_api.stop_planning(payload)
        data, status_code = parse_response(raw_response)
        if not data['success']:
            raise OptimoError(data['message'])

    def get(self, request_id):
        """Gets the results of the plan optimization corresponding to the
        ``request_id``.

        :param request_id: the string request id that was provided to
                           optimoroute for a specific plan optimization.
        :return: dictionary with information about the planned optimization.
        """
        raw_response = self.core_api.get_result(request_id)
        data, status_code = parse_response(raw_response)
        if data['success'] is True:
            return data
        elif data['code'] == 'ERR_PLANNING_IN_PROGRESS':
            # Just return None. No reason to panic.
            return
        else:
            raise OptimoError(data['message'])
