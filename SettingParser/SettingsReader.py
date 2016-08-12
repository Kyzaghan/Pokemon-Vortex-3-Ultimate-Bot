import json
from pprint import pprint


def settings_reader(x: object) -> object:
    """Json parser for settings file"""
    with open('Config/' + x) as data_file:
        data = json.load(data_file)
    assert isinstance(data, object)
    return data


def read_authentication():
    """Read Auth Information
    :return: data
    """
    return settings_reader('authentication.json')

def read_config():
    """Read Auth Information
    :return: data
    """
    return settings_reader('config.json')

