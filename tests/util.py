# -*- coding: utf-8 -*-

SUCCESSFUL_GET_RESPONSE = {
    'content': '{"creationTime":"2014-12-04T17:01:52","requestId":"1234",'
               '"success":true,"result":{"routes":[{"driverId":"123",'
               '"orders":[{"scheduledAt":"2014-12-05T08:04","id":"123"},'
               '{"scheduledAt":"2014-12-05T08:27","id":"456"}]}],'
               '"unservedOrders":[]}}',
    'headers': {
        'content-length': '236',
        'server': 'TornadoServer/4.0.2',
        'connection': 'keep-alive',
        'etag': '"505dfd429ec44bb17e7f47a3cf6e11305cc15a80"',
        'date': 'Fri, 05 Dec 2014 15:22:16 GMT',
        'content-type': 'application/json',
    },
    'status_code': 200,
}

REQUEST_ID_NOT_FOUND_RESPONSE = {
    'content': '{"message":"Request with the requestId specified (\'43b2\') '
               'was not found.","code":"ERR_REQ_NOT_EXISTING","success":false}',
    'status_code': 200,
    'headers': {
        'content-length': '120',
        'server': 'TornadoServer/4.0.2',
        'connection': 'keep-alive',
        'etag': '"de2a7344fe6a9f09559b9b2fa46b767fd30e3634"',
        'date': 'Tue, 09 Dec 2014 13:17:33 GMT',
        'content-type': 'application/json',
    }
}

PLANNING_IN_PROGRESS_RESPONSE = {
    'content': '{"message":"Optimization is still running.",'
               '"code":"ERR_PLANNING_IN_PROGRESS","success":false}',
    'status_code': 200,
    'headers': {
        'content-length': '120',
        'server': 'TornadoServer/4.0.2',
        'connection': 'keep-alive',
        'etag': '"de2a7344fe6a9f09559b9b2fa46b767fd30e3634"',
        'date': 'Tue, 09 Dec 2014 13:17:33 GMT',
        'content-type': 'application/json',
    }
}

SUCCESSFUL_PLAN_RESPONSE = {
    'content': '{"success":true}',
    'status_code': 200,
    'headers': {
        'date': 'Mon, 08 Dec 2014 10:36:03 GMT',
        'content-length': '16',
        'content-type': 'application/json',
        'connection': 'keep-alive',
        'server': 'TornadoServer/4.0.2',
    }
}

UNSUCCESSFUL_PLAN_RESPONSE = {
    'content': '{"message":"an internal server error occured",'
               '"code":"ERR_INTERNAL","success":false}',
    'status_code': 500,
    'headers': {
        'date': 'Mon, 08 Dec 2014 10:36:03 GMT',
        'content-length': '16',
        'content-type': 'application/json',
        'connection': 'keep-alive',
        'server': 'TornadoServer/4.0.2',
    }
}

SUCCESSFUL_STOP_RESPONSE = {
    'content': '{"success":true}',
    'status_code': 200,
    'headers': {
        'date': 'Mon, 08 Dec 2014 10:36:03 GMT',
        'content-length': '16',
        'content-type': 'application/json',
        'connection': 'keep-alive',
        'server': 'TornadoServer/4.0.2',
    }
}

REQUEST_ID_TO_RESPONSE = {
    '1234': SUCCESSFUL_GET_RESPONSE,
    '0000': REQUEST_ID_NOT_FOUND_RESPONSE,
    '0110': PLANNING_IN_PROGRESS_RESPONSE,
    '4321': SUCCESSFUL_PLAN_RESPONSE,
    '3421': SUCCESSFUL_STOP_RESPONSE,
    '666': UNSUCCESSFUL_PLAN_RESPONSE,
}


class MockedResponse(object):
    """This will replace the :class:`Response <requests.models.Response>`
    object, that gets returned by `requests.sessions.Session.request` method.
    """
    def __init__(self, content, headers, status_code):
        self.content = content
        self.headers = headers
        self.status_code = status_code
