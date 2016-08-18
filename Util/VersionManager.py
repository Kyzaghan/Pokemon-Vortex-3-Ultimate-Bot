# -*- coding: utf-8 -*-

import requests
from Util.SettingsReader import read_authentication, read_config
from Util.Translation import translation
from Util.Logger import logger

class version_manager :

    def __init__(self):
        self.s = requests.session()
        self.c = read_config()
        self.a = read_authentication()
        self.tl = translation()
        self.l = logger()

    def do_req(self, type, url, data=""):
        if (type == "post"):
            r = self.s.post(url, data, proxies=self.a["proxy"], headers={"user-agent" : self.c["UserAgent"]})
        else:
            r = self.s.get(url, proxies=self.a["proxy"], headers={"user-agent" : self.c["UserAgent"]})
        return r

    def checkVersion(self):
        r = self.do_req("get", "https://github.com/Kyzaghan/Pokemon-Vortex-3-Ultimate-Bot/releases/latest")
        tmp_url = str(r.url)
        version = tmp_url[tmp_url.rfind("/") + 1:]
        if version != self.c["Version"]:
            self.l.writelog(self.tl.getLanguage("Catcher", "newVersionAvaliable").format(self.c["Version"], version), "info")
        else:
            self.l.writelog(self.tl.getLanguage("Catcher", "yourVersionUpToDate").format(self.c["Version"], version), "info")

