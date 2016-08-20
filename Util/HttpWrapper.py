# -*- coding: utf-8 -*-

import requests

from Util.SettingsReader import read_config, read_authentication

try:
    from BeautifulSoup import BeautifulSoup
except ImportError:
    from bs4 import BeautifulSoup


class http_wrapper:
    def __init__(self):
        self.c = read_config()
        self.a = read_authentication()
        self.s = requests.session()

    def do_request(self, url, request_type="get", data=""):
        """
        Request function
        :return:
        :param self: Not Set
        :param request_type: post or get, default value get
        :param url: request url
        :param data: post data
        :return: request response
        :rtype: object
        """
        if request_type == "post":
            r = self.s.post(url, data, proxies=self.a["proxy"], headers={"user-agent": self.c["UserAgent"]})
        else:
            r = self.s.get(url, proxies=self.a["proxy"], headers={"user-agent": self.c["UserAgent"]})
        return r

    def download_file(self, url):
        """
        Request function
        :return:
        :param self: Not Set
        :param url: request url
        :rtype: object
        """
        r = self.s.get(url, proxies=self.a["proxy"], headers={"user-agent": self.c["UserAgent"]}, stream=True)
        return r