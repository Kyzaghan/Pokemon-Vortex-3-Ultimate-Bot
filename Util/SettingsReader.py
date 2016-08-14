# -*- coding: utf-8 -*-
import json
from pprint import pprint


def settings_reader(x):
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
    """Read Config Information
    :return: data
    """
    return settings_reader('config.json')

def read_map():
    """Read Map Information
    :return: data
    """
    return settings_reader('map.json')

def read_legys():
    """Read Legendary Pokémon Information
    :return: data
    """
    return settings_reader('legy.json')


