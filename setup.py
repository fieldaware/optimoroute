# -*- coding: utf-8 -*-
from setuptools import setup


with open('README.md', 'r') as f:
    readme = f.read()

packages = [
    'optimoroute',
    'optimoroute.core',
    'optimoroute.core.schema',
    'optimoroute.core.schema.v1',
    'optimoroute.api',
    'tests'
]

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
    packages=packages,
    long_description=readme,
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Natural Language :: English',""
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
    ],
)