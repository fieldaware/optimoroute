# -*- coding: utf-8 -*-
import os
from setuptools import setup


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name = "optimoroute",
    version = "0.0.1a1",
    install_requires=[
        "requests",
        "pytz",
    ],
    tests_require=[
        "pytest",
        "jsonschema==2.4.0"
    ],
    author = "George Spanos",
    author_email = "spanosgeorge@gmail.com",
    description = "A python library for OptimoRoute's web service",
    license = "BSD",
    url = "https://github.com/fieldaware/optimoroute",
    packages=['optimoroute', 'tests'],
    long_description=read('README.md'),
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Natural Language :: English',""
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
    ],
)