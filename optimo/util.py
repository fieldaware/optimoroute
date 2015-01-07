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


def validate_url(url):
    """Asserts that the url string has a valid protocol scheme.

    :param url: ``str`` url we want to validate
    :raises OptimoError: When we can't deduce a valid protocol scheme
    """
    _url = parse_url(url)
    if not _url.scheme:
        raise OptimoError("The url: '{}' does not define a protocol scheme"
                          .format(url))


def validate_config_params(optimo_url, version, access_key):
    """Validates and normalizes the parameters passed to
    :class:`optimo.api.OptimoAPI` constructor.

    :param optimo_url: string url of the optimoroute's service
    :param version: ``int`` or ``str`` denoting the API version
    :param access_key: string access key provided by optimoroute
    :return: ``tuple`` of the, possibly adjusted, passed parameters.
    :raises OptimoError: On providing incomplete or invalid config data
    """
    if not optimo_url or not isinstance(optimo_url, basestring):
        raise OptimoError("'optimo_url' must be a url string")

    validate_url(optimo_url)

    if not version or not isinstance(version, basestring) or not \
            version.startswith('v'):
        raise OptimoError("'version' must be a string denoting the API version "
                          "you want to use('v1', 'v2', etc")

    if not access_key or not isinstance(access_key, basestring):
        raise OptimoError("'access_key' must be the string access key provided "
                          "to you by optimoroute")
    return optimo_url, version, access_key
