# -*- coding: utf-8 -*-
from setuptools import setup


with open('README.rst', 'r') as f:
    readme = f.read()

packages = [
    'optimo',
    'tests',
]

setup(
    name="optimo",
    version="0.2.3",
    install_requires=[
        "requests",
        "pytz",
    ],
    tests_require=[
        "pytest",
        "jsonschema==2.4.0",
        "pytest-cov",
    ],
    author="George Spanos",
    author_email="spanosgeorge@gmail.com",
    description="A python library for OptimoRoute's web service",
    license="BSD",
    url="https://github.com/fieldaware/optimoroute",
    packages=packages,
    long_description=readme,
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Natural Language :: English',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
    ],
)
