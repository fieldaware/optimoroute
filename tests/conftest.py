# -*- coding: utf-8 -*-
import json
import pytest

from tests.util import MockedResponse, REQUEST_ID_TO_RESPONSE


@pytest.fixture(autouse=True)
def mock_requests(monkeypatch):
    """To avoid any network operations, we will mock the
    :class:`requests.sessions.Session`'s `request` method to make it return our
    MockedResponse object, instead of :class:`requests.models.Response`.

    The fake MockedResponse object will contain real, albeit canned, responses.
    The `REQUEST_ID_TO_RESPONSE` is a dictionary that maps example request_ids
    to arbitrary successful or unsuccessful, raw optimoroute responses.
    """
    def request(self, method, url, **kwargs):
        if method == 'get':
            request_id = kwargs['params']['requestId']
        else:
            # post
            request_id = json.loads(kwargs['data'])['requestId']

        raw_response = REQUEST_ID_TO_RESPONSE[request_id]
        return MockedResponse(
            content=raw_response['content'],
            headers=raw_response['headers'],
            status_code=raw_response['status_code']
        )

    monkeypatch.setattr('requests.sessions.Session.request', request)
