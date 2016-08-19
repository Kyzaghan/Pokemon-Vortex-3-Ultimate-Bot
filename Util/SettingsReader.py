# -*- coding: utf-8 -*-
import json


def settings_reader(x):
    """Json parser for settings file"""
    with open('Config/' + x, encoding='utf-8') as data_file:
        read_data = data_file.read()
        data_file.closed
    data = json.loads(read_data)
    return data


def settings_reader_general(x):
    """Json parser for settings file"""
    with open(x, encoding='utf-8') as data_file:
        read_data = data_file.read()
        data_file.closed
    data = json.loads(read_data)
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


def read_pokys():
    """Read Normal Pokémon Information
    :return: data
    """
    return settings_reader('poky.json')


def read_trans(lang):
    """Read Translations
    :return: data
    """
    return settings_reader('Translation/translation.' + lang)


def config_copy(config, oldconfig):
    data = settings_reader_general(config)
    olddata = settings_reader_general(oldconfig)
    for key, value in data.items():
        if (olddata[key] != None and key != "Version"):
            data[key] = olddata[key]
    json.dump(data, open(config, "w"))
