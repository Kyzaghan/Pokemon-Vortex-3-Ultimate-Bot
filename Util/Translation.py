# -*- coding: utf-8 -*-
from Util.SettingsReader import read_config, read_trans


class translation:
    def __init__(self):
        self.c = read_config()
        self.l = read_trans(self.c["Language"])

    def get_language(self, bot, key):
        """
        Get language key value
        :param bot: Catcher or Expbot
        :param key: Language key
        :return:
        """
        for lang in self.l[bot]:
            if lang["Key"] == key:
                return lang["Value"]
