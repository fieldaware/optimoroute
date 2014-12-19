# -*- coding: utf-8 -*-
class OptimoError(Exception):
    """Raised when an operation was not successful"""


class OptimoValidationError(OptimoError):
    """Raised for higher-level model validation errors"""
