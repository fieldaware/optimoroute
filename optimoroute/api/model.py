# -*- coding: utf-8 -*-
import abc


class BaseModel(object):
    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def validate(self):
        pass

    @abc.abstractmethod
    def as_optimo_schema(self):
        pass
