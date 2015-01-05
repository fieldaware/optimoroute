# -*- coding: utf-8 -*-
"""This is only used on our test suite, not in any user-facing code."""
import os
import glob
import json


CURRENT_DIR = os.path.dirname(__file__)


def _get_json_file(dirpath):
    """Returns the first .json filename it encounters on the passed directory
    path.

    :param dirpath: `str` name of the directory we're going to search for json
                    files.
    :return: the first json filename we encounter.
    """
    file_list = glob.glob(dirpath + '/*.json')
    return file_list[0]


def _load_schema_store():
    """Loads the JSON schema provided by Optimoroute in memory, namespaced by
    their version number. This assumes that each JSON schema version is placed
    in their own directory(e.g. v1, v2, etc)

    :return: `dict`
    """
    store = {}
    for entry in os.listdir(CURRENT_DIR):
        if entry.startswith('.'):
            continue
        entry_path = os.path.join(CURRENT_DIR, entry)
        if os.path.isdir(entry_path):
            json_file = _get_json_file(entry_path)
            with open(json_file) as f:
                json_schema = json.load(f)
                store[entry] = json_schema
                return store
    raise IOError("JSON Schema spec file not found.")

SCHEMA_STORE = _load_schema_store()
