# -*- coding: utf-8 -*-
import json

import requests

from optimo.util import CoreOptimoEncoder


ENDPOINT_METHODS = {
    'get_result': 'GET',
    'plan_routes': 'POST',
    'stop_planning': 'POST',
}


class CoreOptimoAPI(object):
    """Low-level interface for the optimoroute API.

    Leverages the ``requests`` library to perform the HTTP requests to the
    OptimoRoute's service.

    :param base_url: the url of the optimoroute's service
    :param version: API version string(v1, v2, ...). Will be appended to ``base_url``
    :param access_key: access key for the account (provided by optimoroute)

    Usage:
      >>> from optimo.base import CoreOptimoAPI
      >>> core_api = CoreOptimoAPI('https://api.optimoroute.com', 'v1', 'myaccesskey')
      # dictionary of a route plan, as expected by OptimoRoute
      >>> plan_data = {requestId: '1234',...}
      >>> core_api.plan_routes(plan_data)  # Start a plan optimization
      >>> core_api.get_result('1234') # Get the results of a plan optimization
      # dictionary with the requestId of the optimization we want to stop
      >>> stop_plan_data = {'requestId': '1234'}
      >>> core_api.stop_planning(stop_plan_data)
    """
    def __init__(self, base_url, version, access_key):
        self.base_url = base_url
        self.version = version
        self.access_key = access_key

    def raw_request(self, url, method, params, data=None, headers=None):
        """Performs the actual http requests to OptimoRoute's service, by using
        the ``requests`` library.

        If for some reason someone would want to use a different library, this
        is the function they should override.

        The only requirement is to always return a dictionary of the form:
        {
            'status_code': $INT_STATUS_CODE,
            'headers': {...},
            'content': '$NON-PROCESSED_STRING_CONTENT_RETURN_BY_SERVER'
        }

        :param url: the full url for the specific operation
        :param method: the HTTP method ('GET' and 'POST' are currently supported)
        :param params: url parameters (the access key is always passed in this way)
        :param data: (optional) for POST operations it will hold the data that
                     will be sent to the server.
        :param headers: (optional) dictionary with any additional custom headers
        :return: dictionary containing the server's raw response
        """
        if method == 'GET':
            resp = requests.get(url, params=params, headers=headers)
        else:
            # POST
            resp = requests.post(url, params=params, data=data, headers=headers)

        resp_dict = {
            'status_code': resp.status_code,
            'headers': resp.headers,
            'content': resp.content
        }
        return resp_dict

    def do_request(self, endpoint, request_id=None, data=None, headers=None,
                   encoder=CoreOptimoEncoder):
        """Resolves optimoroute operations to HTTP methods and prepares the
        data that will be passed to ``raw_request()``.

        :param endpoint: one of ('get_result', 'plan_routes', 'stop_planning')
        :param request_id: the id of the request the operation will be applied.
        :param data: (optional) holds the data for the POST operations.
        :param headers: (optional) dictionary of additional custom headers
        :param encoder: (optional) custom encoder to be used on the data.
        :return: dictionary containing the server's raw response
        """
        method = ENDPOINT_METHODS[endpoint]
        url = u'/'.join([self.base_url, self.version, endpoint])
        params = {'key': self.access_key}

        if method == 'GET':
            params['requestId'] = request_id

        else:
            # POST
            if data:
                data = json.dumps(data, cls=encoder)

        resp_dict = self.raw_request(url, method, params, data, headers)
        return resp_dict

    def plan_routes(self, data, headers=None, encoder=CoreOptimoEncoder):
        """Performs request to start a plan optimization.

        :param data: dictionary with route plan data as expected by optimoroute
        :param headers: dictionary of additional custom headers
        :param encoder:
        :return: dictionary containing the server's raw response
        """
        resp_dict = self.do_request('plan_routes', data=data, headers=headers,
                                    encoder=encoder)
        return resp_dict

    def get_result(self, request_id, headers=None):
        """Performs request to get the results of a specific optimization.

        :param request_id: string id of the optimization we want the results of
        :param headers: dictionary of additional custom headers
        :return: dictionary containing the server's raw response
        """
        resp_dict = self.do_request('get_result', request_id=request_id, headers=headers)
        return resp_dict

    def stop_planning(self, data, headers=None):
        """

        :param data: dictionary containing the 'requestId' string of the
                     optimization we want to stop.
        :param headers: dictionary of additional custom headers
        :return: dictionary containing the server's raw response
        """
        # Data only contains the requestId in this case.
        resp_dict = self.do_request('stop_planning', data=data, headers=headers)
        return resp_dict
