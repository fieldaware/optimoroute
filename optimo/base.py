# -*- coding: utf-8 -*-
import json

import os
import requests

from optimo.util import CoreOptimoEncoder


ENDPOINT_METHODS = {
    'get_result': 'GET',
    'plan_routes': 'POST',
    'stop_planning': 'POST',
}


class CoreOptimoAPI(object):
    def __init__(self, base_url, version, access_key):
        # optimoroute's base url
        self.base_url = base_url
        # optimoroute's version: v1, v2, etc..
        self.version = version
        # optimoroute's access_key
        self.access_key = access_key

    def raw_request(self, url, method, params, data=None, headers=None):
        """
        If some people want to use some library other than ``requests``, or
        perform their own CERT verification, this is the function they'll need
        to override.

        In any case, they must adhere to the fact that the return value must
        always be a dict of the form:
        {
            'status_code': $INT_STATUS_CODE,
            'headers': {},
            'content': '$NON-PROCESSED_CONTENT_RETURN_BY_SERVER'
        }

        This is a reference implementation using the ``requests`` library.
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

        method = ENDPOINT_METHODS[endpoint]
        url = os.path.join(self.base_url, self.version, endpoint)
        params = {'key': self.access_key}

        if method == 'GET':
            params['requestId'] = request_id

        else:
            # POST
            if data:
                data = json.dumps(data, cls=encoder)

        resp_dict = self.raw_request(url, method, params, data, headers)
        # TODO: handle errors if content isn't json (status 500, etc)
        return resp_dict

    def plan_routes(self, data, headers=None, encoder=CoreOptimoEncoder):
        resp_dict = self.do_request('plan_routes', data=data, headers=headers,
                                    encoder=encoder)
        return resp_dict

    def get_result(self, request_id, headers=None):
        resp_dict = self.do_request('get_result', request_id=request_id, headers=headers)
        return resp_dict

    def stop_planning(self, data, headers=None):
        # Data only contains the requestId in this case.
        resp_dict = self.do_request('stop_planning', data=data, headers=headers)
        return resp_dict
