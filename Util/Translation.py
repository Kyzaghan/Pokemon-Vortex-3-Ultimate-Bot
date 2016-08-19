# -*- coding: cp857 -*-
from Util.SettingsReader import read_config, read_trans


class translation:
    def __init__(self):
        self.c = read_config()
        self.l = read_trans(self.c["Language"])

    def getLanguage(self, bot, key):
        for lang in self.l[bot]:
            if lang["Key"] == key:
                return lang["Value"]
