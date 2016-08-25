# -*- coding: utf-8 -*-
import sys

try:
    from BeautifulSoup import BeautifulSoup
except ImportError:
    from bs4 import BeautifulSoup

sys.setrecursionlimit(1000000000)


class battle:
    def __init__(self):
        self.enemy_hp = 0
        self.your_hp = 0
        self.your_status = ""
        self.enemy_status = ""

    def get_war_status(self, response):
        """
        Parse war status
        :param response: html response
        """
        ph = BeautifulSoup(response, "html.parser")
        tmp_image = ph.find_all("img")
        if len(tmp_image) >= 4:
            self.your_hp = tmp_image[2]['width']
            self.enemy_hp = tmp_image[3]['width']
        else:
            self.enemy_hp = 0
            self.your_hp = 0

        tmp_status = ph.find_all("td", attrs={"valign": "top"})
        if len(tmp_status) >= 2:
            self.your_status = tmp_status[0].text
            self.enemy_status = tmp_status[1].text
        else:
            self.your_status = ""
            self.enemy_status = ""

    def print_war_status(self):
        """
        Print War
        """
        print("Your HP={0}%\nEnemy HP={1}%\nYour Status={2}\nEnemy Status={3}".format(
            self.your_hp, self.enemy_hp, self.your_status, self.enemy_status))
