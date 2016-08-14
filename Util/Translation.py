# -*- coding: cp857 -*-
from Util.SettingsReader import read_config, read_trans

class translation:
    def __init__(self):
        self.c = read_config()
        self.l = read_trans(self.c["Language"])

    def getLanguage(self, key):
        for lang in self.l["Translations"] :
           if lang["Key"] == key :
               return lang["Value"]