# -*- coding: utf-8 -*-
import os
import glob
import json


CURRENT_DIR = os.path.dirname(__file__)


def _get_json_file(dirpath):
    file_list = glob.glob(dirpath + '/*.json')
    return file_list[0]


def _load_schema_store():
    store = {}
    for entry in os.listdir(CURRENT_DIR):
        if entry.startswith('.'):
            continue
        entry_path = os.path.join(CURRENT_DIR, entry)
        if os.path.isdir(entry_path):
            json_file = _get_json_file(entry_path)
            json_schema = json.load(open(json_file))
            store[entry] = json_schema
            return store
    raise IOError("JSON Schema spec file not found.")

SCHEMA_STORE = _load_schema_store()
