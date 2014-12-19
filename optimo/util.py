# -*- coding: utf-8 -*-
import json
import datetime

from decimal import Decimal

from requests.packages.urllib3.util import parse_url

from .models import BaseModel
from .errors import OptimoError


DEFAULT_API_VERSION = 'v1'


class CoreOptimoEncoder(json.JSONEncoder):
    """Custom JSON encoder that knows how to serialize ``datetime.datetime``
    and ``decimal.Decimal`` objects.
    """
    def default(self, o):
        if isinstance(o, datetime.datetime):
            return o.strftime('%Y-%m-%dT%H:%M')
        if isinstance(o, Decimal):
            return float(o)


class OptimoEncoder(CoreOptimoEncoder):
    """Custom JSON encoder that knows how to serialize
    :class:`optimo.models.BaseModel <BaseModel>` objects.
    """
    def default(self, o):
        if isinstance(o, BaseModel):
            return o.as_optimo_schema()
        return super(OptimoEncoder, self).default(o)


def process_optimo_params(optimo_url, version, access_key):
    """Validates and normalizes the parameters passed to
    :class:`optimo.api.OptimoAPI` constructor.

    :param optimo_url: string url of the optimoroute's service
    :param version: `int` or `str` denoting the API version
    :param access_key: string access key provided by optimoroute
    :return: None if successful, or raises OptimoError otherwise
    """
    if not optimo_url or not isinstance(optimo_url, basestring):
        raise OptimoError("'optimo_url' must be a url string")

    url = parse_url(optimo_url)
    if not url.scheme:
        optimo_url = 'https://' + url.hostname

    if isinstance(version, (int, long)):
        if version < 1:
            raise OptimoError("{} is an invalid API version".format(version))
        version = 'v' + str(version)
    elif isinstance(version, basestring):
        if not version:
            raise OptimoError("'version' cannot be an empty string")
    else:
        raise OptimoError("'version' must be a string denoting the API version "
                          "you want to use")

    if not access_key or not isinstance(access_key, basestring):
        raise OptimoError("'access_key' must be the string access key provided "
                          "to you by optimoroute")
    return optimo_url, version, access_key
